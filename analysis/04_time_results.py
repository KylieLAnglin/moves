# %%

import pandas as pd
import matplotlib.pyplot as plt

from moves.library import start

time = pd.read_csv(start.DATA_PATH + "clean/" + "times.csv")


# %%
df = time.sort_values(by="week")

plt.style.use("seaborn")

fig, ax = plt.subplots()

ax.plot(df[df.coder == 1].week, df[df.coder == 1].seconds_per_100 / 60, color="black")
ax.plot(df[df.coder == 3].week, df[df.coder == 3].seconds_per_100 / 60, color="black")

ax.plot([2, 3, 4, 5], df[df.coder == 2].seconds_per_100 / 60, color="gray")
ax.plot([2, 3, 4, 5], df[df.coder == 4].seconds_per_100 / 60, color="gray")

plt.xlabel("Context")
plt.ylabel("Minutes")
plt.ylim(0, 240)
plt.xticks([1, 2, 3, 4, 5], labels=["In", "Out", "In", "Out", "In"])
ax.legend()
plt.yticks([0, 30, 60, 90, 120, 150, 180, 210, 240])
plt.savefig(start.RESULTS_PATH + "single_case_time.png")

# %%
