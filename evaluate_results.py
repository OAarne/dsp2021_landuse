#%%
import pandas as pd
import numpy as np
from typing import List, Dict
import matplotlib.pyplot as plt
import seaborn as sns

import argparse

# RESULTS_PATH = "results/Paraguay_results_1931.csv"

RESULTS_PATHS: List[str] = [
    "results/N_east_all.csv",
    "results/N_se_h1-cc80.csv",
    "results/indonesia_1_0200.csv",
    "results/indonesia_2_200.csv",
    "results/indonesia_2_180.csv"
]

#%%
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


#%%
def parse_histo_input(s: str):
    s_array = s[6:-1]
    return hist_to_percentage(eval(s_array))


#%%
def load_histo_file(path: str) -> pd.DataFrame:
    histo = pd.read_csv(path)
    for col in histo.columns:
        if "Histogram" in col:
            histo.loc[:, col.replace("Histogram", "")] = histo.loc[:, col].map(
                parse_histo_input
            )
    histo.loc[:, "plotID"] = histo.loc[:, "plotID"].astype(float)
    return histo


#%%
col_correspondence = {
    "deforestation 2000-2010": "% Forest Loss 2000-2010",
    "deforestation 2010-2018": "% Forest Loss 2010-2018",
}


def get_mae(total: pd.DataFrame, print_results=True) -> Dict[str, float]:
    maes = {}
    for pred_col, label_col in col_correspondence.items():
        preds = np.array(total[pred_col])
        labels = np.array(total[label_col])
        error = np.mean(np.abs(preds - labels))
        maes[label_col] = error
        if print_results:
            print(label_col)
            print("Mean absolute error")
            print(error)
            print("Average actual deforestation")
            print(np.mean(labels))
            print("Average predicted deforestation")
            print(np.mean(preds))
            print()
    return maes

def get_score_df(total: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with various summary statistics describing the results.

    "% of deforestation missed" refers to the percentage of
    hexes for which the model predicted 0 deforestation,
    out of all the hexes for which actual deforestation
    was greater than 0. This is a kind of false negative rate.
    """
    df = pd.DataFrame({"MAE": [], "Correlation": [], "% of deforestation missed": [], "% Precision": [], "Avg. actual": [], "Avg. predicted": []})
    for pred_col, label_col in col_correspondence.items():
        preds = np.array(total[pred_col])
        labels = np.array(total[label_col])
        error = np.mean(np.abs(preds - labels))
        correlation = np.corrcoef(preds, labels)[0, 1]
        missed = (sum((preds == 0) & (labels > 0))/sum(labels > 0))*100
        precision = sum((preds > 0) & (labels > 0))/sum(preds > 0)
        df.loc[label_col] = [error, correlation, missed, precision, np.mean(labels), np.mean(preds)]
    return df

#%%
def main():
    labels_df = pd.read_csv("label_CSVs/training_complete.csv")
    # labels_df.loc[:, "pl_plotid"] = labels_df.loc[:, "pl_plotid"].map(int)

    # total = pd.merge(histo, labels_df, how="inner", left_on="plotID", right_on="pl_plotid")

    score_dfs = {}
    for result_file in RESULTS_PATHS:
        print()
        print(result_file)
        print()
        histo = load_histo_file(result_file)
        total = pd.merge(
            histo, labels_df, how="inner", left_on="plotID", right_on="pl_plotid"
        )
        # get_mae(total)
        score_df = get_score_df(total)
        print(score_df)
        score_dfs[result_file] = score_df

#%%

# sns.catplot(score_dfs[RESULTS_PATHS[0]], kind="bar")

# sns.barplot(score_dfs[RESULTS_PATHS[0]])

def visualize_score_dfs(score_dfs):
    fig, axes = plt.subplots(nrows=len(RESULTS_PATHS), ncols=len(col_correspondence))
    for path in RESULTS_PATHS:
        print(path)
        plt.ylim((0, 50))
        for i in range(0, len(col_correspondence)):
            plt.bar(x=score_dfs[path].columns, height=score_dfs[path].iloc[0, :])
            plt.show()

#%%

# Idea for results: What fraction deforestation was missed?
