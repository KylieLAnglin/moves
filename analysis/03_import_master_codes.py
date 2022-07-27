# %%
import os

import pandas as pd
import numpy as np

from moves.library import start

MASTER_FILES = start.SHARED_PATH + "coding files/master coding/"

# %%
filenames = os.listdir(MASTER_FILES)
filenames = [filename for filename in filenames if filename.startswith("Transcript")]

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


def import_incontext(folder_path: str):
    transcript_df = pd.DataFrame(
        columns=[
            "ID",
            "Speaker",
            "Text",
            "Move 1",
            "Move 2",
            "Move 3",
            "Move 4",
            "Move 5",
            "Mark as Question",
        ]
    )
    for transcript in list(range(1, 31)):
        df = pd.read_excel(
            folder_path + "Transcript" + str(transcript) + ".xlsx",
            skiprows=2,
        )
        transcript_df = transcript_df.append(df)

    for n in list(range(1, 9)):
        move_num = "move" + str(n)
        transcript_df[move_num] = np.where(
            transcript_df[["Move 1", "Move 2", "Move 3", "Move 4", "Move 5"]]
            .isin([moves[n - 1]])
            .any(axis=1),
            1,
            0,
        )
    transcript_df = transcript_df[transcript_df.Speaker == "Coach"]
    return transcript_df


master_codes = import_incontext(folder_path=MASTER_FILES)

# %% Merge with coder files
final_full = pd.DataFrame(
    columns=[
        "ID",
        "week",
        "incontext_a",
        "incontext_b",
        "outcontext_a",
        "outcontext_b",
        "master",
    ]
)
for n in list(range(len(moves))):
    move_n = n + 1

    move_column = "move" + str(move_n)
    coders = pd.read_csv(start.DATA_PATH + "clean/" + moves[n] + ".csv")
    final = coders.merge(
        master_codes[["ID", move_column]].rename(columns={move_column: "master"})
    )
    final.to_csv(start.DATA_PATH + "clean/" + moves[n] + " Final" + ".csv", index=False)
    final["move"] = move_n
    final["move_label"] = moves[n]
    final_full = final_full.append(final)

# %% Add transcript ID
utterance_id = pd.read_csv(start.CC_PATH + "data/utterance_id.csv")

final_wide = final_full.merge(
    utterance_id[["id", "doc"]], left_on="ID", right_on="id", indicator=True
)
# %%

final_wide.to_csv(start.CC_PATH + "data/clean/" + "final_wide.csv", index=False)

# %%
