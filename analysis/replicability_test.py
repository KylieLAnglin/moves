# %%
import pandas as pd
import numpy as np

from moves.library import start

# %%
moves = [
    "1 TellBack Positive Evaluation",
    "2 Tellback Observation",
    "3 Tellforward Suggestion",
    "4 Tellforward Instruction",
    "5 Tellforward Demonstration",
    "6 Askforward Anticipation",
    "7 Practice",
    "8 Rapport Encouragement",
]

todd_naming_dict = {
    "6 Askforward Anticipation": "af_anticipation_check",
    "7 Practice": "practice_check",
    "8 Rapport Encouragement": "rapport_encouragement_check",
    "2 Tellback Observation": "tb_observation_check",
    "1 TellBack Positive Evaluation": "tb_pos_eval_check",
    "5 Tellforward Demonstration": "tf_demonstration_check",
    "4 Tellforward Instruction": "tf_instruction_check",
    "3 Tellforward Suggestion": "tf_suggestion_check",
}
# %% Import my version (start with 01)
n = 1
kylie_df = (
    pd.read_csv(start.DATA_PATH + "clean/" + moves[n - 1] + ".csv")
    .rename(columns={"ID": "id"})
    .set_index("id")
)

file_date = "2021-07-06"
todd_df = pd.read_csv(
    start.IRR_PATH
    + "outputs/spotcheck_files/"
    + file_date
    + " "
    + todd_naming_dict[moves[n - 1]]
    + ".csv"
).set_index("id")

todd_df = todd_df[(todd_df.week == 1) | (todd_df.week == 2)]
todd_df = todd_df[
    ~todd_df.index.isin([574, 423, 575, 572, 585, 568, 570, 591, 581, 583, 589, 461])
]

todd_df = todd_df.astype({"week": "int32"})
kylie_df = kylie_df.astype({"week": "int32", "incontext_b": "int64"})
kylie_df = kylie_df[~kylie_df.index.isin([461])]

# %%
compare_df = kylie_df.merge(
    todd_df, how="outer", indicator=True, left_index=True, right_index=True
)

compare_df = compare_df[
    [
        "week_x",
        "week_y",
        "text",
        "incontext_a",
        "coder_a_incontext",
        "incontext_b",
        "coder_b_incontext",
        "outcontext_a",
        "coder_a_outcontext",
        "outcontext_b",
        "coder_b_outcontext",
    ]
]
# %% Check replication

assert len(compare_df[compare_df.coder_a_incontext != compare_df.incontext_a]) == 0
assert len(compare_df[compare_df.coder_b_incontext != compare_df.incontext_b]) == 0
assert len(compare_df[compare_df.coder_a_outcontext != compare_df.outcontext_a]) == 0
assert len(compare_df[compare_df.coder_b_outcontext != compare_df.outcontext_b]) == 0

# %%
