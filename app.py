
# Streamlit app with glow effect on "Map column" labels in dark mode
import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Excel to JSON Converter", layout="centered")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <style>
    .qa-banner { text-align: center; font-size: 28px; font-weight: 800; color: #1976d2; }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="qa-banner">QA TEAM</div>', unsafe_allow_html=True)
    password = st.text_input("Type your Access Password", type="password")
    if password == "Ashutosh@79836666":
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.error("Incorrect password")
    st.stop()

# Theme toggle
theme = st.sidebar.radio("Theme", ["Light", "Dark"], index=0)
st.session_state.theme = theme

# Apply theme styles
if theme == "Dark":
    st.markdown("""
    <style>
    body, .main, .stApp { background-color: #121212; color: #e0e0e0; }
    .qa-banner { color: #ffeb3b; text-shadow: 0 0 8px #ffeb3b; }
    .map-columns-title {
        color: #64b5f6;
        text-shadow: 0 0 8px #64b5f6, 0 0 16px rgba(100,181,246,.55);
        font-weight: 800;
        margin: 8px 0 6px;
    }
    .map-label {
        font-weight: 600;
        color: #90caf9;
        text-shadow: 0 0 6px #90caf9;
        margin-top: 12px;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .map-columns-title { color: #0d47a1; font-weight: 800; margin: 8px 0 6px; }
    .map-label { font-weight: 600; color: #0d47a1; margin-top: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="qa-banner">QA TEAM</div>', unsafe_allow_html=True)
st.title("Excel to JSON Payload Converter")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file, engine="openpyxl")
    sheet_names = xls.sheet_names
    first_sheet = sheet_names[0] if sheet_names else "Sheet1"
    df = xls.parse(first_sheet)
    df = df.fillna("null").astype(str)

    st.subheader("Preview Excel Data")
    st.dataframe(df.head(10), use_container_width=True)

    st.markdown("<h3 class='map-columns-title'>🛠️ Optional: Map Columns to JSON Keys</h3>", unsafe_allow_html=True)
    column_mapping = {}
    for col in df.columns:
        st.markdown(f"<div class='map-label'>Map column '<strong>{col}</strong>' to JSON key</div>", unsafe_allow_html=True)
        new_key = st.text_input("", value=col, key=f"map_{col}")
        column_mapping[col] = new_key

    df = df.rename(columns=column_mapping)
    payload = df.to_dict(orient="records")

    st.subheader("Converted JSON Payload")
    st.json(payload)

    json_bytes = json.dumps(payload, indent=4).encode("utf-8")
    st.download_button("Download JSON", data=json_bytes, file_name="output.json", mime="application/json")

    if st.button("Clear Uploaded File"):
        st.session_state.clear()
        st.rerun()
