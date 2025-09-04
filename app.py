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

# --- Main App ---
st.title("Excel to JSON Payload Converter")

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

    df = df.rename(columns={k: v for k, v in expected_columns.items() if k in df.columns})
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

    # --- Matching Logic ---
    def is_matching(row):
        # Define your matching condition here
        return row["busorgId"] == "1-E9U2L" or row["sid"] == "1-E9U2L"

    cleaned_rows = []
    for _, row in df.iterrows():
        cleaned = clean_row(row)
        if is_matching(cleaned):
            cleaned_rows.append(cleaned)

    # --- Build Payload ---
    if cleaned_rows:
        payload = {"importGcrImpactsRequest": {"impacts": cleaned_rows}}
    else:
        payload = {"message": "No matching data found"}

    # --- Display and Download ---
    st.subheader("Converted JSON Payload")
    st.json(payload)

    json_bytes = json.dumps(payload, indent=4).encode("utf-8")
    st.download_button("Download JSON", data=json_bytes, file_name="output.json", mime="application/json")
