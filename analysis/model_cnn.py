# %%
# %%
import pandas as pd
import re

from moves.library import start

import spacy
from tqdm.auto import tqdm
from spacy.tokens import DocBin

nlp = spacy.load("en_core_web_sm")

code_df = pd.read_csv(start.DATA_PATH + "clean/" + "final_wide.csv")
text_df = pd.read_csv(start.CC_PATH + "utterance_id.csv")

from moves.library import train_classifier

# %%
df = code_df.merge(
    text_df[["id", "Text"]], left_on="ID", right_on="id", indicator="_merge2"
)

df = df[["ID", "move", "master", "Text"]]

df["text"] = df.Text.str.replace("  ", " ")
df["text"] = df.Text.str.replace("  ", " ")

df["text"] = [re.sub("[\(\[].*?[\)\]]", "", text) for text in df.text]

df = df[df.move == 3]

df[["ID", "master", "text"]].to_excel(
    start.DATA_PATH + "clean/move3_training_data.xlsx", index=False
)

# %%

annotations = df.sample(len(df), random_state=5)

train_texts = list(annotations.text)
train_cats = list(annotations.master)

train_data = [(text, label) for text, label in zip(train_texts, train_cats)]

# %%
# first we need to transform all the training data
# train_classifier.train(
#     texts=train_texts,
#     binary_cats=train_cats,
#     model="en_core_web_sm",
#     output_dir=start.MAIN_DIR + "models/move3-0.1",
# )

train_classifier.train(
    texts=train_texts,
    binary_cats=train_cats,
    model="en_core_web_sm",
    output_dir=start.MAIN_DIR + "models/move2-0.0",
)
# %%
