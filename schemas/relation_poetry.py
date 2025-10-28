from pydantic import BaseModel, RootModel
from enum import Enum
from typing import List

class RelationType(str, Enum):
    co_occurrence = "co-occurrence"
    contextual = "contextual"
    metaphoric = "metaphoric"
    emotional_association = "emotional_association"

class Relation(BaseModel):
    node1: str
    node2: str
    relation_type: RelationType
    topic_terms: List[str]
    dominant_emotion: str
    symbolic_layer: str
    typical_lexicon: List[str]

class RelationListPoetry(RootModel[List[Relation]]):
    pass
