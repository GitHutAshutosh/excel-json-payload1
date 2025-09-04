import streamlit as st
import pandas as pd
import json
from io import BytesIO

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


st.title("Excel to JSON Payload Converter")

uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df = df.fillna("null").astype(str)

    column_mapping = {
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

    df = df.rename(columns=column_mapping)

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

    st.subheader("Converted JSON Payload")
    st.json(payload)

    json_bytes = json.dumps(payload, indent=4).encode("utf-8")
    st.download_button("Download JSON", data=json_bytes, file_name="output.json", mime="application/json")