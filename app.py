import streamlit as st
import pandas as pd
import json

# --- Password Protection ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Enter password", type="password")
    if password == "Ashutosh@79836666":
        st.session_state.authenticated = True
        st.rerun()
    elif password:
        st.error("Incorrect password")
    st.stop()

# --- Logout Option ---
if st.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()

# --- Main App (Only visible after correct password) ---
st.title("Excel to JSON Payload Converter")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        st.stop()

    df = df.fillna("null").astype(str)

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

    # --- Row Cleaning Function ---
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

    # --- Convert to JSON Payload ---
    impacts = [clean_row(row) for _, row in df.iterrows()]
    payload = {"importGcrImpactsRequest": {"impacts": impacts}}

    # --- Display and Download ---
    st.subheader("Converted JSON Payload")
    st.json(payload)

    json_bytes = json.dumps(payload, indent=4).encode("utf-8")
    st.download_button("Download JSON", data=json_bytes, file_name="output.json", mime="application/json")

# --- New Feature: Convert Text to JSON ---
st.title("Text to JSON Converter")

text_input = st.text_area("Paste your text here to convert into JSON")

if text_input:
    try:
        parsed_json = json.loads(text_input)
        st.success("Valid JSON detected!")
        st.json(parsed_json)
        json_bytes = json.dumps(parsed_json, indent=4).encode("utf-8")
        st.download_button("Download Converted JSON", data=json_bytes, file_name="converted_text.json", mime="application/json")
    except json.JSONDecodeError as e:
        error_line = e.lineno
        st.error(f"Issue detected in line {error_line}: {e.msg}. Please fix this issue and try again.")
