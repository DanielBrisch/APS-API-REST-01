from typing import Optional

from sqlmodel import Field, Relationship, SQLModel
from src.models.provas_model import Provas

class Resultados(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nome: str
    q1: str
    q2: str
    q3: str
    q4: str
    q5: str
    q6: str
    q7: str
    q8: str
    q9: str
    q10: str
    nota: float = Optional[float]
    prova_id: int = Field(nullable=False, foreign_key="provas.id")
    provas: Optional[Provas] = Relationship(back_populates="resultados")