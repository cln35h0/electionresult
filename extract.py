import os
import re
import pandas as pd

# Mapping state/UT codes to names
state_mapping = {
    "S01": "Andhra Pradesh", "S02": "Arunachal Pradesh", "S03": "Assam",
    "S04": "Bihar", "S05": "Goa", "S06": "Gujarat", "S07": "Haryana",
    "S08": "Himachal Pradesh", "S10": "Karnataka", "S11": "Kerala",
    "S12": "Madhya Pradesh", "S13": "Maharashtra", "S14": "Manipur",
    "S15": "Meghalaya", "S16": "Mizoram", "S17": "Nagaland",
    "S18": "Odisha", "S19": "Punjab", "S20": "Rajasthan", "S21": "Sikkim",
    "S22": "Tamil Nadu", "S23": "Tripura", "S24": "Uttar Pradesh",
    "S25": "West Bengal", "S26": "Chhattisgarh", "S27": "Jharkhand",
    "S28": "Uttarakhand", "S29": "Telangana",
    "U01": "Andaman & Nicobar Islands", "U02": "Chandigarh",
    "U03": "Dadra & Nagar Haveli and Daman & Diu", "U05": "NCT of Delhi",
    "U06": "Lakshadweep", "U07": "Puducherry", "U08": "Jammu and Kashmir",
    "U09": "Ladakh"
}

# Input folder
folder = "saved_pages"
data = []

for filename in os.listdir(folder):
    if filename.endswith(".txt"):
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        # --- Extract constituency info ---
        m = re.search(r"Parliamentary Constituency\s+(\d+)\s*-\s*([^(]+)", text)
        const_no = m.group(1).strip() if m else "NA"
        const_name = m.group(2).strip() if m else "NA"

        # --- Get State code & name ---
        code = filename.split("-")[0][:3]
        state = state_mapping.get(code, "Unknown")

        # --- Extract candidate details ---
        # This regex now allows status to be optional (covers NOTA)
        blocks = re.findall(r"(Won|Lost)?\s*([\d,]+).*?\n(.*?)\n(.*)", text)

        for status, votes, candidate, party in blocks:
            votes = votes.replace(",", "").strip()
            candidate = candidate.strip()
            party = party.strip()

            # Handle NOTA case
            if candidate.upper() == "NOTA":
                status = "NOTA"
                party = "NOTA"

            # Skip useless rows (status missing and not NOTA)
            if not status:
                continue

            # Ensure votes is integer
            try:
                votes = int(votes)
            except ValueError:
                continue  # skip if votes not numeric

            data.append({
                "stateUt _code": code,
                "stateUt": state,
                "constituencyNo": const_no,
                "constituencyName": const_name,
                "candidateName": candidate,
                "partyNames": party,
                "votes": votes,
                "status": status
            })

# Save to CSV
df = pd.DataFrame(data)
df.to_csv("results.csv", index=False, encoding="utf-8-sig")

print("Extracted", len(df), "rows into all_results.csv")
