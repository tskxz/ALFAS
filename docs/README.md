# ALFAS

Plataforma web de literacia em saúde desenvolvida para estudantes do ensino básico e secundário, professores e profissionais de saúde.

## Funcionalidades

- **Formações:** Webinars e workshops temáticos com vídeos e materiais de apoio.
- **Avaliação de Aprendizagem:** Questionários de diagnóstico inicial e final para medir a evolução do utilizador.
- **Gamificação:** Atribuição de badges e certificados para pontuações a partir de 85% na avaliação final.
- **Biblioteca:** Artigos, notícias de saúde, agenda de eventos e destaques geridos pelo backoffice.
- **Consentimento Parental:** Validação de idade e recolha de autorização parental para menores.

## Atores do Sistema

- **Convidado:** Consulta conteúdos públicos e realiza o registo.
- **Utilizador Registado:** Inscreve-se em formações, responde a questionários e acompanha o seu progresso.
- **Gestor de Conteúdos:** Gere formações, questionários, notícias e consulta métricas.
- **Administrador:** Gere utilizadores, permissões e configurações da plataforma.

## Tecnologias

- **Frontend:** React
- **Backend:** Python com Flask
- **Base de Dados:** MySQL / SQL Server

---

## Como Executar o Projeto

Para correr o projeto em ambiente local de desenvolvimento, é necessário iniciar o **Backend** e o **Frontend** em dois terminais separados.

### Pré-requisitos

- [Python 3.10+](https://www.python.org/)
- [Node.js 18+](https://nodejs.org/) e `npm`

---

### 1. Backend

No primeiro terminal, a partir da raiz do repositório:

```bash
# 1. Entrar na pasta do backend
cd src/backend

# 2. Criar o ambiente virtual (apenas na primeira configuração)
python -m venv venv

# 3. Ativar o ambiente virtual:
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate

# 4. Instalar as dependências
pip install -r requirements.txt

# 5. Iniciar o servidor backend
python app.py
```

O servidor da API ficará em execução em:
- **Servidor:** `http://localhost:5000`
- **Endpoint de teste:** `http://localhost:5000/api/hello`

---

### 2. Frontend

No segundo terminal, a partir da raiz do repositório:

```bash
# 1. Entrar na pasta do frontend
cd src/frontend

# 2. Instalar as dependências (apenas na primeira configuração)
npm install

# 3. Iniciar o servidor de desenvolvimento
npm start
```

A aplicação abrirá automaticamente no navegador em:
- **Aplicação:** `http://localhost:3000`