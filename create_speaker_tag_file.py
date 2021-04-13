import os
import fnmatch

import pandas as pd
from openpyxl import load_workbook

from moves.library import start

# %%


files = [file for file in os.listdir(start.TRANSCRIPTS_PATH) if fnmatch.fnmatch(file, "*docx")]

files.sort()
tag_file = pd.DataFrame({"doc": files})

# %%
# Merge previous tags
tags = pd.read_excel("/Users/kylie/Dropbox/moves/data/speaker_tags.xlsx")

tag_file = tags.merge(tag_file, how="left", left_on="doc", right_on="doc")
# %%
/Users/kylie/Dropbox/moves/data/speaker_tags.xlsx
tag_file.to_excel(path + "fall2019_speaker_tags.xlsx", index=False)
# %%
