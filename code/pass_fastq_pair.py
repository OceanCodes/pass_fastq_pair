import shutil
import sys
import subprocess
from glob import glob
from pathlib import Path

import config

fastq_dict = {}
pair_dict = {}


for path in glob(str(f"{config.dir_path}/**/*"), recursive=True):
    if Path(path).is_file():
        this_file = str(path)
        prefix = subprocess.run(["get_read_prefix.py", this_file], capture_output=True).stdout
        prefix = prefix.decode("utf-8").strip()
        if prefix in fastq_dict:
            if this_file not in fastq_dict[prefix]:
                fastq_dict[prefix].append(this_file)
            else:
                pass
                # there is some error in the pipelines mapping
        else:
            fastq_dict[prefix] = [this_file]

for k,v in fastq_dict.items():
    if len(v) == 3:
        # this is the pair to move into results folder
        for elem in v:
            parent_path = Path(elem).parent
            if parent_path in pair_dict:
                # as soon as 1 of the 2 possible keys has 2 elements, this is the key that has the 2 elements we want to move into the results folder.
                pair_dict[parent_path].append(elem)
                shutil.copy(pair_dict[parent_path][0], "../results")
                shutil.copy(pair_dict[parent_path][1], "../results")
                sys.exit()
            else:
                pair_dict[parent_path] = [elem]
        break

print("There were no reads files identified as a complementary pair to move into results. Please check your data as well as your mapping configuration in the pipelines UI.")
