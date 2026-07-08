import streamlit as st
import json
import random
import os

# Konfiguration
st.set_page_config(page_title="Wappen-Quiz", page_icon="🛡️")

# Hilfsfunktion für den Vergleich (ignoriert Umlaute und Groß-/Kleinschreibung)
def normalize_string(s):
    s = s.strip().lower()
    s = s.replace("ü", "ue").replace("ö", "oe").replace("ä", "ae").replace("ß", "ss")
    return s

# Daten laden und NUR Bilder verwenden, die im Hauptverzeichnis existieren
def load_and_filter_data():
    if not os.path.exists("wappen.json"):
        return None
    
    with open("wappen.json", "r", encoding="utf-8") as f:
        all_data = json.load(f)
    
    valid_data = []
    for item in all_data:
        # Dateiname aus JSON nehmen
        basis_name = os.path.splitext(item['image_file'])[0]
        # Suche direkt im aktuellen Ordner (Root)
        image_path = basis_name + ".png"
        
        # Nur aufnehmen, wenn die Datei auch physisch existiert
        if os.path.exists(image_path):
            valid_data.append(item)
            
    return valid_data

# Initialisierung
if 'data' not in st.session_state:
    st.session_state.data = load_and_filter_data()
    st.session_state.score = 0

# Fehlerbehandlung
if st.session_state.data is None or len(st.session_state.data) == 0:
    st.error("Fehler: Keine gültigen Bilder gefunden.")
    st.write("Bitte prüfe, ob die .png Dateien direkt neben der app.py liegen.")
    st.stop()

if 'current' not in st.session_state:
    st.session_state.current = random.choice(st.session_state.data)

# UI
st.title("🛡️ Wappen-Quiz")
st.write(f"### Aktueller Punktestand: {st.session_state.score}")

# Bild laden
basis_name = os.path.splitext(st.session_state.current['image_file'])[0]
image_path = basis_name + ".png"

# Bild anzeigen
st.image(image_path, width=300)

st.write("---")

# Eingabe
answer = st.text_input("Welche Stadt ist das?")

if st.button("Antwort prüfen"):
    input_norm = normalize_string(answer)
    target_norm = normalize_string(st.session_state.current['name'])
    
    if input_norm == target_norm:
        st.success(f"Richtig! Das ist {st.session_state.current['name']}! 🎉")
        st.session_state.score += 1
        st.session_state.current = random.choice(st.session_state.data)
        st.rerun()
    else:
        st.error("Leider falsch!")

if st.button("Nächste Frage"):
    st.session_state.current = random.choice(st.session_state.data)
    st.rerun()
