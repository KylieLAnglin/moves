# %%
from datetime import date


import pandas as pd
import numpy as np

from moves.library import start

# %%
file_date = date.today()
file_date = "2021-07-06"
print("File date:", file_date)

file_folder = start.IRR_PATH + "outputs/spotcheck_files/"

utterance_id = pd.read_csv(start.SHARED_PATH + "/utterance_id.csv")

filenames = [
    "af_anticipation_check",
    "na_check",
    "practice_check",
    "rapport_encouragement_check",
    "tb_observation_check",
    "tb_pos_eval_check",
    "tf_demonstration_check",
    "tf_instruction_check",
    "tf_suggestion_check",
]
# %%
df1 = pd.read_csv(file_folder + str(file_date) + " " + "af_anticipation_check" + ".csv")
df1["move"] = "anticipation"

df2 = pd.read_csv(file_folder + str(file_date) + " " + "practice_check" + ".csv")
df2["move"] = "practice"

df3 = pd.read_csv(
    file_folder + str(file_date) + " " + "rapport_encouragement_check" + ".csv"
)
df3["move"] = "rapport"

df4 = pd.read_csv(file_folder + str(file_date) + " " + "tb_observation_check" + ".csv")
df4["move"] = "observation"

df5 = pd.read_csv(file_folder + str(file_date) + " " + "tb_pos_eval_check" + ".csv")
df5["move"] = "positive_evaluation"

df6 = pd.read_csv(
    file_folder + str(file_date) + " " + "tf_demonstration_check" + ".csv"
)
df6["move"] = "demonstration"

df7 = pd.read_csv(file_folder + str(file_date) + " " + "tf_instruction_check" + ".csv")
df7["move"] = "instruction"

df8 = pd.read_csv(file_folder + str(file_date) + " " + "tf_suggestion_check" + ".csv")
df8["move"] = "suggestion"

df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8])

df = df.merge(
    utterance_id[["id", "doc", "turn_count", "Text"]],
    how="left",
    left_on="id",
    right_on="id",
)

df = df[
    [
        "week",
        "id",
        "doc",
        "turn_count",
        "text",
        "move",
        "coder_a_incontext",
        "coder_b_incontext",
        "coder_a_outcontext",
        "coder_b_outcontext",
    ]
]

df = df[(df.week == 1) | (df.week == 2)]
# %%
df["incontext_agree"] = np.where(df.coder_a_incontext == df.coder_b_incontext, 1, 0)

df["outcontext_agree"] = np.where(df.coder_a_outcontext == df.coder_b_outcontext, 1, 0)


df["all_agree"] = np.where(
    (df.coder_a_incontext == df.coder_b_incontext)
    & (df.coder_a_incontext == df.coder_a_outcontext)
    & (df.coder_a_outcontext == df.coder_b_outcontext),
    1,
    0,
)

df["any_positive"] = np.where(
    (df.coder_a_incontext == 1)
    | (df.coder_b_incontext == 1)
    | (df.coder_b_outcontext == 1)
    | (df.coder_b_outcontext == 1),
    1,
    0,
)

df["incontext_sum"] = df.coder_a_incontext + df.coder_b_incontext
df["outcontext_sum"] = df.coder_a_outcontext + df.coder_b_outcontext

df[
    [
        "week",
        "move",
        "doc",
        "all_agree",
        "any_positive",
        "incontext_sum",
        "outcontext_sum",
    ]
]


# %%
df["utterances"] = 1
df_sum = (
    df[
        [
            "week",
            "move",
            "utterances",
            "all_agree",
            "any_positive",
            "incontext_sum",
            "outcontext_sum",
        ]
    ]
    .groupby(by=["week", "move"])
    .sum()
)

df_sum = (
    df[
        [
            "move",
            "utterances",
            "all_agree",
            "any_positive",
            "incontext_sum",
            "outcontext_sum",
        ]
    ]
    .groupby(by=["move"])
    .sum()
)

df_sum_sum = df_sum.reset_index().groupby()
# %%
