# %%
import pandas as pd
from pathlib import Path

# from scipy.spatial import distance
import matplotlib.pyplot as plt
import seaborn as sns

from evaluate_results import load_histo_file

# %%
def get_root():
    return Path(__file__).parent


root = get_root()

pred_file = root / "results" / "finland_subset1_samples.csv"

# Get predictions
if not pred_file.exists():
    print("Downloading the prediction file.")
    import os

    os.system(
        "wget https://www.dropbox.com/s/4flndto7dztqeya/finland_subset1_samples.csv?dl=0 -O results/finland_subset1_samples.csv"
    )
else:
    print(f"{pred_file} exists already, no need to download it.")


df = load_histo_file(pred_file)
# Cast plotID to int.
df["plotID"] = df["plotID"].astype(int)

# Gold data
gold = pd.read_csv(
    Path("label_CSVs") / "training_complete.csv")

# %%


def get_lon_lat(plot_id):

    # Get lon of particular plot
    lon = gold[gold["smpl_plotid"] == plot_id]["lon"].iloc[0]
    lat = gold[gold["smpl_plotid"] == plot_id]["lat"].iloc[0]

    return lon, lat


def get_ee_point(plot_id):
    lon, lat = get_lon_lat(plot_id)
    ee = f"var point = ee.Geometry.Point([{lon}, {lat}])"
    return ee


def compare(plot_id):
    print(f"plotID: {plot_id}\n")
    print("Classification:")
    cols = [
        "deforestation 2000-2018",
        "deforestation 2010-2018",
        "forest 2000",
        "forest 2010",
        "forest 2018",
    ]
    for col in cols:
        data = df[df["plotID"] == plot_id][col]
        print(f"{data.name}: {data.iloc[0]}")
    print()

    print("Gold:")
    cols = ["% of Forest", "% Forest Loss 2000-2010", "% Forest Loss 2010-2018"]
    for col in cols:
        data = gold[gold["smpl_plotid"] == plot_id][col]
        print(f"{data.name}: {data.iloc[0]}")


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
    cols = ["plotID", *list(rename_mapper)]
    results_with_labels = pd.merge(
        pred_df, gold_df, how="inner", left_on="plotID", right_on="pl_plotid"
    )[cols]
    results_with_labels = results_with_labels.rename(columns=rename_mapper)
    return results_with_labels


# %%

# To get the code for a single point geometry for google earth engine
# print(get_ee_point(522687900))

# %%

comp = get_comparison(df, gold)

f_2018_g = comp[["plotID", "forest 2018 g", "forest 2018 p"]].sample(50)

print("Forest gold (g) vs predictions (p) with 50 randomly selected hexas: ")
print(f_2018_g)
print()

f_2018_p = comp[["plotID", "loss 2010-2018 g", "loss 2010-2018 p"]].sample(50)
print("Forest loss 2018 (g) vs predictions (p) with 50 randomly selected hexas: ")
print(f_2018_p)
print()

# cos_sim = 1 - distance.cosine(f_2018_g["forest 2018 g"], f_2018_g["forest 2018 p"])
# print(f"Cosine similarity between f 2018 gold and pred subset: {cos_sim}")
# %%

print("All the hexas where loss 2010-2018 > 20")
comp[comp["loss 2010-2018 g"] > 20][["plotID", "loss 2010-2018 g", "loss 2010-2018 p"]]

# %%
sns.histplot(comp["forest 2018 g"], bins=5)
plt.ylabel("Number of hexas")
plt.title("Forest in 2018 (gold)")
# %%
plt.title("Forest in 2018 (predictions)")
plt.ylabel("Number of hexas")
sns.histplot(comp["forest 2018 p"], bins=5)
# %%
plt.title("Forest loss 2010-2018 (gold)")
plt.ylabel("Number of hexas")
sns.histplot(comp["loss 2010-2018 g"], bins=5)

# %%
plt.title("Forest loss 2010-2018 (predictions)")
plt.ylabel("Number of hexas")
sns.histplot(comp["loss 2010-2018 p"], bins=5)
