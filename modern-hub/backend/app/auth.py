from __future__ import annotations

from typing import Dict, List


# Map coaches to their allowed teams (as detected by Excel filenames)
# Passwords are plain for dev; replace with proper auth in production
COACHES: Dict[str, Dict[str, List[str]]] = {
    # username: { password: str, teams: [team_names] }
    "kyle": {"password": "bolts", "teams": ["2013 MLS Next"]},
    "denis": {"password": "bolts", "teams": ["2012 MLS Next"]},
    "bryce": {"password": "bolts", "teams": ["2011 MLS Next"]},
    "sean": {"password": "bolts", "teams": ["2010 MLS Next"]},
    "jonny": {"password": "bolts", "teams": ["2009 MLS Next", "2007-08 MLS Next"]},
}


def verify_login(username: str, password: str):
    u = (username or "").strip().lower()
    if u in COACHES and COACHES[u]["password"] == (password or "").strip():
        return {"username": u, "teams": COACHES[u]["teams"]}
    return None

