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
        margin-top: -6px;
    }
    @keyframes marquee {
        0%   { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* Global page base for password screen */
    body, .stApp { background-color: #f5f5f5; color: #000; }

    /* QA TEAM heading */
    .qa-banner {
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        color: #1976d2;
        letter-spacing: .5px;
        margin: 2px 0 6px 0;
    }

    /* Auth area tweaks (move a bit upward, center the field) */
    .auth { margin-top: -8px; }
    .auth .stTextInput { max-width: 520px; margin: 2px auto 8px auto; }

    /* Make the "Type your Access Password" label clearer */
    .auth label {
        font-weight: 600 !important;
        color: #0d47a1 !important;
    }

    /* DEFAULT STATE — highlight BEFORE typing/clicking */
    .auth .stTextInput input {
        font-size: 18px !important;
        padding: 12px 14px !important;
        border: 2px solid #1e88e5 !important;       /* blue border by default */
        border-radius: 12px !important;
        background: #ffffff !important;
        color: #0a0a0a !important;
        /* subtle blue glow by default to make it stand out before typing */
        box-shadow:
            0 8px 20px rgba(30,136,229,.08),
            0 0 0 3px rgba(30,136,229,.12) !important;
        transition: box-shadow .2s ease, border-color .2s ease !important;
    }

    /* FOCUS or HAS VALUE — change to green accent once user interacts/types */
    .auth .stTextInput input:focus,
    .auth .stTextInput input:not(:placeholder-shown) {
        outline: none !important;
        border-color: #43a047 !important; /* professional green */
        box-shadow:
            0 10px 24px rgba(67,160,71,.15),
            0 0 0 4px rgba(67,160,71,.14) !important;
    }

    /* Footer – clean & professional */
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

    # Header + Auth UI (NO extra box under QA TEAM)
    st.markdown('<div class="qa-banner">QA TEAM</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth">', unsafe_allow_html=True)
    st.subheader("👋 Welcome!")
    st.header("🔐 Secure Access")

    # Highlighted password input (styled via CSS above)
    password = st.text_input("Type your Access Password", type="password", placeholder="Enter your password")

    if password == "Ashutosh@79836666":
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.error("❌ Incorrect password. Please try again.")

    # Footer (clean + professional)
    st.markdown("""
        <div class="app-footer">
            <div class="divider"></div>
            <div class="meta">© 2025 <strong>QA TEAM</strong> • Developed by <strong>Ashutosh Rana</strong> ❤️ • v1.0</div>
        </div>
    """, unsafe_allow_html=True)

    # Close auth container
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- Theme Toggle (only after login) ---
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"], index=0)
st.session_state.theme = theme

# --- Apply Theme Styling ---
if theme == "Dark":
    st.markdown("""
    <style>
    body, .main, .stApp { background-color: #121212; color: #e0e0e0; }
    .sidebar .sidebar-content { background-color: #1e1e1e; color: #e0e0e0; }
    .toggle-status { color: #81c784; }
    .stTextInput > div > input { background-color: #2c2c2c; color: #e0e0e0; }
    .stDownloadButton button { background-color: #333; color: #fff; }
    footer { color: #aaa; }
    .qa-banner {
        text-align: center; font-size: 28px; font-weight: 800;
        color: #ffeb3b; text-shadow: 0 0 8px #ffeb3b; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    body, .main, .stApp { background-color: #f5f5f5; color: #000; }
    .sidebar .sidebar-content { background-color: #ffffff; color: #000; }
    .toggle-status { color: #1b5e20; }
    footer { color: #555; }
    .qa-banner {
        text-align: center; font-size: 28px; font-weight: 800;
        color: #1976d2; margin-bottom: 10px; letter-spacing: .5px;
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
