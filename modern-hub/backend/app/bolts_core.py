from __future__ import annotations

import re
import glob
from pathlib import Path
from typing import Dict, List, Tuple, Any

import pandas as pd


# Repo root to read Excel files living at the top-level directory
ROOT_DIR = Path(__file__).resolve().parents[3]


def _excel_files() -> List[Path]:
    return [Path(p) for p in glob.glob(str(ROOT_DIR / "*.xlsx"))]


def _team_name_from_filename(fname: str) -> str | None:
    m = re.search(r"(\d{4}|07_08|\d{2})", fname)
    if not m:
        return None
    year = m.group(1)
    if year == "09":
        year = "2009"
    elif year == "07_08":
        year = "2007-08"
    return f"{year} MLS Next"


def list_teams_and_players() -> Dict[str, List[str]]:
    teams: Dict[str, List[str]] = {}
    for f in _excel_files():
        team_name = _team_name_from_filename(f.name)
        if not team_name:
            continue
        try:
            profiles_df = pd.read_excel(f, sheet_name='Profiles')
            if 'ACTIVE ATHLETE' in profiles_df.columns:
                active_athletes = profiles_df[profiles_df['ACTIVE ATHLETE'] == True]
            else:
                active_athletes = profiles_df
            for _, row in active_athletes.iterrows():
                pname = str(row.get('NAME', '')).strip()
                if not pname:
                    continue
                teams.setdefault(team_name, []).append(pname)
        except Exception:
            # Fallback to first sheet heuristic
            try:
                df = pd.read_excel(f, sheet_name=0)
                header = df.columns[0]
                name_match = re.search(r'FOR (.+?) -', header)
                if name_match:
                    pname = name_match.group(1).strip()
                    if pname:
                        teams.setdefault(team_name, []).append(pname)
            except Exception:
                continue
    # de-dup and sort
    for k, v in list(teams.items()):
        teams[k] = sorted(list(dict.fromkeys(v)))
    return teams


def _load_testing_sheet(xlsx_path: Path) -> pd.DataFrame:
    testing_df = pd.read_excel(xlsx_path, sheet_name='TestingData')
    metric_names = testing_df.iloc[0].values
    testing_df.columns = metric_names
    testing_clean = testing_df.iloc[1:].reset_index(drop=True)
    testing_clean['Date'] = pd.to_datetime(testing_clean['Date'], errors='coerce')
    return testing_clean


def _load_phv_sheet(xlsx_path: Path) -> pd.DataFrame | None:
    try:
        return pd.read_excel(xlsx_path, sheet_name='PHV Calculator', header=7)
    except Exception:
        return None


def _find_player_rows_testing(testing_df: pd.DataFrame, player_name: str) -> pd.DataFrame:
    return testing_df[testing_df['Name'].str.contains(player_name, na=False, case=False)]


def _extract_phv_for_player(phv_df: pd.DataFrame, player_name: str) -> Dict[str, Any]:
    def sim(a: str, b: str) -> float:
        a = (a or '').lower().strip()
        b = (b or '').lower().strip()
        if not a or not b:
            return 0.0
        common = len(set(a.split()) & set(b.split()))
        return common / max(1, len(set(a.split()) | set(b.split())))

    if phv_df is None:
        return {}
    for _, row in phv_df.iterrows():
        first_name = str(row.get('First Name', '')).strip()
        last_name = str(row.get('Last Name', '')).strip()
        if not first_name or not last_name:
            continue
        full = f"{first_name} {last_name}"
        if sim(player_name, full) >= 0.5:
            h = row.get('Height (cm)', None)
            w = row.get('Weight (kg)', None)
            return {
                'Name': full,
                'Height': h if pd.notna(h) and h != 0 else None,
                'Weight': w if pd.notna(w) and w != 0 else None,
            }
    return {}


def _team_to_files() -> Dict[str, List[Path]]:
    out: Dict[str, List[Path]] = {}
    for f in _excel_files():
        t = _team_name_from_filename(f.name)
        if t:
            out.setdefault(t, []).append(f)
    return out


def player_detail(team: str, player: str) -> Dict[str, Any]:
    team_files = _team_to_files().get(team, [])
    latest_testing_row = None
    phv_payload = {}

    for x in team_files:
        testing_df = _load_testing_sheet(x)
        rows = _find_player_rows_testing(testing_df, player)
        if not rows.empty:
            most_recent = rows.loc[rows['Date'].idxmax()]
            latest_testing_row = most_recent.to_dict()
        phv_df = _load_phv_sheet(x)
        p = _extract_phv_for_player(phv_df, player)
        if p:
            phv_payload = p

    return {
        'team': team,
        'player': player,
        'testing_data': latest_testing_row,
        'phv': phv_payload,
    }

