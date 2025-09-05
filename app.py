import streamlit as st
import pandas as pd
import json

# --- Page Configuration ---
st.set_page_config(page_title="Excel to JSON Converter", layout="centered")

# --- Password Protection ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    # Moving Payload Converter Line (only on password page)
    st.markdown("""
    <style>
    .marquee {
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
        font-size: 24px;
        font-weight: bold;
        color: #2196f3;
        animation: marquee 10s linear infinite;
        padding: 10px 0;
        text-align: center;
        margin-top: -10px;
    }
    @keyframes marquee {
        0%   { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    </style>
    <div class="marquee">🚀 Payload Converter</div>
    """, unsafe_allow_html=True)

    # Styling for password box and input
    st.markdown("""
    <style>
    body, .stApp {
        background-color: #f5f5f5;
        color: #000;
    }
    .qa-banner {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #1976d2;
        margin-bottom: 0px;
    }
    .password-box {
        background-color: #e3f2fd;
        padding: 25px;
        border-radius: 10px;
        border: 2px solid #2196f3;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: -10px;
    }
    .stTextInput > div > input {
        font-size: 18px !important;
        padding: 10px !important;
        border: 2px solid #2196f3 !important;
        border-radius: 5px !important;
        color: #000 !important;
        background-color: #ffffff !important;
    }
    footer {
        font-size: 16px;
        color: #555;
        margin-top: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="qa-banner">QA TEAM</div>', unsafe_allow_html=True)
    st.subheader("👋 Welcome!")
    st.header("🔐 Secure Access")
    password = st.text_input("Type your Access Password", type="password")
    if password == "Ashutosh@79836666":
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.error("❌ Incorrect password. Please try again.")
    st.markdown('<footer>Developed by Ashutosh Rana ❤️</footer>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- Theme Toggle ---
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"], index=0)
st.session_state.theme = theme

# --- Apply Theme Styling ---
if theme == "Dark":
    st.markdown("""
    <style>
    body, .main, .stApp {
        background-color: #121212;
        color: #e0e0e0;
    }
    .sidebar .sidebar-content {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    .toggle-status {
        color: #81c784;
    }
    .stTextInput > div > input {
        background-color: #2c2c2c;
        color: #e0e0e0;
    }
    .stDownloadButton button {
        background-color: #333;
        color: #fff;
    }
    footer {
        color: #aaa;
    }
    .qa-banner {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #ffeb3b;
        text-shadow: 0 0 8px #ffeb3b;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    body, .main, .stApp {
        background-color: #f5f5f5;
        color: #000000;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        color: #000000;
    }
    .toggle-status {
        color: #1b5e20;
    }
    footer {
        color: #555;
    }
    .qa-banner {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #1976d2;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    with st.expander("⚙️ GCR Settings", expanded=False):
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        enable_impact = st.toggle("🔄 Enable GCR Service Impact", value=False, key="impact_toggle")
        if enable_impact:
            st.markdown('<div class="toggle-status">✅ Impact Enabled</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="toggle-status">❌ Impact Disabled</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔓 Logout"):
        st.session_state.authenticated = False
        st.rerun()

# --- Main App ---
st.markdown('<div class="qa-banner">QA TEAM</div>', unsafe_allow_html=True)
st.title("📊 Excel to JSON Payload Converter")

# --- Upload Section ---
if theme == "Dark":
    st.markdown("""
    <div style="border-top: 1px solid white; margin-top: 30px; padding-top: 10px;">
        <h4 style='color: #64b5f6;'>📁 Upload your Excel file</h4>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="border-top: 1px solid #ccc; margin-top: 30px; padding-top: 10px;">
        <h4 style='color: #000;'>📁 Upload your Excel file</h4>
    </div>
    """, unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        st.stop()

    df = df.fillna("null").astype(str)

    st.subheader("🔍 Preview Excel Data")
    st.dataframe(df.head(10), use_container_width=True)

    if enable_impact:
        expected_columns = {
            "SID": "sid", "Alt SID": "altSid", "Busorg ID": "busorgId", "Busorg Name": "busorgName",
            "Protection": "protection", "Bandwidth": "bandwidth", "Product": "product",
            "Product Family": "productFamily", "A End CLLI": "getaEndClli", "Z End CLLI": "getzEndClli",
            "TSP Code": "tspCode", "Affected Object Name": "afftectedObjectName", "Order Number": "orderNum",
            "Alt Acct Id": "altAcctId", "Alt Acct Type": "altAcctType", "Notification Name": "notificationName"
        }

        df = df.rename(columns={k: v for k, v in expected_columns.items() if k in df.columns})
        for original_col, new_col in expected_columns.items():
            if new_col not in df.columns:
                df[new_col] = "null"

        def clean_row(row):
            if pd.isna(row.get("busorgId")) or str(row["busorgId"]).lower().startswith("null") or row["busorgId"].isnumeric():
                row["busorgId"] = "1-E9U2L"
            if row.get("sid", "").isnumeric():
                row["sid"] = "1-E9U2L"
            row["protection"] = row["protection"].lower() == "true"
            for field in ["altAcctId", "orderNum", "tspCode"]:
                try:
                    row[field] = int(row[field]) if row[field] != "null" else "null"
                except:
                    row[field] = "null"
            return {k: v if isinstance(v, (bool, int)) else v for k, v in row.items()}

        impacts = [clean_row(row) for _, row in df.iterrows()]
        payload = {"importGcrImpactsRequest": {"impacts": impacts}}
    else:
        st.subheader("🛠️ Optional: Map Columns to JSON Keys")
        column_mapping = {}
        for col in df.columns:
            new_key = st.text_input(f"Map column '{col}' to JSON key", value=col)
            column_mapping[col] = new_key
        df = df.rename(columns=column_mapping)
        payload = df.to_dict(orient="records")

    st.subheader("📥 Converted JSON Payload")
    st.json(payload)

    try:
        json_bytes = json.dumps(payload, indent=4).encode("utf-8")
        st.download_button("📥 Download JSON", data=json_bytes, file_name="output.json", mime="application/json")
    except Exception as e:
        st.error(f"Error generating JSON: {e}")

    if st.button("🧹 Clear Uploaded File"):
        st.session_state.clear()
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
