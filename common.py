from pathlib import Path
import pandas as pd
from evaluate_results import load_histo_file
import yaml


def get_root():
    return Path(__file__).parent


def get_full_path(filename, results_dir):

    return str(get_root() / results_dir / filename)


def get_config():
    try:
        with open('config.yaml') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        # If config.yaml does not exist, use app_config.yaml.
        # This is the case when running the app on Heroku.
        with open('app_config.yaml') as f:
            config = yaml.safe_load(f)
    return config

def load_results():
    # Get predictions.
    config = get_config()

    pred_file = config["results_files"][0]
    pred_df = load_histo_file(get_full_path(pred_file, config["results_dir"]))

    for result_file in config["results_files"][1:]:
        pred_histo = load_histo_file(get_full_path(result_file, config["results_dir"]))
        pred_df = pred_df.append(pred_histo)

    return pred_df


def get_rename_mapper():
    rename_mapper = {
        "deforestation 2000-2010": "loss 2000-2010 p",
        "deforestation 2010-2018": "loss 2010-2018 p",
        "forest 2000": "forest 2000 p",
        "forest 2010": "forest 2010 p",
        "forest 2018": "forest 2018 p",
        "% of Forest": "forest 2018 g",
        "% Forest Loss 2000-2010": "loss 2000-2010 g",
        "% Forest Loss 2010-2018": "loss 2010-2018 g",
    }
    return rename_mapper


def get_cols():
    rename_mapper = get_rename_mapper()
    cols = [
        "plotID",
        "pl_plotid",
        "lon",
        "lat",
        "Sub-Categories if Naturally regenerated forest",
        "Sub-Categories if Planted forest",
        *list(rename_mapper),
    ]
    return cols


def get_comparison(pred_df, gold_df, how):

    rename_mapper = get_rename_mapper()
    cols = get_cols()
    results_with_labels = pd.merge(
        pred_df, gold_df, how=how, left_on="plotID", right_on="pl_plotid"
    )[cols]
    results_with_labels = results_with_labels.rename(columns=rename_mapper)
    return results_with_labels


def exclude_unstocked(df):
    mask_planted_unstocked = df["Sub-Categories if Planted forest"] == "Temporarily unstocked planted forest"
    mask_unstocked = df["Sub-Categories if Naturally regenerated forest"] == "Temporarily unstocked forest"
    
    # Rows that are NOT unstocked nor planted unstocked
    return df[~(mask_unstocked | mask_planted_unstocked)]



