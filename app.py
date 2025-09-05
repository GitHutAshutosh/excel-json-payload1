import streamlit as st
import pandas as pd
import json

# --- Page Configuration ---
st.set_page_config(page_title="Excel to JSON Converter", layout="wide")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
    }
    .password-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Password Protection ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="password-box">', unsafe_allow_html=True)
    st.header("🔐 Secure Access")
    password = st.text_input("Enter password to access the app", type="password")
    if password == "Ashutosh@79836666":
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.error("❌ Incorrect password. Please try again.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- Sidebar Toggle ---
with st.sidebar:
    st.header("⚙️ Settings")
    enable_impact = st.toggle("Enable GCR Service Impact", value=False, key="impact_toggle")
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

# --- Main App ---
st.markdown('<div class="main">', unsafe_allow_html=True)
st.title("📊 Excel to JSON Payload Converter")

# --- File Upload ---
uploaded_file = st.file_uploader("📁 Upload your Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        st.stop()

    df = df.fillna("null").astype(str)

    if enable_impact:
        # --- Expected Columns and Mapping ---
        expected_columns = {
            "SID": "sid",
            "Alt SID": "altSid",
            "Busorg ID": "busorgId",
            "Busorg Name": "busorgName",
            "Protection": "protection",
            "Bandwidth": "bandwidth",
            "Product": "product",
            "Product Family": "productFamily",
            "A End CLLI": "getaEndClli",
            "Z End CLLI": "getzEndClli",
            "TSP Code": "tspCode",
            "Affected Object Name": "afftectedObjectName",
            "Order Number": "orderNum",
            "Alt Acct Id": "altAcctId",
            "Alt Acct Type": "altAcctType",
            "Notification Name": "notificationName"
        }

        # Rename columns if they exist
        df = df.rename(columns={k: v for k, v in expected_columns.items() if k in df.columns})

        # Add missing columns with default value "null"
        for original_col, new_col in expected_columns.items():
            if new_col not in df.columns:
                df[new_col] = "null"

        # --- Row Cleaning Function for Impact Format ---
        def clean_row(row):
            if row.get("busorgId", "").upper().startswith("NULL") or row["busorgId"].isnumeric():
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
        payload = df.to_dict(orient="records")

    # --- Display and Download ---
    st.subheader("📥 Converted JSON Payload")
    st.json(payload)

    json_bytes = json.dumps(payload, indent=4).encode("utf-8")
    st.download_button("Download JSON", data=json_bytes, file_name="output.json", mime="application/json")

st.markdown('</div>', unsafe_allow_html=True)
