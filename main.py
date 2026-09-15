import sqlite3
import requests
from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()

def init_db():
    conn = sqlite3.connect("agendamentos.db")
    conn.execute("CREATE TABLE IF NOT EXISTS agendamentos (data TEXT, hora TEXT, nome TEXT, telefone TEXT)")
    conn.close()
init_db()

feriados_cache = None

def get_feriados():
    global feriados_cache
    if feriados_cache is not None:
        return feriados_cache

    try:
        url = "https://date.nager.at/api/v3/PublicHolidays/2026/BR"
        resp = requests.get(url, timeout=5).json()
        feriados_cache = [item['date'] for item in resp] 
        return feriados_cache
    except:
        return [] 

@app.get("/available")
def ver_vagas(date: str):

    try:
        dt = datetime.strptime(date, "%Y-%m-%d")
    except:
        raise HTTPException(status_code=400, detail="Use formato YYYY-MM-DD ex: 2026-02-10")

    if dt.weekday() >= 5: # 5=sab, 6=dom
        raise HTTPException(status_code=400, detail="Clínica fechada no fim de semana")

    # REGRA: Feriado via API
    feriados = get_feriados()
    if date in feriados:
        raise HTTPException(status_code=400, detail=f"Feriado {date}, clínica fechada")

    todos_horarios = ["08:00", "09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

    conn = sqlite3.connect("agendamentos.db")
    agendados = conn.execute("SELECT hora FROM agendamentos WHERE data =?", (date,)).fetchall()
    conn.close()

    horas_ocupadas = [h[0] for h in agendados]
    livres = [h for h in todos_horarios if h not in horas_ocupadas]

    return {"data": date, "horarios_disponiveis": livres, "feriado": False}


@app.post("/appointments")
def agendar(dados: dict):

    ver_vagas(dados['data'])

    conn = sqlite3.connect("agendamentos.db")

    existe = conn.execute("SELECT 1 FROM agendamentos WHERE data=? AND hora=?", (dados['data'], dados['hora'])).fetchone()
    if existe:
        conn.close()
        raise HTTPException(status_code=400, detail="Horário já ocupado")

    conn.execute("INSERT INTO agendamentos (data, hora, nome, telefone) VALUES (?,?,?,?)",
                 (dados['data'], dados['hora'], dados['nome'], dados['telefone']))
    conn.commit()
    conn.close()

    return {"mensagem": "Agendado com sucesso!", "data": dados['data'], "hora": dados['hora']}

@app.get("/appointments")
def listar_todos():
    conn = sqlite3.connect("agendamentos.db")
    todos = conn.execute("SELECT data, hora, nome, telefone FROM agendamentos").fetchall()
    conn.close()
    return [{"data": r[0], "hora": r[1], "nome": r[2], "telefone": r[3]} for r in todos]

@app.get("/available-times")
def compatibilidade(data: str):
    # aceita 16/09 e converte
    if "/" in data:
        data = datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d") if len(data)>5 else f"2026-{data.split('/')[1]}-{data.split('/')[0]}"
    return ver_vagas(data)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])