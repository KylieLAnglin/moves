# %%
import os
import re
import fnmatch
import collections
from numpy import NaN
import xlsxwriter
import numpy as np
import re
import pandas as pd
import docx

import random
from moves.library import start
from moves.library import process_transcripts
from moves.library import dictionary_tools

# %%
moves = pd.read_excel(start.SHARED_PATH + "-coaching moves/List of Moves.xlsx")
speaker_tags_df = pd.read_excel(start.SHARED_PATH + "speaker_tags.xlsx")
speaker_tags = speaker_tags_df.set_index("doc").to_dict(orient="index")
speaker_tags = dictionary_tools.fold_nested_dictionary(speaker_tags, "coach")

# %%
types = list(moves.columns)
MOVES = []
for cat in types:
    for move in moves[cat]:
        if type(move) == str:
            MOVES.append(cat + " " + move)


# %% Create df
def create_transcript_df(filepath, filename, extension):
    if extension == ".docx":
        # Word to transcript dict
        transcript = process_transcripts.word_to_transcript(
            doc_file=filepath + filename + extension
        )
    if extension == ".txt":
        transcript = process_transcripts.txt_to_transcript(
            filepath=filepath, filename=filename
        )
    # transcript dict to df
    transcript_df = process_transcripts.transcript_to_cleaned_df(transcript=transcript)
    transcript_df = transcript_df.reset_index().rename(columns={"index": "turn_count"})

    # fix speaker tags
    full_filename = filename + extension
    if full_filename in list(speaker_tags_df.doc):
        transcript_df = transcript_df.replace(
            speaker_tags[full_filename].replace(":", ""), "Coach"
        )

    # Create df with preceding utterance
    coach_df = transcript_df[transcript_df.speaker == "Coach"]
    teacher_df = transcript_df[transcript_df.speaker != "Coach"]
    teacher_df["turn_count"] = teacher_df.turn_count + 1

    teacher_df = teacher_df.rename(columns={"text": "preceding_teacher_text"})

    df = coach_df.merge(
        teacher_df[["preceding_teacher_text", "turn_count"]],
        how="left",
        left_on=["turn_count"],
        right_on=["turn_count"],
    )
    df = df[["turn_count", "time", "preceding_teacher_text", "text"]]
    df["preceding_teacher_text"] = np.where(
        df.preceding_teacher_text.isnull(), "None", df.preceding_teacher_text
    )

    return df


# %%


def write_excel(output_path, filename, df):
    # Print workbook
    workbook = xlsxwriter.Workbook(output_path + filename + ".xlsx")
    worksheet = workbook.add_worksheet()

    bolded = workbook.add_format({"bold": True, "italic": False})
    wrapped = workbook.add_format(
        {"color": "black", "underline": False, "text_wrap": True}
    )
    bolded_and_wrapped = workbook.add_format(
        {"color": "black", "bold": True, "text_wrap": True}
    )
    worksheet.set_column(2, 3, 30)
    worksheet.set_column(15, 20, 30)

    worksheet.write("A1", "ID", bolded)
    worksheet.write("B1", "Time", bolded)
    worksheet.write("C1", "Preceding Teacher Text", bolded)
    worksheet.write("D1", "Coach Text", bolded)
    worksheet.write("E1", "Move 1", bolded)
    worksheet.write("F1", "Move 2", bolded)
    worksheet.write("G1", "Move 3", bolded)
    worksheet.write("H1", "Move 4", bolded)
    worksheet.write("I1", "Move 5", bolded)
    worksheet.write("J1", "Move 6", bolded)
    worksheet.write("K1", "Move 7", bolded)
    worksheet.write("L1", "Move 8", bolded)
    worksheet.write("M1", "Move 9", bolded)
    worksheet.write("N1", "Move 10", bolded)

    worksheet.write("O1", "Additional Moves", bolded)
    worksheet.write("P1", "Notes", bolded)

    # id
    start_row = 1
    col = 0
    for value in df.index:
        worksheet.write(start_row, col, str(value))
        start_row = start_row + 1

    start_row = 1
    col = 1
    for value in df.time:
        worksheet.write(start_row, col, str(value))
        start_row = start_row + 1

    start_row = 1
    col = 2
    for value in df.preceding_teacher_text:
        worksheet.write(start_row, col, value, wrapped)
        start_row = start_row + 1

    start_row = 1
    col = 3
    for value in df.text:
        worksheet.write(start_row, col, value, wrapped)
        start_row = start_row + 1

    # Print moves for validation
    start_row = 1
    col = 25
    for move in MOVES:
        worksheet.write(start_row, col, move)
        start_row = start_row + 1

    # Add move validation
    worksheet.data_validation(
        1, 4, 100, 13, {"validate": "list", "source": "=$Z$2:$Z$41"}
    )

    answers = ["never or rarely", "about half of the time", "most of the time"]
    worksheet.write(
        "Q1",
        "How frequently does the coach use brief interjections that indicate the coach is listening (e.g. yeah, uh-huh, okay)?",
        wrapped,
    )
    worksheet.data_validation("Q2", {"validate": "list", "source": answers})

    worksheet.write(
        "R1",
        "To what extent is the coach responding to teacher questions throughout the conversation?",
        wrapped,
    )
    worksheet.data_validation("R2", {"validate": "list", "source": answers})

    worksheet.write(
        "S1",
        "To what extent are the coach's Ask-Back questions closed, yes/no questions?",
        wrapped,
    )
    worksheet.data_validation("S2", {"validate": "list", "source": answers})

    worksheet.write(
        "T1",
        "To what extent are the coach's Ask-Forward questions closed, yes/no questions?",
        wrapped,
    )
    worksheet.data_validation("T2", {"validate": "list", "source": answers})

    workbook.close()


# %% Test
filename = "2019_96_5C_Transcript"
filepath = start.SHARED_PATH + "transcripts_for_coding/"
output_path = start.SHARED_PATH + "transcripts_to_excel/"
df = create_transcript_df(filepath=filepath, filename=filename, extension=".docx")
write_excel(output_path=output_path, filename=filename, df=df)


# %% Word files
files = [
    filename.replace(".docx", "")
    for filename in os.listdir(start.SHARED_PATH + "transcripts_for_coding/")
    if fnmatch.fnmatch(filename, "*.docx") and not filename.startswith("~$")
]
short = []
for filename in files:
    filepath = start.SHARED_PATH + "transcripts_for_coding/"
    output_path = start.SHARED_PATH + "transcripts_to_excel/"
    df = create_transcript_df(filepath=filepath, filename=filename, extension=".docx")
    if len(df) < 3:
        short.append(filename)
    write_excel(output_path=output_path, filename=filename, df=df)

# %% Clean txt files
filename = "01_004_22c_032.txt"
doc_name = filename.replace(".txt", "")
filepath = start.SHARED_PATH + "transcripts_for_coding/"
output_path = start.SHARED_PATH + "transcripts_to_excel/"
# df = create_transcript_df(filepath=filepath, filename=filename, input="word")
# write_excel(output_path=output_path, doc_name=doc_name, df=df)
files = [
    filename.replace(".txt", "")
    for filename in os.listdir(start.SHARED_PATH + "transcripts_for_coding/")
    if fnmatch.fnmatch(filename, "*.txt") and not filename.startswith("~$")
]
for filename in files:
    doc_name = filename.replace(".txt", "")
    filepath = start.SHARED_PATH + "transcripts_for_coding/"
    output_path = start.SHARED_PATH + "transcripts_to_excel/"
    df = create_transcript_df(filepath=filepath, filename=filename, extension=".txt")
    if len(df) < 3:
        short.append(filename)
    write_excel(output_path=output_path, filename=doc_name, df=df)
# %%
