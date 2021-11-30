# %%
import random

import pandas as pd
import numpy as np

import xlsxwriter

from moves.library import start


# %%
random_order = pd.read_csv(start.CC_PATH + "assignments.csv")

transcript_files = list(random_order["0"])
transcript_files = [f[:-4] + "xlsx" for f in transcript_files]

df = pd.read_csv(start.CC_PATH + "utterance_id.csv")

# %% Select 10 transcripts for coding
week0_list = list(transcript_files[0:1])
week1_list = list(transcript_files[1:11])
week2_list = list(transcript_files[11:21])
week3_list = list(transcript_files[52:57])
week4_list = list(transcript_files[58:63])

master_coding_list = week1_list + week2_list + week3_list + week4_list

master_transcripts = df[df.doc.isin(master_coding_list)]

# %%
def create_in_context_file(filepath: str, turns_df: pd.DataFrame):
    moves = [
        "1 TellBack Positive Evaluation",
        "2 Tellback Observation",
        "3 Tellforward Suggestion",
        "4 Tellforward Instruction",
        "5 Tellforward Demonstration",
        "6 Askforward Anticipation",
        "7 Practice",
        "8 Rapport Encouragement",
        "Teacher",
        "NA",
    ]

    transcript = 1
    for doc in set(turns_df.doc):

        transcript_df = turns_df[turns_df.doc == doc]

        # In Context
        workbook = xlsxwriter.Workbook(
            filepath + "Transcript" + str(transcript) + ".xlsx"
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
        worksheet.write("I3", "Mark as Question", bolded)

        start_row = 3
        col = 0
        for value in transcript_df.id:
            worksheet.write(start_row, col, value)
            start_row = start_row + 1

        start_row = 3
        col = 1
        for value in transcript_df.Speaker:
            worksheet.write(start_row, col, value)
            start_row = start_row + 1

        start_row = 3
        col = 2
        for value in transcript_df.Text:
            worksheet.write(start_row, col, value, wrapped)
            start_row = start_row + 1

        worksheet.data_validation(3, 3, 100, 7, {"validate": "list", "source": moves})

        transcript = transcript + 1

        workbook.close()


# %%
create_in_context_file(
    filepath=start.CC_PATH + "coding files/master coding/",
    turns_df=master_transcripts,
)

# %%
