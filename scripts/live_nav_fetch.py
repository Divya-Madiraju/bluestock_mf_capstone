import requests
import pandas as pd
from pathlib import Path

# Scheme codes provided in the assignment
schemes = {
    "HDFC_Top100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

# Create output directory if it doesn't exist
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

for fund_name, scheme_code in schemes.items():
    try:
        url = f"https://api.mfapi.in/mf/{scheme_code}"

        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        # Convert NAV history to DataFrame
        nav_df = pd.DataFrame(data["data"])

        # Save as CSV
        file_path = output_dir / f"{fund_name}.csv"
        nav_df.to_csv(file_path, index=False)

        print(f"Saved: {file_path}")

    except Exception as e:
        print(f"Error fetching {fund_name}: {e}")

print("\nNAV data fetch completed!")