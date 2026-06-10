# ==========================================================
# DATA CLEANING UTILITIES
# ==========================================================

import pandas as pd

# ==========================================================
# AGENCY STANDARDIZATION
# ==========================================================

AGENCY_MAPPING = {

    "Other (specify)": "MTRD",
    "Other: MTRD": "MTRD",
    "Other: mtrd": "MTRD",
    "Mtrd": "MTRD"

}

# ==========================================================
# POSITION STANDARDIZATION
# ==========================================================

POSITION_MAPPING = {

    "Other (specify): Engineer":
        "Engineer",

    "Other (specify): ENGINEER":
        "Engineer",

    "Other (specify): Inspector":
        "Inspector",

    "Other (specify): Deputy CE":
        "Deputy Chief Engineer",

    "Other (specify): Senior Principal Engineer":
        "Senior Principal Engineer",

    "Other (specify): Senior Assistant Roads officer":
        "Senior Assistant Roads Officer"
}

# ==========================================================
# CLEAN DATASET
# ==========================================================

def clean_master_dataset(df):

    agency_col = (
        "Q1. What agency do you work for?"
    )

    position_col = (
        "Q3. What position do you currently hold?"
    )

    if agency_col in df.columns:

        df[agency_col] = (
            df[agency_col]
            .replace(AGENCY_MAPPING)
        )

    if position_col in df.columns:

        df[position_col] = (
            df[position_col]
            .replace(POSITION_MAPPING)
        )

    return df


# ==========================================================
# INDEX DIAGNOSTICS
# ==========================================================

def index_diagnostics(indices_df):

    results = []

    for col in ["DMI", "FMI", "RRI", "DRI"]:

        if col not in indices_df.columns:
            continue

        unique_values = (
            indices_df[col]
            .dropna()
            .nunique()
        )

        results.append({

            "Index": col,
            "Records": len(indices_df),
            "Unique Values": unique_values,
            "Min": indices_df[col].min(),
            "Max": indices_df[col].max(),
            "Mean": round(
                indices_df[col].mean(),
                1
            )
        })

    return pd.DataFrame(results)
