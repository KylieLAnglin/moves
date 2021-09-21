# %%
import pandas as pd
import numpy as np
import re

import nltk
from moves.library import start

# %%


code_df = pd.read_csv(start.DATA_PATH + "clean/" + "final_wide.csv")
text_df = pd.read_csv(start.SHARED_PATH + "utterance_id.csv")


# %%
df = code_df.merge(
    text_df[["id", "Text"]], left_on="ID", right_on="id", indicator="_merge2"
)

df = df[["ID", "move", "master", "Text"]]

df["text"] = df.Text.str.replace("  ", " ")
df["text"] = df.Text.str.replace("  ", " ")

df["text"] = [re.sub("[\(\[].*?[\)\]]", "", text) for text in df.text]

df = df[df.move == 3]

# %%
tokenizer = nltk.tokenize.RegexpTokenizer(r"\w+")
df["tokens"] = [tokenizer.tokenize(text) for text in df.text]
# %%
df["length_of_utterance"] = [len(tokenizer.tokenize(text)) for text in df.text]

# %%
df = df[df.length_of_utterance > 0]

print(df.length_of_utterance.mean())
print(min(df.length_of_utterance))
print(max(df.length_of_utterance))
# %%

count_moves = code_df[["ID", "master"]].groupby(by=["ID"]).sum()
print(count_moves.master.mean())
count_moves.master.hist()
print(len(count_moves[count_moves.master > 4]))

# %%
