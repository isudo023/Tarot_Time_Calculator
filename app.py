
import streamlit as st
from pathlib import Path

from timing_engine import (
    CARDS,
    calculate_card_timing,
    calculate_combined_timing,
    calculate_sequential_timing
)


# ==================================================
# 1. PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Tarot Time",
    page_icon="🔮",
    layout="wide"
)


# ==================================================
# 2. PASTEL THEME
# ==================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F8F4FA;
    }

    h1, h2, h3, h4 {
        color: #705581;
    }

    p, label {
        color: #65566D;
    }

    div.stButton > button {
        background-color: #DCCBE8;
        color: #554064;
        border-radius: 12px;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
    }

    div.stButton > button:hover {
        background-color: #C9B1DB;
        color: #554064;
    }

    div[data-testid="stMetric"] {
        background-color: #F5E8E8;
        padding: 15px;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #705581;
    }

    div[data-testid="stMetricValue"] {
        color: #65566D;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 3. APP TITLE
# ==================================================

st.title("🔮 Tarot Time")

st.subheader("A Tarot-Based Timing Calculator")

st.write(
    "Discover possible timing through your selected tarot cards. "
    "Choose your reading type, select your cards, and explore "
    "your estimated timeline."
)

st.divider()


# ==================================================
# 4. LOAD TAROT CARDS
# ==================================================

card_names = [card["name"] for card in CARDS]


# ==================================================
# 5. TAROT CARD IMAGE MAPPING
# ==================================================

CARD_IMAGE_FOLDER = Path("assets") / "cards"


MAJOR_CARD_IMAGES = {
    "The Fool": "00_Fool.jpg",
    "The Magician": "01_Magician.jpg",
    "The High Priestess": "02_High_Priestess.jpg",
    "The Empress": "03_Empress.jpg",
    "The Emperor": "04_Emperor.jpg",
    "The Hierophant": "05_Hierophant.jpg",
    "The Lovers": "06_Lovers.jpg",
    "The Chariot": "07_Chariot.jpg",
    "Strength": "08_Strength.jpg",
    "The Hermit": "09_Hermit.jpg",
    "Wheel of Fortune": "10_Wheel_of_Fortune.jpg",
    "Justice": "11_Justice.jpg",
    "The Hanged Man": "12_Hanged_Man.jpg",
    "Death": "13_Death.jpg",
    "Temperance": "14_Temperance.jpg",
    "The Devil": "15_Devil.jpg",
    "The Tower": "16_Tower.jpg",
    "The Star": "17_Star.jpg",
    "The Moon": "18_Moon.jpg",
    "The Sun": "19_Sun.jpg",
    "Judgement": "20_Judgement.jpg",
    "The World": "21_World.jpg"
}


CARD_RANKS = {
    "Ace": "01",
    "Two": "02",
    "Three": "03",
    "Four": "04",
    "Five": "05",
    "Six": "06",
    "Seven": "07",
    "Eight": "08",
    "Nine": "09",
    "Ten": "10",
    "Page": "11",
    "Knight": "12",
    "Queen": "13",
    "King": "14"
}


def get_card_image(card_name):

    if card_name in MAJOR_CARD_IMAGES:
        filename = MAJOR_CARD_IMAGES[card_name]

    else:
        parts = card_name.split(" of ")

        if len(parts) != 2:
            return None

        rank, suit = parts

        if rank not in CARD_RANKS:
            return None

        suit_names = {
            "Cups": "Cups",
            "Pentacles": "Pents",
            "Swords": "Swords",
            "Wands": "Wands"
        }

        if suit not in suit_names:
            return None

        filename = (
            suit_names[suit]
            + CARD_RANKS[rank]
            + ".jpg"
        )

    image_path = CARD_IMAGE_FOLDER / filename

    if image_path.exists():
        return str(image_path)

    return None


# ==================================================
# 6. CHECK CARD IMAGES
# ==================================================

missing_images = []

for card_name in card_names:

    if get_card_image(card_name) is None:
        missing_images.append(card_name)


if missing_images:

    st.error("Some card images could not be found:")

    for name in missing_images:
        st.write(name)

else:

    st.success(
        "Discover the Possible Timing of Your Question!"
    )


# ==================================================
# 7. READING TYPE
# ==================================================

reading_type = st.selectbox(
    "Choose Your Reading Type",
    [
        "Single Card Timing",
        "Three Card Combined Timing",
        "Three Card Sequential Timing"
    ]
)


# ==================================================
# 8. QUESTION AND STARTING DATE
# ==================================================

question = st.text_input(
    "Your Question",
    placeholder="Example: When will I get a new job?"
)

start_date = st.date_input(
    "Select Starting Date"
)

st.divider()


# ==================================================
# 9. SINGLE CARD TIMING
# ==================================================

if reading_type == "Single Card Timing":

    st.subheader("Select Your Tarot Card")

    selected_card = st.selectbox(
        "Choose a Card",
        card_names,
        key="single_card"
    )

    orientation = st.radio(
        "Card Orientation",
        ["upright", "reversed"],
        horizontal=True,
        key="single_orientation"
    )

    if st.button("Calculate Timing"):

        result = calculate_card_timing(
            start_date,
            selected_card,
            orientation
        )

        st.divider()

        st.subheader("Your Timing Result")

        st.info(
            f"Your Question: {question if question else 'Not provided'}"
        )

        col1, col2 = st.columns([1, 2])

        with col1:

            image_path = get_card_image(result["card"])

            if image_path:
                st.image(image_path, width=220)
            else:
                st.warning("Card image not found.")

        with col2:

            st.markdown(f"### 🃏 {result['card']}")

            st.write(
                f"**Orientation:** {result['orientation']}"
            )

            st.write(
                f"**Interpretation:** {result['interpretation']}"
            )

            st.write(
                f"**Speed:** {result['speed']}"
            )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Minimum Timing",
                f"{result['minimum_days']} days"
            )

        with col2:

            st.metric(
                "Maximum Timing",
                f"{result['maximum_days']} days"
            )

        st.success(
            "Estimated Date Range: "
            f"{result['earliest_date'].strftime('%d %B %Y')} "
            "to "
            f"{result['latest_date'].strftime('%d %B %Y')}"
        )


# ==================================================
# 10. THREE CARD COMBINED TIMING
# ==================================================

elif reading_type == "Three Card Combined Timing":

    st.subheader("Select Three Different Tarot Cards")

    selections = []
    selected_names = []

    for i in range(3):

        st.markdown(f"### Card {i + 1}")

        # Only show cards that have not already been selected.

        available_cards = [
            name for name in card_names
            if name not in selected_names
        ]

        selected_card = st.selectbox(
            f"Choose Card {i + 1}",
            available_cards,
            key=f"combined_card_{i}"
        )

        orientation = st.radio(
            f"Orientation for Card {i + 1}",
            ["upright", "reversed"],
            horizontal=True,
            key=f"combined_orientation_{i}"
        )

        selected_names.append(selected_card)

        selections.append({
            "name": selected_card,
            "orientation": orientation
        })

    if st.button("Calculate Combined Timing"):

        if len(set(selected_names)) != 3:

            st.error("Please select three different cards.")

        else:

            result = calculate_combined_timing(
                start_date,
                selections
            )

            st.divider()

            st.subheader("Your Combined Timing Result")

            st.info(
                f"Your Question: {question if question else 'Not provided'}"
            )

            st.markdown("### Your Selected Cards")

            # Display all three cards separately.

            for item in result["cards"]:

                with st.container(border=True):

                    col1, col2 = st.columns([1, 2])

                    with col1:

                        image_path = get_card_image(item["card"])

                        if image_path:
                            st.image(image_path, width=180)
                        else:
                            st.warning("Card image not found.")

                    with col2:

                        st.markdown(f"### 🃏 {item['card']}")

                        st.write(
                            f"**Orientation:** {item['orientation']}"
                        )

                        st.write(item["interpretation"])

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Average Minimum Timing",
                    f"{result['minimum_days']} days"
                )

            with col2:

                st.metric(
                    "Average Maximum Timing",
                    f"{result['maximum_days']} days"
                )

            st.success(
                "Estimated Date Range: "
                f"{result['earliest_date'].strftime('%d %B %Y')} "
                "to "
                f"{result['latest_date'].strftime('%d %B %Y')}"
            )


# ==================================================
# 11. THREE CARD SEQUENTIAL TIMING
# ==================================================

elif reading_type == "Three Card Sequential Timing":

    st.subheader("Select Three Different Tarot Cards")

    stage_names = [
        "Stage 1 – Initial Development",
        "Stage 2 – Waiting Period",
        "Stage 3 – Final Manifestation"
    ]

    selections = []
    selected_names = []

    for i in range(3):

        st.markdown(f"### {stage_names[i]}")

        # Remove cards selected in earlier stages.

        available_cards = [
            name for name in card_names
            if name not in selected_names
        ]

        selected_card = st.selectbox(
            f"Choose Card for Stage {i + 1}",
            available_cards,
            key=f"sequential_card_{i}"
        )

        orientation = st.radio(
            f"Orientation for Stage {i + 1}",
            ["upright", "reversed"],
            horizontal=True,
            key=f"sequential_orientation_{i}"
        )

        selected_names.append(selected_card)

        selections.append({
            "name": selected_card,
            "orientation": orientation
        })

    if st.button("Calculate Sequential Timing"):

        if len(set(selected_names)) != 3:

            st.error("Please select three different cards.")

        else:

            result = calculate_sequential_timing(
                start_date,
                selections
            )

            st.divider()

            st.subheader("Your Sequential Timing Result")

            st.info(
                f"Your Question: {question if question else 'Not provided'}"
            )

            # ------------------------------------------
            # VISUAL SEQUENTIAL TIMELINE
            # ------------------------------------------

            st.subheader("Your Visual Timeline")

            for i, stage in enumerate(result["stages"]):

                with st.container(border=True):

                    st.markdown(f"### {stage_names[i]}")

                    col1, col2 = st.columns([1, 2])

                    # CARD IMAGE

                    with col1:

                        image_path = get_card_image(stage["card"])

                        if image_path:
                            st.image(image_path, width=180)
                        else:
                            st.warning("Card image not found.")

                    # CARD DETAILS

                    with col2:

                        st.markdown(
                            f"**🃏 {stage['card']} — "
                            f"{stage['orientation']}**"
                        )

                        st.write(stage["interpretation"])

                    # STAGE DATES

                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(
                            "Earliest Possible Date",
                            stage["earliest_date"].strftime(
                                "%d %B %Y"
                            )
                        )

                    with col2:

                        st.metric(
                            "Latest Possible Date",
                            stage["latest_date"].strftime(
                                "%d %B %Y"
                            )
                        )

                    st.caption(
                        "Cumulative Timing: "
                        f"{stage['minimum_days_from_start']}–"
                        f"{stage['maximum_days_from_start']} days "
                        "from starting date"
                    )

            # ------------------------------------------
            # FINAL ESTIMATED TIMELINE
            # ------------------------------------------

            st.divider()

            st.subheader("Final Estimated Timeline")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Total Minimum Timing",
                    f"{result['minimum_days']} days"
                )

            with col2:

                st.metric(
                    "Total Maximum Timing",
                    f"{result['maximum_days']} days"
                )

            st.success(
                "Final Estimated Date Range: "
                f"{result['earliest_date'].strftime('%d %B %Y')} "
                "to "
                f"{result['latest_date'].strftime('%d %B %Y')}"
            )


# ==================================================
# 12. DISCLAIMER
# ==================================================

st.divider()

st.caption(
    "🔮 Disclaimer: Tarot timing is interpretive and intended "
    "for personal reflection and entertainment. Date ranges are "
    "estimates based on configurable card timing values. They are "
    "not guaranteed predictions or fixed outcomes."
)
