import subprocess
import pandas as pd
from pathlib import Path
import fsspec
import json


def sync_notebook(file):
    command = ["jupytext", "--sync", file]
    subprocess.run(command)


def get_files(folder):
    fs = fsspec.filesystem("file")
    return fs.glob(f"{folder}/memray*.json")


def get_test_info_from_filename(file):
    results_base = file.split(".")[0]
    _, task, method, driver, virtualization = results_base.split("-")
    return task, method, driver, virtualization


def load_data(filepath):
    with open(filepath) as f:
        return json.load(f)


def process_results(summary_dir):
    df = pd.DataFrame()
    files = get_files(summary_dir)
    for ind, file in enumerate(files):
        filename = Path(file).name
        print(filename)
        (
            df.loc[ind, "task"],
            df.loc[ind, "method"],
            df.loc[ind, "driver"],
            df.loc[ind, "virtual"],
        ) = get_test_info_from_filename(filename)
        memray_data = load_data(f"results/{filename}")
        df.loc[ind, "peak memory (GB)"] = memray_data["metadata"]["peak_memory"] * 1e-9
        pyinstrument_data = load_data(
            f"results/pyinstrument-{'-'.join(filename.split('-')[1:])}"
        )
        df.loc[ind, "duration (s)"] = pyinstrument_data["duration"]
    return df
