# %%
import pandas as pd
import fnmatch

from moves.library import start

# %%
speaker_tags = pd.read_excel(start.DATA_PATH + "speaker_tags.xlsx")

# %%

files = [
    filename
    for filename in os.listdir(start.SHARED_PATH + "transcripts_for_coding/")
    if fnmatch.fnmatch(filename, "*.docx") and not filename.startswith("~$")
]

speaker_tags_list = list(speaker_tags.doc)
# %%
missing_tags = []
for file in files:
    if file not in speaker_tags_list:
        missing_tags.append(file)
    # if file in speaker_tags_list:
    #     # print(file, " in list")

# %%
