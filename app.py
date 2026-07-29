import os
import sqlite3
import base64
import uuid
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import streamlit as st


# --------------------------------------------------
# APP SETUP
# --------------------------------------------------

st.set_page_config(
    page_title="Walk In Closet",
    page_icon="W",
    layout="wide"
)

# --------------------------------------------------
# WALK IN CLOSET DESIGN SYSTEM
# --------------------------------------------------

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,500;6..96,600&display=swap');

    /* ----------------------------------------------
       COLOR AND FONT VARIABLES
    ---------------------------------------------- */

    :root {
        --closet-panel: rgba(255, 252, 249, 0.96);
        --closet-card: #fffdfb;
        --closet-text: #3f3038;
        --closet-muted: #806d76;
        --closet-accent: #9b6479;
        --closet-border: rgba(119, 78, 96, 0.18);
        --closet-shadow: 0 12px 32px rgba(48, 33, 40, 0.16);
        --closet-card-shadow: 0 7px 18px rgba(48, 33, 40, 0.12);
    }


    /* ----------------------------------------------
       GENERAL PAGE
    ---------------------------------------------- */

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: var(--closet-text);
    }

    p {
        color: var(--closet-text);
    }


    /* ----------------------------------------------
       SIDEBAR BRAND HEADER
    ---------------------------------------------- */

    .closet-brand-header {
        text-align: center;
        padding: 0.55rem 0.35rem 1rem;
    }

    .closet-brand-title {
        font-family: "Bodoni Moda", "Didot", "Bodoni 72", Georgia, serif;
        font-size: 2.15rem;
        font-weight: 600;
        line-height: 1.05;
        letter-spacing: -0.025em;
        color: var(--closet-text);
        margin: 0;
    }

    .closet-brand-tagline {
        margin-top: 0.55rem;
        color: var(--closet-muted);
        font-size: 0.67rem;
        font-weight: 600;
        letter-spacing: 0.19em;
        text-transform: uppercase;
    }

    .closet-brand-rule {
        width: 72%;
        height: 1px;
        margin: 1rem auto 0;
        background: var(--closet-border);
    }

    /* ----------------------------------------------
       LARGE SECTION PANELS
    ---------------------------------------------- */

    [class*="st-key-panel-"] {
        background: var(--closet-panel);
        border: 1px solid var(--closet-border);
        border-radius: 24px;
        padding: 1.8rem 2rem;
        box-shadow: var(--closet-shadow);
        margin-bottom: 1.4rem;
    }


    /* ----------------------------------------------
       CLOTHING CARDS
    ---------------------------------------------- */

    [class*="st-key-closet-card-"] {
        background: var(--closet-card);
        border: 1px solid var(--closet-border);
        border-radius: 18px;
        padding: 0.75rem;
        box-shadow: var(--closet-card-shadow);
        height: 100%;
        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease;
    }

    [class*="st-key-closet-card-"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 26px rgba(48, 33, 40, 0.17);
    }

    [class*="st-key-closet-card-"] img {
        border-radius: 13px;
        width: 100%;
    }

    [class*="st-key-closet-card-"] h3 {
        font-size: 1.15rem;
        line-height: 1.25;
        margin-top: 0.35rem;
        margin-bottom: 0.15rem;
    }

    [class*="st-key-closet-card-"] [data-testid="stCaptionContainer"] {
        color: var(--closet-muted);
    }
    [class*="st-key-inspiration-card-"] {
    padding: 0;
    overflow: hidden;
    border-radius: 18px;
    }

    [class*="st-key-inspiration-card-"] img {
        width: 100%;
        display: block;
        border-radius: 18px;
    }


    /* ----------------------------------------------
       METRIC TILES
    ---------------------------------------------- */

    [class*="st-key-metric-tile-"] {
        background: rgba(255, 247, 248, 0.92);
        border: 1px solid rgba(155, 100, 121, 0.14);
        border-radius: 16px;
        padding: 0.8rem 0.6rem;
        text-align: center;
        min-height: 105px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    [class*="st-key-metric-tile-"] [data-testid="stMetric"] {
        text-align: center;
        width: 100%;
    }

    [class*="st-key-metric-tile-"]
    [data-testid="stMetricLabel"] {
        justify-content: center;
    }

    [class*="st-key-metric-tile-"]
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        color: var(--closet-text);
    }


    /* ----------------------------------------------
       SECTION TITLES
    ---------------------------------------------- */

    .closet-section-title {
        font-size: 1.65rem;
        font-weight: 700;
        color: var(--closet-text);
        margin: 0;
        padding: 0;
    }

    .closet-section-subtitle {
        color: var(--closet-muted);
        margin-top: 0.2rem;
        margin-bottom: 0;
    }

    .closet-welcome-question {
        font-size: 1.45rem;
        font-style: italic;
        font-weight: 600;
        color: var(--closet-accent);
        margin-top: -0.4rem;
        margin-bottom: 1rem;
    }


    /* ----------------------------------------------
       BUTTONS
    ---------------------------------------------- */

    div.stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(155, 100, 121, 0.32);
        background: rgba(255, 250, 249, 0.95);
        color: var(--closet-accent);
        transition: all 0.18s ease;
    }

    div.stButton > button:hover {
        border-color: var(--closet-accent);
        color: #75485a;
        transform: translateY(-1px);
    }


    /* ----------------------------------------------
       SIDEBAR
    ---------------------------------------------- */

    section[data-testid="stSidebar"] {
        background: rgba(255, 250, 248, 0.97);
        border-right: 1px solid rgba(119, 78, 96, 0.12);
    }

    section[data-testid="stSidebar"] h1 {
        color: var(--closet-text);
    }
    /* ----------------------------------------------
       FORMS AND INPUTS
    ---------------------------------------------- */

    div[data-testid="stForm"] {
        background: rgba(255, 253, 251, 0.78);
        border: 1px solid rgba(119, 78, 96, 0.12);
        border-radius: 18px;
        padding: 1.4rem;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] > div {
        background-color: rgba(255, 255, 255, 0.97);
        border-radius: 12px;
    }

    div[data-testid="stFileUploader"] section {
        background: rgba(255, 255, 255, 0.94);
        border-radius: 14px;
    }
    [class*="st-key-calendar-day-"] {
    background: rgba(255, 253, 251, 0.96);
    border: 1px solid var(--closet-border);
    border-radius: 18px;
    padding: 0.75rem;
    min-height: 390px;
    box-shadow: var(--closet-card-shadow);
    }

    [class*="st-key-calendar-day-"] img {
        border-radius: 12px;
        aspect-ratio: 4 / 5;
        object-fit: cover;
        width: 100%;
    }

    [class*="st-key-calendar-day-"] p {
        margin-bottom: 0.25rem;
    }

    [class*="st-key-calendar-day-"] div.stButton > button {
        font-size: 0.78rem;
        padding-left: 0.25rem;
        padding-right: 0.25rem;
    }

    [class*="st-key-mini-outfit-"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.2rem;
}

[class*="st-key-mini-outfit-"] img {
    width: 100%;
    max-height: 105px;
    object-fit: contain;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.72);
}


    </style>
    """,
    unsafe_allow_html=True,
)

IMAGE_FOLDER = Path("images")
INSPIRATION_FOLDER = Path("inspiration_images")
BACKGROUND_FOLDER = Path("background_images")
DATABASE_FILE = "closet.db"
WISHLIST_FOLDER = Path("wishlist_images")

DATABASE_FILE = "closet.db"

IMAGE_FOLDER.mkdir(exist_ok=True)
INSPIRATION_FOLDER.mkdir(exist_ok=True)
BACKGROUND_FOLDER.mkdir(exist_ok=True)
WISHLIST_FOLDER.mkdir(exist_ok=True)


# --------------------------------------------------
# DATABASE FUNCTIONS
# --------------------------------------------------

def connect_to_database():
    return sqlite3.connect(DATABASE_FILE)


def create_clothing_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clothing (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            color TEXT,
            season TEXT,
            favorite INTEGER,
            photo_path TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def add_clothing_item(
    item_name,
    category,
    color,
    season,
    favorite,
    photo_path
):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO clothing (
            item_name,
            category,
            color,
            season,
            favorite,
            photo_path
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            item_name,
            category,
            color,
            season,
            int(favorite),
            photo_path
        )
    )

    connection.commit()
    connection.close()


def get_clothing_items():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            item_name,
            category,
            color,
            season,
            favorite,
            photo_path
        FROM clothing
        ORDER BY id DESC
        """
    )

    clothing_items = cursor.fetchall()

    connection.close()

    return clothing_items


def save_uploaded_photo(photo):
    if photo is None:
        return None

    safe_filename = photo.name.replace(" ", "_")
    photo_path = IMAGE_FOLDER / safe_filename

    with open(photo_path, "wb") as image_file:
        image_file.write(photo.getbuffer())

    return str(photo_path)


def create_inspiration_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inspiration (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            board_name TEXT,
            notes TEXT,
            image_path TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def add_inspiration_pin(title, board_name, notes, image_path):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO inspiration (
            title,
            board_name,
            notes,
            image_path
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            title,
            board_name,
            notes,
            image_path
        )
    )

    connection.commit()
    connection.close()


def get_inspiration_pins():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            board_name,
            notes,
            image_path
        FROM inspiration
        ORDER BY id DESC
        """
    )

    pins = cursor.fetchall()
    connection.close()

    return pins


def delete_inspiration_pin(pin_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT image_path
        FROM inspiration
        WHERE id = ?
        """,
        (pin_id,)
    )

    result = cursor.fetchone()

    cursor.execute(
        """
        DELETE FROM inspiration
        WHERE id = ?
        """,
        (pin_id,)
    )

    connection.commit()
    connection.close()

    if result:
        image_path = result[0]

        if image_path and os.path.exists(image_path):
            os.remove(image_path)


def save_inspiration_image(uploaded_image):
    if uploaded_image is None:
        return None

    file_extension = Path(uploaded_image.name).suffix.lower()
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    image_path = INSPIRATION_FOLDER / unique_filename

    with open(image_path, "wb") as image_file:
        image_file.write(uploaded_image.getbuffer())

    return str(image_path)

def create_outfits_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS outfits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outfit_name TEXT NOT NULL,
            occasion TEXT,
            notes TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS outfit_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outfit_id INTEGER NOT NULL,
            clothing_id INTEGER NOT NULL,
            FOREIGN KEY (outfit_id) REFERENCES outfits(id),
            FOREIGN KEY (clothing_id) REFERENCES clothing(id)
        )
        """
    )
def add_outfit(
    outfit_name,
    occasion,
    notes,
    clothing_ids
):
    connection = connect_to_database()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO outfits (
                outfit_name,
                occasion,
                notes
            )
            VALUES (?, ?, ?)
            """,
            (
                outfit_name,
                occasion,
                notes,
            )
        )

        outfit_id = cursor.lastrowid

        for clothing_id in clothing_ids:
            cursor.execute(
                """
                INSERT INTO outfit_items (
                    outfit_id,
                    clothing_id
                )
                VALUES (?, ?)
                """,
                (
                    outfit_id,
                    clothing_id,
                )
            )

        connection.commit()

        return outfit_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
def get_saved_outfits():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            outfit_name,
            occasion,
            notes
        FROM outfits
        ORDER BY id DESC
        """
    )

    outfits = cursor.fetchall()

    connection.close()

    return outfits

def get_outfit_items(outfit_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            clothing.id,
            clothing.item_name,
            clothing.category,
            clothing.color,
            clothing.season,
            clothing.favorite,
            clothing.photo_path
        FROM clothing
        JOIN outfit_items
            ON clothing.id = outfit_items.clothing_id
        WHERE outfit_items.outfit_id = ?
        """,
        (outfit_id,)
    )

    items = cursor.fetchall()

    connection.close()

    return items

    connection.commit()
    connection.close()

    connection.commit()
    connection.close()


def create_outfit_calendar_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS outfit_calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            outfit_id INTEGER NOT NULL,
            wear_date TEXT NOT NULL,
            event_name TEXT,
            notes TEXT,
            FOREIGN KEY (outfit_id) REFERENCES outfits(id)
        )
        """
    )

    connection.commit()
    connection.close()


def get_calendar_outfits_between(start_date, end_date):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            outfit_calendar.id,
            outfit_calendar.wear_date,
            outfit_calendar.event_name,
            outfit_calendar.notes,
            outfits.id,
            outfits.outfit_name,
            outfits.occasion
        FROM outfit_calendar
        JOIN outfits
            ON outfit_calendar.outfit_id = outfits.id
        WHERE outfit_calendar.wear_date BETWEEN ? AND ?
        ORDER BY outfit_calendar.wear_date ASC
        """,
        (
            start_date,
            end_date,
        )
    )

    calendar_outfits = cursor.fetchall()

    connection.close()

    return calendar_outfits

def create_wishlist_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            category TEXT,
            color TEXT,
            store_name TEXT,
            price REAL,
            item_link TEXT,
            priority TEXT,
            notes TEXT,
            image_path TEXT,
            purchased INTEGER DEFAULT 0
        )
        """
    )

    connection.commit()
    connection.close()
def save_wishlist_image(uploaded_image):
    if uploaded_image is None:
        return None

    file_extension = Path(uploaded_image.name).suffix.lower()

    unique_filename = (
        f"{uuid.uuid4().hex}{file_extension}"
    )

    image_path = WISHLIST_FOLDER / unique_filename

    with open(image_path, "wb") as image_file:
        image_file.write(
            uploaded_image.getbuffer()
        )

    return str(image_path)

def add_wishlist_item(
    item_name,
    category,
    color,
    store_name,
    price,
    item_link,
    priority,
    notes,
    image_path
):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO wishlist (
            item_name,
            category,
            color,
            store_name,
            price,
            item_link,
            priority,
            notes,
            image_path,
            purchased
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """,
        (
            item_name,
            category,
            color,
            store_name,
            price,
            item_link,
            priority,
            notes,
            image_path,
        )
    )

    connection.commit()
    connection.close()

def get_wishlist_items():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            item_name,
            category,
            color,
            store_name,
            price,
            item_link,
            priority,
            notes,
            image_path,
            purchased
        FROM wishlist
        ORDER BY id DESC
        """
    )

    wishlist_items = cursor.fetchall()

    connection.close()

    return wishlist_items

def update_wishlist_purchase_status(
    wishlist_id,
    purchased
):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE wishlist
        SET purchased = ?
        WHERE id = ?
        """,
        (
            int(purchased),
            wishlist_id,
        )
    )

    connection.commit()
    connection.close()

def delete_wishlist_item(wishlist_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT image_path
        FROM wishlist
        WHERE id = ?
        """,
        (wishlist_id,)
    )

    result = cursor.fetchone()

    cursor.execute(
        """
        DELETE FROM wishlist
        WHERE id = ?
        """,
        (wishlist_id,)
    )

    connection.commit()
    connection.close()

    if result:
        image_path = result[0]

        if image_path and os.path.exists(image_path):
            os.remove(image_path)

# --------------------------------------------------
# DESIGN COMPONENTS
# --------------------------------------------------

def render_section_heading(title, subtitle=None):
    st.markdown(
        f'<p class="closet-section-title">{title}</p>',
        unsafe_allow_html=True,
    )

    if subtitle:
        st.markdown(
            f'<p class="closet-section-subtitle">{subtitle}</p>',
            unsafe_allow_html=True,
        )


def render_metric_tile(label, value, tile_key):
    with st.container(
        key=f"metric-tile-{tile_key}"
    ):
        st.metric(
            label=label,
            value=value,
        )


def render_clothing_card(item, location="closet"):
    item_id = item[0]
    item_name = item[1]
    category = item[2]
    color = item[3]
    season = item[4]
    favorite = item[5]
    photo_path = item[6]

    with st.container(
        key=f"closet-card-{location}-{item_id}"
    ):

        if photo_path and os.path.exists(photo_path):
            st.image(
                photo_path,
                use_container_width=True,
            )
        else:
            st.info("No image available")

        title_column, heart_column = st.columns(
            [5, 1],
            vertical_alignment="center",
        )

        with title_column:
            st.markdown(
                f"### {item_name}"
            )

        with heart_column:
            if favorite:
                st.markdown(
                    "<h3 style='text-align:right;'>♡</h3>",
                    unsafe_allow_html=True,
                )

        st.caption(category)

        details = []

        if color:
            details.append(color)

        if season:
            details.append(season)

        if details:
            st.write(" • ".join(details))

def render_wishlist_card(item):
    wishlist_id = item[0]
    item_name = item[1]
    category = item[2]
    color = item[3]
    store_name = item[4]
    price = item[5]
    item_link = item[6]
    priority = item[7]
    notes = item[8]
    image_path = item[9]
    purchased = item[10]

    with st.container(
        key=f"closet-card-wishlist-{wishlist_id}"
    ):

        if image_path and os.path.exists(image_path):
            st.image(
                image_path,
                use_container_width=True,
            )
        else:
            st.info("No reference image")

        st.markdown(
            f"### {item_name}"
        )

        details = []

        if category:
            details.append(category)

        if color:
            details.append(color)

        if details:
            st.caption(
                " • ".join(details)
            )

        if price is not None:
            st.markdown(
                f"**${price:,.2f}**"
            )

        if store_name:
            st.write(
                f"Store: {store_name}"
            )

        if priority:
            st.write(
                f"Priority: {priority}"
            )

        if notes:
            st.write(notes)

        if item_link:
            st.link_button(
                "View Item",
                item_link,
                use_container_width=True,
            )

        if purchased:
            st.success("Purchased")
# --------------------------------------------------
# BACKGROUND SETTINGS
# --------------------------------------------------

def create_background_settings_table():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS background_settings (
            page_name TEXT PRIMARY KEY,
            image_path TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def save_page_background(page_name, image_path):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO background_settings (page_name, image_path)
        VALUES (?, ?)
        ON CONFLICT(page_name)
        DO UPDATE SET image_path = excluded.image_path
        """,
        (page_name, image_path),
    )

    connection.commit()
    connection.close()


def get_page_background(page_name):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT image_path
        FROM background_settings
        WHERE page_name = ?
        """,
        (page_name,),
    )

    result = cursor.fetchone()

    connection.close()

    if result:
        return result[0]

    return None


def remove_page_background(page_name):
    image_path = get_page_background(page_name)

    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM background_settings
        WHERE page_name = ?
        """,
        (page_name,),
    )

    connection.commit()
    connection.close()

    if image_path and os.path.exists(image_path):
        os.remove(image_path)

# --------------------------------------------------
# BACKGROUND IMAGE HELPERS
# --------------------------------------------------

def save_background_image(uploaded_file, page_name):
    if uploaded_file is None:
        return None

    extension = uploaded_file.name.split(".")[-1].lower()

    safe_page_name = (
        page_name.lower()
        .replace(" ", "_")
        .replace("🏠", "")
        .replace("➕", "")
        .replace("👚", "")
        .replace("👗", "")
        .replace("📌", "")
        .replace("📅", "")
        .replace("❤️", "")
        .replace("🎨", "")
        .strip("_")
    )

    file_name = (
        f"{safe_page_name}_{uuid.uuid4().hex}.{extension}"
    )

    image_path = BACKGROUND_FOLDER / file_name

    with open(image_path, "wb") as image_file:
        image_file.write(uploaded_file.getbuffer())

    return str(image_path)


def apply_page_background(page_name):
    image_path = get_page_background(page_name)

    if not image_path or not os.path.exists(image_path):
        return

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(
            image_file.read()
        ).decode()

    extension = image_path.split(".")[-1].lower()

    if extension == "jpg":
        extension = "jpeg"

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(255, 255, 255, 0.08),
                    rgba(255, 255, 255, 0.08)
                ),
                url("data:image/{extension};base64,{encoded_image}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        .block-container {{
            max-width: 1250px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


create_clothing_table()
create_inspiration_table()
create_background_settings_table()
create_outfits_table()
create_outfit_calendar_table()
create_wishlist_table()

def add_outfit_to_calendar(
    outfit_id,
    wear_date,
    event_name,
    notes
):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO outfit_calendar (
            outfit_id,
            wear_date,
            event_name,
            notes
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            outfit_id,
            wear_date,
            event_name,
            notes,
        )
    )

    connection.commit()
    connection.close()

def get_calendar_outfits():
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            outfit_calendar.id,
            outfit_calendar.wear_date,
            outfit_calendar.event_name,
            outfit_calendar.notes,
            outfits.id,
            outfits.outfit_name,
            outfits.occasion
        FROM outfit_calendar
        JOIN outfits
            ON outfit_calendar.outfit_id = outfits.id
        ORDER BY outfit_calendar.wear_date ASC
        """
    )

    calendar_outfits = cursor.fetchall()

    connection.close()

    return calendar_outfits

def delete_calendar_outfit(calendar_id):
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM outfit_calendar
        WHERE id = ?
        """,
        (calendar_id,)
    )

    connection.commit()
    connection.close()

# --------------------------------------------------
# DASHBOARD HELPERS
# --------------------------------------------------

WEATHER_CITY = "Atlanta"


@st.cache_data(ttl=1800, show_spinner=False)
def get_current_weather(city_name):
    """Return current weather without requiring an API key."""
    try:
        geocode_query = urlencode(
            {
                "name": city_name,
                "count": 1,
                "language": "en",
                "format": "json",
            }
        )

        with urlopen(
            f"https://geocoding-api.open-meteo.com/v1/search?{geocode_query}",
            timeout=5,
        ) as response:
            geocode_data = json.load(response)

        results = geocode_data.get("results", [])
        if not results:
            return None

        location = results[0]
        latitude = location["latitude"]
        longitude = location["longitude"]

        forecast_query = urlencode(
            {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,apparent_temperature,weather_code",
                "temperature_unit": "fahrenheit",
                "timezone": "auto",
            }
        )

        with urlopen(
            f"https://api.open-meteo.com/v1/forecast?{forecast_query}",
            timeout=5,
        ) as response:
            forecast_data = json.load(response)

        current = forecast_data.get("current", {})
        weather_code = current.get("weather_code")

        descriptions = {
            0: "Clear",
            1: "Mostly clear",
            2: "Partly cloudy",
            3: "Cloudy",
            45: "Foggy",
            48: "Foggy",
            51: "Light drizzle",
            53: "Drizzle",
            55: "Heavy drizzle",
            61: "Light rain",
            63: "Rain",
            65: "Heavy rain",
            71: "Light snow",
            73: "Snow",
            75: "Heavy snow",
            80: "Light showers",
            81: "Showers",
            82: "Heavy showers",
            95: "Thunderstorms",
            96: "Thunderstorms",
            99: "Thunderstorms",
        }

        return {
            "city": location.get("name", city_name),
            "temperature": round(current.get("temperature_2m", 0)),
            "feels_like": round(current.get("apparent_temperature", 0)),
            "description": descriptions.get(weather_code, "Current conditions"),
        }

    except Exception:
        return None


def get_weather_suggestion(temperature, description):
    description_lower = description.lower()

    if "rain" in description_lower or "shower" in description_lower:
        return "A light layer and weather-ready shoes would work well today."
    if temperature >= 82:
        return "Lightweight dresses, tanks, sandals, and breathable fabrics fit the day."
    if temperature >= 68:
        return "A simple top-and-bottom combination or a light dress should feel comfortable."
    if temperature >= 52:
        return "Try a light jacket, knit, or layered outfit."
    return "A warm coat, knit layers, and closed-toe shoes make the most sense today."


def move_closet_spotlight(direction, item_count):
    if item_count == 0:
        return

    current_start = st.session_state.get("closet_spotlight_start", 0)
    st.session_state["closet_spotlight_start"] = (
        current_start + direction
    ) % item_count


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

def navigate_to(page_name):
    """Change pages safely before the sidebar radio is recreated."""
    st.session_state["sidebar_navigation"] = page_name

with st.sidebar:
    st.markdown(
        """
        <div class="closet-brand-header">
            <div class="closet-brand-title">Walk In Closet</div>
            <div class="closet-brand-tagline">Your Digital Wardrobe</div>
            <div class="closet-brand-rule"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    navigation_options = [
        "Dashboard",
        "Add Item",
        "My Closet",
        "Outfit Builder",
        "Inspiration",
        "Outfit Calendar",
        "Wishlist",
        "Closet Reno",
    ]

    if "sidebar_navigation" not in st.session_state:
        st.session_state["sidebar_navigation"] = "Dashboard"

    page = st.radio(
        "Navigation",
        navigation_options,
        label_visibility="collapsed",
        key="sidebar_navigation",
    )

    st.divider()
    st.caption("Step into your style.")

apply_page_background(page)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    clothing_items = get_clothing_items()
    inspiration_pins = get_inspiration_pins()
    calendar_outfits = get_calendar_outfits()

    top_count = sum(item[2] == "Top" for item in clothing_items)
    bottom_count = sum(item[2] == "Bottom" for item in clothing_items)
    dress_count = sum(item[2] == "Dress" for item in clothing_items)
    shoe_count = sum(item[2] == "Shoes" for item in clothing_items)

    # ----------------------------------------------
    # WELCOME PANEL
    # ----------------------------------------------

    with st.container(key="panel-dashboard-welcome"):
        welcome_column, metrics_column = st.columns(
            [1.15, 2],
            gap="large",
            vertical_alignment="center",
        )

        with welcome_column:
            st.title("Welcome back.")
            st.markdown(
                """
                <p class="closet-welcome-question">
                    What are we wearing today?
                </p>
                """,
                unsafe_allow_html=True,
            )

        with metrics_column:
            metric_columns = st.columns(4, gap="small")

            with metric_columns[0]:
                render_metric_tile("Tops", top_count, "tops")
            with metric_columns[1]:
                render_metric_tile("Bottoms", bottom_count, "bottoms")
            with metric_columns[2]:
                render_metric_tile("Dresses", dress_count, "dresses")
            with metric_columns[3]:
                render_metric_tile("Shoes", shoe_count, "shoes")

    # ----------------------------------------------
    # TODAY + WEATHER
    # ----------------------------------------------

    today_string = date.today().isoformat()
    todays_calendar_entries = [
        entry for entry in calendar_outfits
        if entry[1] == today_string
    ]
    current_weather = get_current_weather(WEATHER_CITY)

    today_column, weather_column = st.columns(
        [1.65, 1],
        gap="large",
        vertical_alignment="top",
    )

    with today_column:
        with st.container(key="panel-dashboard-today"):
            render_section_heading(
                "Today's Outfit",
                "Your look for today, pulled from the outfit calendar.",
            )
            st.write("")

            if todays_calendar_entries:
                today_entry = todays_calendar_entries[0]
                outfit_id = today_entry[4]
                outfit_name = today_entry[5]
                occasion = today_entry[6]
                event_name = today_entry[2]
                outfit_items = get_outfit_items(outfit_id)

                image_column, details_column = st.columns(
                    [1.35, 1],
                    gap="large",
                    vertical_alignment="center",
                )

                with image_column:
                    if outfit_items:
                        outfit_image_columns = st.columns(
                            min(len(outfit_items), 3),
                            gap="small",
                        )
                        for index, item in enumerate(outfit_items[:3]):
                            with outfit_image_columns[index]:
                                if item[6] and os.path.exists(item[6]):
                                    st.image(
                                        item[6],
                                        use_container_width=True,
                                    )

                with details_column:
                    st.markdown(f"### {outfit_name}")
                    if event_name:
                        st.write(event_name)
                    if occasion:
                        st.caption(occasion)
                    st.button(
                        "Open Calendar",
                        key="dashboard-open-calendar",
                        use_container_width=True,
                        on_click=navigate_to,
                        args=("Outfit Calendar",),
                    )
            else:
                st.markdown("### Nothing planned for today.")
                st.caption("Choose a saved outfit and add it to your calendar.")
                st.button(
                    "Plan Today's Outfit",
                    key="dashboard-plan-today",
                    on_click=navigate_to,
                    args=("Outfit Calendar",),
                )

    with weather_column:
        with st.container(key="panel-dashboard-weather"):
            render_section_heading("Today's Weather", WEATHER_CITY)
            st.write("")

            if current_weather:
                st.markdown(
                    f"<div style='font-size:3rem;font-weight:700;line-height:1;'>"
                    f"{current_weather['temperature']}°</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"### {current_weather['description']}")
                st.caption(
                    f"Feels like {current_weather['feels_like']}°"
                )
                st.write(
                    get_weather_suggestion(
                        current_weather["temperature"],
                        current_weather["description"],
                    )
                )
            else:
                st.markdown("### Weather unavailable")
                st.caption(
                    "The rest of the dashboard will continue working normally."
                )

    # ----------------------------------------------
    # CLOSET SPOTLIGHT CAROUSEL
    # ----------------------------------------------

    with st.container(key="panel-dashboard-spotlight"):
        heading_column, controls_column, button_column = st.columns(
            [5, 1.35, 1.2],
            vertical_alignment="center",
        )

        with heading_column:
            render_section_heading(
                "Closet Spotlight",
                "Move through your closet and rediscover what you already own.",
            )

        with controls_column:
            previous_column, next_column = st.columns(2, gap="small")
            with previous_column:
                st.button(
                    "Previous",
                    key="spotlight-previous",
                    use_container_width=True,
                    on_click=move_closet_spotlight,
                    args=(-1, len(clothing_items)),
                    disabled=len(clothing_items) <= 3,
                )
            with next_column:
                st.button(
                    "Next",
                    key="spotlight-next",
                    use_container_width=True,
                    on_click=move_closet_spotlight,
                    args=(1, len(clothing_items)),
                    disabled=len(clothing_items) <= 3,
                )

        with button_column:
            st.button(
                "View All",
                use_container_width=True,
                key="dashboard-view-all",
                on_click=navigate_to,
                args=("My Closet",),
            )

        st.write("")

        if not clothing_items:
            st.info("Your closet is empty. Add your first item.")
        else:
            start_index = st.session_state.get("closet_spotlight_start", 0)
            visible_count = min(3, len(clothing_items))
            spotlight_items = [
                clothing_items[(start_index + offset) % len(clothing_items)]
                for offset in range(visible_count)
            ]

            clothing_columns = st.columns(visible_count, gap="medium")
            for index, item in enumerate(spotlight_items):
                with clothing_columns[index]:
                    render_clothing_card(
                        item,
                        location=f"spotlight-{start_index}",
                    )

    # ----------------------------------------------
    # STYLE INSPIRATION
    # ----------------------------------------------

    with st.container(key="panel-dashboard-inspiration"):
        heading_column, button_column = st.columns(
            [5, 1],
            vertical_alignment="center",
        )

        with heading_column:
            render_section_heading(
                "Style Inspiration",
                "A few ideas from your saved pins.",
            )

        with button_column:
            st.button(
                "View All",
                key="dashboard-view-inspiration",
                use_container_width=True,
                on_click=navigate_to,
                args=("Inspiration",),
            )

        st.write("")

        if not inspiration_pins:
            st.info("Add a few inspiration images and they will appear here.")
        else:
            visible_pins = inspiration_pins[:3]
            pin_columns = st.columns(len(visible_pins), gap="medium")

            for index, pin in enumerate(visible_pins):
                pin_id = pin[0]
                image_path = pin[4]

                with pin_columns[index]:
                    with st.container(
                        key=f"inspiration-card-dashboard-{pin_id}"
                    ):
                        if image_path and os.path.exists(image_path):
                            st.image(
                                image_path,
                                use_container_width=True,
                            )
                        else:
                            st.info("Image unavailable")

# --------------------------------------------------
# ADD ITEM
# --------------------------------------------------

elif page == "Add Item":

    with st.container(
        key="panel-add-item"
    ):

        render_section_heading(
            "Add Clothing",
            "Add a new piece to your digital closet.",
        )

        st.write("")

        with st.form(
            "add_clothing_form",
            clear_on_submit=True,
        ):

            item_name = st.text_input(
                "Item Name"
            )

            category = st.selectbox(
                "Category",
                [
                    "Top",
                    "Bottom",
                    "Dress",
                    "Shoes",
                    "Outerwear",
                    "Bag",
                    "Accessory",
                ],
            )

            color = st.text_input(
                "Color"
            )

            season = st.multiselect(
                "Season",
                [
                    "Spring",
                    "Summer",
                    "Fall",
                    "Winter",
                ],
            )

            favorite = st.checkbox(
                "Favorite ⭐"
            )

            photo = st.file_uploader(
                "Photo",
                type=["jpg", "jpeg", "png"],
            )

            submitted = st.form_submit_button(
                "Add to Closet"
            )

            if submitted:

                if item_name.strip() == "":

                    st.error(
                        "Please enter an item name."
                    )

                else:

                    photo_path = save_uploaded_photo(photo)

                    season_text = ", ".join(season)

                    add_clothing_item(
                        item_name=item_name.strip(),
                        category=category,
                        color=color.strip(),
                        season=season_text,
                        favorite=favorite,
                        photo_path=photo_path,
                    )

                    st.success(
                        f"{item_name} added to your closet!"
                    )
# --------------------------------------------------
# MY CLOSET
# --------------------------------------------------

elif page == "My Closet":

    clothing_items = get_clothing_items()


    # ----------------------------------------------
    # CLOSET HEADER AND FILTERS
    # ----------------------------------------------

    with st.container(
        key="panel-my-closet-filters"
    ):

        render_section_heading(
            "My Closet",
            "Search, filter, and browse everything you own.",
        )

        st.write("")

        if len(clothing_items) == 0:

            st.info(
                "Your closet is empty. Add your first item!"
            )

        else:

            search = st.text_input(
                "Search your closet",
                placeholder="Try: white, dress, summer...",
            )

            filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(
                4,
                gap="small",
            )

            with filter_col1:

                category_filter = st.selectbox(
                    "Category",
                    [
                        "All",
                        "Top",
                        "Bottom",
                        "Dress",
                        "Shoes",
                        "Outerwear",
                        "Bag",
                        "Accessory",
                    ],
                )

            with filter_col2:

                season_filter = st.selectbox(
                    "Season",
                    [
                        "All",
                        "Spring",
                        "Summer",
                        "Fall",
                        "Winter",
                    ],
                )

            with filter_col3:

                favorite_filter = st.selectbox(
                    "Favorite",
                    [
                        "All",
                        "Favorites only",
                        "Not favorited",
                    ],
                )

            with filter_col4:

                sort_option = st.selectbox(
                    "Sort by",
                    [
                        "Newest first",
                        "Oldest first",
                        "Name A–Z",
                        "Name Z–A",
                    ],
                )


    # ----------------------------------------------
    # FILTER CLOTHING ITEMS
    # ----------------------------------------------

    if len(clothing_items) > 0:

        filtered_items = []

        for item in clothing_items:

            item_name = item[1]
            category = item[2]
            color = item[3] or ""
            season = item[4] or ""
            favorite = item[5]

            search_text = search.strip().lower()

            matches_search = (
                search_text == ""
                or search_text in item_name.lower()
                or search_text in category.lower()
                or search_text in color.lower()
                or search_text in season.lower()
            )

            matches_category = (
                category_filter == "All"
                or category == category_filter
            )

            matches_season = (
                season_filter == "All"
                or season_filter in season
            )

            matches_favorite = (
                favorite_filter == "All"
                or (
                    favorite_filter == "Favorites only"
                    and favorite == 1
                )
                or (
                    favorite_filter == "Not favorited"
                    and favorite == 0
                )
            )

            if (
                matches_search
                and matches_category
                and matches_season
                and matches_favorite
            ):

                filtered_items.append(item)

        if sort_option == "Oldest first":

            filtered_items.sort(
                key=lambda item: item[0]
            )

        elif sort_option == "Name A–Z":

            filtered_items.sort(
                key=lambda item: item[1].lower()
            )

        elif sort_option == "Name Z–A":

            filtered_items.sort(
                key=lambda item: item[1].lower(),
                reverse=True,
            )

        else:

            filtered_items.sort(
                key=lambda item: item[0],
                reverse=True,
            )


        # ------------------------------------------
        # CLOSET GALLERY
        # ------------------------------------------

        with st.container(
            key="panel-my-closet-gallery"
        ):

            heading_column, count_column = st.columns(
                [4, 1],
                vertical_alignment="center",
            )

            with heading_column:

                render_section_heading(
                    "Your Wardrobe"
                )

            with count_column:

                st.caption(
                    f"{len(filtered_items)} of "
                    f"{len(clothing_items)} items"
                )

            st.write("")

            if len(filtered_items) == 0:

                st.warning(
                    "No clothing items match those filters."
                )

            else:

                clothing_columns = st.columns(
                    3,
                    gap="medium",
                )

                for index, item in enumerate(filtered_items):

                    with clothing_columns[index % 3]:

                        render_clothing_card(
                            item,
                            location="closet",
                        )
# --------------------------------------------------
# OUTFIT BUILDER
# --------------------------------------------------

elif page == "Outfit Builder":

    clothing_items = get_clothing_items()

    render_section_heading(
        "Outfit Builder",
        "Mix and match pieces from your digital closet.",
    )

    st.write("")

    build_tab, saved_tab = st.tabs(
        [
            "Build an Outfit",
            "Saved Outfits",
        ]
    )

    # --------------------------------------------------
    # BUILD OUTFIT TAB
    # --------------------------------------------------

    with build_tab:

        if len(clothing_items) == 0:

            st.info(
                "Your closet is empty. Add clothing before building an outfit."
            )

        else:

            tops = [
                item for item in clothing_items
                if item[2] == "Top"
            ]

            bottoms = [
                item for item in clothing_items
                if item[2] == "Bottom"
            ]

            dresses = [
                item for item in clothing_items
                if item[2] == "Dress"
            ]

            shoes = [
                item for item in clothing_items
                if item[2] == "Shoes"
            ]

            outerwear = [
                item for item in clothing_items
                if item[2] == "Outerwear"
            ]

            bags = [
                item for item in clothing_items
                if item[2] == "Bag"
            ]

            accessories = [
                item for item in clothing_items
                if item[2] == "Accessory"
            ]

            outfit_name = st.text_input(
                "Outfit Name",
                placeholder="Example: Pink Dinner Outfit",
            )

            occasion = st.selectbox(
                "Occasion",
                [
                    "Everyday",
                    "School",
                    "Work",
                    "Dinner",
                    "Party",
                    "Date Night",
                    "Formal",
                    "Vacation",
                    "Other",
                ],
            )

            st.write("### Choose your pieces")

            base_type = st.radio(
                "Choose an outfit base",
                [
                    "Top and Bottom",
                    "Dress",
                ],
                horizontal=True,
            )

            selected_items = []

            if base_type == "Top and Bottom":

                base_column1, base_column2 = st.columns(2)

                with base_column1:

                    selected_top = st.selectbox(
                        "Top",
                        options=[None] + tops,
                        format_func=lambda item: (
                            "Choose a top"
                            if item is None
                            else item[1]
                        ),
                    )

                    if selected_top is not None:
                        selected_items.append(selected_top)

                with base_column2:

                    selected_bottom = st.selectbox(
                        "Bottom",
                        options=[None] + bottoms,
                        format_func=lambda item: (
                            "Choose a bottom"
                            if item is None
                            else item[1]
                        ),
                    )

                    if selected_bottom is not None:
                        selected_items.append(selected_bottom)

            else:

                selected_dress = st.selectbox(
                    "Dress",
                    options=[None] + dresses,
                    format_func=lambda item: (
                        "Choose a dress"
                        if item is None
                        else item[1]
                    ),
                )

                if selected_dress is not None:
                    selected_items.append(selected_dress)

            extra_column1, extra_column2 = st.columns(2)

            with extra_column1:

                selected_shoes = st.selectbox(
                    "Shoes",
                    options=[None] + shoes,
                    format_func=lambda item: (
                        "No shoes selected"
                        if item is None
                        else item[1]
                    ),
                )

                if selected_shoes is not None:
                    selected_items.append(selected_shoes)

                selected_bag = st.selectbox(
                    "Bag",
                    options=[None] + bags,
                    format_func=lambda item: (
                        "No bag selected"
                        if item is None
                        else item[1]
                    ),
                )

                if selected_bag is not None:
                    selected_items.append(selected_bag)

            with extra_column2:

                selected_outerwear = st.selectbox(
                    "Outerwear",
                    options=[None] + outerwear,
                    format_func=lambda item: (
                        "No outerwear selected"
                        if item is None
                        else item[1]
                    ),
                )

                if selected_outerwear is not None:
                    selected_items.append(selected_outerwear)

                selected_accessory = st.selectbox(
                    "Accessory",
                    options=[None] + accessories,
                    format_func=lambda item: (
                        "No accessory selected"
                        if item is None
                        else item[1]
                    ),
                )

                if selected_accessory is not None:
                    selected_items.append(selected_accessory)

            outfit_notes = st.text_area(
                "Notes",
                placeholder=(
                    "Add styling notes, hairstyle ideas, "
                    "jewelry choices, or where you plan to wear it."
                ),
            )

            st.divider()

            # ------------------------------------------
            # OUTFIT PREVIEW
            # ------------------------------------------

            st.write("### Outfit Preview")

            if len(selected_items) == 0:

                st.info(
                    "Choose clothing pieces to preview your outfit."
                )

            else:

                preview_columns = st.columns(
                    min(len(selected_items), 4)
                )

                for index, item in enumerate(selected_items):

                    with preview_columns[index % len(preview_columns)]:

                        render_clothing_card(
                            item,
                            location=f"outfit-preview-{index}",
                        )

            st.write("")

        save_outfit = st.button(
            "Save Outfit",
            type="primary",
            use_container_width=True,
            key="save_outfit_button",
        )

        if save_outfit:

            if outfit_name.strip() == "":
                st.error("Please give your outfit a name.")

            elif len(selected_items) == 0:
                st.error("Please choose at least one clothing item.")

            elif (
                base_type == "Top and Bottom"
                and (
                    selected_top is None
                    or selected_bottom is None
                )
            ):
                st.error("Please choose both a top and a bottom.")

            elif (
                base_type == "Dress"
                and selected_dress is None
            ):
                st.error("Please choose a dress.")

            else:
                clothing_ids = [
                    item[0]
                    for item in selected_items
                ]

                try:
                    add_outfit(
                        outfit_name=outfit_name.strip(),
                        occasion=occasion,
                        notes=outfit_notes.strip(),
                        clothing_ids=clothing_ids,
                    )

                    st.success(
                        f"{outfit_name.strip()} was saved! "
                        "Open the Saved Outfits tab to view it."
                    )

                except Exception as error:
                    st.error(
                        f"The outfit could not be saved: {error}"
                    )

    # --------------------------------------------------
    # SAVED OUTFITS TAB
    # --------------------------------------------------

    with saved_tab:

        saved_outfits = get_saved_outfits()

        if len(saved_outfits) == 0:

            st.info(
                "You have not saved any outfits yet."
            )

        else:

            for outfit in saved_outfits:

                outfit_id = outfit[0]
                outfit_name = outfit[1]
                occasion = outfit[2]
                notes = outfit[3]

                with st.container(
                    key=f"panel-saved-outfit-{outfit_id}"
                ):

                    st.markdown(
                        f"## {outfit_name}"
                    )

                    if occasion:
                        st.caption(
                            f"Occasion: {occasion}"
                        )

                    if notes:
                        st.write(notes)

                    outfit_items = get_outfit_items(
                        outfit_id
                    )

                    if len(outfit_items) > 0:

                        category_order = {
                            "Outerwear": 0,
                            "Top": 1,
                            "Dress": 1,
                            "Bottom": 2,
                            "Shoes": 3,
                            "Bag": 4,
                            "Accessory": 5,
                        }

                        sorted_outfit_items = sorted(
                            outfit_items,
                            key=lambda item: category_order.get(
                                item[2],
                                99,
                            ),
                        )

                        with st.container(
                            key=f"mini-outfit-saved-{outfit_id}"
                        ):

                            for item in sorted_outfit_items:

                                item_name = item[1]
                                category = item[2]
                                photo_path = item[6]

                                if (
                                    photo_path
                                    and os.path.exists(photo_path)
                                ):

                                    st.image(
                                        photo_path,
                                        use_container_width=True,
                                    )

                                else:

                                    st.caption(
                                        f"{category}: {item_name}"
                                    )
# --------------------------------------------------
# INSPIRATION STUDIO
# --------------------------------------------------

elif page == "Inspiration":

    st.title(" Inspiration Studio")

    st.write(
        "Save screenshots and ideas that inspire your outfits."
    )

    inspiration_tab, add_pin_tab = st.tabs(
        [
            "My Inspiration",
            "Add a Pin",
        ]
    )


    # ----------------------------------------------
    # ADD A PIN
    # ----------------------------------------------
    with add_pin_tab:

        st.subheader("Add inspiration")

        with st.form(
            "add_inspiration_form",
            clear_on_submit=True,
        ):

            pin_title = st.text_input(
                "Title (optional)",
                placeholder="Example: Pink rush outfit",
            )

            board_name = st.text_input(
                "Board",
                placeholder="Example: Rush, Summer, Date Night",
            )

            pin_notes = st.text_area(
                "Notes",
                placeholder=(
                    "What do you like about this look? "
                    "Do you own anything similar?"
                ),
            )

            inspiration_image = st.file_uploader(
                "Upload a screenshot",
                type=["jpg", "jpeg", "png"],
                key="inspiration_image_uploader",
            )

            save_pin = st.form_submit_button(
                "Save to Inspiration"
            )

            if save_pin:

                if inspiration_image is None:

                    st.error(
                        "Please upload a screenshot."
                    )

                else:

                    image_path = save_inspiration_image(
                        inspiration_image
                    )

                    saved_title = pin_title.strip()
                    
                    add_inspiration_pin(
                        title=saved_title,
                        board_name=board_name.strip(),
                        notes=pin_notes.strip(),
                        image_path=image_path,
                    )

                    st.success(
                        "Your inspiration was saved!"
                    )

                    st.rerun()
    # ----------------------------------------------
    # VIEW INSPIRATION
    # ----------------------------------------------

    with inspiration_tab:

        pins = get_inspiration_pins()

        if len(pins) == 0:

            st.info(
                "Your inspiration studio is empty. "
                "Add your first screenshot!"
            )

        else:

            board_names = sorted(
                {
                    pin[2]
                    for pin in pins
                    if pin[2] is not None
                    and pin[2].strip() != ""
                }
            )

            board_filter = st.selectbox(
                "Board",
                ["All Boards"] + board_names,
            )

            if board_filter == "All Boards":

                visible_pins = pins

            else:

                visible_pins = [
                    pin
                    for pin in pins
                    if pin[2] == board_filter
                ]

            st.caption(
                f"Showing {len(visible_pins)} inspiration pins"
            )

            st.divider()

            columns = st.columns(3)

            for index, pin in enumerate(visible_pins):

                pin_id = pin[0]
                title = pin[1]
                board = pin[2]
                notes = pin[3]
                image_path = pin[4]

                with columns[index % 3]:

                    with st.container(key = f"inspiration-card-{pin_id}"):

                        if (
                            image_path
                            and os.path.exists(image_path)
                        ):

                            st.image(
                                image_path,
                                use_container_width=True,
                            )

                        else:

                            st.write(
                                "📷 Image unavailable"
                            )

                        if title.strip():

                            st.markdown(
                                f"### {title}"
                            )

                        if board:

                            st.caption(
                                f"📌 {board}"
                            )

                        if notes:

                            st.write(notes)

                        if st.button(
                            "Delete",
                            key=f"delete_pin_{pin_id}",
                        ):

                            delete_inspiration_pin(
                                pin_id
                            )

                            st.rerun()


# --------------------------------------------------
# OUTFIT CALENDAR
# --------------------------------------------------

elif page == "Outfit Calendar":

    from datetime import date, datetime, timedelta

    render_section_heading(
        "Outfit Calendar",
        "Plan a look for every day of your week.",
    )

    st.write("")

    # --------------------------------------------------
    # WEEKLY CALENDAR STATE
    # --------------------------------------------------

    if "calendar_week_start" not in st.session_state:

        today = date.today()

        st.session_state.calendar_week_start = (
            today - timedelta(days=today.weekday())
        )

    week_start = st.session_state.calendar_week_start
    week_end = week_start + timedelta(days=6)

    # --------------------------------------------------
    # WEEK NAVIGATION
    # --------------------------------------------------

    previous_column, title_column, next_column = st.columns(
        [1, 4, 1],
        vertical_alignment="center",
    )

    with previous_column:

        if st.button(
            "← Previous",
            use_container_width=True,
            key="previous_calendar_week",
        ):

            st.session_state.calendar_week_start = (
                week_start - timedelta(days=7)
            )

            st.rerun()

    with title_column:

        st.markdown(
            (
                "<h3 style='text-align:center;'>"
                f"{week_start.strftime('%B %d')} – "
                f"{week_end.strftime('%B %d, %Y')}"
                "</h3>"
            ),
            unsafe_allow_html=True,
        )

    with next_column:

        if st.button(
            "Next →",
            use_container_width=True,
            key="next_calendar_week",
        ):

            st.session_state.calendar_week_start = (
                week_start + timedelta(days=7)
            )

            st.rerun()

    center_column1, center_column2, center_column3 = st.columns(
        [2, 1, 2]
    )

    with center_column2:

        if st.button(
            "This Week",
            use_container_width=True,
            key="return_to_current_week",
        ):

            today = date.today()

            st.session_state.calendar_week_start = (
                today - timedelta(days=today.weekday())
            )

            st.rerun()

    st.write("")

    # --------------------------------------------------
    # RETRIEVE THIS WEEK'S OUTFITS
    # --------------------------------------------------

    weekly_entries = get_calendar_outfits_between(
        week_start.isoformat(),
        week_end.isoformat(),
    )

    entries_by_date = {}

    for entry in weekly_entries:

        wear_date = entry[1]

        if wear_date not in entries_by_date:
            entries_by_date[wear_date] = []

        entries_by_date[wear_date].append(entry)

    # --------------------------------------------------
    # SEVEN-DAY CALENDAR
    # --------------------------------------------------

    day_columns = st.columns(
        7,
        gap="small",
    )

    today = date.today()

    for day_index in range(7):

        current_date = (
            week_start + timedelta(days=day_index)
        )

        date_key = current_date.isoformat()

        with day_columns[day_index]:

            with st.container(
                key=f"calendar-day-{date_key}"
            ):

                if current_date == today:

                    st.markdown(
                        (
                            "<p style='text-align:center; "
                            "font-weight:700;'>"
                            f"✨ {current_date.strftime('%A')}"
                            "</p>"
                        ),
                        unsafe_allow_html=True,
                    )

                else:

                    st.markdown(
                        (
                            "<p style='text-align:center; "
                            "font-weight:700;'>"
                            f"{current_date.strftime('%A')}"
                            "</p>"
                        ),
                        unsafe_allow_html=True,
                    )

                st.markdown(
                    (
                        "<p style='text-align:center; "
                        "font-size:1.4rem;'>"
                        f"{current_date.day}"
                        "</p>"
                    ),
                    unsafe_allow_html=True,
                )

                st.divider()

                day_entries = entries_by_date.get(
                    date_key,
                    []
                )

                if len(day_entries) == 0:

                    st.caption(
                        "No outfit planned"
                    )

                    if st.button(
                        "＋ Add Outfit",
                        key=f"add-outfit-{date_key}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            "calendar_selected_date"
                        ] = current_date

                        st.session_state[
                            "show_calendar_form"
                        ] = True

                        st.rerun()

                else:

                    for entry in day_entries:

                        calendar_id = entry[0]
                        event_name = entry[2]
                        notes = entry[3]
                        outfit_id = entry[4]
                        outfit_name = entry[5]
                        occasion = entry[6]

                        outfit_items = get_outfit_items(
                            outfit_id
                        )

                        if len(outfit_items) > 0:

                            category_order = {
                                "Outerwear": 0,
                                "Top": 1,
                                "Dress": 1,
                                "Bottom": 2,
                                "Shoes": 3,
                                "Bag": 4,
                                "Accessory": 5,
                            }

                            sorted_outfit_items = sorted(
                                outfit_items,
                                key=lambda item: category_order.get(
                                    item[2],
                                    99,
                                ),
                            )

                            with st.container(
                                key=f"mini-outfit-calendar-{calendar_id}"
                            ):

                                for item in sorted_outfit_items:

                                    item_name = item[1]
                                    category = item[2]
                                    image_path = item[6]

                                    if (
                                        image_path
                                        and os.path.exists(image_path)
                                    ):

                                        st.image(
                                            image_path,
                                            use_container_width=True,
                                        )

                                    else:

                                        st.caption(
                                            f"{category}: {item_name}"
                                        )

                        st.markdown(
                            f"**{outfit_name}**"
                        )

                        if event_name:
                            st.caption(event_name)

                        elif occasion:
                            st.caption(occasion)

                        if notes:

                            with st.expander(
                                "Notes"
                            ):

                                st.write(notes)

                        if st.button(
                            "Remove",
                            key=(
                                f"remove-calendar-"
                                f"{calendar_id}"
                            ),
                            use_container_width=True,
                        ):

                            delete_calendar_outfit(
                                calendar_id
                            )

                            st.rerun()

                    if st.button(
                        "＋ Add Another",
                        key=f"add-another-{date_key}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            "calendar_selected_date"
                        ] = current_date

                        st.session_state[
                            "show_calendar_form"
                        ] = True

                        st.rerun()

    # --------------------------------------------------
    # ADD OUTFIT FORM
    # --------------------------------------------------

    if st.session_state.get(
        "show_calendar_form",
        False,
    ):

        st.write("")

        selected_date = st.session_state.get(
            "calendar_selected_date",
            date.today(),
        )

        with st.container(
            key="panel-calendar-add-outfit"
        ):

            render_section_heading(
                (
                    "Plan an Outfit for "
                    f"{selected_date.strftime('%A, %B %d')}"
                )
            )

            saved_outfits = get_saved_outfits()

            if len(saved_outfits) == 0:

                st.info(
                    "Save an outfit in the Outfit Builder first."
                )

            else:

                with st.form(
                    "weekly_calendar_form"
                ):

                    selected_outfit = st.selectbox(
                        "Saved Outfit",
                        options=saved_outfits,
                        format_func=lambda outfit: outfit[1],
                    )

                    event_name = st.text_input(
                        "Plans or Event",
                        placeholder=(
                            "Class, dinner, birthday party..."
                        ),
                    )

                    calendar_notes = st.text_area(
                        "Notes",
                        placeholder=(
                            "Jewelry, hairstyle, weather, "
                            "or styling reminders..."
                        ),
                    )

                    save_calendar_outfit = (
                        st.form_submit_button(
                            "Save to Calendar",
                            use_container_width=True,
                        )
                    )

                    cancel_calendar_outfit = (
                        st.form_submit_button(
                            "Cancel",
                            use_container_width=True,
                        )
                    )

                    if save_calendar_outfit:

                        add_outfit_to_calendar(
                            outfit_id=selected_outfit[0],
                            wear_date=selected_date.isoformat(),
                            event_name=event_name.strip(),
                            notes=calendar_notes.strip(),
                        )

                        st.session_state[
                            "show_calendar_form"
                        ] = False

                        st.success(
                            (
                                f"{selected_outfit[1]} was "
                                f"planned for "
                                f"{selected_date.strftime('%A')}!"
                            )
                        )

                        st.rerun()

                    if cancel_calendar_outfit:

                        st.session_state[
                            "show_calendar_form"
                        ] = False

                        st.rerun()

# --------------------------------------------------
# WISHLIST
# --------------------------------------------------

elif page == "Wishlist":

    render_section_heading(
        "Wishlist",
        "Save the pieces your closet is missing.",
    )

    st.write("")

    wishlist_tab, add_item_tab, purchased_tab = st.tabs(
        [
            "My Wishlist",
            "Add an Item",
            "Purchased",
        ]
    )

    # --------------------------------------------------
    # ADD WISHLIST ITEM
    # --------------------------------------------------

    with add_item_tab:

        with st.container(
            key="panel-add-wishlist-item"
        ):

            render_section_heading(
                "Add to Wishlist",
                "Save something you may want to buy later.",
            )

            st.write("")

            with st.form(
                "add_wishlist_form",
                clear_on_submit=True,
            ):

                item_name = st.text_input(
                    "Item Name",
                    placeholder="Example: Pink satin heels",
                )

                form_column1, form_column2 = st.columns(2)

                with form_column1:

                    category = st.selectbox(
                        "Category",
                        [
                            "Top",
                            "Bottom",
                            "Dress",
                            "Shoes",
                            "Outerwear",
                            "Bag",
                            "Accessory",
                            "Other",
                        ],
                    )

                    color = st.text_input(
                        "Color",
                        placeholder="Example: Blush pink",
                    )

                    store_name = st.text_input(
                        "Store or Brand",
                        placeholder="Example: Revolve",
                    )

                with form_column2:

                    price = st.number_input(
                        "Price",
                        min_value=0.0,
                        value=0.0,
                        step=1.0,
                        format="%.2f",
                    )

                    priority = st.selectbox(
                        "Priority",
                        [
                            "Low",
                            "Medium",
                            "High",
                            "Dream Item",
                        ],
                    )

                    item_link = st.text_input(
                        "Item Link",
                        placeholder="Paste the shopping link",
                    )

                notes = st.text_area(
                    "Notes",
                    placeholder=(
                        "What would you wear this with? "
                        "Why do you want it?"
                    ),
                )

                wishlist_image = st.file_uploader(
                    "Reference Photo",
                    type=["jpg", "jpeg", "png"],
                    key="wishlist_image_uploader",
                )

                save_wishlist_item = st.form_submit_button(
                    "Add to Wishlist",
                    use_container_width=True,
                )

                if save_wishlist_item:

                    if item_name.strip() == "":

                        st.error(
                            "Please enter an item name."
                        )

                    else:

                        try:

                            image_path = save_wishlist_image(
                                wishlist_image
                            )

                            saved_price = (
                                price
                                if price > 0
                                else None
                            )

                            add_wishlist_item(
                                item_name=item_name.strip(),
                                category=category,
                                color=color.strip(),
                                store_name=store_name.strip(),
                                price=saved_price,
                                item_link=item_link.strip(),
                                priority=priority,
                                notes=notes.strip(),
                                image_path=image_path,
                            )

                            st.success(
                                f"{item_name.strip()} was added "
                                "to your wishlist!"
                            )

                        except Exception as error:

                            st.error(
                                f"The item could not be saved: {error}"
                            )

    # --------------------------------------------------
    # ACTIVE WISHLIST
    # --------------------------------------------------

    with wishlist_tab:

        wishlist_items = get_wishlist_items()

        active_items = [
            item
            for item in wishlist_items
            if item[10] == 0
        ]

        if len(active_items) == 0:

            st.info(
                "Your wishlist is empty."
            )

        else:

            filter_column1, filter_column2 = st.columns(2)

            with filter_column1:

                category_filter = st.selectbox(
                    "Filter by Category",
                    [
                        "All",
                        "Top",
                        "Bottom",
                        "Dress",
                        "Shoes",
                        "Outerwear",
                        "Bag",
                        "Accessory",
                        "Other",
                    ],
                    key="wishlist_category_filter",
                )

            with filter_column2:

                priority_filter = st.selectbox(
                    "Filter by Priority",
                    [
                        "All",
                        "Low",
                        "Medium",
                        "High",
                        "Dream Item",
                    ],
                    key="wishlist_priority_filter",
                )

            filtered_wishlist = []

            for item in active_items:

                category = item[2]
                priority = item[7]

                matches_category = (
                    category_filter == "All"
                    or category == category_filter
                )

                matches_priority = (
                    priority_filter == "All"
                    or priority == priority_filter
                )

                if (
                    matches_category
                    and matches_priority
                ):
                    filtered_wishlist.append(item)

            st.caption(
                f"{len(filtered_wishlist)} wishlist items"
            )

            st.write("")

            if len(filtered_wishlist) == 0:

                st.warning(
                    "No wishlist items match those filters."
                )

            else:

                wishlist_columns = st.columns(
                    3,
                    gap="medium",
                )

                for index, item in enumerate(
                    filtered_wishlist
                ):

                    wishlist_id = item[0]

                    with wishlist_columns[index % 3]:

                        render_wishlist_card(item)

                        if st.button(
                            "Mark as Purchased",
                            key=f"purchase_wishlist_{wishlist_id}",
                            use_container_width=True,
                        ):

                            update_wishlist_purchase_status(
                                wishlist_id,
                                True,
                            )

                            st.rerun()

                        if st.button(
                            "Delete",
                            key=f"delete_wishlist_{wishlist_id}",
                            use_container_width=True,
                        ):

                            delete_wishlist_item(
                                wishlist_id
                            )

                            st.rerun()

    # --------------------------------------------------
    # PURCHASED ITEMS
    # --------------------------------------------------

    with purchased_tab:

        wishlist_items = get_wishlist_items()

        purchased_items = [
            item
            for item in wishlist_items
            if item[10] == 1
        ]

        if len(purchased_items) == 0:

            st.info(
                "You have not marked any items as purchased."
            )

        else:

            purchased_columns = st.columns(
                3,
                gap="medium",
            )

            for index, item in enumerate(
                purchased_items
            ):

                wishlist_id = item[0]

                with purchased_columns[index % 3]:

                    render_wishlist_card(item)

                    if st.button(
                        "Move Back to Wishlist",
                        key=f"restore_wishlist_{wishlist_id}",
                        use_container_width=True,
                    ):

                        update_wishlist_purchase_status(
                            wishlist_id,
                            False,
                        )

                        st.rerun()

                    if st.button(
                        "Delete",
                        key=f"delete_purchased_{wishlist_id}",
                        use_container_width=True,
                    ):

                        delete_wishlist_item(
                            wishlist_id
                        )

                        st.rerun()

# --------------------------------------------------
# CLOSET RENO
# --------------------------------------------------

elif page == "Closet Reno":

    st.title("Closet Reno")

    st.write(
        "Renovate each room of your digital closet with "
        "your own wallpaper."
    )

    customizable_pages = [
        "Dashboard",
        "Add Item",
        "My Closet",
        "Outfit Builder",
        "Inspiration",
        "Outfit Calendar",
        "Wishlist",
    ]

    selected_page = st.selectbox(
        "Choose a room to renovate",
        customizable_pages,
    )

    st.subheader(selected_page)

    current_background = get_page_background(
        selected_page
    )

    if (
        current_background
        and os.path.exists(current_background)
    ):

        st.caption("Current wallpaper")

        st.image(
            current_background,
            use_container_width=True,
        )

        if st.button(
            "Remove Wallpaper",
            key=f"remove_background_{selected_page}",
        ):

            remove_page_background(selected_page)

            st.success(
                "Wallpaper removed."
            )

            st.rerun()

    else:

        st.info(
            "This room does not have a custom wallpaper yet."
        )

    uploaded_background = st.file_uploader(
        "Drag and drop a wallpaper",
        type=["jpg", "jpeg", "png"],
        key=f"background_upload_{selected_page}",
    )

    if uploaded_background is not None:

        st.caption("New wallpaper preview")

        st.image(
            uploaded_background,
            use_container_width=True,
        )

        if st.button(
            "Save Wallpaper",
            key=f"save_background_{selected_page}",
        ):

            old_background = get_page_background(
                selected_page
            )

            new_background = save_background_image(
                uploaded_background,
                selected_page,
            )

            save_page_background(
                selected_page,
                new_background,
            )

            if (
                old_background
                and old_background != new_background
                and os.path.exists(old_background)
            ):
                os.remove(old_background)

            st.success(
                f"{selected_page} has been renovated!"
            )

            st.rerun()
