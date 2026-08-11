# PetHope
Projeto Anual de POAS e PDSI

## Equipe do Projeto: 
- Amanda Alves de Souza
- Fernanda Erika Brito da Silva
- Maria Cristiani Gomes Oliveira
- Priscylla Beatriz Alves de Araújo

## Descrição do Tema:
O PetHope é um sistema focado em ajudar ONGs de proteção de animais e protetores independentes que necessitam de ferramentas eficientes e organizadas para o gerenciamento de suas atividades, oferencendo uma experiência moderna, rápida e intuitiva para os usuários.

## Tecnologias:
- **Backend:** FastAPI (Python)
- **Frontend:** VueJS

## Como rodar o projeto:

**Backend (FastAPI)**
```bash
cd backend
pip install -r requirements.txt
cd ..
uvicorn backend.main:app --reload --port 8000
```
API disponível em `http://localhost:8000` (documentação automática em `/docs`).

**Frontend (Vue.js)**
```bash
cd frontend
npm install
npm run dev
```
Aplicação disponível em `http://localhost:5173`.

## Endpoints:
```markdown
| Método | Endpoint                     | Descrição                           |
|--------|------------------------------|-------------------------------------|
| POST   | /api/users                   | Cadastrar usuário                   |
| POST   | /api/auth/login              | Login de usuário                    |
| POST   | /api/auth/logout             | Logout                              |
| GET    | /api/auth/me                 | Sessão atual (usuário ou ONG)       |
| POST   | /api/ongs                    | Cadastrar ONG                       |
| POST   | /api/ongs/login              | Login de ONG                        |
| POST   | /api/animals                 | Cadastrar animal (ONG autenticada)  |
| GET    | /api/animals                 | Listar animais (filtros opcionais)  |
| GET    | /api/animals/{id}            | Detalhes do animal                  |
| PUT    | /api/animals/{id}            | Editar animal (dono)                |
| DELETE | /api/animals/{id}            | Excluir animal (dono)               |
| POST   | /api/animals/{id}/adopt      | Solicitar adoção                    |
| GET    | /api/adoptions/mine          | Minhas solicitações (usuário)       |
| GET    | /api/adoptions/requests      | Solicitações recebidas (ONG)        |
| POST   | /api/adoptions/{id}/approve  | Aprovar solicitação                 |
| POST   | /api/adoptions/{id}/reject   | Recusar solicitação                 |
```

## Documento V1:
https://docs.google.com/document/d/1RB4fP2UmctnbEGBAA-88CDeRxlwhdnB0u1H9pY4OUws/edit?usp=sharing

## Cronograma do Projeto dividido por Requisitos Funcionais:

### Cadastrar Usuário 
- Backend (21/04/26 - 26/05/26)
- Frontend (05/06/26 - 09/06/26)
  
### Cadastrar ONG
- Backend (24/05/26 - 28/05/26)
- Frontend (05/06/26 - 09/06/26)

### Cadastrar Animais 
- Backend (14/06/26 - 27/06/26)
- Frontend (21/06/26 - 27/06/26)

### Gerenciar Adoções
- Backend (28/06/26 - 11/07/26)
- Frontend (05/07/26 - 11/07/26)

### Gerenciar Doações
- Backend (12/07/26 - 25/07/26)
- Frontend (19/07/26 - 25/07/26)

### Implementar busca e filtros
- Backend (26/07/26 - 08/08/26)
- Frontend (02/08/26 - 08/08/26)

### Validação de Formulários
- Backend (09/08/26 - 22/08/26)
- Frontend (16/08/26 - 22/08/26)

### Integração entre telas
- Backend (23/08/26 - 05/09/26)
- Frontend (30/08/26 - 05/09/26)

### Integração completa com backend
- Backend (06/09/26 - 19/09/26)
- Frontend (13/09/26 - 19/09/26)

### Testes funcionais e correção de bugs
- Backend (20/09/26 - 03/10/26)
- Frontend (27/09/26 - 03/10/26)

