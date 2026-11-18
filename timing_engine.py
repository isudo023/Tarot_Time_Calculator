
import json
from pathlib import Path
from datetime import timedelta


# --------------------------------
# 1. LOAD THE TAROT DATABASE
# --------------------------------

ROOT = Path(__file__).parent
DATABASE_PATH = ROOT / "data" / "cards.json"


def load_cards():
    with open(DATABASE_PATH, "r", encoding="utf-8") as file:
        database = json.load(file)

    return database["cards"]


# Load all cards once
CARDS = load_cards()


# --------------------------------
# 2. FIND A CARD BY ITS NAME
# --------------------------------

def get_card(card_name):
    for card in CARDS:
        if card["name"].lower() == card_name.lower():
            return card

    raise ValueError(f"Card not found: {card_name}")


# --------------------------------
# 3. APPLY REVERSED CARD ADJUSTMENT
# --------------------------------

def get_timing_range(card, orientation):
    minimum = card["min_days"]
    maximum = card["max_days"]

    if orientation.lower() == "reversed":

        effect = card.get("reversed_effect", "")

        if effect == "Possible delay":
            minimum += 7
            maximum += 14

        elif effect == "Strong possible delay":
            minimum += 14
            maximum += 30

        elif effect in ("Uncertainty", "Uncertain"):
            minimum = max(1, minimum - 7)
            maximum += 30

    elif orientation.lower() != "upright":
        raise ValueError("Orientation must be upright or reversed.")

    return minimum, maximum


# --------------------------------
# 4. CALCULATE ONE CARD'S TIMING
# --------------------------------

def calculate_card_timing(start_date, card_name, orientation="upright"):

    card = get_card(card_name)

    minimum, maximum = get_timing_range(card, orientation)

    earliest_date = start_date + timedelta(days=minimum)
    latest_date = start_date + timedelta(days=maximum)

    if orientation.lower() == "upright":
        interpretation = card["upright"]
    else:
        interpretation = card["reversed"]

    return {
        "card": card["name"],
        "orientation": orientation.title(),
        "minimum_days": minimum,
        "maximum_days": maximum,
        "earliest_date": earliest_date,
        "latest_date": latest_date,
        "speed": card["speed"],
        "interpretation": interpretation
    }


# --------------------------------
# 5. THREE-CARD COMBINED TIMING
# --------------------------------

def calculate_combined_timing(start_date, selections):

    results = []

    for selection in selections:
        result = calculate_card_timing(
            start_date,
            selection["name"],
            selection["orientation"]
        )

        results.append(result)

    average_minimum = round(
        sum(item["minimum_days"] for item in results) / len(results)
    )

    average_maximum = round(
        sum(item["maximum_days"] for item in results) / len(results)
    )

    return {
        "cards": results,
        "minimum_days": average_minimum,
        "maximum_days": average_maximum,
        "earliest_date": start_date + timedelta(days=average_minimum),
        "latest_date": start_date + timedelta(days=average_maximum)
    }


# --------------------------------
# 6. THREE-CARD SEQUENTIAL TIMING
# --------------------------------

def calculate_sequential_timing(start_date, selections):

    results = []
    current_minimum = 0
    current_maximum = 0

    for selection in selections:

        card = get_card(selection["name"])

        minimum, maximum = get_timing_range(
            card,
            selection["orientation"]
        )

        current_minimum += minimum
        current_maximum += maximum

        results.append({
            "card": card["name"],
            "orientation": selection["orientation"].title(),
            "interpretation": (
                card["upright"]
                if selection["orientation"].lower() == "upright"
                else card["reversed"]
            ),
            "minimum_days_from_start": current_minimum,
            "maximum_days_from_start": current_maximum,
            "earliest_date": start_date + timedelta(days=current_minimum),
            "latest_date": start_date + timedelta(days=current_maximum)
        })

    return {
        "stages": results,
        "minimum_days": current_minimum,
        "maximum_days": current_maximum,
        "earliest_date": start_date + timedelta(days=current_minimum),
        "latest_date": start_date + timedelta(days=current_maximum)
    }
