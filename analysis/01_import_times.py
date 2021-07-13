# %%
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from moves.library import start


# %% Extract time


def extract_times_in_context(folder_path: str, week: int, coder: int):
    incontext_time_df = pd.DataFrame(columns=["week", "coder", "transcript", "seconds"])

    for n in list(range(1, 11)):
        time_df = pd.read_excel(
            start.SHARED_PATH
            + "coding/"
            + folder_path
            + "Transcript"
            + str(n)
            + ".xlsx"
        ).head(1)[["Minutes", "Seconds"]]
        time_df["week"] = week
        time_df["coder"] = coder
        time_df["transcript"] = n
        time_df["seconds"] = time_df.Minutes * 60 + time_df.Seconds
        incontext_time_df = incontext_time_df.append(time_df)

    return incontext_time_df


# %%
incontext_times = pd.DataFrame(columns=["week", "coder", "transcript", "seconds"])

# Week 1
incontext_times = incontext_times.append(
    extract_times_in_context(
        folder_path="Week 1 Coder 1 In-Context/",
        week=1,
        coder=1,
    )
)

incontext_times = incontext_times.append(
    extract_times_in_context(
        folder_path="Week 1 Coder 3 In-Context/",
        week=1,
        coder=3,
    )
)

# Week 2
incontext_times = incontext_times.append(
    extract_times_in_context(
        folder_path="Week 2 Coder 2 In-Context/",
        week=2,
        coder=2,
    )
)

incontext_times = incontext_times.append(
    extract_times_in_context(
        folder_path="Week 2 Coder 4 In-Context/",
        week=2,
        coder=4,
    )
)

incontext_total_time = (
    incontext_times[["coder", "week", "seconds"]].groupby(by=["week", "coder"]).sum()
)

incontext_total_time = incontext_total_time.reset_index()
incontext_total_time["context"] = "in"
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


def extract_time_out_context(folder_path: str, week: int, coder: int):
    outcontext_time_df = pd.DataFrame(columns=["week", "coder", "move", "seconds"])
    for move in moves:
        time_df = pd.read_excel(
            start.SHARED_PATH + "coding/" + folder_path + move + ".xlsx"
        ).loc[0:0][["Minutes", "Seconds"]]

        time_df["week"] = week
        time_df["coder"] = coder
        time_df["move"] = move
        time_df["seconds"] = time_df.Minutes * 60 + time_df.Seconds
        outcontext_time_df = outcontext_time_df.append(time_df)

    return outcontext_time_df


outcontext_time = pd.DataFrame(columns=["week", "coder", "move", "seconds"])

outcontext_time = outcontext_time.append(
    extract_time_out_context(
        folder_path="Week 1 Coder 2 Out-of-Context/", week=1, coder=2
    )
)

outcontext_time = outcontext_time.append(
    extract_time_out_context(
        folder_path="Week 1 Coder 4 Out-of-Context/", week=1, coder=4
    )
)
outcontext_time = outcontext_time.append(
    extract_time_out_context(
        folder_path="Week 2 Coder 1 Out-of-Context/", week=2, coder=1
    )
)

outcontext_time = outcontext_time.append(
    extract_time_out_context(
        folder_path="Week 2 Coder 3 Out-of-Context/", week=2, coder=3
    )
)


outcontext_total_time = (
    outcontext_time[["coder", "week", "seconds"]].groupby(by=["week", "coder"]).sum()
)

outcontext_total_time = outcontext_total_time.reset_index()
outcontext_total_time["context"] = "out"

time = incontext_total_time.append(outcontext_total_time)

# %%
time["week"] = np.where(
    (((time.week == 1) & (time.context == "out"))), time.week + 1, time.week
)

time["week"] = np.where(
    (((time.week == 2) & (time.context == "in"))), time.week + 1, time.week
)
# %%
plt.style.use("seaborn")

fig, ax = plt.subplots()

for coder in range(5):
    ax.plot(
        time[(time.coder == coder)].week,
        time[(time.coder == coder)].seconds / 60,
        color="black",
    )


plt.xlabel("Week")
plt.ylabel("Minutes")
plt.xticks([1, 2, 3, 4], labels=["in", "out", "in", "out"])
ax.legend()
plt.show()


# %%
