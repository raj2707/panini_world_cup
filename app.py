import streamlit as st
import json
from supabase import create_client

# --- Conexiune Supabase ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)


# --- Citim stickerele ---
with open("stickere.json", "r", encoding="utf-8") as f:
    stickere_data = json.load(f)

# --- Utilizator ---
st.title("Catalog Panini WC 2026 🌍")

utilizator = st.text_input("Numele tău:", placeholder="ex: raj")

if not utilizator:
    st.info("Introdu numele tău.")
    st.stop()

# --- Citim progresul din Supabase ---
rezultat = supabase.table("progres").select("*").eq("utilizator", utilizator).execute()
progres = {row["cod_sticker"]: row["colectat"] for row in rezultat.data}

# --- Filtru ---
filtru = st.radio("Afișează:", ["All", "Collected", "Missing"], horizontal=True)

# --- Afișare stickere ---
total_stickere = 0
total_colectate = 0
modificari = []

for echipa, stickere in stickere_data.items():
    st.subheader(echipa)
    cols = st.columns(4)
    col_idx = 0

    for cod in stickere:
        valoare_curenta = progres.get(cod, False)

        if filtru == "Collected" and not valoare_curenta:
            total_stickere += 1
            continue
        if filtru == "Missing" and valoare_curenta:
            total_stickere += 1
            if valoare_curenta:
                total_colectate += 1
            continue

        with cols[col_idx % 4]:
            bifare_noua = st.checkbox(cod, value=valoare_curenta, key=cod)

        if bifare_noua != valoare_curenta:
            modificari.append({
                "utilizator": utilizator,
                "cod_sticker": cod,
                "colectat": bifare_noua
            })
            progres[cod] = bifare_noua

        if progres.get(cod, False):
            total_colectate += 1

        col_idx += 1
        total_stickere += 1

# --- Salvare modificari ---
if modificari:
    supabase.table("progres").upsert(modificari).execute()

# --- Contor ---
st.divider()
st.metric("Total colectate", f"{total_colectate} / {total_stickere}")