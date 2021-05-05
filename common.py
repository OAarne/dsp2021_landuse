import pandas as pd


def get_comparison(pred_df, gold_df):
    rename_mapper = {
        "deforestation 2000-2018": "loss 2000-2018 p",
        "deforestation 2010-2018": "loss 2010-2018 p",
        "forest 2000": "forest 2000 p",
        "forest 2010": "forest 2010 p",
        "forest 2018": "forest 2018 p",
        "% of Forest": "forest 2018 g",
        "% Forest Loss 2000-2010": "loss 2000-2018 g",
        "% Forest Loss 2010-2018": "loss 2010-2018 g",
    }
    cols = ["plotID", "lon", "lat", "Sub-Categories if Naturally regenerated forest", "Sub-Categories if Planted forest", *list(rename_mapper)]
    results_with_labels = pd.merge(
        pred_df, gold_df, how="inner", left_on="plotID", right_on="pl_plotid"
    )[cols]
    results_with_labels = results_with_labels.rename(columns=rename_mapper)
    return results_with_labels