"""Shared helper for loading GUV diameter data from the project's Excel workbooks."""

import pandas as pd


def load_guv_sizes(path, condition_map=None):
    """Load a GUV-size workbook into a tidy long-format DataFrame.

    Parameters
    ----------
    path : str
        Path to an .xlsx file where each sheet is a single column of GUV
        diameters (um) for one condition.
    condition_map : dict, optional
        Maps raw sheet names to display labels. Sheets not in the map keep
        their original name.

    Returns
    -------
    pandas.DataFrame with columns: condition, diameter_um, radius_um,
    area_um2, volume_um3 (area/volume assume a perfect sphere -- see notebook
    for caveats).
    """
    condition_map = condition_map or {}
    xls = pd.ExcelFile(path)
    records = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet).dropna(how="all")
        if df.shape[1] == 0:
            continue
        label = condition_map.get(sheet, sheet)
        for v in df.iloc[:, 0].dropna().astype(float).values:
            records.append({"condition": label, "diameter_um": v})

    data = pd.DataFrame(records)
    if data.empty:
        return data
    data["radius_um"] = data["diameter_um"] / 2
    data["area_um2"] = 3.141592653589793 * data["radius_um"] ** 2
    data["volume_um3"] = (4 / 3) * 3.141592653589793 * data["radius_um"] ** 3
    return data
