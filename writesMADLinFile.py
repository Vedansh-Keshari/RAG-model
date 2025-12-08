"""
ReusabilityRAG - Core system for extracting, analyzing, and indexing reusable code methods
Phases: A (Build RAG), C (Improve RAG), E (Add MADL)
Integrated with Google Gemini API for reusability analysis
Now includes MADL insertion directly into source files as comments
"""

import os
import json
import re
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

LLM_CALL_COUNT = 0
LLM_CALL_LIMIT = 10


@dataclass
class MethodMetadata:
    """Core metadata structure for a reusable method"""
    id: str
    file_path: str
    language: str
    class_name: Optional[str]
    method_name: str
    signature: str
    start_line: int
    end_line: int
    source: str
    calls: List[str]
    called_by: List[str]
    reusable: bool
    reusability_reason: str
    madl: Dict[str, Any]
    confidence: float = 0.0
    embedding_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FileScanner:
    """Recursively scans directories for source files"""
    
    SUPPORTED_EXTENSIONS = {
        '.py': 'python',
        '.java': 'java',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.cpp': 'cpp',
        '.go': 'go'
    }
    
    def __init__(self, root_path: str, exclude_patterns: List[str] = None):
        self.root_path = Path(root_path).resolve()
        self.exclude_patterns = exclude_patterns or ['node_modules', 'venv', '__pycache__', 'build', 'dist']
    
    def scan(self) -> List[Dict[str, str]]:
        """Returns list of {path, language} dicts"""
        files = []
        for ext, lang in self.SUPPORTED_EXTENSIONS.items():
            for file_path in self.root_path.rglob(f'*{ext}'):
                if not any(pattern in str(file_path) for pattern in self.exclude_patterns):
                    files.append({
                        'path': str(file_path),
                        'language': lang
                    })
        return files


class MethodExtractor:
    """Extracts methods from source files with call graph analysis"""
    
    def __init__(self):
        pass
    
    def extract_methods(self, file_path: str, language: str) -> List[Dict[str, Any]]:
        """Extract all methods from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
        except Exception as e:
            print(f"   [!] Error reading {file_path}: {e}")
            return []
        
        if language == 'python':
            return self._extract_python_methods(source, file_path)
        elif language == 'java':
            return self._extract_java_methods(source, file_path)
        else:
            return []
    
    def _extract_python_methods(self, source: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Python methods"""
        methods = []
        lines = source.split('\n')
        
        method_pattern = re.compile(r'^\s*(def|async def)\s+(\w+)\s*\((.*?)\):')
        
        current_class = None
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Track class context
            class_match = re.match(r'^class\s+(\w+)', line)
            if class_match:
                current_class = class_match.group(1)
            
            # Find method definitions
            method_match = method_pattern.match(line)
            if method_match:
                method_type = method_match.group(1)
                method_name = method_match.group(2)
                params = method_match.group(3)
                
                # Extract method body
                start_line = i + 1
                indent = len(line) - len(line.lstrip())
                end_line = start_line
                
                # Find end of method
                for j in range(i + 1, len(lines)):
                    current_line = lines[j]
                    if current_line.strip():
                        current_indent = len(current_line) - len(current_line.lstrip())
                        if current_indent <= indent:
                            end_line = j
                            break
                else:
                    end_line = len(lines)
                
                method_source = '\n'.join(lines[i:end_line])
                
                # Extract function calls
                calls = re.findall(r'(\w+)\s*\(', method_source)
                calls = list(set([c for c in calls if c != method_name and not c.startswith('_')]))
                
                method_id = f"file://{file_path}::{current_class or 'module'}::{method_name}::line{start_line}"
                
                methods.append({
                    'id': method_id,
                    'file_path': file_path,
                    'language': 'python',
                    'class_name': current_class,
                    'method_name': method_name,
                    'signature': f"{method_type} {method_name}({params})",
                    'start_line': start_line,
                    'end_line': end_line,
                    'source': method_source,
                    'calls': calls[:10],
                    'called_by': [],
                    'def_line_index': i  # Store the actual line index where def starts
                })
            
            i += 1
        
        return methods
    
    def _extract_java_methods(self, source: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Java methods (basic implementation)"""
        methods = []
        lines = source.split('\n')
        
        method_pattern = re.compile(
            r'^\s*(public|private|protected)?\s*(static)?\s*(\w+)\s+(\w+)\s*\((.*?)\)\s*\{'
        )
        
        current_class = None
        
        for i, line in enumerate(lines, 1):
            class_match = re.match(r'^\s*(public|private)?\s*class\s+(\w+)', line)
            if class_match:
                current_class = class_match.group(2)
            
            method_match = method_pattern.match(line)
            if method_match:
                visibility = method_match.group(1) or 'default'
                return_type = method_match.group(3)
                method_name = method_match.group(4)
                params = method_match.group(5)
                
                if method_name == current_class:
                    continue
                
                method_id = f"file://{file_path}::{current_class or 'class'}::{method_name}::line{i}"
                
                methods.append({
                    'id': method_id,
                    'file_path': file_path,
                    'language': 'java',
                    'class_name': current_class,
                    'method_name': method_name,
                    'signature': f"{visibility} {return_type} {method_name}({params})",
                    'start_line': i,
                    'end_line': i + 10,
                    'source': line,
                    'calls': [],
                    'called_by': [],
                    'def_line_index': i - 1
                })
        
        return methods
    
    def build_call_graph(self, all_methods: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build call graph to populate called_by fields"""
        method_map = {m['method_name']: m for m in all_methods}
        
        for method in all_methods:
            for called_method_name in method['calls']:
                if called_method_name in method_map:
                    if method['method_name'] not in method_map[called_method_name]['called_by']:
                        method_map[called_method_name]['called_by'].append(method['method_name'])
        
        return all_methods


class ReusabilityRAG:
    """Determines reusability using Google Gemini API"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def _parse_reusability_response(self, response_text: str) -> Dict[str, Any]:
        response_text = response_text.strip()
        response_text = re.sub(r'^```json?\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)

        try:
            data = json.loads(response_text)
            return {
                "reusable": data.get("reusable", False),
                "reusability_reason": data.get("reusability_reason", "No reason provided"),
                "confidence": float(data.get("confidence", 0.5))
            }
        except Exception:
            return {
                "reusable": True,
                "reusability_reason": "Fallback: LLM output unreadable",
                "confidence": 0.4
            }

    def analyze_reusability(self, method: Dict[str, Any]) -> Dict[str, Any]:
        global LLM_CALL_COUNT, LLM_CALL_LIMIT
        """Analyze if a method is reusable using Gemini"""
        
        prompt = self._create_reusability_prompt(method)
        
        try:
            if LLM_CALL_COUNT < LLM_CALL_LIMIT:
                LLM_CALL_COUNT += 1
                response = self.model.generate_content(prompt)
                result = self._parse_reusability_response(response.text)
            else:
                result = {
                    "reusable": True,
                    "reusability_reason": "Heuristic fallback: LLM quota exceeded.",
                    "confidence": 0.3
                }
        except Exception as e:
            print(f"   [!] Error analyzing {method['method_name']}: {e}")
            result = self._heuristic_analysis(method)
        
        method.update(result)
        return method
    
    def _create_reusability_prompt(self, method: Dict[str, Any]) -> str:
        """Create prompt for reusability analysis"""
        return f"""Analyze if this method is reusable across different contexts.

Method: {method['method_name']}
Signature: {method['signature']}
Language: {method['language']}
Source Code:
```
{method['source'][:1000]}
```

Calls: {', '.join(method['calls'][:5])}
Called by: {', '.join(method['called_by'][:5])}

Consider these factors:
1. Does it have side effects (file I/O, network, database)?
2. Is it parameterized and context-independent?
3. Is it stateless or has minimal state dependencies?
4. Can it be used in different scenarios without modification?
5. Does it have clear inputs and outputs?

Respond with ONLY valid JSON (no markdown, no explanation):
{{
  "reusable": true or false,
  "reusability_reason": "brief explanation in one sentence",
  "confidence": 0.0 to 1.0
}}"""
    
    def _heuristic_analysis(self, method: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback heuristic analysis if API fails"""
        source = method['source'].lower()
        
        has_side_effects = any(keyword in source for keyword in [
            'open(', 'write', 'delete', 'drop', 'insert', 'update',
            'request.', 'http', 'socket', 'global ', 'nonlocal'
        ])
        
        has_params = '(' in method['signature'] and method['signature'].count(',') > 0
        
        reusable = not has_side_effects and has_params
        confidence = 0.5
        
        if reusable:
            reason = "Appears stateless with parameters"
        else:
            reason = "Has side effects or no parameters"
        
        return {
            'reusable': reusable,
            'reusability_reason': reason,
            'confidence': confidence
        }


class MADLGenerator:
    """Generates Method Annotation Description Language metadata"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_madl(self, method: Dict[str, Any]) -> Dict[str, Any]:
        global LLM_CALL_COUNT, LLM_CALL_LIMIT
        """Generate MADL annotations for a reusable method"""

        if not method.get('reusable', False):
            return {}
        
        prompt = self._create_madl_prompt(method)
        
        try:
            if LLM_CALL_COUNT < LLM_CALL_LIMIT:
                LLM_CALL_COUNT += 1
                response = self.model.generate_content(prompt)
                madl = self._parse_madl_response(response.text)
                if madl:
                    return madl
            
            # Fallback if quota exceeded or parse failed
            return self._generate_basic_madl(method)

        except Exception as e:
            print(f"   [!] Error generating MADL for {method['method_name']}: {e}")
            return self._generate_basic_madl(method)
    
    def _create_madl_prompt(self, method: Dict[str, Any]) -> str:
        """Create prompt for strict MADL JSON format"""
        return f"""
    Generate a JSON object with EXACTLY these fields:

    {{
        "method_name": "",
        "class_name": "",
        "intent": "",
        "semantic_description": "",
        "keywords": [],
        "parameters": "",
        "method_code": ""
    }}

    Rules:
    - Do NOT add extra fields
    - Do NOT add agents, triggers, confidence or metadata
    - Fill values based ONLY on the method

    Respond with ONLY valid JSON.

    Method Name: {method['method_name']}
    Class Name: {method.get('class_name', '')}
    Parameters: {method['signature']}
    Method Code:
    {method['source']}
    """


    def _parse_madl_response(self, response_text: str) -> Dict[str, Any]:
        try:
            response_text = response_text.strip()
            response_text = response_text.replace("```json", "").replace("```", "")
            data = json.loads(response_text)

            return {
                "method_name": data.get("method_name", ""),
                "class_name": data.get("class_name", ""),
                "intent": data.get("intent", ""),
                "semantic_description": data.get("semantic_description", ""),
                "keywords": data.get("keywords", []),
                "parameters": data.get("parameters", ""),
                "method_code": data.get("method_code", "")
            }

        except Exception as e:
            print("MADL JSON Parse Error:", e)
            return {}

    def _generate_basic_madl(self, method: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback that STILL follows strict JSON rules"""
        return {
            "method_name": method['method_name'],
            "class_name": method['class_name'] or "",
            "intent": f"Auto-generated intent for {method['method_name']}.",
            "semantic_description": f"Auto-generated description for {method['method_name']}.",
            "keywords": [],
            "parameters": method['signature'],
            "method_code": method['source']
        }


    def _infer_preconditions(self, method: Dict[str, Any]) -> List[str]:
        """Infer preconditions from method analysis"""
        if not method:
            return []
        
        preconditions = []
        source = method.get('source', '').lower()
        
        if 'login' in source or 'auth' in source:
            preconditions.append('user_authenticated')
        if 'database' in source or 'db' in source:
            preconditions.append('database_connected')
        if 'file' in source or 'open(' in source:
            preconditions.append('file_accessible')
        
        return preconditions
    
    def _infer_triggers(self, method: Dict[str, Any]) -> List[str]:
        """Infer trigger events from method context"""
        if not method:
            return []
        
        triggers = []
        method_name = method.get('method_name', '').lower()
        
        if 'init' in method_name:
            triggers.append('initialization')
        if 'validate' in method_name:
            triggers.append('validation_required')
        if 'process' in method_name:
            triggers.append('data_processing')
        if 'handle' in method_name:
            triggers.append('event_handling')
        
        return triggers


class MADLInserter:
    """Inserts MADL metadata as comments into source files"""
    
    def __init__(self):
        self.comment_styles = {
            'python': '#',
            'java': '//',
            'javascript': '//',
            'typescript': '//',
            'cpp': '//',
            'go': '//'
        }
    
    def insert_madl_into_files(self, reusable_methods: List[Dict[str, Any]]) -> None:
        """Insert MADL comments into all source files"""
        # Group methods by file
        files_to_update = {}
        for method in reusable_methods:
            file_path = method['file_path']
            if file_path not in files_to_update:
                files_to_update[file_path] = []
            files_to_update[file_path].append(method)
        
        # Process each file
        for file_path, methods in files_to_update.items():
            self._insert_madl_into_file(file_path, methods)
    
    def _insert_madl_into_file(self, file_path: str, methods: List[Dict[str, Any]]) -> None:
        """Insert MADL comments into a single file"""
        try:
            # Read original file
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # REMOVE all old MADL blocks
            lines = self._remove_old_madl_blocks(lines)

            # Recalculate def_line_index AFTER cleaning
            for m in methods:
                method_name = m["method_name"]
                for idx, line in enumerate(lines):
                    if line.strip().startswith("def " + method_name):
                        m["def_line_index"] = idx
                        break

            # Sort methods by line number in reverse order (bottom to top)
            # This prevents line number shifts when inserting
            methods_sorted = sorted(methods, key=lambda m: m['def_line_index'], reverse=True)
            
            language = methods[0]['language']
            comment_prefix = self.comment_styles.get(language, '#')
            
            # Insert MADL comments for each method
            for method in methods_sorted:
                madl = method.get('madl', {})
                if not madl:
                    continue
                
                # Check if MADL already exists
                def_line_idx = method['def_line_index']

                # SAFETY CHECK: prevent list index out of range
                if def_line_idx is None or def_line_idx < 0 or def_line_idx >= len(lines):
                    print(f"   [ERROR] Skipping {method['method_name']} — invalid def_line_index ({def_line_idx})")
                    continue

                # Safety: skip invalid indexes
                if def_line_idx < 0 or def_line_idx >= len(lines):
                    print(f"   [SKIP] Invalid def_line_index for {method['method_name']}: {def_line_idx}")
                    continue

                # Skip if MADL already exists
                if self._madl_already_exists(lines, def_line_idx, comment_prefix):
                    print(f"   [SKIP] MADL already exists for {method['method_name']}")
                    continue
                
                # Create MADL comment block
                # madl_comment = self._format_madl_comment(madl, comment_prefix, method)
                madl_comment = self._format_madl_comment(madl, comment_prefix)
                
                # Insert before the method definition
                indent = self._get_indent(lines[def_line_idx])
                madl_lines = [indent + line + '\n' for line in madl_comment.split('\n')]
                
                # Insert the MADL block
                for i, madl_line in enumerate(madl_lines):
                    lines.insert(def_line_idx + i, madl_line)
                
                print(f"   [INSERT] MADL added for {method['method_name']} at line {def_line_idx + 1}")
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print(f"   [SAVED] {file_path}")
        
        except Exception as e:
            print(f"   [ERROR] Failed to insert MADL into {file_path}: {e}")
    
    def _madl_already_exists(self, lines: List[str], def_line_idx: int, comment_prefix: str) -> bool:
        """Check if MADL comment already exists above this method"""
        # Look at the 10 lines before the method definition
        start_idx = max(0, def_line_idx - 10)
        for i in range(start_idx, def_line_idx):
            if 'MADL_METADATA' in lines[i] or 'MADL:' in lines[i]:
                return True
        return False
    
    def _remove_old_madl_blocks(self, lines: List[str]) -> List[str]:
        """Remove ALL old MADL blocks of any format safely."""
        clean = []
        skip = False

        for line in lines:

            # Start of ANY MADL block
            if (
                "===== MADL_METADATA" in line
                or line.strip().startswith("# --- MADL ---")
            ):
                skip = True
                continue

            # End of block: either a separator or an empty line
            if skip:
                if (
                    line.strip().startswith("=====")  # end of old block
                    or line.strip() == ""            # blank line after block
                    or line.strip().startswith("# ===========================")
                ):
                    skip = False
                continue

            # Keep normal code lines
            clean.append(line)

        return clean
    
    
    def _format_madl_block(self, metadata: Dict[str, Any]) -> str:
        json_block = json.dumps(metadata, indent=2)

        return (
            "# --- MADL ---\n"
            "# " + json_block.replace("\n", "\n# ") + "\n"
        )

    def _format_madl_comment(self, madl: Dict[str, Any], prefix: str) -> str:
        json_block = json.dumps(madl, indent=2)
        return "# --- MADL ---\n" + "\n".join(f"# {line}" for line in json_block.split("\n")) + "\n\n# --- END MADL ---\n\n"



    # def _format_madl_comment(self, madl: Dict[str, Any], comment_prefix: str, method: Dict[str, Any]) -> str:
    #     """Format MADL as a comment block"""
    #     lines = []
    #     lines.append(f"{comment_prefix} ====== MADL_METADATA ======")
    #     lines.append(f"{comment_prefix} Method: {method['method_name']}")
    #     lines.append(f"{comment_prefix} Reusability: {method.get('reusability_reason', 'N/A')}")
    #     lines.append(f"{comment_prefix} Confidence: {method.get('confidence', 0.0):.2f}")
    #     lines.append(f"{comment_prefix}")
        
    #     # Agents
    #     agents = madl.get('agents', [])
    #     if agents:
    #         lines.append(f"{comment_prefix} Agents:")
    #         for agent in agents:
    #             role = agent.get('role', 'unknown')
    #             capability = agent.get('capability', 'unknown')
    #             lines.append(f"{comment_prefix}   - Role: {role}, Capability: {capability}")
        
    #     # Preconditions
    #     preconditions = madl.get('preconditions', [])
    #     if preconditions:
    #         lines.append(f"{comment_prefix}")
    #         lines.append(f"{comment_prefix} Preconditions:")
    #         for pc in preconditions:
    #             lines.append(f"{comment_prefix}   - {pc}")
        
    #     # Triggers
    #     triggers = madl.get('triggers', [])
    #     if triggers:
    #         lines.append(f"{comment_prefix}")
    #         lines.append(f"{comment_prefix} Triggers:")
    #         for trigger in triggers:
    #             lines.append(f"{comment_prefix}   - {trigger}")
        
    #     lines.append(f"{comment_prefix} ===========================")    
    #     return '\n'.join(lines)
    
    
    def _get_indent(self, line: str) -> str:
        """Get the indentation of a line"""
        return line[:len(line) - len(line.lstrip())]


class VectorIngester:
    """Ingests methods into vector database with embeddings"""
    
    def __init__(self, vector_db_path: str = "./chroma_db"):
        self.vector_db_path = vector_db_path
        print(f"   [INFO] Vector DB path: {vector_db_path}")
    
    def ingest_method(self, method: MethodMetadata) -> str:
        """Create embedding and store (simulated for now)"""
        embedding_text = self._create_embedding_text(method)
        embedding_id = f"vec_{hash(method.id) % 1000000}"
        return embedding_id
    
    def _create_embedding_text(self, method: MethodMetadata) -> str:
        """Create rich text representation for embedding"""
        agents_text = ', '.join([a.get('role', '') for a in method.madl.get('agents', [])])
        preconditions_text = ', '.join(method.madl.get('preconditions', []))
        triggers_text = ', '.join(method.madl.get('triggers', []))
        
        return f"""
Method: {method.method_name}
Signature: {method.signature}
Language: {method.language}
Reusability: {method.reusability_reason}
MADL Agents: {agents_text}
Preconditions: {preconditions_text}
Triggers: {triggers_text}
Source: {method.source[:500]}
"""


class ReusabilityPipeline:
    """Orchestrates the entire pipeline from scanning to ingestion"""
    
    def __init__(self, root_path: str, api_key: str):
        self.scanner = FileScanner(root_path)
        self.extractor = MethodExtractor()
        self.rag = ReusabilityRAG(api_key)
        self.madl_gen = MADLGenerator(api_key)
        self.ingester = VectorIngester()
        self.inserter = MADLInserter()
    
    def run(self) -> List[MethodMetadata]:
        """Execute full pipeline"""
        print("=" * 80)
        print("REUSABILITY RAG PIPELINE STARTING")
        print("=" * 80)
        
        print("\n[Phase 1] Scanning files...")
        files = self.scanner.scan()
        print(f"   [OK] Found {len(files)} source files")
        for f in files[:5]:
            print(f"      - {f['path']}")
        if len(files) > 5:
            print(f"      ... and {len(files) - 5} more")
        
        print("\n[Phase 2] Extracting methods...")
        all_methods = []
        for file_info in files:
            methods = self.extractor.extract_methods(file_info['path'], file_info['language'])
            all_methods.extend(methods)
            if methods:
                print(f"   [OK] {file_info['path']}: {len(methods)} methods")
        print(f"   [OK] Total extracted: {len(all_methods)} methods")
        
        if not all_methods:
            print("   [WARN] No methods found! Check your code files.")
            return []
        
        print("\n[Phase 3] Building call graph...")
        all_methods = self.extractor.build_call_graph(all_methods)
        print(f"   [OK] Call graph built")
        
        print("\n[Phase 4] Analyzing reusability with Gemini API...")
        for i, method in enumerate(all_methods, 1):
            print(f"   [{i}/{len(all_methods)}] Analyzing: {method['method_name']}")
            method = self.rag.analyze_reusability(method)
        
        reusable_methods = [m for m in all_methods if m.get('reusable', False)]
        print(f"   [OK] Found {len(reusable_methods)} reusable methods")
        
        if not reusable_methods:
            print("   [WARN] No reusable methods identified.")
            return []
        
        print("\n[Phase 5] Generating MADL metadata...")
        for i, method in enumerate(reusable_methods, 1):
            print(f"   [{i}/{len(reusable_methods)}] MADL for: {method['method_name']}")
            method['madl'] = self.madl_gen.generate_madl(method)
        
        print("\n[Phase 6] Inserting MADL into source files...")
        self.inserter.insert_madl_into_files(reusable_methods)
        
        print("\n[Phase 7] Ingesting into vector database...")
        method_objects = []
        for method in reusable_methods:
            if 'madl' not in method:
                method['madl'] = {}
            
            metadata = MethodMetadata(**method)
            embedding_id = self.ingester.ingest_method(metadata)
            metadata.embedding_id = embedding_id
            method_objects.append(metadata)
        
        print(f"   [OK] Ingested {len(method_objects)} methods")
        
        print("\n" + "=" * 80)
        print(f"PIPELINE COMPLETE! Processed {len(method_objects)} reusable methods")
        print("=" * 80)
        
        return method_objects


if __name__ == "__main__":
    GEMINI_API_KEY = "AIzaSyAVTWIDAWHBVAEQ9F5CPdi3pYOF8amLmPQ"
    
    pipeline = ReusabilityPipeline(
        root_path=r"C:\Users\vedan\Downloads\RAG-model",
        api_key=GEMINI_API_KEY
    )
    
    results = pipeline.run()
    
    # Save results to JSON
    output_file = "reusable_methods.json"
    with open(output_file, "w") as f:
        json.dump([m.to_dict() for m in results], f, indent=2)
    
    print(f"\n[SAVED] Results saved to: {output_file}")
    
    if results:
        print("\n[SAMPLE] First result:")
        print(json.dumps(results[0].to_dict(), indent=2))
        
        print(f"\n[STATS] Summary:")
        print(f"   Total reusable methods: {len(results)}")
        print(f"   Average confidence: {sum(m.confidence for m in results) / len(results):.2f}")
        
        languages = {}
        for m in results:
            languages[m.language] = languages.get(m.language, 0) + 1
        print(f"   Methods by language: {languages}")
