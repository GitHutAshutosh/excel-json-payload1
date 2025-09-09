import streamlit as st
import pandas as pd
import json

# --- Page Configuration ---
st.set_page_config(page_title="Excel to JSON Converter", layout="centered")

# --- Password Protection ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
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
        margin-top: -6px;
    }
    @keyframes marquee {
        0%   { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .qa-banner {
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        color: #1976d2;
        letter-spacing: .5px;
        margin: 2px 0 6px 0;
    }
    .auth { margin-top: -8px; }
    .auth .stTextInput { max-width: 520px; margin: 2px auto 8px auto; }
    .auth label {
        font-weight: 600 !important;
        color: #0d47a1 !important;
    }
    .auth .stTextInput input {
        font-size: 18px !important;
        padding: 12px 14px !important;
        border: 2px solid #1e88e5 !important;
        border-radius: 12px !important;
        background: #ffffff !important;
        color: #0a0a0a !important;
        box-shadow: 0 8px 20px rgba(30,136,229,.08), 0 0 0 3px rgba(30,136,229,.12) !important;
        transition: box-shadow .2s ease, border-color .2s ease !important;
    }
    .auth .stTextInput input:focus,
    .auth .stTextInput input:not(:placeholder-shown) {
        outline: none !important;
        border-color: #43a047 !important;
        box-shadow: 0 10px 24px rgba(67,160,71,.15), 0 0 0 4px rgba(67,160,71,.14) !important;
    }
    .app-footer {
        margin-top: 18px;
        text-align: center;
        color: #666;
        font-size: 14px;
    }
    .app-footer .divider {
        height: 1px;
        width: 160px;
        margin: 12px auto 8px;
        background: linear-gradient(90deg, transparent, #bbb, transparent);
        border-radius: 1px;
    }
    .app-footer .meta {
        font-size: 13px;
        color: #555;
    }
    </style>
    <div class="marquee">🚀 Payload Converter</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="qa-banner">QA TEAM</div>', unsafe_allow_html=True)
    st.subheader("👋 Welcome!")
    st.header("🔐 Secure Access")

    password = st.text_input("Type your Access Password", type="password", placeholder="Enter your password")

    if password == "Ashutosh@79836666":
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.error("❌ Incorrect password. Please try again.")

    st.markdown("""
        <div class="app-footer">
            <div class="divider"></div>
            <div class="meta">© 2025 <strong>QA TEAM</strong> • Developed by <strong>Ashutosh Rana</strong> ❤️ • v1.0</div>
        </div>
    """, unsafe_allow_html=True)

    st.stop()

# --- Theme Toggle ---
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"], index=0)
st.session_state.theme = theme

# --- Sidebar ---
with st.sidebar:
    with st.expander("⚙️ GCR Settings", expanded=False):
        enable_impact = st.toggle("🔄 Enable GCR Service Impact", value=False, key="impact_toggle")
        st.markdown(f"<div class='toggle-status'>{'✅ Impact Enabled' if enable_impact else '❌ Impact Disabled'}</div>", unsafe_allow_html=True)

    if st.button("🔓 Logout"):
        st.session_state.authenticated = False
        st.rerun()

# --- Main App ---
st.markdown('<div class="qa-banner">QA TEAM</div>', unsafe_allow_html=True)
st.title("📊 Excel to JSON Payload Converter")

uploaded_file = st.file_uploader("", type=["xlsx"])

if uploaded_file:
    st.markdown(f"<div class='file-name-glow'>📁 Uploaded File: <strong>{uploaded_file.name}</strong></div>", unsafe_allow_html=True)
    try:
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
        first_sheet = sheet_names[0] if sheet_names else "Sheet1"
        df = xls.parse(first_sheet)
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        st.stop()

    st.markdown(f"<div class='sheet-badge'>📄 Sheet: <strong>{first_sheet}</strong></div>", unsafe_allow_html=True)

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
            if pd.isna(row.get("busorgId")) or str(row["busorgId"]).lower().startswith("null") or str(row["busorgId"]).isnumeric():
                row["busorgId"] = "1-E9U2L"
            if str(row.get("sid", "")).isnumeric():
                row["sid"] = "1-E9U2L"
            row["protection"] = str(row["protection"]).lower() == "true"
            for field in ["altAcctId", "orderNum", "tspCode"]:
                try:
                    row[field] = int(row[field]) if row[field] != "null" else "null"
                except Exception:
                    row[field] = "null"
            return {k: v if isinstance(v, (bool, int)) else v for k, v in row.items()}

        impacts = [clean_row(row) for _, row in df.iterrows()]
        payload = {"importGcrImpactsRequest": {"impacts": impacts}}
    else:
        st.markdown("<h3 class='map-columns-title'>🛠️ Optional: Map Columns to JSON Keys</h3>", unsafe_allow_html=True)
        column_mapping = {}
        for col in df.columns:
            new_key = st.text_input(f"Map column '{col}' to JSON key", value=col, key=f"map_{col}")
            column_mapping[col] = new_key
        df = df.rename(columns=column_mapping)
        payload = df.to_dict(orient="records")
        if isinstance(payload, list) and len(payload) == 1:
            payload = payload[0]

    st.subheader("📥 Converted JSON Payload")
    st.json(payload)

    try:
        json_bytes = json.dumps(payload, indent=4).encode("utf-8")
        st.download_button("📥 Download JSON", data=json_bytes, file_name="output.json", mime="application/json")
    except Exception as e:
        st.error(f"Error generating JSON: {e}")

    st.markdown("### 🧪 Validate JSON Input")
    input_text = st.text_area("Paste JSON or text to validate", height=200)
    if input_text:
        col1, col2 = st.columns(2)
        with col1:
            try:
                json.loads(input_text)
                st.success("✅ No errors found in input.")
            except Exception as e:
                st.error(f"❌ Error in input: {e}")
        with col2:
            try:
                parsed = json.loads(input_text)
                st.json(parsed)
            except:
                st.warning("⚠️ Cannot display JSON due to errors.")

    if st.button("🧹 Clear Uploaded File"):
        st.session_state.clear()
        st.rerun()
else:
    st.markdown("""
    <div style="border-top: 1px solid #ccc; margin-top: 30px; padding-top: 10px;">
        <h4 style='color: #000;'>📁 Upload your Excel file</h4>
    </div>
    """, unsafe_allow_html=True)
