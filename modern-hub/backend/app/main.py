from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .bolts_core import list_teams_and_players, player_detail

app = FastAPI(title="Boston Bolts Performance API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/teams")
def get_teams():
    mapping = list_teams_and_players()
    return sorted(mapping.keys())


@app.get("/teams/{team}/players")
def get_team_players(team: str):
    mapping = list_teams_and_players()
    if team not in mapping:
        raise HTTPException(404, detail="team not found")
    return mapping[team]


@app.get("/teams/{team}/players/{player}")
def get_player(team: str, player: str):
    mapping = list_teams_and_players()
    if team not in mapping:
        raise HTTPException(404, detail="team not found")
    if player not in mapping[team]:
        raise HTTPException(404, detail="player not found")
    return player_detail(team, player)
