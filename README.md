# Clínica - Agendamento com Feriados Nacionais

Sistema de agendamento que bloqueia automaticamente finais de semana, feriados nacionais (API Nager) e horários já ocupados.

## 🚀 Tecnologias
- Backend: Python, FastAPI, SQLite3, Requests
- Frontend: HTML5, CSS3, JavaScript (fetch)
- API Externa: Nager.Date (feriados Brasil)

## 📚 Conceitos Aplicados
- Backend puro com regras de negócio
- Consumo de API externa com cache em memória
- Validação com HTTPException (400 para feriado/fim de semana)
- Persistência com SQLite e prevenção de duplo agendamento
- Integração Front -> Back via fetch

## ▶️ Como Rodar
1. pip install fastapi uvicorn requests
2. uvicorn main:app --reload
3. Abra o index.html no navegador

## 🔧 Como funciona
- GET /available?date=YYYY-MM-DD -> retorna vagas livres. Se for feriado ou fim de semana retorna 400
- POST /agendar {data, hora, nome} -> salva no banco, retorna 400 se já ocupado

## 💡 Melhoria futura (UX)
Hoje o backend filtra e só retorna horários livres. A evolução seria retornar:
[{hora: "08:00", disponivel: true}, {hora: "09:00", disponivel: false, motivo: "ocupado"}]
E no front renderizar os indisponíveis em cinza com disabled, melhor para o usuário visualizar.

## 🧠 Maior dificuldade
Backend em Python, por ser meu primeiro backend puro. Usei IA como pair programming mas validei toda a lógica de cache e bloqueio.
