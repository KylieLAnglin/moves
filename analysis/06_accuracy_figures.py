# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook


import statsmodels.formula.api as smf


from moves.library import start

label_list = ["Complex", "Simple", "Complex", "Simple", "Complex"]

# %%
df_long = pd.read_csv(start.DATA_PATH + "clean/final_long.csv")
df_wide = pd.read_csv(start.DATA_PATH + "clean/final_wide.csv")


df_summary = (
    df_long[["week", "coder", "context", "precision", "recall", "accuracy", "code"]]
    .groupby(by=["week", "coder", "context"])
    .mean()
)

summary = df_summary.groupby(["context"]).mean()
# There is no real difference in recall, out of context has slightly gigher.
# But there is a difference in precision. Out-of-context more likely to select yes.
# %%
plt.style.use("seaborn")


def myplot(outcome: str, ylabel: str, saveas: str, ymin, ymax):
    fig, ax = plt.subplots()
    ax.plot(
        [1, 2, 3, 4],
        df_summary.xs(1, level=1, drop_level=False)[outcome],
        color="black",
        linestyle="solid",
        label="Coder 1",
    )

    ax.plot(
        [2, 3, 4, 5],
        df_summary.xs(2, level=1, drop_level=False)[outcome],
        color="gray",
        linestyle="solid",
        label="Coder 2",
    )

    ax.plot(
        [1, 2, 3, 4],
        df_summary.xs(3, level=1, drop_level=False)[outcome],
        color="black",
        linestyle="dashed",
        label="Coder 3",
    )

    ax.plot(
        [2, 3, 4, 5],
        df_summary.xs(4, level=1, drop_level=False)[outcome],
        color="gray",
        linestyle="dashed",
        label="Coder 4",
    )

    plt.xlabel("Context")
    plt.ylabel(ylabel)
    plt.ylim(ymin, ymax)
    plt.xticks([1, 2, 3, 4, 5], labels=label_list)
    plt.legend()
    plt.savefig(start.RESULTS_PATH + saveas)


myplot("accuracy", "Accuracy", saveas="single_case_accuracy.png", ymin=0.9, ymax=1)
myplot("precision", "Precision", saveas="single_case_precision.png", ymin=0.5, ymax=1)
myplot("recall", "Recall", saveas="single_case_recall.png", ymin=0.5, ymax=1)


# 1:
# My preference was the out-of-context transcripts. Overall, it was easier to follow because I only had to focus on one move during the entire time. I felt as if I could get them done quicker than in context transcripts for the aforementioned reason. I thought the provided context was just enough to make an informed decision.

# 2:
# I thought I would prefer coding the out-of-context transcripts more because it was easy to just mark a 0 or 1 and then move on, but I preferred the in-context transcripts more. We only had eight options, so it was easy for me to remember what I should be looking for. The context also helped me understand the tone of the coaching conversation more, and it was helpful to see the progression of the coach's goals for the session.
# Coder 2 showed the most consistent pattern, which matched her preference.

# 3:
# My preference was definitely out-of-context transcripts. I think this was because if I knew that for that one transcript all I needed to focus was one thing (for example, positive encouragement), I felt like it was easier on my brain to focus solely on positive encouragement turns of talk, and I could find that one part in the turn of talk to identify. When there is a lot to look at, or multiple codes, sometimes it becomes overwhelming for me to be able to identify all of the codes in the turn of talk, or I forget some.

# 4:
# I preferred out of context transcripts as I felt it was easier to tell whether a code was present or not rather than trying to figure out which codes were present (like for in-context).

# %% Coder aggrement

incontext = df_wide[["ID", "week", "incontext_a", "incontext_b"]]
incontext["agree"] = np.where(incontext.incontext_a == incontext.incontext_b, 1, 0)

incontext_summary = incontext[["week", "agree"]].groupby(by=["week"]).mean()

outcontext = df_wide[["ID", "week", "outcontext_a", "outcontext_b"]]
outcontext["agree"] = np.where(outcontext.outcontext_a == outcontext.outcontext_b, 1, 0)

outcontext_summary = outcontext[["week", "agree"]].groupby(by=["week"]).mean()

fig, ax = plt.subplots()
ax.plot(
    [1, 2, 3, 4],
    incontext_summary.agree,
    color="black",
    linestyle="solid",
)
ax.plot(
    [2, 3, 4, 5],
    outcontext_summary.agree,
    color="gray",
    linestyle="solid",
)

plt.xlabel("Context")
plt.ylabel("Coder Agreement")
plt.ylim(0.9, 1)
plt.xticks([1, 2, 3, 4, 5], labels=label_list)
plt.savefig(start.RESULTS_PATH + "single_case_agreement")
