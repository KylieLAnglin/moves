# %%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from moves.library import start

time = pd.read_csv(start.CC_PATH + "data/clean/" + "times.csv")


# %%
label_list = ["Complex", "Simple", "Complex", "Simple", "Complex"]

df = time.sort_values(by="week")

plt.style.use("seaborn")

# %%

fig, ax = plt.subplots()

ax.plot(
    df[df.coder == 1].week,
    df[df.coder == 1].seconds_per_utterance,
    color="black",
    linestyle="solid",
    label="Coder 1",
)


ax.plot(
    [2, 3, 4, 5],
    df[df.coder == 2].seconds_per_utterance,
    color="gray",
    linestyle="solid",
    label="Coder 2",
)

ax.plot(
    df[df.coder == 3].week,
    df[df.coder == 3].seconds_per_utterance,
    color="black",
    linestyle="dashed",
    label="Coder 3",
)

ax.plot(
    [2, 3, 4, 5],
    df[df.coder == 4].seconds_per_utterance,
    color="gray",
    linestyle="dashed",
    label="Coder 4",
)

plt.xlabel("Coding Scheme")
plt.ylabel("Seconds")
# plt.ylim(0, 240)
plt.xticks([1, 2, 3, 4, 5], labels=label_list)
ax.legend()
# plt.yticks([0, 30, 60, 90, 120, 150, 180, 210, 240])
plt.savefig(start.CC_PATH + "results/" + "single_case_time.png")

print(df[df.context == "out"].seconds_per_utterance.mean())
print(df[df.context == "in"].seconds_per_utterance.mean())


# %%
time_in_context = df[df.context == "in"]

time_out_context = df[df.context == "out"]

print(time_in_context.seconds_per_10.mean())  # 59 min 7 seconds
print(time_out_context.seconds_per_10.mean())  # 113 min 54 seconds

print(time_out_context.seconds_per_10.mean() - time_in_context.seconds_per_10.mean())
# %%

df_one_move_out_context = df
df_one_move_out_context["adjusted_seconds_per_utterance"] = np.where(
    df_one_move_out_context.context == "out",
    df_one_move_out_context.seconds_per_utterance / 8,
    df_one_move_out_context.seconds_per_utterance,
)


# %%
plt.style.use("seaborn")

fig, ax = plt.subplots()

ax.plot(
    df_one_move_out_context[df_one_move_out_context.coder == 1].week,
    df_one_move_out_context[
        df_one_move_out_context.coder == 1
    ].adjusted_seconds_per_utterance,
    color="black",
    linestyle="solid",
    label="Coder 1",
)


ax.plot(
    [2, 3, 4, 5],
    df_one_move_out_context[
        df_one_move_out_context.coder == 2
    ].adjusted_seconds_per_utterance,
    color="gray",
    linestyle="solid",
    label="Coder 2",
)

ax.plot(
    df_one_move_out_context[df_one_move_out_context.coder == 3].week,
    df_one_move_out_context[
        df_one_move_out_context.coder == 3
    ].adjusted_seconds_per_utterance,
    color="black",
    linestyle="dashed",
    label="Coder 3",
)

ax.plot(
    [2, 3, 4, 5],
    df_one_move_out_context[
        df_one_move_out_context.coder == 4
    ].adjusted_seconds_per_utterance,
    color="gray",
    linestyle="dashed",
    label="Coder 4",
)

plt.xlabel("Coding Scheme")
plt.ylabel("Seconds")
# plt.ylim(0, 240)
plt.xticks([1, 2, 3, 4, 5], labels=label_list)
ax.legend()
# plt.yticks([0, 30, 60, 90, 120, 150, 180, 210, 240])
plt.savefig(start.CC_PATH + "results/" + "single_case_time_per_code.png")


print(
    df_one_move_out_context[
        df_one_move_out_context.context == "in"
    ].adjusted_seconds_per_utterance.mean()
)
print(
    df_one_move_out_context[
        df_one_move_out_context.context == "out"
    ].adjusted_seconds_per_utterance.mean()
)
# %%
