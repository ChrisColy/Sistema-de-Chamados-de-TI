c# Sistema de Chamados de TI

API REST desenvolvida em Python para registrar e gerenciar chamados de suporte técnico.

## Funcionalidades

- Abrir chamados
- Listar chamados
- Consultar um chamado pelo ID
- Filtrar por status, prioridade ou categoria
- Atualizar status, prioridade, técnico responsável e solução
- Excluir chamados

## Tecnologias

- Python
- FastAPI
- SQLite
- Uvicorn

## Como executar

1. Instale o Python 3.10 ou superior.
2. Abra o terminal na pasta do projeto.
3. Crie e ative um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv .venv
   ```

   Windows:

   ```bash
   .venv\Scripts\activate
   ```

   macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

4. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

5. Inicie a API:

   ```bash
   uvicorn main:app --reload
   ```

6. Abra a documentação interativa:

   http://127.0.0.1:8000/docs

O banco `chamados.db` será criado automaticamente ao iniciar a aplicação.

## Exemplo de chamado

Use `POST /chamados` com este JSON:

```json
{
  "solicitante": "Maria Silva",
  "email": "maria@empresa.com",
  "titulo": "Computador não liga",
  "descricao": "O computador não liga após queda de energia.",
  "categoria": "Hardware",
  "prioridade": "Alta"
}
```

## Rotas

| Método | Rota | Ação |
|---|---|---|
| GET | `/` | Informações da API |
| POST | `/chamados` | Criar chamado |
| GET | `/chamados` | Listar e filtrar chamados |
| GET | `/chamados/{id}` | Consultar chamado |
| PATCH | `/chamados/{id}` | Atualizar chamado |
| DELETE | `/chamados/{id}` | Excluir chamado |

## Observação

Este é um projeto de estudo/portfólio. Não possui autenticação ou autorização de usuários e não deve ser utilizado em produção sem melhorias de segurança.
