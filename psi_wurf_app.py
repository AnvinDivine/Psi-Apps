import streamlit as st
import itertools
import pandas as pd

st.title("PSI-Wurf Optimierer")

st.markdown("""
**Wähle deine Eingaben:**
- Wie viele Würfel hast du zur Verfügung?
- Wie schwierig ist die PSI-Anwendung?
- Wie viele Kraftstufen möchtest du erreichen?
""")

wuerfelanzahl = st.slider("Würfelanzahl", min_value=3, max_value=15, value=11)
schwierigkeit = st.selectbox("Schwierigkeit", ["Leicht", "Mittel", "Schwer", "Ultimativ"])
kraftstufe_wunsch = st.slider("Gewünschte Kraftstufen", min_value=1, max_value=6, value=2)

zielbereiche = {
    "Leicht": (8, 12),
    "Mittel": (11, 15),
    "Schwer": (15, 19),
    "Ultimativ": (23, 25)
}
ziel_min, ziel_max = zielbereiche[schwierigkeit]

def erfolgswahrscheinlichkeit(wurfanzahl, z_min, z_max):
    erfolg = 0
    total = 0
    for wurf in itertools.product(range(1, 7), repeat=wurfanzahl):
        if any(z_min <= w <= z_max for w in wurf):
            erfolg += 1
        total += 1
    return round(erfolg / total * 100, 2)

resultate = []
for ziel_erw in range(0, 5):
    verbleibend = wuerfelanzahl - kraftstufe_wunsch - ziel_erw
    if verbleibend < 1:
        continue
    zmin = ziel_min - ziel_erw
    zmax = ziel_max + ziel_erw
    wahrscheinlichkeit = erfolgswahrscheinlichkeit(verbleibend, zmin, zmax)
    resultate.append({
        "Zielerweiterung": ziel_erw,
        "Würfel für Wurf": verbleibend,
        "Zielbereich": f"{zmin}-{zmax}",
        "Erfolgswahrscheinlichkeit (%)": wahrscheinlichkeit
    })

if resultate:
    df = pd.DataFrame(resultate).sort_values(by="Erfolgswahrscheinlichkeit (%)", ascending=False)
    st.subheader("Beste Optionen:")
    st.dataframe(df.reset_index(drop=True))
else:
    st.warning("Nicht genug Würfel für diese Kombination.")
