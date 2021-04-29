# %%
import random

import pandas as pd
from openpyxl import load_workbook


from moves.library import start

random_order = pd.read_csv(start.SHARED_PATH + "random_order.csv")

transcript_files = list(random_order.tail(5)["0"])
transcript_files = [f[:-4] + "xlsx" for f in transcript_files]

df = pd.DataFrame()

for filename in transcript_files:
    file_path = start.SHARED_PATH + "excel transcripts/"
    data = pd.read_excel(file_path + filename)
    data["doc"] = filename
    df = df.append(data)

df["turn_count"] = df.groupby("doc").cumcount()
df["speaker_turn_count"] = df.groupby(["doc", "Speaker"]).cumcount()
df["total_turn_count"] = df.reset_index().index

df = df[df.Speaker == "Coach"]
df = df.sample(len(df))

# %%
