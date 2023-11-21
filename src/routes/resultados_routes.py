# resultados_routes.py

from fastapi import APIRouter
from sqlmodel import select

from src.config.database import get_session
from src.models.provas_model import Provas
from src.models.resultados_model import Resultados

resultados_router = APIRouter(prefix="/resultados")


@resultados_router.post("")
def cria_prova(resultado: Resultados):
    with get_session() as session:
        # Calcular a nota baseado nas questòes da prova

        # Buscar a prova do banco de dados
        statement = select(Provas).where(Provas.id == resultado.prova_id)
        prova = session.exec(statement).first()

        # se tiver prova, vai calcular a nota

        
        resultado.nota = 10

        session.add(resultado)
        session.commit()
        session.refresh(resultado)
        return resultado
