from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import json

app = FastAPI()

# Known values
known_sids = ["1-E9U2L"]
known_busorg_ids = ["1-E9U2L"]

# Column mapping
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

# Row cleaning function
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

# Matching function
def is_matching(row):
    return row.get("sid") in known_sids or row.get("busorgId") in known_busorg_ids

@app.post("/convert")
async def convert_excel(file: UploadFile = File(...)):
    try:
        df = pd.read_excel(file.file, engine="openpyxl")
        df = df.fillna("null").astype(str)

        df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
        for original_col, new_col in column_mapping.items():
            if new_col not in df.columns:
                df[new_col] = "null"

        cleaned_rows = []
        matching_rows = []

        for _, row in df.iterrows():
            cleaned = clean_row(row)
            cleaned_rows.append(cleaned)
            if is_matching(cleaned):
                matching_rows.append(cleaned)

        payload = {"importGcrImpactsRequest": {"impacts": matching_rows}} if matching_rows else {"data": cleaned_rows}

        return JSONResponse(content=payload)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
