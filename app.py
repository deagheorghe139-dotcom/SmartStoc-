import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configurare pagină
st.set_page_config(page_title="SmartStoc AI", page_icon="📊", layout="wide")

st.title("📊 SmartStoc AI - Management Independent de Stoc")
st.write("Soluție securizată pentru magazine. Nu necesită conectare la serverele centrale.")

# Inițializare bază de date locală în memoria browserului
if "produse" not in st.session_state:
    st.session_state.produse = [
        {"id": 1, "nume": "Iaurt Natural", "cantitate": 12, "pret": 4.29, "expirare": (datetime.today() + timedelta(days=2)).strftime("%Y-%m-%d")},
        {"id": 2, "nume": "Lapte UHT", "cantitate": 15, "pret": 6.49, "expirare": (datetime.today() + timedelta(days=15)).strftime("%Y-%m-%d")},
        {"id": 3, "nume": "Brânză Fresh", "cantitate": 8, "pret": 12.50, "expirare": (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")},
    ]

# --- PANOU 1: ADAUGĂ PRODUSE (Magazinul își face singur baza de date) ---
st.header("📥 Adaugă Produs Nou în Sistem")
col1, col2, col3, col4 = st.columns(4)

with col1:
    nou_nume = st.text_input("Nume produs (ex: Glob de Zăpadă)", key="nume")
with col2:
    nou_cantitate = st.number_input("Cantitate", min_value=1, value=10, key="cant")
with col3:
    nou_pret = st.number_input("Preț (RON)", min_value=0.1, value=5.99, key="pret_prod")
with col4:
    noua_expirare = st.date_input("Dată expirare", datetime.today() + timedelta(days=7), key="exp")

if st.button("➕ Salvează Produsul în Stoc"):
    if nou_nume:
        nou_id = len(st.session_state.produse) + 1
        st.session_state.produse.append({
            "id": nou_id,
            "nume": nou_nume,
            "cantitate": nou_cantitate,
            "pret": nou_pret,
            "expirare": noua_expirare.strftime("%Y-%m-%d")
        })
        st.success(f"Produsul '{nou_nume}' a fost adăugat cu succes!")
    else:
        st.error("Te rog introdu numele produsului!")

st.markdown("---")

# --- PANOU 2: ALERTE CRITICE (Ce expira repede) ---
st.header("⚠️ Alerte Termen Expirare")
astazi = datetime.today().date()
alerte_critice = []
alerte_atentie = []

for p in st.session_state.produse:
    data_exp = datetime.strptime(p["expirare"], "%Y-%m-%d").date()
    zile_ramase = (data_exp - astazi).days
    
    if zile_ramase < 0:
        alerte_critice.append(f"❌ [EXPIRAT] {p['nume']} - Expirat de {abs(zile_ramase)} zile!")
    elif zile_ramase <= 3:
        alerte_critice.append(f"🚨 [CRITIC] {p['nume']} - Expiră în {zile_ramase} zile! Propune reducere -30%!")
    elif zile_ramase <= 7:
        alerte_atentie.append(f"🔍 [ATENȚIE] {p['nume']} - Expiră în {zile_ramase} zile.")

if alerte_critice:
    for alerta in alerte_critice:
        st.error(alerta)
if alerte_atentie:
    for alerta in alerte_atentie:
        st.warning(alerta)
if not alerte_critice and not alerte_atentie:
    st.success("✅ Toate produsele sunt în termen regulamentar!")

st.markdown("---")

# --- PANOU 3: RAPOARTE ȘI TABEL STOC ---
st.header("📊 Rapoarte & Stoc Actual")
df = pd.DataFrame(st.session_state.produse)

col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1:
    st.metric("Total Produse în Stoc", int(df["cantitate"].sum()))
with col_stat2:
    st.metric("Tipuri Unice de Produse", len(df))
with col_stat3:
    st.metric("Valoare Totală Stoc (RON)", f"{(df['cantitate'] * df['pret']).sum():.2f} lei")

# Afișare tabel
st.dataframe(df[["id", "nume", "cantitate", "pret", "expirare"]], use_container_width=True)
