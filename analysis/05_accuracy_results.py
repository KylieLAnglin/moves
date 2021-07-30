# %%
import pandas as pd
import numpy as np

from moves.library import start

# %%
df = pd.read_csv(start.DATA_PATH + "clean/final_full.csv")

# %%
coder1 = df[(df.week == 1) | (df.week == 3)][
    ["ID", "incontext_a", "week", "master", "move", "move_label"]
].rename(columns={"incontext_a": "code"})
coder1["context"] = "in"
coder1 = coder1.append(
    df[(df.week == 2) | (df.week == 4)][
        ["ID", "outcontext_a", "week", "master", "move", "move_label"]
    ].rename(columns={"outcontext_a": "code"})
)
coder1["context"] = np.where(coder1.context == "in", "in", "out")
coder1["correct"] = np.where(coder1.code == coder1.master, 1, 0)
coder1["coder"] = 1


coder2 = df[(df.week == 1) | (df.week == 3)][
    ["ID", "outcontext_a", "week", "master", "move", "move_label"]
].rename(columns={"outcontext_a": "code"})
coder2["context"] = "out"
coder2 = coder2.append(
    df[(df.week == 2) | (df.week == 4)][
        ["ID", "incontext_a", "week", "master", "move", "move_label"]
    ].rename(columns={"incontext_a": "code"})
)
coder2["context"] = np.where(coder2.context == "out", "out", "in")
coder2["correct"] = np.where(coder2.code == coder2.master, 1, 0)
coder2["coder"] = 2


coder3 = df[(df.week == 1) | (df.week == 3)][
    ["ID", "incontext_b", "week", "master", "move", "move_label"]
].rename(columns={"incontext_b": "code"})
coder3["context"] = "in"
coder3 = coder3.append(
    df[(df.week == 2) | (df.week == 4)][
        ["ID", "outcontext_b", "week", "master", "move", "move_label"]
    ].rename(columns={"outcontext_b": "code"})
)
coder3["context"] = np.where(coder3.context == "in", "in", "out")
coder3["correct"] = np.where(coder3.code == coder3.master, 1, 0)
coder3["coder"] = 3


coder4 = df[(df.week == 1) | (df.week == 3)][
    ["ID", "outcontext_b", "week", "master", "move", "move_label"]
].rename(columns={"outcontext_b": "code"})
coder4["context"] = "out"
coder4 = coder4.append(
    df[(df.week == 2) | (df.week == 4)][
        ["ID", "incontext_b", "week", "master", "move", "move_label"]
    ].rename(columns={"incontext_b": "code"})
)
coder4["context"] = np.where(coder4.context == "out", "out", "in")
coder4["correct"] = np.where(coder4.code == coder4.master, 1, 0)
coder4["coder"] = 4

df_full = pd.concat([coder1, coder2, coder3, coder4])[
    ["ID", "week", "coder", "context", "move", "code", "master"]
]
df_full["precision"] = np.where(df_full.code == 1, 0, np.nan)
df_full["precision"] = np.where(
    (df_full.master == 1) & (df_full.code == 1), 1, df_full.precision
)

df_full["recall"] = np.where(df_full.master == 1, 0, np.nan)
df_full["recall"] = np.where(
    (df_full.master == 1) & (df_full.code == 1), 1, df_full.recall
)

df_full["accuracy"] = np.where(df_full.code == df_full.master, 1, 0)

df_summary = (
    df_full[["week", "coder", "context", "precision", "recall", "accuracy"]]
    .groupby(by=["week", "coder", "context"])
    .mean()
)

summary = df_summary.groupby(["context"]).mean()
# %%
# df = time.sort_values(by="week")

# plt.style.use("seaborn")

# fig, ax = plt.subplots()

# ax.plot(df[df.coder == 1].week, df[df.coder == 1].seconds_per_100 / 60, color="black")
# ax.plot(df[df.coder == 3].week, df[df.coder == 3].seconds_per_100 / 60, color="black")

# ax.plot([2, 3, 4, 5], df[df.coder == 2].seconds_per_100 / 60, color="gray")
# ax.plot([2, 3, 4, 5], df[df.coder == 4].seconds_per_100 / 60, color="gray")

# plt.xlabel("Context")
# plt.ylabel("Minutes")
# plt.ylim(0, 240)
# plt.xticks([1, 2, 3, 4, 5], labels=["In", "Out", "In", "Out", "In"])
# ax.legend()
# plt.yticks([0, 30, 60, 90, 120, 150, 180, 210, 240])
# plt.savefig(start.RESULTS_PATH + "single_case_time.png")