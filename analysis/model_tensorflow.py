# %%
print("here")
# %%
import os
import numpy as np
import pandas as pd

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds

print("Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())
print("Hub version: ", hub.__version__)

# https://www.tensorflow.org/tutorials/keras/text_classification_with_hub
# %%
print("Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())
print("Hub version: ", hub.__version__)

from moves.library import start

# %%
code_df = pd.read_csv(start.DATA_PATH + "clean/" + "final_wide.csv")
text_df = pd.read_csv(start.SHARED_PATH + "utterance_id.csv")

df = code_df.merge(
    text_df[["id", "Text"]], left_on="ID", right_on="id", indicator="_merge2"
)

df = df[["ID", "move", "master", "Text"]]

# df["text"] = df.text.str.replace()
df.to_csv(start.DATA_PATH + "raw/utterances_for_cleaning.csv")
df = pd.read_csv(start.DATA_PATH + "raw/utterances_for_cleaning.csv")

df["text"] = df.Text.str.replace("  ", " ")
df["text"] = df.Text.str.replace("  ", " ")

df["text"] = [re.sub("[\(\[].*?[\)\]]", "", text) for text in df.text]

df = df[df.move == 2]

annotations = df.sample(len(df), random_state=5)

train_texts = list(annotations.text)
train_cats = list(annotations.master)

train_data = [(text, label) for text, label in zip(train_texts, train_cats)]

# %%
embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"
hub_layer = hub.KerasLayer(embedding, input_shape=[], dtype=tf.string, trainable=True)
hub_layer(annotations.text[:3])

# %%
