from pathlib import Path
import json

import numpy as np
import pandas as pd


# Paths
DAILY_FILE = Path(
    "data/processed/chirps/chirps_lokoja_daily_area_average_standardized.csv"
)
ACCUMULATION_FILE = Path(
    "data/processed/chirps/chirps_lokoja_area_average_accumulations.csv"
)
REPORT_FILE = Path(
    "data/processed/chirps/chirps_lokoja_accumulation_validation_report.json"
)

# Change these names only if your accumulation-generation script used different ones.
ACCUMULATION_COLUMNS = {
    1: "rainfall_1d_mm",
    3: "rainfall_3d_mm",
    7: "rainfall_7d_mm",
    14: "rainfall_14d_mm",
}

DATE_COLUMN = "date"
DAILY_RAINFALL_COLUMN = "rainfall_mean_mm_day"

# Allow tiny floating-point differences, but not meaningful discrepancies.
ATOL = 1e-8
RTOL = 1e-8


def main():
    daily = pd.read_csv(DAILY_FILE)
    accumulations = pd.read_csv(ACCUMULATION_FILE)

    # Parse and validate dates.
    daily[DATE_COLUMN] = pd.to_datetime(
        daily[DATE_COLUMN], errors="raise"
    )
    accumulations[DATE_COLUMN] = pd.to_datetime(
        accumulations[DATE_COLUMN], errors="raise"
    )

    daily = daily.sort_values(DATE_COLUMN).reset_index(drop=True)
    accumulations = accumulations.sort_values(DATE_COLUMN).reset_index(drop=True)

    daily_values = pd.to_numeric(
        daily[DAILY_RAINFALL_COLUMN], errors="coerce"
    )

    # Independently recompute the expected rolling sums from daily inputs.
    expected = pd.DataFrame({DATE_COLUMN: daily[DATE_COLUMN]})
    for window, column in ACCUMULATION_COLUMNS.items():
        expected[column] = daily_values.rolling(
            window=window,
            min_periods=window,
        ).sum()

    report = {
        "input_daily_file": str(DAILY_FILE),
        "input_accumulation_file": str(ACCUMULATION_FILE),
        "units": {
            "daily_input": "mm/day",
            "accumulation_products": "mm accumulated over each window",
        },
        "spatial_alignment": {
            "status": "not_applicable",
            "reason": (
                "These products are area-average time series, not rasters. "
                "Raster alignment requires daily accumulation raster products."
            ),
        },
        "checks": {},
        "issues": [],
    }

    # Check dates and row counts.
    same_dates = (
        len(daily) == len(accumulations)
        and daily[DATE_COLUMN].equals(accumulations[DATE_COLUMN])
    )
    report["checks"]["dates_match_daily_series"] = bool(same_dates)

    if not same_dates:
        report["issues"].append(
            "Accumulation dates or row count do not match the daily series."
        )

    # Check each saved product against independently recalculated values.
    for window, column in ACCUMULATION_COLUMNS.items():
        if column not in accumulations.columns:
            report["checks"][f"{window}_day_product"] = {
                "status": "missing_column",
                "column_expected": column,
            }
            report["issues"].append(
                f"Missing accumulation column: {column}"
            )
            continue

        actual = pd.to_numeric(accumulations[column], errors="coerce")
        expected_values = expected[column]

        # Missing values must occur in the same places.
        same_nodata = actual.isna().equals(expected_values.isna())

        # Compare values only where both products have values.
        valid = actual.notna() & expected_values.notna()
        values_match = bool(
            np.allclose(
                actual[valid].to_numpy(),
                expected_values[valid].to_numpy(),
                atol=ATOL,
                rtol=RTOL,
            )
        )

        # Explicitly confirm the 1-day product matches verified daily rainfall.
        one_day_matches_daily = None
        if window == 1:
            one_day_matches_daily = bool(
                np.allclose(
                    actual[valid].to_numpy(),
                    daily_values[valid].to_numpy(),
                    atol=ATOL,
                    rtol=RTOL,
                )
            )

        expected_valid_count = max(len(daily) - window + 1, 0)
        actual_valid_count = int(actual.notna().sum())

        product_result = {
            "status": (
                "pass"
                if same_nodata and values_match
                else "fail"
            ),
            "expected_valid_days": expected_valid_count,
            "actual_valid_days": actual_valid_count,
            "nodata_positions_match": bool(same_nodata),
            "recomputed_sums_match": values_match,
        }

        if window == 1:
            product_result["matches_verified_daily_rainfall"] = (
                one_day_matches_daily
            )

        report["checks"][f"{window}_day_product"] = product_result

        if not same_nodata:
            report["issues"].append(
                f"{column}: NoData positions differ from the expected window."
            )
        if not values_match:
            report["issues"].append(
                f"{column}: saved sums do not match recomputed sums."
            )
        if actual_valid_count != expected_valid_count:
            report["issues"].append(
                f"{column}: unexpected number of valid accumulation days."
            )

    report["overall_status"] = (
        "pass" if not report["issues"] else "fail"
    )

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Overall validation: {report['overall_status'].upper()}")
    print(f"Report saved to: {REPORT_FILE}")

    for issue in report["issues"]:
        print(f"- {issue}")


if __name__ == "__main__":
    main()