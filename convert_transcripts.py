# %%
import os
import re
import fnmatch
import collections

import pandas as pd
import docx
from openpyxl import load_workbook

import random
from moves.library import start

# %%
def extract_paragraphs(doc_file: str):
    """Extracts paragraphs (new lines) from .docx file

    Args:
        doc_file (str): path to docx file

    Returns:
        [list]: list of text in paragraphs
    """
    doc = docx.Document(doc_file)

    paragraphs = [para.text for para in doc.paragraphs if len(para.text) > 0]

    return paragraphs


def extract_data_from_go_transcript(turns_of_talk: list):
    time_stamp_regex = re.compile(r"\[[0-9:]*\]")
    time_stamps = [time_stamp_regex.findall(text) for text in turns_of_talk]
    turns_of_talk = [re.sub(time_stamp_regex, "", text) for text in turns_of_talk]

    speaker_tag_regex = re.compile(r"\S[a-z]+\:")
    speaker_tags = [speaker_tag_regex.findall(text) for text in turns_of_talk]
    turns_of_talk = [re.sub(speaker_tag_regex, "", text) for text in turns_of_talk]

    Transcript = collections.namedtuple(
        "Transcript", ["time_stamps", "speaker_tags", "text"]
    )

    transcript = Transcript(
        time_stamps=time_stamps, speaker_tags=speaker_tags, text=turns_of_talk
    )

    return transcript


def extract_data_from_otter_transcript(turns_of_talk: list):
    speaker_tags = []
    time_stamps = []
    texts = []
    turn = 6
    while turn < len(turns_of_talk):
        speaker_tags.append(turns_of_talk[turn][:-5])
        time_stamps.append(turns_of_talk[turn][-5:])
        turn = turn + 1

        texts.append(turns_of_talk[turn])
        turn = turn + 1

    Transcript = collections.namedtuple(
        "Transcript", ["time_stamps", "speaker_tags", "text"]
    )

    transcript = Transcript(
        time_stamps=time_stamps, speaker_tags=speaker_tags, text=texts
    )
    return transcript


def word_to_transcript(doc_file=str):
    paragraphs = extract_paragraphs(doc_file=doc_file)
    if "[0" in paragraphs[0]:
        return extract_data_from_go_transcript(turns_of_talk=paragraphs)
    if paragraphs[2] == "SUMMARY KEYWORDS":
        return extract_data_from_otter_transcript(turns_of_talk=paragraphs)

    else:
        print("error with " + doc_file)


# %%
def transcript_to_excel(transcript, excel_template: str, excel_file: str):

    wb = load_workbook(excel_template)
    ws = wb.active

    row = 2
    col = 1
    for time in transcript.time_stamps:
        ws.cell(row=row, column=col).value = str(time)
        row = row + 1

    row = 2
    col = 2
    for speaker in transcript.speaker_tags:
        ws.cell(row=row, column=col).value = str(speaker)
        row = row + 1

    row = 2
    col = 3
    for text in transcript.text:
        ws.cell(row=row, column=col).value = text
        row = row + 1

    wb.save(excel_file)


# %%

# PATH = "/Users/kylie/Dropbox/1 Projects/Coaching Moves/"
# doc_file = "29_c_Transcript-updated"

# transcript_to_excel(
#     excel_template=PATH + "template.xlsx",
#     doc_file=PATH + doc_file + ".docx",
#     excel_file=PATH + doc_file + ".xlsx",
# )

files = [
    filename
    for filename in os.listdir(start.MAIN_PATH + "uncoded transcripts/")
    if fnmatch.fnmatch(filename, "*.docx") and not filename.startswith("~$")
]

for filename in files:
    # paragraphs = extract_paragraphs(doc_file=start.TRANSCRIPTS_PATH + filename)
    # transcript = extract_data_from_go_transcript(turns_of_talk=paragraphs)
    transcript = word_to_transcript(doc_file=start.TRANSCRIPTS_PATH + filename)
    filename = filename[:-5]
    if transcript:
        transcript_to_excel(
            transcript=transcript,
            excel_template=start.MAIN_PATH + "template.xlsx",
            excel_file=start.MAIN_PATH + "excel transcripts/" + filename + ".xlsx",
        )


# %%

# Create random order of files for coding
random.seed(10)
random.shuffle(files)
random_df = pd.DataFrame(files)
random_df.to_csv(MAIN_PATH + "random_order.csv")


first_three = [
    "01_1920_02_2670167_22c_Transcript.docx",
    "2019_96_5C_Transcript.docx",
    "01_1920_01_2842293_12c_Transcript.docx",
]
for filename in first_three:
    filename = filename[:-5]
    print(filename)
    transcript_to_excel(
        excel_template=start.MAIN_PATH + "template.xlsx",
        doc_file=start.MAIN_PATH + "uncoded transcripts/" + filename + ".docx",
        excel_file=start.MAIN_PATH + "excel transcripts/" + filename + ".xlsx",
    )
