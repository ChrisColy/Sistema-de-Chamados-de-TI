# 🎫 Sistema de Chamados

Sistema de gerenciamento de chamados (tickets) de suporte, desenvolvido em **Python** com banco de dados **SQLite** e executado direto no terminal. Permite registrar problemas, acompanhar o andamento de cada um e manter todo o histórico salvo localmente.

O projeto foi criado com fins de estudo, com foco em boas práticas básicas: código organizado em funções, validação de dados e proteção contra SQL Injection.

---

## 📋 Sumário

- [Funcionalidades](#-funcionalidades)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Como executar](#-como-executar)
- [Como usar](#-como-usar)
- [Banco de dados](#-banco-de-dados)
- [Como o código funciona](#-como-o-código-funciona)
- [Boas práticas aplicadas](#-boas-práticas-aplicadas)
- [Melhorias futuras](#-melhorias-futuras)
- [Autora](#-autora)

---

## ✨ Funcionalidades

- **Abrir chamado**: registra título, descrição, nome do solicitante e prioridade (Baixa, Média ou Alta). A data e a hora de abertura são salvas automaticamente.
- **Listar chamados**: exibe todos os chamados, do mais recente para o mais antigo, com número, título, solicitante, prioridade, status e data.
- **Atualizar status**: altera o andamento de um chamado entre **Aberto**, **Em andamento** e **Fechado**.
- **Menu interativo**: navegação simples por números, que se repete até o usuário escolher sair.
- **Validações**: campos obrigatórios, número de chamado válido e tratamento de opções inválidas, evitando que o programa quebre.
- **Persistência de dados**: os chamados ficam salvos em um arquivo local, então não se perdem ao fechar o programa.

---

## 🛠 Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| **Python 3** | Linguagem principal do projeto |
| **SQLite** (`sqlite3`) | Banco de dados local, já incluído no Python |
| **datetime** | Registro automático da data e hora de abertura |
| **Git e GitHub** | Controle de versão e hospedagem do código |

Não é necessário instalar nenhuma biblioteca externa.

---

## 📁 Estrutura do projeto

```
Sistema_Chamados/
│
├── sistema_chamados.py   # Código principal do sistema
├── README.md             # Documentação do projeto
├── .gitignore            # Arquivos ignorados pelo Git
└── chamados.db           # Banco de dados (criado automaticamente, não é enviado ao GitHub)
```

---

## ✅ Pré-requisitos

- **Python 3.8 ou superior** instalado.

Para verificar, rode no terminal:

```bash
python --version
```

Caso não esteja instalado, baixe em [python.org](https://www.python.org/downloads/).

---

## 🚀 Como executar

**1. Clone o repositório**

```bash
git clone https://github.com/SEU-USUARIO/sistema-chamados.git
```

**2. Entre na pasta do projeto**

```bash
cd sistema-chamados
```

**3. Execute o sistema**

```bash
python sistema_chamados.py
```

Na primeira execução, o arquivo `chamados.db` é criado automaticamente.

---

## 💻 Como usar

Ao iniciar, o menu principal é exibido:

```
===== SISTEMA DE CHAMADOS =====
1 - Abrir chamado
2 - Listar chamados
3 - Atualizar status
0 - Sair
Escolha uma opção:
```

### 1. Abrir chamado

Informe o título, a descrição, seu nome e a prioridade:

```
--- NOVO CHAMADO ---
Título: Internet fora do ar
Descrição: Sem acesso à rede desde o início da manhã
Seu nome: Maria
Prioridade: 1 - Baixa | 2 - Média | 3 - Alta
Escolha (1, 2 ou 3): 3
Chamado #1 aberto com sucesso!
```

### 2. Listar chamados

```
--- LISTA DE CHAMADOS ---
#1 | Internet fora do ar
    Solicitante: Maria | Prioridade: Alta
    Status: Aberto | Aberto em: 07/11/2026 14:30
----------------------------------------
```

### 3. Atualizar status

Escolha o número do chamado e o novo status:

```
Novo status: 1 - Aberto | 2 - Em andamento | 3 - Fechado
Escolha (1, 2 ou 3): 2
Chamado #1 atualizado para: Em andamento
```

### 0. Sair

Encerra o programa.

---

## 🗄 Banco de dados

Os dados ficam na tabela `chamados`, dentro do arquivo `chamados.db`:

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INTEGER | Número único do chamado (gerado automaticamente) |
| `titulo` | TEXT | Resumo do problema |
| `descricao` | TEXT | Detalhes do problema |
| `solicitante` | TEXT | Nome de quem abriu o chamado |
| `prioridade` | TEXT | Baixa, Média ou Alta |
| `status` | TEXT | Aberto, Em andamento ou Fechado (padrão: Aberto) |
| `data_abertura` | TEXT | Data e hora de criação (formato `dd/mm/aaaa hh:mm`) |

---

## 🧠 Como o código funciona

O arquivo `sistema_chamados.py` é dividido em funções, cada uma com uma responsabilidade:

| Função | O que faz |
|---|---|
| `conectar()` | Abre a conexão com o banco `chamados.db` |
| `criar_tabela()` | Cria a tabela de chamados, caso ainda não exista |
| `abrir_chamado()` | Coleta os dados, valida e insere um novo chamado |
| `listar_chamados()` | Busca e exibe todos os chamados |
| `atualizar_status()` | Localiza um chamado pelo número e altera seu status |
| `menu()` | Exibe o menu em laço e chama as demais funções |

---

## 🔒 Boas práticas aplicadas

- **Consultas parametrizadas** (`?`): os dados digitados pelo usuário nunca são colocados diretamente no comando SQL, o que protege contra **SQL Injection**.
- **Validação de entrada**: campos vazios e números inválidos são tratados antes de chegar ao banco.
- **Código modular**: cada funcionalidade em uma função, facilitando manutenção e reaproveitamento.
- **`.gitignore`**: o banco de dados com informações dos chamados não é enviado ao repositório.
- **Conexões fechadas corretamente** após cada operação.

---

## 🔮 Melhorias futuras

- [ ] Ver detalhes completos de um chamado (incluindo a descrição)
- [ ] Filtrar chamados por status ou prioridade
- [ ] Buscar chamados por palavra no título
- [ ] Excluir chamados
- [ ] Registrar a data de fechamento
- [ ] Interface gráfica com Tkinter
- [ ] Versão web com Flask

---

## 👩‍💻 Autora

Desenvolvido por **SEU NOME**.

- GitHub:https://github.com/ChrisColy

---

⭐ Se este projeto te ajudou, deixe uma estrela no repositório!
