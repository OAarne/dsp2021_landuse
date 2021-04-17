#%%
import pandas as pd
import random
#%%
data_path = "label_CSVs/complete.csv"
test_frac = 0.2

df = pd.read_csv(data_path, index_col=False)

test_set = df.groupby(by="Country").apply(lambda c: c.sample(frac=test_frac, random_state=123))

training_set_mask = df.index.isin(el[1] for el in test_set.index)
training_set_mask = [not val for val in training_set_mask]

training_set = df.loc[training_set_mask]

#%%

def prefix(prefix, path):
    path = path.split("/")
    path[-1] = prefix + path[-1]
    path = "/".join(path)
    return path

test_set.to_csv(prefix("test_", data_path), index=False)
training_set.to_csv(prefix("training_", data_path), index=False)

# test_set.to_csv
