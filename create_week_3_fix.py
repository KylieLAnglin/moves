# %%
import pandas as pd
import fnmatch
import numpy as np

from moves.library import start

# %%
utterance_ids = pd.read_csv(start.SHARED_PATH + "utterance_id.csv")

# %% import in context files to get a list of transcripts by merging with utterance id.
files = [
    filename
    for filename in os.listdir(start.SHARED_PATH + "coding/Week 3 Coder 1 In-Context")
    if fnmatch.fnmatch(filename, "*.xlsx") and not filename.startswith("~$")
]

in_context = pd.DataFrame()
for file in files:

    df = pd.concat(
        pd.read_excel(
            start.SHARED_PATH + "coding/Week 3 Coder 1 In-Context/" + file,
            sheet_name=None,
            skiprows=2,
        ),
        ignore_index=True,
        sort=False,
    )

    # Appending excel files one by one
    in_context = in_context.append(df, ignore_index=True)


in_context = in_context.merge(
    utterance_ids[["id", "doc"]], how="left", left_on="ID", right_on="id"
)

in_context_transcripts = list(in_context.doc.unique())

# %% import out of context files to get list of transcripts
out_context = pd.read_excel(
    start.SHARED_PATH
    + "coding/Week 3 Coder 2 Out-of-Context/1 TellBack Positive Evaluation.xlsx",
    skiprows=3,
)

out_context = out_context.merge(
    utterance_ids[["id", "doc"]], how="left", left_on="ID", right_on="id"
)

out_context_transcripts = list(out_context.doc.unique())
# %% Big list of utterances
df = pd.read_csv(start.SHARED_PATH + "utterance_id.csv")

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

# %% Create new week 4 assignments
# start.SHARED_PATH + "/coding files/Week 4 In-Context /"
new_week_4_out_of_context = new_df[new_df.doc.isin(in_context_transcripts)]
new_week_4_out_of_context = new_week_4_out_of_context.sample(
    len(new_week_4_out_of_context), random_state=5
)


def create_out_of_context_files(filepath: str, turns_df: pd.DataFrame):
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

    for move in moves:
        workbook = xlsxwriter.Workbook(filepath + move + ".xlsx")
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
        worksheet.write("E4", "Mark as Question", bolded)

        start_row = 4
        col = 0
        for value in turns_df.id:
            worksheet.write(start_row, col, value)
            start_row = start_row + 1

        start_row = 4
        col = 1
        for value in turns_df.preceding_teacher_text:
            worksheet.write(start_row, col, value, wrapped)
            start_row = start_row + 1

        start_row = 4
        col = 2
        for value in turns_df.Text:
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


create_out_of_context_files(
    start.SHARED_PATH + "/coding files/Week 4 Out-of-Context NEW/",
    turns_df=new_week_4_out_of_context,
)

# %%
new_week_4_in_context = df[df.doc.isin(out_context_transcripts)]


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


create_in_context_file(
    filepath=start.SHARED_PATH + "coding files/Week 4 In-Context NEW/",
    turns_df=new_week_4_in_context,
)
# %%
