# ==========================================================
# THEMATIC CODING ENGINE
# Sprint 3C.2
# ==========================================================

import pandas as pd

from utils.theme_dictionary import (
    THEME_KEYWORDS
)


def assign_themes(text):

    if pd.isna(text):

        return []

    text = str(text).lower()

    matched_themes = []

    for theme, keywords in THEME_KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in text:

                matched_themes.append(theme)

                break

    return matched_themes


def build_theme_dataset(
    df,
    text_columns,
    agency_column
):

    coded_rows = []

    for _, row in df.iterrows():

        agency = row[agency_column]

        for col in text_columns:

            response = row[col]

            themes = assign_themes(
                response
            )

            for theme in themes:

                coded_rows.append({

                    "Agency": agency,

                    "Question": col,

                    "Response": response,

                    "Theme": theme

                })

    return pd.DataFrame(
        coded_rows
    )
