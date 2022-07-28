# %%
import os
import re
import fnmatch
import collections
from numpy import NaN
import xlsxwriter

import pandas as pd
import docx

import random
from moves.library import start
from moves.library import process_transcripts
from moves.library import dictionary_tools

# %%
moves = pd.read_excel(start.SHARED_PATH + "-coaching moves/List of Moves.xlsx")
speaker_tags_df = pd.read_excel(start.DATA_PATH + "speaker_tags.xlsx")
speaker_tags = speaker_tags_df.set_index("doc").to_dict(orient="index")
speaker_tags = dictionary_tools.fold_nested_dictionary(speaker_tags, "coach")

# %%
types = list(moves.columns)
MOVES = []
for cat in types:
    for move in moves[cat]:
        if type(move) == str:
            MOVES.append(cat + " " + move)
# %%
filename = "01_1920_01_1154874_22c_Transcript.docx"
transcript = process_transcripts.word_to_transcript(
    doc_file=start.SHARED_PATH + "transcripts_for_coding/" + filename
)
transcript_df = process_transcripts.transcript_to_cleaned_df(transcript=transcript)
if filename in speaker_tags_df.doc:
    transcript_df.speaker = transcript_df.speaker.replace(
        speaker_tags[filename], "Coach:"
    )
# %%
doc_name = filename.replace(".docx", "").replace(".txt", "")
# In Context
workbook = xlsxwriter.Workbook(
    start.SHARED_PATH + "transcripts_to_excel/" + doc_name + ".xlsx"
)
worksheet = workbook.add_worksheet()

bolded = workbook.add_format({"bold": True, "italic": False})
wrapped = workbook.add_format({"color": "black", "underline": False, "text_wrap": True})
bolded_and_wrapped = workbook.add_format(
    {"color": "black", "bold": True, "text_wrap": True}
)
worksheet.set_column(2, 3, 30)
worksheet.set_column(15, 20, 30)


worksheet.write("A1", "ID", bolded)
worksheet.write("B1", "Time", bolded)
worksheet.write("C1", "Speaker", bolded)
worksheet.write("D1", "Text", bolded)
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

worksheet.write("O1", "Mark as Question", bolded)

start_row = 1
col = 0
for value in transcript_df.index:
    worksheet.write(start_row, col, str(value))
    start_row = start_row + 1

start_row = 1
col = 1
for value in transcript_df.time:
    worksheet.write(start_row, col, str(value))
    start_row = start_row + 1

start_row = 1
col = 2
for value in transcript_df.speaker:
    worksheet.write(start_row, col, value)
    start_row = start_row + 1

start_row = 1
col = 3
for value in transcript_df.text:
    worksheet.write(start_row, col, value, wrapped)
    start_row = start_row + 1

start_row = 1
col = 20
for move in MOVES:
    worksheet.write(start_row, col, move)
    start_row = start_row + 1
worksheet.data_validation(1, 4, 100, 13, {"validate": "list", "source": "=$U$2:$U$41"})

answers = ["never or rarely", "about half of the time", "most of the time"]
worksheet.write(
    "P1",
    "How frequently does the coach use brief interjections that indicate the coach is listening (e.g. yeah, uh-huh, okay)?",
    wrapped,
)
worksheet.data_validation("P2", {"validate": "list", "source": answers})

worksheet.write(
    "Q1",
    "To what extent is the coach’s responding to teacher questions throughout the conversation?",
    wrapped,
)
worksheet.data_validation("Q2", {"validate": "list", "source": answers})

worksheet.write(
    "R1",
    "To what extent is the coach’s responding to teacher questions throughout the conversation?",
    wrapped,
)
worksheet.data_validation("R2", {"validate": "list", "source": answers})

worksheet.write(
    "S1", "To what extent are Ask-Forward questions closed yes/no questions?", wrapped
)
worksheet.data_validation("S2", {"validate": "list", "source": answers})


workbook.close()

# %%
