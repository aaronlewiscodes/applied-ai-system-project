"""
Evaluation script for the AI interface layer.

Runs a set of sample inputs through parse_natural_language_to_profile() and
checks that each output profile matches expected characteristics. Does not
require exact values — only that the model's choices are directionally correct.

Usage:
    python eval.py
"""

from src.ai_interface import parse_natural_language_to_profile

CASES = [
    {
        "description": "high energy EDM for a workout",
        "expect": {"genre": "edm", "energy_min": 0.7, "likes_acoustic": False},
    },
    {
        "description": "quiet acoustic folk music for a rainy afternoon",
        "expect": {"energy_max": 0.5, "likes_acoustic": True},
    },
    {
        "description": "chill lofi beats to study to",
        "expect": {"genre": "lofi", "energy_max": 0.55},
    }
]


def check(profile: dict, expect: dict) -> list[str]:
    failures = []
    if "genre" in expect and profile["genre"] != expect["genre"]:
        failures.append(f"genre: got {profile['genre']!r}, expected {expect['genre']!r}")
    if "mood" in expect and profile["mood"] != expect["mood"]:
        failures.append(f"mood: got {profile['mood']!r}, expected {expect['mood']!r}")
    if "energy_min" in expect and profile["energy"] < expect["energy_min"]:
        failures.append(f"energy {profile['energy']:.2f} below minimum {expect['energy_min']}")
    if "energy_max" in expect and profile["energy"] > expect["energy_max"]:
        failures.append(f"energy {profile['energy']:.2f} above maximum {expect['energy_max']}")
    if "likes_acoustic" in expect and profile["likes_acoustic"] != expect["likes_acoustic"]:
        failures.append(
            f"likes_acoustic: got {profile['likes_acoustic']}, expected {expect['likes_acoustic']}"
        )
    return failures


def main():
    passed = 0
    failed = 0

    print("=" * 55)
    print("  AI Interface Evaluation")
    print("=" * 55)

    for case in CASES:
        desc = case["description"]
        print(f"\nInput:   {desc!r}")
        try:
            profile = parse_natural_language_to_profile(desc)
            print(f"Profile: genre={profile['genre']}, mood={profile['mood']}, "
                  f"energy={profile['energy']:.2f}, acoustic={profile['likes_acoustic']}")
            failures = check(profile, case["expect"])
            if failures:
                print(f"FAIL")
                for f in failures:
                    print(f"  - {f}")
                failed += 1
            else:
                print("PASS")
                passed += 1
        except Exception as exc:
            print(f"ERROR: {exc}")
            failed += 1

    print(f"\n{'=' * 55}")
    print(f"Results: {passed} passed, {failed} failed out of {len(CASES)} cases")
    print("=" * 55)


if __name__ == "__main__":
    main()
