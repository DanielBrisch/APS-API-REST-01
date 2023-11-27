# provas_routes.py

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from src.models.provas_model import Provas
from src.config.database import get_session

provas_router = APIRouter(prefix="/provas")

@provas_router.post("", status_code=status.HTTP_201_CREATED)
def cria_prova(prova: Provas):
    with get_session() as session:
        # Verificar se já existe uma prova com a mesma descrição e data
        statement = select(Provas).where(Provas.descricao == prova.descricao, Provas.data_prova == prova.data_prova)
        resultado = session.exec(statement).first()

        if resultado:
            # Se já existe, retorna erro 400
            raise HTTPException(status_code=400, detail="Prova já cadastrada.")

        # Se não existir, adiciona a nova prova
        session.add(prova)
        session.commit()
        session.refresh(prova)
        return prova

@provas_router.delete("/{prova_id}", status_code=status.HTTP_200_OK)
def deleta_prova(prova_id: int):
    with get_session() as session:
        
        resultado = session.exec(select(Resultados).where(Resultados.prova_id == prova_id)).first()
        if resultado:
            raise HTTPException(status_code=400, detail="Não é possível excluir a prova, pois existem resultados associados.")

        prova = session.exec(select(Provas).where(Provas.id == prova_id)).first()
        if not prova:
            raise HTTPException(status_code=404, detail="Prova não encontrada")

        session.delete(prova)
        session.commit()
        return {"detail": "Prova excluída com sucesso"}
