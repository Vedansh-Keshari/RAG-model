"""
COMPLETE GUIDE: Integrating Qdrant Vector Database
================================================================================
This script shows how to push reusable methods + MADL metadata to Qdrant Cloud

PREREQUISITES:
1. Install Qdrant client: pip install qdrant-client
2. Install sentence-transformers for embeddings: pip install sentence-transformers
3. Get your Qdrant API key from: https://cloud.qdrant.io/

YOUR QDRANT DETAILS:
- Cluster ID: 059f73a2-60c9-40b4-a87f-afc6832b0e27
- Endpoint: https://059f73a2-60c9-40b4-a87f-afc6832b0e27.us-east4-0.gcp.cloud.qdrant.io
- Collection Name: reusable_methods (you can change this)
================================================================================
"""

import os
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
from sentence_transformers import SentenceTransformer


@dataclass
class MethodMetadata:
    """Your existing MethodMetadata structure"""
    id: str
    file_path: str
    language: str
    class_name: str
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
    confidence: float
    embedding_id: str = None


class QdrantVectorDB:
    """
    Complete Qdrant Vector Database integration
    Handles: Connection, Collection Creation, Embedding, Upload, Search
    """
    
    def __init__(
        self,
        cluster_url: str,
        api_key: str,
        collection_name: str = "reusable_methods",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize Qdrant client and embedding model
        
        Args:
            cluster_url: Your Qdrant cloud endpoint
            api_key: *******8YGzd_aI
            collection_name: Name for your collection
            embedding_model: HuggingFace model for embeddings (384 dimensions)
        """
        print(f"[INIT] Connecting to Qdrant Cloud...")
        self.client = QdrantClient(
            url=cluster_url,
            api_key=api_key,
            timeout=60  # Increase timeout for large operations
        )
        
        self.collection_name = collection_name
        
        print(f"[INIT] Loading embedding model: {embedding_model}...")
        self.encoder = SentenceTransformer(embedding_model)
        self.vector_size = self.encoder.get_sentence_embedding_dimension()
        
        print(f"[INIT] Vector dimension: {self.vector_size}")
        print(f"[OK] Qdrant initialized successfully!")
    
    def create_collection(self, recreate: bool = False):
        """
        Create collection in Qdrant for storing method embeddings
        
        Args:
            recreate: If True, deletes existing collection and creates new one
        """
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            
            if exists:
                if recreate:
                    print(f"[DELETE] Removing existing collection: {self.collection_name}")
                    self.client.delete_collection(self.collection_name)
                else:
                    print(f"[EXISTS] Collection '{self.collection_name}' already exists")
                    return
            
            # Create new collection
            print(f"[CREATE] Creating collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE  # Cosine similarity for semantic search
                )
            )
            print(f"[OK] Collection created successfully!")
        
        except Exception as e:
            print(f"[ERROR] Failed to create collection: {e}")
            raise
    
    def generate_embedding(self, method: MethodMetadata) -> List[float]:
        """
        Generate embedding vector for a method using its metadata
        
        Args:
            method: MethodMetadata object
            
        Returns:
            List of floats (embedding vector)
        """
        # Combine all relevant text for embedding
        embedding_text = self._create_embedding_text(method)
        
        # Generate embedding
        embedding = self.encoder.encode(embedding_text, convert_to_numpy=True)
        
        return embedding.tolist()
    
    def _create_embedding_text(self, method: MethodMetadata) -> str:
        """
        Create rich text representation for embedding
        Combines method signature, MADL metadata, and source code
        """
        madl = method.madl or {}
        
        # Extract MADL fields
        intent = madl.get('intent', '')
        description = madl.get('semantic_description', '')
        keywords = ', '.join(madl.get('keywords', []))
        
        # Build comprehensive text
        parts = [
            f"Method: {method.method_name}",
            f"Class: {method.class_name or 'module-level'}",
            f"Language: {method.language}",
            f"Signature: {method.signature}",
            f"Intent: {intent}",
            f"Description: {description}",
            f"Keywords: {keywords}",
            f"Reusability: {method.reusability_reason}",
            f"Source code: {method.source[:300]}"  # First 300 chars
        ]
        
        return "\n".join(parts)
    
    def upload_method(self, method: MethodMetadata, point_id: int) -> bool:
        """
        Upload a single method to Qdrant
        
        Args:
            method: MethodMetadata object
            point_id: Unique integer ID for this point
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate embedding
            embedding = self.generate_embedding(method)
            
            # Prepare payload (all metadata except embedding)
            payload = {
                "method_id": method.id,
                "file_path": method.file_path,
                "language": method.language,
                "class_name": method.class_name or "",
                "method_name": method.method_name,
                "signature": method.signature,
                "start_line": method.start_line,
                "end_line": method.end_line,
                "source": method.source,
                "calls": method.calls,
                "called_by": method.called_by,
                "reusable": method.reusable,
                "reusability_reason": method.reusability_reason,
                "confidence": method.confidence,
                
                # MADL metadata (flattened for easy filtering)
                "madl_intent": method.madl.get('intent', ''),
                "madl_description": method.madl.get('semantic_description', ''),
                "madl_keywords": method.madl.get('keywords', []),
                "madl_parameters": method.madl.get('parameters', ''),
                "madl_full": json.dumps(method.madl)  # Full MADL as JSON string
            }
            
            # Create point
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload
            )
            
            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            return True
        
        except Exception as e:
            print(f"[ERROR] Failed to upload {method.method_name}: {e}")
            return False
    
    def batch_upload(self, methods: List[MethodMetadata], batch_size: int = 100):
        """
        Upload multiple methods in batches for efficiency
        
        Args:
            methods: List of MethodMetadata objects
            batch_size: Number of methods to upload per batch
        """
        total = len(methods)
        print(f"\n[UPLOAD] Starting batch upload of {total} methods...")
        
        points = []
        successful = 0
        failed = 0
        
        for idx, method in enumerate(methods, 1):
            try:
                # Generate embedding
                embedding = self.generate_embedding(method)
                
                # Prepare payload
                payload = {
                    "method_id": method.id,
                    "file_path": method.file_path,
                    "language": method.language,
                    "class_name": method.class_name or "",
                    "method_name": method.method_name,
                    "signature": method.signature,
                    "start_line": method.start_line,
                    "end_line": method.end_line,
                    "source": method.source,
                    "calls": method.calls,
                    "called_by": method.called_by,
                    "reusable": method.reusable,
                    "reusability_reason": method.reusability_reason,
                    "confidence": method.confidence,
                    "madl_intent": method.madl.get('intent', ''),
                    "madl_description": method.madl.get('semantic_description', ''),
                    "madl_keywords": method.madl.get('keywords', []),
                    "madl_parameters": method.madl.get('parameters', ''),
                    "madl_full": json.dumps(method.madl)
                }
                
                # Create point
                point = PointStruct(
                    id=idx,
                    vector=embedding,
                    payload=payload
                )
                points.append(point)
                
                # Upload batch when size is reached
                if len(points) >= batch_size:
                    self.client.upsert(
                        collection_name=self.collection_name,
                        points=points
                    )
                    successful += len(points)
                    print(f"   [BATCH] Uploaded {successful}/{total} methods")
                    points = []
            
            except Exception as e:
                print(f"   [ERROR] Failed to process {method.method_name}: {e}")
                failed += 1
        
        # Upload remaining points
        if points:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            successful += len(points)
        
        print(f"[OK] Upload complete! Success: {successful}, Failed: {failed}")
    
    def search(
        self,
        query: str,
        limit: int = 5,
        language_filter: str = None,
        min_confidence: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Search for similar methods using semantic search
        
        Args:
            query: Natural language query (e.g., "function to validate email")
            limit: Number of results to return
            language_filter: Filter by language (e.g., "python")
            min_confidence: Minimum reusability confidence score
            
        Returns:
            List of matching methods with scores
        """
        try:
            # Generate query embedding
            query_embedding = self.encoder.encode(query, convert_to_numpy=True).tolist()
            
            # Build filters
            filters = []
            if language_filter:
                filters.append(
                    FieldCondition(
                        key="language",
                        match=MatchValue(value=language_filter)
                    )
                )
            
            filter_obj = Filter(must=filters) if filters else None
            
            # Search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                query_filter=filter_obj,
                with_payload=True
            )
            
            # Format results
            matches = []
            for result in results:
                if result.payload.get('confidence', 0) >= min_confidence:
                    matches.append({
                        'score': result.score,
                        'method_name': result.payload['method_name'],
                        'class_name': result.payload['class_name'],
                        'language': result.payload['language'],
                        'signature': result.payload['signature'],
                        'intent': result.payload.get('madl_intent', ''),
                        'description': result.payload.get('madl_description', ''),
                        'confidence': result.payload['confidence'],
                        'source': result.payload['source'][:200] + "..."
                    })
            
            return matches
        
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
            return []
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "total_points": info.points_count,
                "vector_size": info.config.params.vectors.size,
                "distance_metric": info.config.params.vectors.distance,
                "status": info.status
            }
        except Exception as e:
            print(f"[ERROR] Failed to get stats: {e}")
            return {}


def load_methods_from_json(json_file: str) -> List[MethodMetadata]:
    """Load methods from your reusable_methods.json file"""
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    methods = []
    for item in data:
        method = MethodMetadata(
            id=item['id'],
            file_path=item['file_path'],
            language=item['language'],
            class_name=item.get('class_name', ''),
            method_name=item['method_name'],
            signature=item['signature'],
            start_line=item['start_line'],
            end_line=item['end_line'],
            source=item['source'],
            calls=item['calls'],
            called_by=item['called_by'],
            reusable=item['reusable'],
            reusability_reason=item['reusability_reason'],
            madl=item.get('madl', {}),
            confidence=item.get('confidence', 0.0),
            embedding_id=item.get('embedding_id', '')
        )
        methods.append(method)
    
    return methods


# ==============================================================================
# MAIN EXECUTION SCRIPT
# ==============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("QDRANT VECTOR DATABASE INTEGRATION")
    print("=" * 80)
    
    # ========== STEP 1: Configuration ==========
    QDRANT_URL = "https://059f73a2-60c9-40b4-a87f-afc6832b0e27.us-east4-0.gcp.cloud.qdrant.io"
    QDRANT_API_KEY = "*******8YGzd_aI"  # Get from cloud.qdrant.io
    COLLECTION_NAME = "reusable_methods"
    JSON_FILE = "reusable_methods.json"
    
    # Validate API key
    if QDRANT_API_KEY == "*******8YGzd_aI":
        print("\n[ERROR] Please set your QDRANT_API_KEY!")
        print("Get it from: https://cloud.qdrant.io/")
        exit(1)
    
    # ========== STEP 2: Initialize Qdrant ==========
    print("\n[STEP 1] Initializing Qdrant client...")
    qdrant = QdrantVectorDB(
        cluster_url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=COLLECTION_NAME
    )
    
    # ========== STEP 3: Create Collection ==========
    print("\n[STEP 2] Creating collection...")
    qdrant.create_collection(recreate=False)  # Set to True to recreate
    
    # ========== STEP 4: Load Methods ==========
    print("\n[STEP 3] Loading methods from JSON...")
    methods = load_methods_from_json(JSON_FILE)
    print(f"[OK] Loaded {len(methods)} methods")
    
    # ========== STEP 5: Upload to Qdrant ==========
    print("\n[STEP 4] Uploading methods to Qdrant...")
    qdrant.batch_upload(methods, batch_size=50)
    
    # ========== STEP 6: Verify Upload ==========
    print("\n[STEP 5] Verifying upload...")
    stats = qdrant.get_collection_stats()
    print(f"[STATS] Collection Statistics:")
    for key, value in stats.items():
        print(f"  - {key}: {value}")
    
    # ========== STEP 7: Test Search ==========
    print("\n[STEP 6] Testing semantic search...")
    
    test_queries = [
        "function to validate user input",
        "method for data processing",
        "authentication related code"
    ]
    
    for query in test_queries:
        print(f"\n  Query: '{query}'")
        results = qdrant.search(query, limit=3)
        
        for i, result in enumerate(results, 1):
            print(f"    {i}. {result['method_name']} (score: {result['score']:.3f})")
            print(f"       Intent: {result['intent'][:60]}...")
    
    print("\n" + "=" * 80)
    print("QDRANT SETUP COMPLETE!")
    print("=" * 80)
    print("\nYour vector database is now ready for:")
    print("  ✓ Semantic search of reusable methods")
    print("  ✓ AI agent retrieval and composition")
    print("  ✓ Intelligent code recommendation")
    print("\nNext steps:")
    print("  1. Integrate search into your IDE/agent")
    print("  2. Build RAG pipeline for code generation")
    print("  3. Create API endpoints for method retrieval")