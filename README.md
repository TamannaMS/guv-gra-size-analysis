# GUV-GrA Size Analysis

Statistical analysis of giant unilamellar vesicle (GUV) diameters at two concentrations
of Gramicidin A (GrA), in DOPC:DOPG membranes. Compares distribution shape, spread, and
central tendency between conditions and produces publication-style figures.

## ⚠️ Data notice

** I've kept the data notice and schema sections in this README because they're accurate and they matter — every figure here was generated from the synthetic toy dataset, not from my real measurements, and I don't want anyone citing placeholder numbers as results. The wording is brief, but the substance stays: this repo demonstrates the analysis pipeline; the science comes from the real data, which stays private.
## Data schema

| | |
|---|---|
| **Membrane** | DOPC:DOPG (60:40 mol%), my standard GUV prep |
| **Peptide** | Gramicidin A, 0.01% and 0.02% (w/w) |
| **Measured** | GUV diameter (µm) |
| **Format** | one `.xlsx` workbook, one sheet per condition, one column of diameters per sheet |
| **Not included here** | raw micrographs, per-vesicle shape/circularity, replicate metadata |
## Repo structure

```
.
├── data/
│   └── toy_dataset/
│       └── toy_guv_sizes.xlsx              # synthetic, n=20/condition -- the only data tracked by git
├── notebooks/
│   └── 01_exploratory_analysis.ipynb       # stats + figures, runs end-to-end on the toy data
├── src/
│   └── load_data.py                        # shared data-loading helper
├── scripts/
│   └── generate_toy_data.py                # regenerates the toy dataset
├── figures/                                 # PNG + SVG outputs from the notebook (toy-data run)
├── requirements.txt
├── .gitignore                               # excludes any real data file placed in data/
└── LICENSE
```

## Quickstart

```bash
git clone <this-repo-url>
cd guv-gra-size-analysis
pip install -r requirements.txt
jupyter notebook notebooks/01_exploratory_analysis.ipynb
```

The notebook defaults to `USE_TOY_DATA = True` since the real workbook isn't shipped here.
Flip it to `False` once you've added your own `data/size_distribution_of_guvs.xlsx`.

To regenerate the toy dataset:

```bash
cd scripts && python generate_toy_data.py
```

## What the notebook does

1. Loads diameters from the workbook (toy or real) into a tidy dataframe
2. Descriptive statistics per condition (mean, median, CV, skew, kurtosis)
3. Normality checks (Shapiro-Wilk, raw vs. log-transformed)
4. Between-condition comparison: Mann-Whitney U, Welch's t-test, Cohen's d, KS test
5. Four publication-style figures: histogram+KDE, violin/box/strip, ECDF, Q-Q plots

## Planned extensions (blocked on raw images)

`02_image_segmentation.ipynb`, `03_shape_analysis.ipynb`, and
`04_correlation_with_manual_counts.ipynb` would add vesicle segmentation, circularity/shape
descriptors, and validation against manually counted diameters — all require the original
micrographs, which are outside the scope of this repo.

## Machine learning applicability

With only one continuous variable (diameter) per vesicle and two labeled conditions, this
dataset does not support meaningful ML — a classifier here would just be re-deriving the
Mann-Whitney/KS results above with extra steps. ML becomes worth considering once
per-vesicle shape descriptors (area, circularity, aspect ratio, texture) are extracted from
images.

## Related repository

For the theoretical side of the same system, see
[membrane-biophysics-models](https://github.com/TamannaMS/membrane-biophysics-models) —
Python simulations of GUV osmotic swelling, bilayer permeability, electroporation pore
kinetics, and a Gramicidin A concentration–radius model that complements the
experimental analysis in this repo.

## License

MIT — see [LICENSE](LICENSE). Update the copyright holder name before publishing.
