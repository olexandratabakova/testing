from pydantic import BaseModel, RootModel
from enum import Enum
from typing import List
class RelationType(str, Enum):
    co_occurrence = "co-occurrence"
    context = "context"

class Relation(BaseModel):
    node1: str
    node2: str
    relation_type: RelationType
    topic_terms: List[str]
    typical_lexicon: List[str]

class RelationListPoetry(RootModel[List[Relation]]):
    pass