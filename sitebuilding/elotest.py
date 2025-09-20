import random
import json

K = 32  # K-factor for rating adjustment
DATABASE_FILE = 'elo_ratings.json'


def get_expected_score(rating_a, rating_b):
    """Calculates the expected score for player A."""
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def update_ratings(database, winner_id, loser_id):
    """Updates the ratings of the winner and loser."""
    rating_a = database[winner_id]
    rating_b = database[loser_id]

    expected_a = get_expected_score(rating_a, rating_b)
    expected_b = get_expected_score(rating_b, rating_a)

    # Winner's rating change
    database[winner_id] = round(rating_a + K * (1 - expected_a))
    # Loser's rating change
    database[loser_id] = round(rating_b + K * (0 - expected_b))


def load_database():
    """Loads the player database from the JSON file."""
    try:
        with open(DATABASE_FILE, 'r') as f:
            # Keys from JSON are strings, so they match your player IDs
            return json.load(f)
    except FileNotFoundError:
        print(f"File '{DATABASE_FILE}' not found. Please create it with initial player data.")
        return None


def save_database(database):
    """Saves the updated player database to the JSON file."""
    with open(DATABASE_FILE, 'w') as f:
        # Use indent for a human-readable format
        json.dump(database, f, indent=4)


# Main script logic
database = load_database()

if database:
    players = list(database.keys())

    # Example simulation loop
    for _ in range(129):
        # Select two unique players
        p1, p2 = random.sample(players, 2)

        print(f"\nMatch between Player {p1} (Rating: {database[p1]}) and Player {p2} (Rating: {database[p2]})")
        winner_id = input(f"Who won? Enter {p1} or {p2}: ")

        if winner_id == p1:
            update_ratings(database, p1, p2)
        elif winner_id == p2:
            update_ratings(database, p2, p1)
        else:
            print("Invalid input, no rating change.")

    # Save the updated ratings
    save_database(database)

    # Print current ratings
    print("\n--- Final Ratings ---")
    sorted_ratings = sorted(database.items(), key=lambda item: item[1], reverse=True)
    for player, rating in sorted_ratings:
        print(f"Player {player}: {rating}")