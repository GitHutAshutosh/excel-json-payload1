import streamlit as st
import pandas as pd
import json

# --- Page Configuration ---
st.set_page_config(page_title="Excel to JSON Converter", layout="centered")

# --- Theme Styling ---
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"], index=0)

if theme == "Dark":
    st.markdown("""
    <style>
    body, .main, .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .password-box, .sidebar .sidebar-content {
        background-color: #2c2c2c;
        color: #ffffff;
    }
    .toggle-status {
        color: #81c784;
    }
    footer {
        color: #aaa;
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
    .password-box, .sidebar .sidebar-content {
        background-color: #ffffff;
        color: #000000;
    }
    .toggle-status {
        color: #1b5e20;
    }
    footer {
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Password Protection ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="password-box">', unsafe_allow_html=True)
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
st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("📊 Excel to JSON Payload Converter")

uploaded_file = st.file_uploader("📁 Upload your Excel file", type=["xlsx"])

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
