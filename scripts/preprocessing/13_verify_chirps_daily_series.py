import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_CSV = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "chirps"
    / "chirps_v3_lokoja_2018_09_daily.csv"
)

STANDARDIZED_CSV = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "chirps"
    / "chirps_lokoja_daily_area_average_standardized.csv"
)

REPORT_JSON = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "chirps"
    / "chirps_lokoja_daily_verification_report.json"
)

VALUE_TOLERANCE = 1e-9


def inspect_series(df, name):
    """Check dates and rainfall values, and calculate summary statistics."""
    dates = pd.to_datetime(df["date"], errors="coerce")
    rainfall = pd.to_numeric(df["rainfall_mean_mm_day"], errors="coerce")

    invalid_dates = dates.isna()
    invalid_rainfall = rainfall.isna() | ~rainfall.map(
        lambda value: pd.notna(value) and value != float("inf")
        and value != float("-inf")
    )
    negative_rainfall = rainfall < 0

    valid_dates = dates.dropna()
    duplicate_dates = valid_dates[valid_dates.duplicated()].dt.strftime(
        "%Y-%m-%d"
    ).tolist()

    missing_dates = []
    if not valid_dates.empty:
        expected_dates = pd.date_range(
            valid_dates.min(),
            valid_dates.max(),
            freq="D",
        )
        missing_dates = expected_dates.difference(
            pd.DatetimeIndex(valid_dates.unique())
        ).strftime("%Y-%m-%d").tolist()

    valid_rainfall = rainfall.dropna()

    return {
        "name": name,
        "record_count": int(len(df)),
        "invalid_date_count": int(invalid_dates.sum()),
        "duplicate_dates": duplicate_dates,
        "missing_dates": missing_dates,
        "invalid_rainfall_count": int(invalid_rainfall.sum()),
        "negative_rainfall_count": int(negative_rainfall.sum()),
        "summary_mm_per_day": {
            "count": int(valid_rainfall.count()),
            "min": float(valid_rainfall.min()),
            "max": float(valid_rainfall.max()),
            "mean": float(valid_rainfall.mean()),
            "sum": float(valid_rainfall.sum()),
            "standard_deviation_sample": float(valid_rainfall.std()),
        },
    }


def main():
    raw = pd.read_csv(RAW_CSV)
    standardized = pd.read_csv(STANDARDIZED_CSV)

    required_columns = {"date", "rainfall_mean_mm_day"}

    for name, df in [("raw", raw), ("standardized", standardized)]:
        missing_columns = required_columns - set(df.columns)
        if missing_columns:
            raise ValueError(
                f"{name} file is missing columns: {sorted(missing_columns)}"
            )

    raw_report = inspect_series(raw, "raw")
    standardized_report = inspect_series(standardized, "standardized")

    # Compare date/value pairs between the source and standardized files.
    raw_compare = raw[["date", "rainfall_mean_mm_day"]].copy()
    standardized_compare = standardized[
        ["date", "rainfall_mean_mm_day"]
    ].copy()

    raw_compare["date"] = pd.to_datetime(raw_compare["date"], errors="coerce")
    standardized_compare["date"] = pd.to_datetime(
        standardized_compare["date"], errors="coerce"
    )

    raw_compare["rainfall_mean_mm_day"] = pd.to_numeric(
        raw_compare["rainfall_mean_mm_day"], errors="coerce"
    )
    standardized_compare["rainfall_mean_mm_day"] = pd.to_numeric(
        standardized_compare["rainfall_mean_mm_day"], errors="coerce"
    )

    comparison = raw_compare.merge(
        standardized_compare,
        on="date",
        how="outer",
        suffixes=("_raw", "_standardized"),
        indicator=True,
    )

    comparison["value_difference"] = (
        comparison["rainfall_mean_mm_day_raw"]
        - comparison["rainfall_mean_mm_day_standardized"]
    ).abs()

    mismatches = comparison[
        (comparison["_merge"] != "both")
        | (comparison["value_difference"] > VALUE_TOLERANCE)
    ]

    report = {
        "source_file": str(RAW_CSV.relative_to(PROJECT_ROOT)),
        "standardized_file": str(STANDARDIZED_CSV.relative_to(PROJECT_ROOT)),
        "raw_series": raw_report,
        "standardized_series": standardized_report,
        "source_comparison": {
            "matched_date_and_value_pairs": int(
                (comparison["_merge"] == "both").sum()
                - len(mismatches)
            ),
            "mismatch_count": int(len(mismatches)),
            "mismatches": [
                {
                    "date": (
                        row["date"].strftime("%Y-%m-%d")
                        if pd.notna(row["date"])
                        else None
                    ),
                    "raw_value": (
                        float(row["rainfall_mean_mm_day_raw"])
                        if pd.notna(row["rainfall_mean_mm_day_raw"])
                        else None
                    ),
                    "standardized_value": (
                        float(row["rainfall_mean_mm_day_standardized"])
                        if pd.notna(
                            row["rainfall_mean_mm_day_standardized"]
                        )
                        else None
                    ),
                }
                for _, row in mismatches.iterrows()
            ],
        },
    }

    # Overall pass/fail checks
    report["verification_passed"] = (
        raw_report["invalid_date_count"] == 0
        and standardized_report["invalid_date_count"] == 0
        and not raw_report["duplicate_dates"]
        and not standardized_report["duplicate_dates"]
        and not raw_report["missing_dates"]
        and not standardized_report["missing_dates"]
        and raw_report["invalid_rainfall_count"] == 0
        and standardized_report["invalid_rainfall_count"] == 0
        and raw_report["negative_rainfall_count"] == 0
        and standardized_report["negative_rainfall_count"] == 0
        and len(mismatches) == 0
    )

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_JSON.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(f"Verification report saved to: {REPORT_JSON}")
    print(f"Verification passed: {report['verification_passed']}")
    print(f"Source comparison mismatches: {len(mismatches)}")


if __name__ == "__main__":
    main()