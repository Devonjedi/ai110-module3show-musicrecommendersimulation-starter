import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _score_song_oop(user: UserProfile, song: Song) -> Tuple[float, List[str]]:
    """Compute a relevance score for a Song against a UserProfile, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if song.genre == user.favorite_genre:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.mood == user.favorite_mood:
        score += 1.5
        reasons.append("mood match (+1.5)")

    energy_proximity = 1.0 - abs(song.energy - user.target_energy)
    score += 1.0 * energy_proximity
    reasons.append(f"energy proximity (+{energy_proximity:.2f})")

    if user.likes_acoustic and song.acousticness > 0.6:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")

    return score, reasons


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by relevance score for the given user."""
        scored = [(song, _score_song_oop(user, song)[0]) for song in self.songs]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        _, reasons = _score_song_oop(user, song)
        if not reasons:
            return "No strong match found, but included for variety."
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Score a single song dict against user preference dict.

    Returns (score, explanation_string).
    Scoring weights: genre match +2.0, mood match +1.5,
    energy proximity +1.0*(1-|diff|), valence proximity +0.5*(1-|diff|),
    acoustic bonus +0.5.
    """
    score = 0.0
    reasons = []

    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song.get("mood") == user_prefs.get("mood"):
        score += 1.5
        reasons.append("mood match (+1.5)")

    if "energy" in user_prefs:
        energy_proximity = 1.0 - abs(song["energy"] - user_prefs["energy"])
        score += 1.0 * energy_proximity
        reasons.append(f"energy proximity (+{energy_proximity:.2f})")

    if "valence" in user_prefs:
        valence_proximity = 1.0 - abs(song["valence"] - user_prefs["valence"])
        score += 0.5 * valence_proximity
        reasons.append(f"valence proximity (+{0.5 * valence_proximity:.2f})")

    if user_prefs.get("likes_acoustic") and song.get("acousticness", 0) > 0.6:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")

    explanation = "; ".join(reasons) if reasons else "no strong match"
    return score, explanation


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top-k as (song, score, explanation) tuples, sorted highest first."""
    scored = [(*[song], *score_song(user_prefs, song)) for song in songs]
    # scored items: (song, score, explanation)
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
