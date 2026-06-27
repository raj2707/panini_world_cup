import streamlit as st
import json
import os

# All the stickers
with open("stickere.json", "r", encoding="utf-8") as f:
    stickers_data = json.load(f)

# Progress
FILE_PROGRESS = "progres.json"

if os.path.exists(FILE_PROGRESS):
    with open(FILE_PROGRESS, "r") as f:
        progress = json.load(f)
else:
    progress = {}

#Interface
st.title("Panini WC 2026 ")

total_stickers = 0
total_collected = 0

for team, stickers in stickers_data.items():
    st.subheader(team)
    cols = st.columns(4)
    col_idx = 0

    for cod in stickers:
        if cod not in progress:
            progress[cod] = False
        with cols[col_idx % 4]:
            check = st.checkbox(cod, value=progress[cod], key=cod)
            progress[cod] = check
            if check:
                total_collected += 1
        col_idx += 1
        total_stickers += 1


# Accccounting
st.divider()
st.metric("Total colectate", f"{total_collected} / {total_stickers}")

# Saving the progress
with open(FILE_PROGRESS, "w") as f:
    json.dump(progress, f)