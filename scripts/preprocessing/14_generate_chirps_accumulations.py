from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_CSV = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "chirps"
    / "chirps_lokoja_daily_area_average_standardized.csv"
)

OUTPUT_CSV = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "chirps"
    / "chirps_lokoja_area_average_accumulations.csv"
)

WINDOWS = (1, 3, 7, 14)


def main():
    df = pd.read_csv(INPUT_CSV)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["rainfall_mean_mm_day"] = pd.to_numeric(
        df["rainfall_mean_mm_day"],
        errors="coerce",
    )

    if df["date"].isna().any():
        raise ValueError("Invalid or missing dates found.")

    if df["date"].duplicated().any():
        raise ValueError("Duplicate dates found.")

    df = df.sort_values("date").reset_index(drop=True)

    # Require a continuous daily sequence. Do not fill missing dates.
    expected_dates = pd.date_range(
        df["date"].min(),
        df["date"].max(),
        freq="D",
    )

    if not df["date"].equals(pd.Series(expected_dates, name="date")):
        raise ValueError(
            "Dates are not continuous. Resolve the date gap before calculating."
        )

    rainfall = df["rainfall_mean_mm_day"]

    if (rainfall.dropna() < 0).any():
        raise ValueError("Negative rainfall values found.")

    output = pd.DataFrame({
        "date": df["date"].dt.strftime("%Y-%m-%d"),
        "daily_rainfall_mm": rainfall,
    })

    for window in WINDOWS:
        column = f"rainfall_{window}day_accumulation_mm"

        # Each value includes the dated day and the preceding window-1 days.
        # min_periods=window leaves incomplete windows as NaN.
        output[column] = rainfall.rolling(
            window=window,
            min_periods=window,
        ).sum()

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(OUTPUT_CSV, index=False, na_rep="")

    print(f"Accumulation series saved to: {OUTPUT_CSV}")
    for window in WINDOWS:
        column = f"rainfall_{window}day_accumulation_mm"
        print(f"{window}-day valid sums: {output[column].notna().sum()}")


if __name__ == "__main__":
    main()