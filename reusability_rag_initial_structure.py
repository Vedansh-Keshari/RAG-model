"""
ReusabilityRAG - Core system for extracting, analyzing, and indexing reusable code methods
Phases: A (Build RAG), C (Improve RAG), E (Add MADL)
"""

import os
import json
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

# Mock imports - replace with actual libraries
# from tree_sitter import Language, Parser  # For robust parsing
# from openai import OpenAI  # For embeddings & LLM calls
# import chromadb  # For vector storage
# import psycopg2  # For metadata storage


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
        # In production, initialize tree-sitter parsers for each language
        self.parsers = {}
    
    def extract_methods(self, file_path: str, language: str) -> List[Dict[str, Any]]:
        """Extract all methods from a file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Simple regex-based extraction (replace with tree-sitter in production)
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
        
        # Simple pattern matching (use AST or tree-sitter in production)
        method_pattern = re.compile(r'^\s*(def|async def)\s+(\w+)\s*\((.*?)\):')
        
        current_class = None
        for i, line in enumerate(lines, 1):
            class_match = re.match(r'^class\s+(\w+)', line)
            if class_match:
                current_class = class_match.group(1)
            
            method_match = method_pattern.match(line)
            if method_match:
                method_name = method_match.group(2)
                params = method_match.group(3)
                
                # Extract method body (simple version)
                start_line = i
                indent = len(line) - len(line.lstrip())
                end_line = start_line
                
                for j in range(i, len(lines)):
                    if lines[j].strip() and not lines[j].startswith(' ' * (indent + 1)) and j > i:
                        end_line = j
                        break
                else:
                    end_line = len(lines)
                
                method_source = '\n'.join(lines[start_line-1:end_line])
                
                # Extract function calls (simple regex)
                calls = re.findall(r'(\w+)\s*\(', method_source)
                calls = list(set([c for c in calls if c != method_name]))
                
                method_id = f"file://{file_path}::{current_class or 'module'}::{method_name}::line{start_line}"
                
                methods.append({
                    'id': method_id,
                    'file_path': file_path,
                    'language': 'python',
                    'class_name': current_class,
                    'method_name': method_name,
                    'signature': f"def {method_name}({params})",
                    'start_line': start_line,
                    'end_line': end_line,
                    'source': method_source,
                    'calls': calls,
                    'called_by': []  # Will be populated by call graph analysis
                })
        
        return methods
    
    def _extract_java_methods(self, source: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract Java methods (simplified)"""
        # Implement similar to Python but with Java patterns
        # In production, use tree-sitter for accurate parsing
        return []
    
    def build_call_graph(self, all_methods: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build call graph to populate called_by fields"""
        method_map = {m['method_name']: m for m in all_methods}
        
        for method in all_methods:
            for called_method_name in method['calls']:
                if called_method_name in method_map:
                    method_map[called_method_name]['called_by'].append(method['method_name'])
        
        return all_methods


class ReusabilityRAG:
    """Determines reusability and generates reasoning using RAG + LLM"""
    
    def __init__(self, api_key: str = None):
        # In production: self.client = OpenAI(api_key=api_key)
        self.client = None
    
    def analyze_reusability(self, method: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze if a method is reusable using LLM reasoning
        Returns updated method with reusable, reusability_reason, and confidence
        """
        
        # Create prompt for LLM
        prompt = self._create_reusability_prompt(method)
        
        # In production: Call Claude API
        # response = self._call_llm(prompt)
        # result = self._parse_llm_response(response)
        
        # Mock response for demonstration
        result = {
            'reusable': True,
            'reusability_reason': 'Pure function with no side effects, parameterized inputs',
            'confidence': 0.87
        }
        
        method.update(result)
        return method
    
    def _create_reusability_prompt(self, method: Dict[str, Any]) -> str:
        """Create prompt for reusability analysis"""
        return f"""Analyze if this method is reusable across different contexts.

Method: {method['method_name']}
Signature: {method['signature']}
Source:
{method['source']}

Calls: {', '.join(method['calls'])}
Called by: {', '.join(method['called_by'])}

Consider:
1. Does it have side effects?
2. Is it parameterized and context-independent?
3. Is it stateless?
4. Can it be used in different scenarios?

Return JSON:
{{
  "reusable": true/false,
  "reusability_reason": "explanation",
  "confidence": 0.0-1.0
}}"""
    
    def _call_llm(self, prompt: str) -> str:
        """Call Claude API for analysis"""
        # In production implementation:
        """
        response = await fetch("https://api.anthropic.com/v1/messages", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                model: "claude-sonnet-4-20250514",
                max_tokens: 1000,
                messages: [{"role": "user", "content": prompt}]
            })
        })
        """
        pass


class MADLGenerator:
    """Generates Method Annotation Description Language metadata"""
    
    def __init__(self, api_key: str = None):
        self.client = None  # OpenAI client in production
    
    def generate_madl(self, method: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate MADL annotations for a reusable method
        Returns MADL dict with agents, preconditions, triggers
        """
        if not method.get('reusable', False):
            return {}
        
        prompt = self._create_madl_prompt(method)
        
        # Mock MADL generation
        madl = {
            'agents': [
                {'role': 'executor', 'capability': 'run-method'}
            ],
            'preconditions': self._infer_preconditions(method),
            'triggers': self._infer_triggers(method),
            'confidence': method.get('confidence', 0.5)
        }
        
        return madl
    
    def _create_madl_prompt(self, method: Dict[str, Any]) -> str:
        """Create prompt for MADL generation"""
        return f"""Generate MADL (Method Annotation Description Language) metadata.

Method: {method['method_name']}
Source: {method['source']}
Reusability: {method['reusability_reason']}

Generate JSON:
{{
  "agents": [
    {{"role": "agent-type", "capability": "what-it-does"}}
  ],
  "preconditions": ["condition1", "condition2"],
  "triggers": ["event1", "event2"],
  "confidence": 0.0-1.0
}}"""
    
    def _infer_preconditions(self, method: Dict[str, Any]) -> List[str]:
        """Infer preconditions from method analysis"""
        preconditions = []
        source = method['source'].lower()
        
        if 'login' in source or 'auth' in source:
            preconditions.append('user_authenticated')
        if 'database' in source or 'db' in source:
            preconditions.append('database_connected')
        
        return preconditions
    
    def _infer_triggers(self, method: Dict[str, Any]) -> List[str]:
        """Infer trigger events from method context"""
        triggers = []
        method_name = method['method_name'].lower()
        
        if 'init' in method_name:
            triggers.append('initialization')
        if 'validate' in method_name:
            triggers.append('validation_required')
        
        return triggers


class VectorIngester:
    """Ingests methods into vector database with embeddings"""
    
    def __init__(self, vector_db_path: str = "./chroma_db"):
        # In production: self.client = chromadb.PersistentClient(path=vector_db_path)
        # self.collection = self.client.get_or_create_collection("reusable_methods")
        self.collection = None
    
    def ingest_method(self, method: MethodMetadata) -> str:
        """
        Create embedding and store in vector DB
        Returns embedding_id
        """
        # Create text for embedding
        embedding_text = self._create_embedding_text(method)
        
        # In production: Generate embedding
        # embedding = self._generate_embedding(embedding_text)
        
        # In production: Store in vector DB
        # embedding_id = self.collection.add(
        #     documents=[embedding_text],
        #     embeddings=[embedding],
        #     metadatas=[method.to_dict()],
        #     ids=[method.id]
        # )
        
        embedding_id = f"vec_{hash(method.id) % 100000}"
        return embedding_id
    
    def _create_embedding_text(self, method: MethodMetadata) -> str:
        """Create rich text representation for embedding"""
        return f"""
Method: {method.method_name}
Signature: {method.signature}
Language: {method.language}
Reusability: {method.reusability_reason}
MADL Agents: {', '.join([a['role'] for a in method.madl.get('agents', [])])}
Preconditions: {', '.join(method.madl.get('preconditions', []))}
Triggers: {', '.join(method.madl.get('triggers', []))}
Source: {method.source[:500]}
"""
    
    def _generate_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI or similar"""
        # In production: use text-embedding-3-small or similar
        pass
    
    def search(self, query: str, k: int = 5) -> List[MethodMetadata]:
        """Semantic search for relevant methods"""
        # In production: 
        # query_embedding = self._generate_embedding(query)
        # results = self.collection.query(query_embeddings=[query_embedding], n_results=k)
        pass


class ReusabilityPipeline:
    """Orchestrates the entire pipeline from scanning to ingestion"""
    
    def __init__(self, root_path: str, api_key: str = None):
        self.scanner = FileScanner(root_path)
        self.extractor = MethodExtractor()
        self.rag = ReusabilityRAG(api_key)
        self.madl_gen = MADLGenerator(api_key)
        self.ingester = VectorIngester()
    
    def run(self) -> List[MethodMetadata]:
        """Execute full pipeline"""
        print("🔍 Phase 1: Scanning files...")
        files = self.scanner.scan()
        print(f"   Found {len(files)} source files")
        
        print("\n📝 Phase 2: Extracting methods...")
        all_methods = []
        for file_info in files:
            methods = self.extractor.extract_methods(file_info['path'], file_info['language'])
            all_methods.extend(methods)
        print(f"   Extracted {len(all_methods)} methods")
        
        print("\n🔗 Phase 3: Building call graph...")
        all_methods = self.extractor.build_call_graph(all_methods)
        
        print("\n🤖 Phase 4: Analyzing reusability with RAG...")
        for i, method in enumerate(all_methods):
            print(f"   Analyzing {i+1}/{len(all_methods)}: {method['method_name']}")
            method = self.rag.analyze_reusability(method)
        
        reusable_methods = [m for m in all_methods if m.get('reusable', False)]
        print(f"   Found {len(reusable_methods)} reusable methods")
        
        print("\n🏷️  Phase 5: Generating MADL metadata...")
        for method in reusable_methods:
            method['madl'] = self.madl_gen.generate_madl(method)
        
        print("\n💾 Phase 6: Ingesting into vector database...")
        method_objects = []
        for method in reusable_methods:
            metadata = MethodMetadata(**method)
            embedding_id = self.ingester.ingest_method(metadata)
            metadata.embedding_id = embedding_id
            method_objects.append(metadata)
        
        print(f"\n✅ Pipeline complete! Processed {len(method_objects)} reusable methods")
        return method_objects


# Example usage
if __name__ == "__main__":
    # Use raw string (r"") or forward slashes for Windows paths
    pipeline = ReusabilityPipeline(
        root_path=r"C:\Users\vedan\Downloads\RAG-model",  # Raw string to handle backslashes
        # api_key=os.getenv("ANTHROPIC_API_KEY")
        api_key=os.getenv("AIzaSyBCT9eKXaYEmKypGEv-B6OWWkCzP-kEXbM")
        # Gemini API key : AIzaSyBCT9eKXaYEmKypGEv-B6OWWkCzP-kEXbM
    )
    
    results = pipeline.run()
    
    # Save results
    with open("reusable_methods.json", "w") as f:
        json.dump([m.to_dict() for m in results], f, indent=2)
    
    print("\n📊 Sample result:")
    if results:
        print(json.dumps(results[0].to_dict(), indent=2))
    else:
        print("No results found.")


## End of reusability_rag.py