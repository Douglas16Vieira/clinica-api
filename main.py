import sqlite3
from fastapi import FastAPI

app = FastAPI()

conn = sqlite3.connect("agendamentos.db")
conn.execute("CREATE TABLE IF NOT EXISTS agendamentos (data TEXT, hora TEXT, nome TEXT, telefone TEXT)")
conn.close()
@app.post("/schedule")
def agendar(dados: dict):
    conn = sqlite3.connect("agendamentos.db") 
    conn.execute("INSERT INTO agendamentos (data, hora, nome, telefone) VALUES (?, ?, ?, ?)",
                 (dados['data'], dados['hora'], dados['nome'], dados['telefone']))
  
    conn.commit()
    conn.close()
    
    return {"mensagem": "Agendado com sucesso!"}

@app.get("/available-times")
def ver_vagas(data: str): # o front vai chamar tipo /available-times?data=16/09
    todos_horarios = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

    conn = sqlite3.connect("agendamentos.db")
    agendados = conn.execute("SELECT hora FROM agendamentos WHERE data =?", (data,)).fetchall()
    conn.close()

    horas_ocupadas = [h[0] for h in agendados]

    livres = [h for h in todos_horarios if h not in horas_ocupadas]

    return livres

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

uvicorn main:app --reload