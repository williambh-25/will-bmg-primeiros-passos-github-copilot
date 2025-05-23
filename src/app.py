"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
   "Clube de Xadrez": {
      "description": "Aprenda estratégias e participe de torneios de xadrez",
      "schedule": "Sextas, 15h30 - 17h",
      "max_participants": 12,
      "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
   },
   "Aula de Programação": {
      "description": "Aprenda fundamentos de programação e desenvolva projetos de software",
      "schedule": "Terças e quintas, 15h30 - 16h30",
      "max_participants": 20,
      "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
   },
   "Educação Física": {
      "description": "Educação física e atividades esportivas",
      "schedule": "Segundas, quartas e sextas, 14h - 15h",
      "max_participants": 30,
      "participants": ["john@mergington.edu", "olivia@mergington.edu"]
   },
   # Esportivas
   "Futebol": {
      "description": "Participe do time de futebol da escola e jogue campeonatos",
      "schedule": "Terças e quintas, 16h - 17h30",
      "max_participants": 22,
      "participants": ["lucas@mergington.edu", "marcos@mergington.edu"]
   },
   "Vôlei": {
      "description": "Aulas e treinos de vôlei para todos os níveis",
      "schedule": "Quartas e sextas, 15h - 16h30",
      "max_participants": 18,
      "participants": ["ana@mergington.edu", "carla@mergington.edu"]
   },
   # Artísticas
   "Teatro": {
      "description": "Oficina de teatro e apresentações culturais",
      "schedule": "Segundas e quartas, 16h - 17h30",
      "max_participants": 15,
      "participants": ["paulo@mergington.edu", "juliana@mergington.edu"]
   },
   "Clube de Música": {
      "description": "Aprenda instrumentos e participe da banda escolar",
      "schedule": "Sextas, 14h - 15h30",
      "max_participants": 12,
      "participants": ["rafael@mergington.edu", "lara@mergington.edu"]
   },
   # Intelectuais
   "Clube de Leitura": {
      "description": "Leitura e discussão de livros clássicos e contemporâneos",
      "schedule": "Terças, 17h - 18h",
      "max_participants": 16,
      "participants": ["camila@mergington.edu", "renato@mergington.edu"]
   },
   "Olimpíada de Matemática": {
      "description": "Preparação para olimpíadas de matemática e desafios lógicos",
      "schedule": "Quintas, 16h - 17h",
      "max_participants": 20,
      "participants": ["bruno@mergington.edu", "aline@mergington.edu"]
   }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if student is already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Estudante já inscrito nesta atividade")

    # Add student
    activity["participants"].append(email)
    return {"message": f"{email} inscrito(a) em {activity_name} com sucesso"}


@app.delete("/activities/{activity_name}/remove")
def remove_participant(activity_name: str, email: str):
    """Remove um participante de uma atividade"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    activity = activities[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participante não encontrado nesta atividade")
    activity["participants"].remove(email)
    return {"message": f"{email} removido(a) de {activity_name} com sucesso"}