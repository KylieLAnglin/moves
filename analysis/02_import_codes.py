# %%
import pandas as pd
import numpy as np

from moves.library import start

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

# %% Append all Coder 1 Week 1 Files

folder_path = "Week 1 Coder 1 In-Context/"


def import_incontext(folder_path: str, week: int, coder: int):
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
    for transcript in list(range(1, 11)):
        df = pd.read_excel(
            start.SHARED_PATH
            + "coding/"
            + folder_path
            + "Transcript"
            + str(transcript)
            + ".xlsx",
            skiprows=2,
        )
        print(len(df))
        transcript_df = transcript_df.append(df)
    transcript_df["week"] = week
    transcript_df["coder"] = coder

    for n in list(range(1, 9)):
        print(moves[n - 1])
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


week1_coder1 = import_incontext(
    folder_path="Week 1 Coder 1 In-Context/", week=1, coder=1
)

week1_coder3 = import_incontext(
    folder_path="Week 1 Coder 3 In-Context/", week=1, coder=3
)


week2_coder2 = import_incontext(
    folder_path="Week 2 Coder 2 In-Context/", week=2, coder=2
)

week2_coder4 = import_incontext(
    folder_path="Week 2 Coder 4 In-Context/", week=2, coder=4
)

incontext_a = week1_coder1.append(week2_coder2)[
    [
        "ID",
        "week",
        "coder",
        "move1",
        "move2",
        "move3",
        "move4",
        "move5",
        "move6",
        "move7",
        "move8",
    ]
]

incontext_b = week1_coder3.append(week2_coder4)[
    [
        "ID",
        "week",
        "coder",
        "move1",
        "move2",
        "move3",
        "move4",
        "move5",
        "move6",
        "move7",
        "move8",
    ]
]

# %% Merge out of context files
def import_outcontext(folder_path: str, week: int, coder: int):
    move = moves[0]
    coder_df = pd.read_excel(
        start.SHARED_PATH + "coding/" + folder_path + move + ".xlsx",
        skiprows=3,
    ).rename(columns={"Code": "move1", "ID 3": "ID", "ID 3 ": "ID"})[
        ["ID", "Coach Text", "move1"]
    ]

    for n in list(range(2, 9)):
        move = moves[n - 1]
        df = pd.read_excel(
            start.SHARED_PATH + "coding/" + folder_path + move + ".xlsx",
            skiprows=3,
        ).rename(columns={"Code": "move" + str(n), "ID 3": "ID", "ID 3 ": "ID"})[
            ["ID", "move" + str(n)]
        ]
        coder_df = coder_df.merge(df, on=["ID"])

    coder_df["week"] = week
    coder_df["coder"] = coder

    return coder_df


week1_coder2 = import_outcontext(
    folder_path="Week 1 Coder 2 Out-of-Context/", week=1, coder=2
)

week1_coder4 = import_outcontext(
    folder_path="Week 1 Coder 4 Out-of-Context/", week=1, coder=4
)

week2_coder1 = import_outcontext(
    folder_path="Week 2 Coder 1 Out-of-Context/", week=2, coder=1
)

week2_coder3 = import_outcontext(
    folder_path="Week 2 Coder 3 Out-of-Context/", week=2, coder=3
)

outcontext_a = week1_coder2.append(week2_coder1)
outcontext_b = week1_coder4.append(week2_coder3)

# %%
def merge_coders(move: str):
    move_dict = {
        "1 TellBack Positive Evaluation": "move1",
        "2 Tellback Observation": "move2",
        "3 Tellforward Suggestion": "move3",
        "4 Tellforward Instruction": "move4",
        "5 Tellforward Demonstration": "move5",
        "6 Askforward Anticipation": "move6",
        "7 Practice": "move7",
        "8 Rapport Encouragement": "move8",
    }
    incontext_a_df = incontext_a[["ID", "week", move_dict[move]]].rename(
        columns={move_dict[move]: "incontext_a"}
    )

    incontext_b_df = incontext_b[["ID", move_dict[move]]].rename(
        columns={move_dict[move]: "incontext_b"}
    )

    outcontext_a_df = outcontext_a[["ID", move_dict[move]]].rename(
        columns={move_dict[move]: "outcontext_a"}
    )

    outcontext_b_df = outcontext_b[["ID", move_dict[move]]].rename(
        columns={move_dict[move]: "outcontext_b"}
    )

    move_df = incontext_a_df.merge(incontext_b_df, on=["ID"])
    move_df = move_df.merge(outcontext_a_df, on=["ID"])
    move_df = move_df.merge(outcontext_b_df, on=["ID"])

    return move_df


for n in list(range(1, 9)):
    move_df = merge_coders(move=moves[n - 1]).sort_values(by="ID")
    move_df.to_csv(start.DATA_PATH + "clean/" + moves[n - 1] + ".csv", index=False)


# %%
