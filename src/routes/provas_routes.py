# provas_routes.py

from fastapi import APIRouter

from src.models.provas_model import Provas
from src.config.database import get_session

provas_router = APIRouter(prefix="/provas")

@provas_router.post("")
def cria_prova(prova: Provas):
    with get_session() as session:
        session.add(prova)
        session.commit()
        session.refresh(prova)
        return prova