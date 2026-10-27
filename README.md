from datetime import datetime
from enum import Enum
from typing import Optional

import sqlite3
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field


DB_NAME = "chamados.db"

app = FastAPI(
    title="Sistema de Chamados de TI",
    description="API simples para abertura, consulta, atualização e exclusão de chamados de suporte.",
    version="1.0.0",
)


class Status(str, Enum):
    aberto = "Aberto"
    em_andamento = "Em andamento"
    resolvido = "Resolvido"
    fechado = "Fechado"


class Prioridade(str, Enum):
    baixa = "Baixa"
    media = "Média"
    alta = "Alta"


class ChamadoCreate(BaseModel):
    solicitante: str = Field(min_length=2, max_length=100)
    email: str = Field(min_length=5, max_length=150)
    titulo: str = Field(min_length=3, max_length=150)
    descricao: str = Field(min_length=5, max_length=2000)
    categoria: str = Field(min_length=2, max_length=80)
    prioridade: Prioridade = Prioridade.media


class ChamadoUpdate(BaseModel):
    status: Optional[Status] = None
    prioridade: Optional[Prioridade] = None
    tecnico_responsavel: Optional[str] = Field(default=None, max_length=100)
    solucao: Optional[str] = Field(default=None, max_length=2000)


def conectar():
    """Abre conexão com o banco SQLite."""
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def inicializar_banco():
    with conectar() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS chamados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                solicitante TEXT NOT NULL,
                email TEXT NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                categoria TEXT NOT NULL,
                prioridade TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Aberto',
                tecnico_responsavel TEXT,
                solucao TEXT,
                criado_em TEXT NOT NULL,
                atualizado_em TEXT NOT NULL
            )
            """
        )
        conn.commit()


@app.on_event("startup")
def startup():
    inicializar_banco()


def chamado_dict(row):
    return dict(row) if row else None


@app.get("/")
def inicio():
    return {
        "mensagem": "Bem-vindo ao Sistema de Chamados de TI!",
        "documentacao": "/docs",
        "rotas_principais": [
            "POST /chamados",
            "GET /chamados",
            "GET /chamados/{id}",
            "PATCH /chamados/{id}",
            "DELETE /chamados/{id}",
        ],
    }


@app.post("/chamados", status_code=201)
def criar_chamado(dados: ChamadoCreate):
    agora = datetime.now().isoformat(timespec="seconds")
    with conectar() as conn:
        cursor = conn.execute(
            """
            INSERT INTO chamados
            (solicitante, email, titulo, descricao, categoria, prioridade,
             status, criado_em, atualizado_em)
            VALUES (?, ?, ?, ?, ?, ?, 'Aberto', ?, ?)
            """,
            (
                dados.solicitante,
                dados.email,
                dados.titulo,
                dados.descricao,
                dados.categoria,
                dados.prioridade.value,
                agora,
                agora,
            ),
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM chamados WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return chamado_dict(row)


@app.get("/chamados")
def listar_chamados(
    status: Optional[Status] = Query(default=None),
    prioridade: Optional[Prioridade] = Query(default=None),
    categoria: Optional[str] = Query(default=None),
):
    query = "SELECT * FROM chamados WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status.value)
    if prioridade:
        query += " AND prioridade = ?"
        params.append(prioridade.value)
    if categoria:
        query += " AND categoria LIKE ?"
        params.append(f"%{categoria}%")

    query += " ORDER BY criado_em DESC"

    with conectar() as conn:
        rows = conn.execute(query, params).fetchall()
    return [chamado_dict(row) for row in rows]


@app.get("/chamados/{chamado_id}")
def consultar_chamado(chamado_id: int):
    with conectar() as conn:
        row = conn.execute(
            "SELECT * FROM chamados WHERE id = ?", (chamado_id,)
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Chamado não encontrado.")
    return chamado_dict(row)


@app.patch("/chamados/{chamado_id}")
def atualizar_chamado(chamado_id: int, dados: ChamadoUpdate):
    atualizacoes = dados.model_dump(exclude_unset=True)

    if not atualizacoes:
        raise HTTPException(
            status_code=400,
            detail="Informe pelo menos um campo para atualizar.",
        )

    # Converte os enums para seus valores textuais antes de salvar.
    for campo, valor in list(atualizacoes.items()):
        if isinstance(valor, Enum):
            atualizacoes[campo] = valor.value

    atualizacoes["atualizado_em"] = datetime.now().isoformat(timespec="seconds")

    campos_permitidos = {
        "status",
        "prioridade",
        "tecnico_responsavel",
        "solucao",
        "atualizado_em",
    }
    campos = [campo for campo in atualizacoes if campo in campos_permitidos]
    set_clause = ", ".join(f"{campo} = ?" for campo in campos)
    valores = [atualizacoes[campo] for campo in campos]

    with conectar() as conn:
        existente = conn.execute(
            "SELECT id FROM chamados WHERE id = ?", (chamado_id,)
        ).fetchone()
        if not existente:
            raise HTTPException(status_code=404, detail="Chamado não encontrado.")

        conn.execute(
            f"UPDATE chamados SET {set_clause} WHERE id = ?",
            valores + [chamado_id],
        )
        conn.commit()
        row = conn.execute(
            "SELECT * FROM chamados WHERE id = ?", (chamado_id,)
        ).fetchone()

    return chamado_dict(row)


@app.delete("/chamados/{chamado_id}")
def excluir_chamado(chamado_id: int):
    with conectar() as conn:
        cursor = conn.execute(
            "DELETE FROM chamados WHERE id = ?", (chamado_id,)
        )
        conn.commit()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Chamado não encontrado.")

    return {"mensagem": f"Chamado {chamado_id} excluído com sucesso."}
