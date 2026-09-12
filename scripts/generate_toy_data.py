"""
Generate a small, synthetic toy dataset shaped like data/size_distribution_of_guvs.xlsx.

Purpose: let anyone clone this repo and run notebooks/01_exploratory_analysis.ipynb
immediately, without the real (larger, unpublished) measurement file. The toy values
are randomly generated from log-normal distributions loosely modeled on the real
data's summary statistics -- they are NOT real measurements and must never be cited
or plotted as if they were.

Usage (from anywhere):
    python scripts/generate_toy_data.py
Writes:
    data/toy_dataset/toy_guv_sizes.xlsx
"""

from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = REPO_ROOT / "data" / "toy_dataset" / "toy_guv_sizes.xlsx"
N_PER_CONDITION = 20
SEED = 42

# Loosely modeled on the real data's mean/spread -- not fit to it precisely.
CONDITIONS = {
    "toy_GrA_0.01pct": dict(mean_log=np.log(14.5), sigma_log=0.30),
    "toy_GrA_0.02pct": dict(mean_log=np.log(13.5), sigma_log=0.42),
}


def make_toy_data():
    rng = np.random.default_rng(SEED)
    sheets = {}
    for name, params in CONDITIONS.items():
        sizes = rng.lognormal(mean=params["mean_log"], sigma=params["sigma_log"],
                               size=N_PER_CONDITION)
        sheets[name] = pd.DataFrame({"diameter_um": np.round(sizes, 2)})
    return sheets


if __name__ == "__main__":
    sheets = make_toy_data()
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(OUT_PATH, engine="openpyxl") as writer:
        for sheet_name, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Wrote toy dataset to {OUT_PATH}")
    for name, df in sheets.items():
        print(f"  {name}: n={len(df)}, mean={df['diameter_um'].mean():.2f} um")
