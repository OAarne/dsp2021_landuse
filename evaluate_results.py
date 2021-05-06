#%%
import pandas as pd
import numpy as np
from typing import List, Dict
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import fbeta_score


col_correspondence = {
    "deforestation 2000-2010": "% Forest Loss 2000-2010",
    "deforestation 2010-2018": "% Forest Loss 2010-2018",
    "reforestation 2000-2010": "% Forest Gain 2000-2010",
    "reforestation 2010-2018": "% Forest Gain 2010-2018",
}


def hist_to_percentage(a):
    zeroes = 0
    ones = 0
    for row in a:
        if row[0] == 0:
            zeroes = row[1]
        elif row[0] == 1:
            ones = row[1]
    percent_ones = (ones / (ones + zeroes)) * 100
    return percent_ones


def parse_histo_input(s: str):
    s_array = s[6:-1]
    return hist_to_percentage(eval(s_array))


def load_histo_file(path: str) -> pd.DataFrame:
    """Load a file containing a type of CSV of the results of a classifier, and process it into a more useful form."""
    histo = pd.read_csv(path)
    for col in histo.columns:
        if "Histogram" in col:
            histo.loc[:, col.replace("Histogram", "")] = histo.loc[:, col].map(
                parse_histo_input
            )
    histo.loc[:, "plotID"] = histo.loc[:, "plotID"].astype(float)
    return histo


def get_score_df(total: pd.DataFrame, beta: float = 5.0) -> pd.DataFrame:
    """Return a DataFrame with various summary statistics describing the results.

    Precision and recall are calculated while treating the model as a binary forest loss or forest gain detector.
    """
    df = pd.DataFrame(
        {
            "MAE": [],
            "Correlation": [],
            "% Precision": [],
            "% Recall": [],
            "F-" + str(beta): [],
            "Avg. actual": [],
            "Avg. predicted": [],
        }
    )
    for pred_col, label_col in col_correspondence.items():
        preds = np.array(total[pred_col])
        labels = np.array(total[label_col])
        error = np.mean(np.abs(preds - labels))
        correlation = np.corrcoef(preds, labels)[0, 1]
        # missed = (sum((preds == 0) & (labels > 0))/sum(labels > 0))*100
        if sum(preds > 0) != 0:
            precision = (sum((preds > 0) & (labels > 0)) / sum(preds > 0)) * 100
        else:
            precision = np.nan

        if sum(labels > 0) != 0:
            recall = (sum((preds > 0) & (labels > 0)) / sum(labels > 0)) * 100
        else:
            recall = np.nan

        fbeta = fbeta_score(labels > 0, preds > 0, beta=beta)

        df.loc[label_col] = [
            error,
            correlation,
            precision,
            recall,
            fbeta,
            np.mean(labels),
            np.mean(preds),
        ]
    return df
