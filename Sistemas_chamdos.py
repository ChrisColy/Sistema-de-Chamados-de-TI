import sqlite3
from datetime import datetime


def conectar():
    return sqlite3.connect("chamados.db")


def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            solicitante TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Aberto',
            data_abertura TEXT NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()


def abrir_chamado():
    print("\n--- NOVO CHAMADO ---")
    titulo = input("Título: ").strip()
    descricao = input("Descrição: ").strip()
    solicitante = input("Seu nome: ").strip()

    print("Prioridade: 1 - Baixa | 2 - Média | 3 - Alta")
    opcao = input("Escolha (1, 2 ou 3): ").strip()
    prioridades = {"1": "Baixa", "2": "Média", "3": "Alta"}
    prioridade = prioridades.get(opcao, "Baixa")

    if not titulo or not descricao or not solicitante:
        print("Erro: todos os campos são obrigatórios.")
        return

    data_abertura = datetime.now().strftime("%d/%m/%Y %H:%M")

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO chamados (titulo, descricao, solicitante, prioridade, data_abertura)
        VALUES (?, ?, ?, ?, ?)
        """,
        (titulo, descricao, solicitante, prioridade, data_abertura),
    )
    conexao.commit()
    numero = cursor.lastrowid
    conexao.close()

    print(f"Chamado #{numero} aberto com sucesso!")

def listar_chamados():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, titulo, solicitante, prioridade, status, data_abertura FROM chamados ORDER BY id DESC"
    )
    chamados = cursor.fetchall()
    conexao.close()

    print("\n--- LISTA DE CHAMADOS ---")

    if not chamados:
        print("Nenhum chamado encontrado.")
        return

    for chamado in chamados:
        id_, titulo, solicitante, prioridade, status, data = chamado
        print(f"#{id_} | {titulo}")
        print(f"    Solicitante: {solicitante} | Prioridade: {prioridade}")
        print(f"    Status: {status} | Aberto em: {data}")
        print("-" * 40)

def atualizar_status():
    listar_chamados()

    print("\n--- ATUALIZAR STATUS ---")
    numero = input("Número do chamado: ").strip()

    if not numero.isdigit():
        print("Erro: digite apenas o número do chamado.")
        return

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, status FROM chamados WHERE id = ?", (numero,))
    chamado = cursor.fetchone()

    if chamado is None:
        conexao.close()
        print(f"Chamado #{numero} não encontrado.")
        return

    print(f"Status atual: {chamado[1]}")
    print("Novo status: 1 - Aberto | 2 - Em andamento | 3 - Fechado")
    opcao = input("Escolha (1, 2 ou 3): ").strip()

    status_opcoes = {"1": "Aberto", "2": "Em andamento", "3": "Fechado"}
    novo_status = status_opcoes.get(opcao)

    if novo_status is None:
        conexao.close()
        print("Opção inválida. Nada foi alterado.")
        return

    cursor.execute("UPDATE chamados SET status = ? WHERE id = ?", (novo_status, numero))
    conexao.commit()
    conexao.close()

    print(f"Chamado #{numero} atualizado para: {novo_status}")    


def menu():
    while True:
        print("\n===== SISTEMA DE CHAMADOS =====")
        print("1 - Abrir chamado")
        print("2 - Listar chamados")
        print("3 - Atualizar status")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            abrir_chamado()
        elif opcao == "2":
            listar_chamados()
        elif opcao == "3":
            atualizar_status()
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    criar_tabela()
    menu()