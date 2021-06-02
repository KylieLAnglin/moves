# %%
import random

import pandas as pd
import numpy as np

import xlsxwriter

from moves.library import start


# %%
files = os.listdir(start.SHARED_PATH + "excel transcripts/")


# Create random order of files for coding
random.seed(10)
random.shuffle(files)
random_df = pd.DataFrame(files)
random_df.to_csv(start.SHARED_PATH + "assignments.csv")

random_order = pd.read_csv(start.SHARED_PATH + "assignments.csv")

transcript_files = list(random_order["0"])
transcript_files = [f[:-4] + "xlsx" for f in transcript_files]

# %%

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

df = pd.read_csv(start.SHARED_PATH + "utterance_id.csv")

# %%

coach_df = df[df.Speaker == "Coach"]
teacher_df = df[df.Speaker != "Coach"]
teacher_df["turn_count"] = teacher_df.turn_count + 1

teacher_df = teacher_df.rename(columns={"Text": "preceding_teacher_text"})

new_df = coach_df.merge(
    teacher_df[["preceding_teacher_text", "doc", "turn_count"]],
    how="left",
    left_on=["doc", "turn_count"],
    right_on=["doc", "turn_count"],
)
new_df = new_df[["id", "doc", "turn_count", "preceding_teacher_text", "Text"]]
new_df["preceding_teacher_text"] = np.where(
    new_df.preceding_teacher_text.isnull(), "None", new_df.preceding_teacher_text
)

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
# %% Select 10 transcripts for coding
week0_incontext_list = list(transcript_files[0:1])

week0_incontext = df[df.doc.isin(week0_incontext_list)]

# %%
week0_outcontext_list = list(transcript_files[1:2])

week0_outcontext = new_df[new_df.doc.isin(week0_outcontext_list)]
week0_outcontext = week0_outcontext.sample(len(week0_outcontext))


# %% Out-of-Context

for move in moves:
    workbook = xlsxwriter.Workbook(
        start.SHARED_PATH + "coding files/Week 0 Out-of-Context/" + move + ".xlsx"
    )
    worksheet = workbook.add_worksheet()

    bolded = workbook.add_format({"bold": True, "italic": False})
    wrapped = workbook.add_format(
        {"color": "black", "underline": False, "text_wrap": True}
    )
    bolded_and_wrapped = workbook.add_format(
        {"color": "black", "bold": True, "text_wrap": True}
    )
    worksheet.set_column(1, 2, 30)
    worksheet.set_column(0, 0, 20)

    worksheet.write(
        "A2",
        "TIME SPENT CODING IN MINUTES (B2) TO THE NEAREST SECOND (D2)",
        bolded_and_wrapped,
    )
    worksheet.write("B1", "Minutes", bolded)
    worksheet.write("C1", "Seconds", bolded)

    worksheet.write("A3", "MOVE: " + move, bolded)
    worksheet.write("A4", "ID", bolded)
    worksheet.write("B4", "Preceding Teacher Text", bolded)
    worksheet.write("C4", "Coach Text", bolded)
    worksheet.write("D4", "Code", bolded)

    start_row = 4
    col = 0
    for value in week0_outcontext.id:
        worksheet.write(start_row, col, value)
        start_row = start_row + 1

    start_row = 4
    col = 1
    for value in week0_outcontext.preceding_teacher_text:
        worksheet.write(start_row, col, value, wrapped)
        start_row = start_row + 1

    start_row = 4
    col = 2
    for value in week0_outcontext.Text:
        worksheet.write(start_row, col, value, wrapped)
        start_row = start_row + 1

    worksheet.data_validation(
        first_row=4,
        first_col=3,
        last_row=200,
        last_col=3,
        options={
            "validate": "integer",
            "criteria": "between",
            "minimum": 0,
            "maximum": 1,
            "input_title": "Enter 0 or 1:",
        },
    )

    workbook.close()

# %%
moves.append("NA")
transcript = 1
for doc in week0_incontext_list:

    transcript_df = df[df.doc == doc]

    # In Context
    workbook = xlsxwriter.Workbook(
        start.SHARED_PATH
        + "coding files/Week 0 In-Context/Transcript"
        + str(transcript)
        + ".xlsx"
    )
    worksheet = workbook.add_worksheet()

    bolded = workbook.add_format({"bold": True, "italic": False})
    wrapped = workbook.add_format(
        {"color": "black", "underline": False, "text_wrap": True}
    )
    bolded_and_wrapped = workbook.add_format(
        {"color": "black", "bold": True, "text_wrap": True}
    )
    worksheet.set_column(1, 2, 30)
    # worksheet.set_column(0, 0, 20)

    worksheet.write(
        "A2",
        "TIME SPENT CODING IN MINUTES (B2) TO THE NEAREST SECOND (D2)",
        bolded_and_wrapped,
    )
    worksheet.write("B1", "Minutes", bolded)
    worksheet.write("C1", "Seconds", bolded)

    worksheet.write("A3", "ID", bolded)
    worksheet.write("B3", "Speaker", bolded)
    worksheet.write("C3", "Text", bolded)

    worksheet.write("D3", "Move 1", bolded)
    worksheet.write("E3", "Move 2", bolded)
    worksheet.write("F3", "Move 3", bolded)
    worksheet.write("G3", "Move 4", bolded)
    worksheet.write("H3", "Move 5", bolded)

    start_row = 3
    col = 0
    for value in week0_incontext.id:
        worksheet.write(start_row, col, value)
        start_row = start_row + 1

    start_row = 3
    col = 1
    for value in week0_incontext.Speaker:
        worksheet.write(start_row, col, value)
        start_row = start_row + 1

    start_row = 3
    col = 2
    for value in week0_incontext.Text:
        worksheet.write(start_row, col, value, wrapped)
        start_row = start_row + 1

    worksheet.data_validation(3, 3, 100, 7, {"validate": "list", "source": moves})

    transcript = transcript + 1

    workbook.close()

# %%


# %%
