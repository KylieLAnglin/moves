# %%
import random

import pandas as pd

from moves.library import start

random.seed(1991)

# Create a LOOONNNGGG dataframe with each turn of talk,
# it's position in the transcript, the transcript name
# and the speaker tag.

# %%

files = os.listdir(start.SHARED_PATH + "excel transcripts/")
files_xlsx = [f for f in files if f[-4:] == "xlsx"]

# %%
df = pd.DataFrame()

for filename in files_xlsx:
    file_path = start.SHARED_PATH + "excel transcripts/"
    data = pd.read_excel(file_path + filename)
    data["doc"] = filename
    df = df.append(data)

df = df[["doc", "Time-stamp", "Speaker", "Text"]]
df["turn_count"] = df.groupby("doc").cumcount()
df["speaker_turn_count"] = df.groupby(["doc", "Speaker"]).cumcount()
df["total_turn_count"] = df.reset_index().index

# Generate random document id
# Create indicator for whether turn of talk is eligible (coach and followed by another coach text)
# Give each eligible coach turn of talk an ID
# Select 5 coach turn of talk IDs
# Generate indicator for selected turns of talk and the followups
# Export turns with indicator to excel, along with random document ID (reset using cumcount() groupby doc) and speaker tags


selection = random.sample(range(len(df)), 5)

# %%
