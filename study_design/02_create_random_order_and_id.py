# %%
import random

import pandas as pd
import numpy as np

import xlsxwriter

from moves.library import start

run = 0



# %%
files = os.listdir(start.SHARED_PATH + "excel transcripts/")

if run {
# # Create random order of files for coding
random.seed(10)
random.shuffle(files)
random_df = pd.DataFrame(files)
random_df.to_csv(start.SHARED_PATH + "assignments.csv")

random_order = pd.read_csv(start.SHARED_PATH + "assignments.csv")

transcript_files = list(random_order["0"])
transcript_files = [f[:-4] + "xlsx" for f in transcript_files]

df = pd.DataFrame()
for filename in transcript_files:
    file_path = start.SHARED_PATH + "excel transcripts/"
    data = pd.read_excel(file_path + filename)
    data["doc"] = filename
    df = df.append(data)


df["turn_count"] = df.groupby("doc").cumcount()
df = df[["doc", "Time-stamp", "turn_count", "Speaker", "Text"]]
# %%
df["id"] = df.reset_index().index

df = df[["id", "doc", "turn_count", "Speaker", "Text"]]

df.to_csv(start.SHARED_PATH + "utterance_id.csv", index=False)
}

