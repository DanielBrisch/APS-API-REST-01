# resultados_routes.py

from fastapi import APIRouter, HTTPException, status, Body
from sqlmodel import select

from src.config.database import get_session
from src.models.provas_model import Provas
from src.models.resultados_model import Resultados

resultados_router = APIRouter(prefix="/resultados_provas")

@resultados_router.post("", status_code=status.HTTP_201_CREATED)
def cria_resultado_prova(resultado: Resultados):
    with get_session() as session:
        # Verificar se a prova existe
        prova = session.exec(select(Provas).where(Provas.id == resultado.prova_id)).first()
        if not prova:
            raise HTTPException(status_code=404, detail="Prova não cadastrada")

        # Calcular a nota
        nota_final = sum(
            getattr(prova, f"q{i}") == getattr(resultado, f"q{i}")
            for i in range(1, 11)
        )
        resultado.nota = nota_final

        # Adicionar resultado no banco de dados
        session.add(resultado)
        session.commit()
        session.refresh(resultado)

        return resultado

@resultados_router.get("/{prova_id}")
def get_resultados_prova(prova_id: int):
    with get_session() as session:
        prova = session.exec(select(Provas).where(Provas.id == prova_id)).first()
        if not prova:
            raise HTTPException(status_code=404, detail="Prova não encontrada")

        resultados = session.exec(select(Resultados).where(Resultados.prova_id == prova_id)).all()

        resultados_formatados = []
        for resultado in resultados:
            status_aluno = "reprovado"
            if resultado.nota >= 7:
                status_aluno = "aprovado"
            elif 5 <= resultado.nota < 7:
                status_aluno = "recuperação"

            resultados_formatados.append({
                "nome": resultado.nome,
                "nota": resultado.nota,
                "resultado": status_aluno
            })

        return {
            "descricao_prova": prova.descricao,
            "data_prova": prova.data_prova,
            "resultados": resultados_formatados
        }

@resultados_router.patch("/{resultado_id}")
def atualiza_respostas_prova(resultado_id: int, respostas: dict = Body(...)):
    with get_session() as session:
        resultado = session.exec(select(Resultados).where(Resultados.id == resultado_id)).first()
        if not resultado:
            raise HTTPException(status_code=404, detail="Resultado não encontrado")

        for i in range(1, 11):
            setattr(resultado, f"q{i}", respostas.get(f"q{i}", getattr(resultado, f"q{i}")))

        prova = session.exec(select(Provas).where(Provas.id == resultado.prova_id)).first()
        if not prova:
            raise HTTPException(status_code=404, detail="Prova não encontrada")

        nota_final = sum(
            getattr(prova, f"q{i}") == getattr(resultado, f"q{i}")
            for i in range(1, 11)
        )
        resultado.nota = nota_final

        session.commit()
        session.refresh(resultado)

        return resultado
