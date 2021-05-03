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

# This is the one with not that good manual labels
# pred_file = root / "results" / "finland_subset1_samples.csv"

# This is the one with better manual labels
# pred_file = root / "results" / "finland_subset1_samples_2.csv"

# This is the one with jaxa + nasa labels
pred_file = root / "results" / "subset1_finland_auto.csv"

# Get predictions
if not pred_file.exists():
    print(f"File {pred_file} missing.")
    import sys; sys.exit()
    # import os

    # os.system(
    #     "wget https://www.dropbox.com/s/4flndto7dztqeya/finland_subset1_samples.csv?dl=0 -O results/finland_subset1_samples.csv"
    # )
else:
    print(f"{pred_file} exists already, no need to download it.")


df = load_histo_file(pred_file)
# Cast plotID to int.
df["plotID"] = df["plotID"].astype(int)

# Gold data
gold = pd.read_csv(Path("label_CSVs") / "training_complete.csv")

# %%


def get_lon_lat(plot_id):

    # Get lon of particular plot
    lon = gold[gold["pl_plotid"] == plot_id]["lon"].iloc[0]
    lat = gold[gold["pl_plotid"] == plot_id]["lat"].iloc[0]

    return lon, lat


def get_ee_point(plot_id, comp_df=None, i=""):
    lon, lat = get_lon_lat(plot_id)
    ee = f"var point{str(i)} = ee.Geometry.Point([{lon}, {lat}]);"
    
    try:
        info = (
            f"// plotID {plot_id} -- forest 2018 gold: {comp_df[comp_df['plotID'] == plot_id]['forest 2018 g'].iloc[0]}, "
            + f"forest 2018 model: {comp_df[comp_df['plotID'] == plot_id]['forest 2018 p'].iloc[0]}"
        )
        ee = info + "\n" + ee
    except TypeError:
        # comp_df was not specified, can't provide info.
        pass
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

comp = get_comparison(df, gold)

f_2018_g = comp[["plotID", "forest 2018 g", "forest 2018 p"]].sample(
    50, random_state=42
)

print("Forest gold (g) vs predictions (p) with 50 randomly selected hexas: ")
print(f_2018_g)
print()

# %%
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

# %%
# comp[comp['plotID'] == 520122608]['forest 2018 g'].iloc[0]
comp[comp["plotID"] == 520758938]["forest 2018 g"].iloc[0]

# %%

# To get the code for a single point geometry for google earth engine
print(get_ee_point(518200182, comp_df=comp))
# %%

# Get code snippet for a single plotID
get_ee_point(520122608)
# %%

# Get javascript code snippet for n hexas with the most difference.
n = 30

diff = (comp["forest 2018 g"]-comp["forest 2018 p"]).abs()
sorted_diff = diff.sort_values(axis=0, ascending=False)

js_snippets = [get_ee_point(x, comp, i) for i, x in enumerate(comp["plotID"][sorted_diff.index[0:n]])]
print("\n\n".join(js_snippets))


# %%



# %%
df.columns
# %%
gold = pd.read_excel("../finland_gold.xlsx", sheet_name="Raw data original")
gold["Forest Sub-Categories"].unique()
# %%
gold["Sub-Categories if Naturally regenerated forest"].unique()
# %%
gold["Sub-Categories if Planted forest"].unique()
# %%

comp.to_csv("percentage_results.csv", index=False)
# %%
comp.columns
# %%
