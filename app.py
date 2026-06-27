import streamlit as st
import json
import os

#Citire stickere din .json
with open("stickere.json", "r", encoding="utf-8") as f:
    stickere_data = json.load(f)

#Progres in .json
FISIER_PROGRES = "progres.json"

if os.path.exists(FISIER_PROGRES):
    with open(FISIER_PROGRES, "r") as f:
        progres = json.load(f)
else:
    progres = {}

#Interfata
st.title("Catalog Panini WC 2026 ")

total_stickere = 0
total_colectate = 0

for echipa, stickere in stickere_data.items():
    st.subheader(echipa)
    cols = st.columns(4)
    col_idx = 0

    for cod in stickere:
        if cod not in progres:
            progres[cod] = False
        with cols[col_idx % 4]:
            bifare = st.checkbox(cod, value=progres[cod], key=cod)
            progres[cod] = bifare
            if bifare:
                total_colectate += 1
        col_idx += 1
        total_stickere += 1

        
#Contorizare
st.divider()
st.metric("Total colectate", f"{total_colectate} / {total_stickere}")

#Salvare progres
with open(FISIER_PROGRES, "w") as f:
    json.dump(progres, f)