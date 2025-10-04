from pydantic import BaseModel, RootModel
from enum import Enum
from typing import List

class RelationType(str, Enum):
    command = "command"
    conflict = "conflict"
    cooperation = "cooperation"

class Polarity(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class Relation(BaseModel):
    person1: str
    person2: str
    relation_type: RelationType
    polarity: Polarity

class RelationList(RootModel[List[Relation]]):
    pass