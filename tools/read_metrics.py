"""Print aggregate Olist results from the team's local 001 ZIP."""
import argparse
import csv
import io
from pathlib import PurePosixPath
from statistics import median
from zipfile import ZipFile


def rows(archive, name):
    matches = [entry for entry in archive.infolist()
               if PurePosixPath(entry.filename).name == name]
    if len(matches) != 1:
        raise ValueError(f"Expected one aggregate table named {name}, found {len(matches)}")
    with archive.open(matches[0]) as stream:
        return list(csv.DictReader(io.TextIOWrapper(stream, encoding="utf-8-sig")))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", help="Path to the 001 project ZIP")
    args = parser.parse_args()
    with ZipFile(args.archive) as archive:
        for days in (180, 365):
            for row in rows(archive, f"metrics_T{days}_track2.csv"):
                print(f"{days} days | {row['model']} | R2 {float(row['R2']):.4f}")
        for row in rows(archive, "olist_final_model_performance.csv"):
            print(row["Model"], "R2", row["R2"], "AUC", row["AUC"])
        issue = next(row for row in rows(archive, "olist_final_impact_analysis.csv")
                     if row["Issue_Label"] == "issue_not_received")
        print("Not received | score coefficient", issue["Linear_Penalty"],
              "| low-rating odds ratio", issue["Logistic_Odds_Ratio"])
        sellers = rows(archive, "B_riskmoney_seller_summary.csv")
        delay_case = [row for row in sellers if row["scenario_issue"] == "issue_delay"
                      and float(row["scenario_reduction_rate"]) == 0.30]
        before = sum(float(row["risk_money_total"]) for row in delay_case)
        after = sum(float(row["risk_money_total_after"]) for row in delay_case)
        print(f"Delay scenario | {len(delay_case)} seller rows | weighted GMV (BRL) "
              f"{before:,.2f} -> {after:,.2f} | reduction {before-after:,.2f}")
        ladder = rows(archive, "A_seller_next_tier_scenario.csv")
        ratios = [float(row["uplift_ratio_next_tier"]) for row in ladder
                  if row["tier"] != row["tier_next"] and row["uplift_ratio_next_tier"]]
        print(f"Tier benchmark | {len(ladder)} rows | {len(ratios)} comparable | "
              f"{sum(ratio < 1 for ratio in ratios)} below 1 | median {median(ratios):.3f}")


if __name__ == "__main__":
    main()
