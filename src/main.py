"""
Command line runner for the Music Recommender.

Usage:
    python -m src.main

Describe what you're in the mood for in plain English. Llama (via Groq's free
API) parses your description into a taste profile, then the recommender scores
and ranks the song catalog against it.

Requires GROQ_API_KEY to be set in the environment or a .env file.
"""

import os
from src.recommender import load_songs, recommend_songs
from src.ai_interface import parse_natural_language_to_profile


def print_recommendations(profile: dict, recommendations: list) -> None:
    print(f"\nExtracted profile:")
    print(f"  Genre:         {profile['genre']}")
    print(f"  Mood:          {profile['mood']}")
    print(f"  Energy:        {profile['energy']:.2f}")
    print(f"  Likes acoustic:{' yes' if profile['likes_acoustic'] else ' no'}")
    print("\nTop recommendations:\n")
    for song, score, explanation in recommendations:
        print(f"  {song['title']} by {song['artist']}  —  Score: {score:.2f}")
        print(f"  {explanation}")
        print()


def main() -> None:
    if not os.environ.get("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY environment variable is not set.")
        print("Get a free key at console.groq.com")
        return

    songs = load_songs("data/songs.csv")

    print("=" * 55)
    print("  Music Recommender — Natural Language Mode")
    print("  Powered by Llama via Groq (free)")
    print("=" * 55)
    print("Describe what you're in the mood for.")
    print("Examples:")
    print('  "something chill to study to with acoustic guitar"')
    print('  "high energy EDM for a workout"')
    print('  "sad rainy day indie music"')
    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        print("Parsing your preferences with Llama via Groq...")
        try:
            profile = parse_natural_language_to_profile(user_input)
        except Exception as exc:
            print(f"Error: {exc}\n")
            continue

        recommendations = recommend_songs(profile, songs, k=5)
        print_recommendations(profile, recommendations)


if __name__ == "__main__":
    main()
