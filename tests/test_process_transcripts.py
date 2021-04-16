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
from moves.library import process_transcripts

# %%
OTTER_TRANSCRIPT = "01_1920_02_2703418_22c_Transcript.docx"
transcript_hub = "01_1920_01_2842069_12c_Transcript.docx"
go_transcript = "12-2C.docx"
split_turns_transcript = "32-2C.docx"  # go transcript

test_paragraphs = process_transcripts.extract_paragraphs(
    start.TRANSCRIPTS_PATH + split_turns_transcript
)
test_transcript = process_transcripts.word_to_transcript(
    start.TRANSCRIPTS_PATH + split_turns_transcript
)

otter_paragraphs = process_transcripts.extract_paragraphs(
    start.TRANSCRIPTS_PATH + OTTER_TRANSCRIPT
)


def test_otter_transcript():
    transcript = process_transcripts.word_to_transcript(
        start.TRANSCRIPTS_PATH + OTTER_TRANSCRIPT
    )
    assert transcript.time_stamps[0] == "00:00"

    df = process_transcripts.transcript_to_cleaned_df(transcript)
    assert df.loc[0]["speaker"] == "Katie"
    assert df.loc[0]["time"] == "00:00"


# %%
