import pandas as pd
import json

# Load Excel file
df = pd.read_excel("FRO2003746840 (1).xlsx")

# Replace NaNs with "null" and convert all to string
df = df.fillna("null").astype(str)

# Rename columns to match Word file format
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

# Define known matching values
known_codes = [
    {"sid": "1-E9U2L", "busorgId": "1-E9U2L"},
    # Add more known values if needed
]

# Clean and match rows
def clean_row(row):
    # Fix Busorg ID
    busorg_id = row.get("busorgId", "")
    if busorg_id.upper().startswith("NULL") or busorg_id.isnumeric():
        row["busorgId"] = "1-E9U2L"
    
    # Fix SID
    sid = row.get("sid", "")
    if sid.isnumeric():
        row["sid"] = "1-E9U2L"
    
    # Convert 'Protection' to boolean
    protection = row.get("protection", "null").lower()
    row["protection"] = protection == "true"

    # Convert numeric fields
    for field in ["altAcctId", "orderNum", "tspCode"]:
        try:
            row[field] = int(row[field]) if row[field] != "null" else "null"
        except:
            row[field] = "null"

    return {k: v if isinstance(v, (bool, int)) else v for k, v in row.items()}

def is_matching(row):
    for code in known_codes:
        if row.get("sid") == code["sid"] or row.get("busorgId") == code["busorgId"]:
            return True
    return False

# Process rows
cleaned_rows = []
matching_rows = []

for _, row in df.iterrows():
    cleaned = clean_row(row)
    cleaned_rows.append(cleaned)
    if is_matching(cleaned):
        matching_rows.append(cleaned)

# Build payload
if matching_rows:
    payload = {"importGcrImpactsRequest": {"impacts": matching_rows}}
else:
    payload = {"data": cleaned_rows}

# Save to JSON
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(payload, f, indent=4)

print("✅ JSON saved as output.json")
