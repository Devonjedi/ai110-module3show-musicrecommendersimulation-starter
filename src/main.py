"""
Command line runner for the Music Recommender Simulation.

Loads songs from data/songs.csv, scores them against several user profiles,
and prints a ranked, explained list of top recommendations for each profile.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop Fan": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "valence": 0.80,
        "likes_acoustic": False,
    },
    "Chill Lofi Listener": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.40,
        "valence": 0.58,
        "likes_acoustic": True,
    },
    "Intense Rock Head": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.92,
        "valence": 0.45,
        "likes_acoustic": False,
    },
    "Adversarial (conflicting prefs)": {
        "genre": "ambient",
        "mood": "sad",
        "energy": 0.90,   # high energy but sad/ambient — conflicting
        "valence": 0.20,
        "likes_acoustic": True,
    },
}


def print_recommendations(profile_name: str, recommendations) -> None:
    """Print a formatted recommendation list for a named profile."""
    separator = "─" * 55
    print(f"\n{'═' * 55}")
    print(f"  Profile: {profile_name}")
    print(f"{'═' * 55}")
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']} — {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Why   : {explanation}")
        print(f"  {separator}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in PROFILES.items():
        recs = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(profile_name, recs)

    print()


if __name__ == "__main__":
    main()
