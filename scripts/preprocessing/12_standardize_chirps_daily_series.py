from pathlib import Path

import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_CSV = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "chirps"
    / "chirps_v3_lokoja_2018_09_daily.csv"
)

OUTPUT_CSV = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "chirps"
    / "chirps_lokoja_daily_area_average_standardized.csv"
)


def main():
    # Load the raw daily rainfall CSV
    df = pd.read_csv(INPUT_CSV)

    # Keep only the date and daily area-average rainfall columns
    df = df[["date", "rainfall_mean_mm_day"]].copy()

    # Standardize dates and rainfall values
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["rainfall_mean_mm_day"] = pd.to_numeric(
        df["rainfall_mean_mm_day"],
        errors="coerce",
    )

    # Sort records chronologically
    df = df.sort_values("date").reset_index(drop=True)

    # Check for invalid or missing values
    if df["date"].isna().any():
        raise ValueError("One or more dates are missing or invalid.")

    if df["rainfall_mean_mm_day"].isna().any():
        raise ValueError("One or more rainfall values are missing or invalid.")

    if (df["rainfall_mean_mm_day"] < 0).any():
        raise ValueError("Negative rainfall values were found.")

    # Check for duplicate dates
    if df["date"].duplicated().any():
        duplicate_dates = df.loc[df["date"].duplicated(), "date"]
        raise ValueError(f"Duplicate dates found: {duplicate_dates.tolist()}")

    # Check that dates are consecutive
    expected_dates = pd.date_range(
        start=df["date"].min(),
        end=df["date"].max(),
        freq="D",
    )

    missing_dates = expected_dates.difference(df["date"])

    if not missing_dates.empty:
        raise ValueError(f"Missing dates found: {missing_dates.tolist()}")

    # Write dates in YYYY-MM-DD format
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # Create output folder if it does not exist
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    # Save standardized data
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"Standardized CSV saved to: {OUTPUT_CSV}")
    print(f"Records: {len(df)}")
    print(f"Date range: {df['date'].iloc[0]} to {df['date'].iloc[-1]}")
    print("Missing rainfall values: 0")
    print("Duplicate dates: 0")


if __name__ == "__main__":
    main()