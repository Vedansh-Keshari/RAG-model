"""
ReusabilityRAG - Core system for extracting, analyzing, and indexing reusable code methods
Phases: A (Build RAG), C (Improve RAG), E (Add MADL)
Integrated with Google Gemini API for reusability analysis
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
# from reusability_rag_new import LLM_CALL_COUNT, LLM_CALL_LIMIT


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
        # Handle Windows paths properly
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
            print(f"   ⚠️  Error reading {file_path}: {e}")
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
                start_line = i + 1  # Line numbers start at 1
                indent = len(line) - len(line.lstrip())
                end_line = start_line
                
                # Find end of method
                for j in range(i + 1, len(lines)):
                    current_line = lines[j]
                    if current_line.strip():  # Non-empty line
                        current_indent = len(current_line) - len(current_line.lstrip())
                        if current_indent <= indent:  # Back to same or less indentation
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
                    'calls': calls[:10],  # Limit to 10 calls
                    'called_by': []
                })
            
            i += 1
        
        return methods
    
    def _extract_java_methods(self, source: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Java methods (basic implementation)"""
        methods = []
        lines = source.split('\n')
        
        # Basic Java method pattern (public/private/protected + return type + method name)
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
                
                # Skip constructors (method name == class name)
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
                    'end_line': i + 10,  # Approximate
                    'source': line,
                    'calls': [],
                    'called_by': []
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
        # self.model = genai.GenerativeModel('gemini-pro')
        # self.model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
        # self.model = genai.GenerativeModel('gemini-1.5-flash-latest')  # Updated model name
        self.model = genai.GenerativeModel('gemini-2.5-flash')  # Updated model name
    
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
            # response = self.model.generate_content(prompt)
            # result = self._parse_llm_response(response.text)
            # from reusability_rag_new import LLM_CALL_COUNT, LLM_CALL_LIMIT
            if LLM_CALL_COUNT < LLM_CALL_LIMIT:
                LLM_CALL_COUNT += 1
                response = self.model.generate_content(prompt)
                result = self._parse_reusability_response(response.text)
            else:
                result = {
                    "reusable": True,
                    # "reusability_reason": "Heuristic fallback: method appears structurally reusable.",
                    "reusability_reason": "Heuristic fallback: LLM quota exceeded.",
                    "confidence": 0.3
                }


        except Exception as e:
            print(f"   ⚠️  Error analyzing {method['method_name']}: {e}")
            # Fallback to heuristic analysis
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
    
    def _parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse LLM response to extract JSON"""
        # Remove markdown code blocks if present
        response_text = response_text.strip()
        response_text = re.sub(r'^```json?\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)
        
        try:
            result = json.loads(response_text)
            return {
                'reusable': result.get('reusable', False),
                'reusability_reason': result.get('reusability_reason', 'Unknown'),
                'confidence': float(result.get('confidence', 0.5))
            }
        except json.JSONDecodeError:
            # Fallback parsing
            reusable = 'true' in response_text.lower() and 'reusable' in response_text.lower()
            return {
                'reusable': reusable,
                'reusability_reason': 'Parsed from unstructured response',
                'confidence': 0.6
            }
    
    def _heuristic_analysis(self, method: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback heuristic analysis if API fails"""
        source = method['source'].lower()
        
        # Check for side effects
        has_side_effects = any(keyword in source for keyword in [
            'open(', 'write', 'delete', 'drop', 'insert', 'update',
            'request.', 'http', 'socket', 'global ', 'nonlocal'
        ])
        
        # Check for parameters
        has_params = '(' in method['signature'] and method['signature'].count(',') > 0
        
        # Heuristic scoring
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
        # self.model = genai.GenerativeModel('gemini-pro')
        # self.model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
        # self.model = genai.GenerativeModel('gemini-1.5-flash-latest')  # Updated model name
        self.model = genai.GenerativeModel('gemini-2.5-flash')  # Updated model name
    
    def generate_madl(self, method: Dict[str, Any]) -> Dict[str, Any]:
        global LLM_CALL_COUNT, LLM_CALL_LIMIT
        """Generate MADL annotations for a reusable method"""

        if not method.get('reusable', False):
            return {}
        
        prompt = self._create_madl_prompt(method)
        
        try:
            # response = self.model.generate_content(
            #     contents = prompt
            #     )
            # madl = self._parse_madl_response(
            #     response.text
            #     )
            # from reusability_rag_new import LLM_CALL_COUNT, LLM_CALL_LIMIT
            if LLM_CALL_COUNT < LLM_CALL_LIMIT:
                LLM_CALL_COUNT += 1
                response = self.model.generate_content(prompt)
                return self._parse_madl_response(response.text)
            else:
                # Basic non-LLM template
                
                # return {
                #     "method_name": method["method_name"],
                #     "class_name": method.get("class_name", ""),
                #     "intent": f"Auto-generated intent for {method['method_name']}",
                #     "semantic_description": f"Auto-generated description for {method['method_name']}",
                #     "keywords": ["auto", "fallback"],
                #     "parameters": method.get("signature", ""),
                #     "method_code": method.get("source", "")[:300]
                # }

                return {
                    "method_name": method["method_name"],
                    "class_name": method.get("class_name", ""),
                    "intent": f"Auto-generated intent for {method['method_name']}",
                    "semantic_description": f"Basic description for {method['method_name']}",
                    "keywords": ["auto", "fallback", "no-llm"],
                    "parameters": method.get("signature", ""),
                    "method_code": method.get("source", "")[:300]
                }

        except Exception as e:
            print(f"   ⚠️  Error generating MADL for {method['method_name']}: {e}")
            madl = self._generate_basic_madl(method)
        
        return madl
    
#     def _create_madl_prompt(self, method: Dict[str, Any]) -> str:
#         """Create prompt for MADL generation"""
#         return f"""Generate MADL (Method Annotation Description Language) metadata for this reusable method.

# Method: {method['method_name']}
# Signature: {method['signature']}
# Reusability: {method['reusability_reason']}
# Source:
    def _create_madl_prompt(self, method: Dict[str, Any]) -> str:
        return f"""
    Generate MADL metadata for the following method.

    Respond ONLY with valid JSON using this strict format:
    {{
        "method_name": "",
        "class_name": "",
        "intent": "",
        "semantic_description": "",
        "keywords": [],
        "parameters": "",
        "method_code": ""
    }}

    Method Name: {method['method_name']}
    Class Name: {method.get('class_name', '')}
    Source Code:
    ```
    {method['source'][:600]}
    ```

    Generate JSON with:
    - agents: List of AI agents that could use this method (role + capability)
    - preconditions: What must be true before calling this method
    - triggers: Events or situations that would trigger calling this method
    - confidence: How confident you are in this MADL (0.0-1.0)

    Respond with ONLY valid JSON:
    {{
        "agents": [
            {{"role": "agent-type", "capability": "what-it-does"}}
        ],
        "preconditions": ["condition1", "condition2"],
        "triggers": ["event1", "event2"],
        "confidence": 0.0 to 1.0
    }}"""
        
    # def _parse_madl_response(self, response_text: str) -> Dict[str, Any]:
    #     """Parse MADL response"""
    #     response_text = response_text.strip()
    #     response_text = re.sub(r'^```json?\s*', '', response_text)
    #     response_text = re.sub(r'\s*```$', '', response_text)
        
    #     try:
    #         return json.loads(response_text)
    #     except json.JSONDecodeError:
    #         return self._generate_basic_madl({})
    
    # def _parse_madl_response(self, response_text: str) -> Dict[str, Any]:
    #     response_text = response_text.strip()
    #     response_text = re.sub(r'^```json?\s*', '', response_text)
    #     response_text = re.sub(r'\s*```$', '', response_text)

    #     try:
    #         data = json.loads(response_text)
    #         return {
    #             "method_name": data.get("method_name", ""),
    #             "class_name": data.get("class_name", ""),
    #             "intent": data.get("intent", ""),
    #             "semantic_description": data.get("semantic_description", ""),
    #             "keywords": data.get("keywords", []),
    #             "parameters": data.get("parameters", ""),
    #             "method_code": data.get("method_code", "")
    #         }
    #     except:
    #         return {}

    def _parse_madl_response(self, response_text: str) -> Dict[str, Any]:
        response_text = response_text.strip()
        response_text = re.sub(r'^```json?\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)

        try:
            return json.loads(response_text)
        except:
            return {}  # allow fallback to trigger


    # def _generate_basic_madl(self, method: Dict[str, Any]) -> Dict[str, Any]:
    #     """Generate basic MADL using heuristics"""
    #     return {
    #         'agents': [
    #             {'role': 'executor', 'capability': 'execute-method'}
    #         ],
    #         'preconditions': self._infer_preconditions(method),
    #         'triggers': self._infer_triggers(method),
    #         'confidence': 0.5
    #     }
    
    def _generate_basic_madl(self, method: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "method_name": method.get("method_name", ""),
            "class_name": method.get("class_name", ""),
            "intent": "Auto-generated fallback intent.",
            "semantic_description": "This is a fallback MADL generated without LLM.",
            "keywords": ["fallback", "auto-generated"],
            "parameters": method.get("signature", ""),
            "method_code": method.get("source", "")[:300]
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


class VectorIngester:
    """Ingests methods into vector database with embeddings"""
    
    def __init__(self, vector_db_path: str = "./chroma_db"):
        self.vector_db_path = vector_db_path
        print(f"   💾 Vector DB path: {vector_db_path}")
    
    def ingest_method(self, method: MethodMetadata) -> str:
        """Create embedding and store (simulated for now)"""
        embedding_text = self._create_embedding_text(method)
        
        # Generate a simple hash-based ID
        embedding_id = f"vec_{hash(method.id) % 1000000}"
        
        # In production: Store in ChromaDB/Pinecone
        # self.collection.add(documents=[embedding_text], ids=[method.id])
        
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
    
    def run(self) -> List[MethodMetadata]:
        """Execute full pipeline"""
        print("=" * 80)
        print("🚀 REUSABILITY RAG PIPELINE STARTING")
        print("=" * 80)
        
        print("\n🔍 Phase 1: Scanning files...")
        files = self.scanner.scan()
        print(f"   ✅ Found {len(files)} source files")
        for f in files[:5]:
            print(f"      - {f['path']}")
        if len(files) > 5:
            print(f"      ... and {len(files) - 5} more")
        
        print("\n📝 Phase 2: Extracting methods...")
        all_methods = []
        for file_info in files:
            methods = self.extractor.extract_methods(file_info['path'], file_info['language'])
            all_methods.extend(methods)
            if methods:
                print(f"   ✅ {file_info['path']}: {len(methods)} methods")
        print(f"   ✅ Total extracted: {len(all_methods)} methods")
        
        if not all_methods:
            print("   ⚠️  No methods found! Check your code files.")
            return []
        
        print("\n🔗 Phase 3: Building call graph...")
        all_methods = self.extractor.build_call_graph(all_methods)
        print(f"   ✅ Call graph built")
        
        print("\n🤖 Phase 4: Analyzing reusability with Gemini API...")
        for i, method in enumerate(all_methods, 1):
            print(f"   [{i}/{len(all_methods)}] Analyzing: {method['method_name']}")
            method = self.rag.analyze_reusability(method)
        
        reusable_methods = [m for m in all_methods if m.get('reusable', False)]
        print(f"   ✅ Found {len(reusable_methods)} reusable methods")
        
        if not reusable_methods:
            print("   ⚠️  No reusable methods identified.")
            return []
        
        print("\n🏷️  Phase 5: Generating MADL metadata...")
        for i, method in enumerate(reusable_methods, 1):
            print(f"   [{i}/{len(reusable_methods)}] MADL for: {method['method_name']}")
            method['madl'] = self.madl_gen.generate_madl(method)
        
        print("\n💾 Phase 6: Ingesting into vector database...")
        method_objects = []
        for method in reusable_methods:
            if 'madl' not in method:
                method['madl'] = {}
            
            metadata = MethodMetadata(**method)
            embedding_id = self.ingester.ingest_method(metadata)
            metadata.embedding_id = embedding_id
            method_objects.append(metadata)
        
        print(f"   ✅ Ingested {len(method_objects)} methods")
        
        print("\n" + "=" * 80)
        print(f"✅ PIPELINE COMPLETE! Processed {len(method_objects)} reusable methods")
        print("=" * 80)
        
        return method_objects


# Example usage
if __name__ == "__main__":
    # Gemini API key
    GEMINI_API_KEY = "AIzaSyCO6OP6UJ0dzTB1M7yRE3sU07jA4WbQ23k"
    
    pipeline = ReusabilityPipeline(
        root_path=r"C:\Users\vedan\Downloads\RAG-model",
        api_key="AIzaSyAVTWIDAWHBVAEQ9F5CPdi3pYOF8amLmPQ"
    )
    
    results = pipeline.run()
    
    # Save results
    output_file = "reusable_methods.json"
    with open(output_file, "w") as f:
        json.dump([m.to_dict() for m in results], f, indent=2)
    
    print(f"\n📄 Results saved to: {output_file}")
    
    if results:
        print("\n📊 Sample result:")
        print(json.dumps(results[0].to_dict(), indent=2))
        
        print(f"\n📈 Summary Statistics:")
        print(f"   Total reusable methods: {len(results)}")
        print(f"   Average confidence: {sum(m.confidence for m in results) / len(results):.2f}")
        
        languages = {}
        for m in results:
            languages[m.language] = languages.get(m.language, 0) + 1
        print(f"   Methods by language: {languages}")