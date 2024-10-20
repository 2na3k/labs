from pydantic import BaseModel, Field
from typing import List 

from labs.utils.enums import BaseEnum

"""
Entity model here
chunker -> retrieval from database(BM25 or model embedder)
"""

class RetrievalModel(BaseEnum):
    BM25 = "BM25"
    BGE = "BAAI/bge-m3"

class RerankerModel(BaseEnum):
    BGE = "BAAI/bge-reranker-v2-m3"

class Chunk(BaseModel):
    context: str
    documents: List[str]

class EmbeddingType:
    SINGLE = "SINGLE"
    MIX = "MIX"

class EmbedderConfig(BaseModel):
    embedding_type: EmbeddingType = Field()
    max_token_per_chunk: int = Field()
    

