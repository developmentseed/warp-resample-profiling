import argparse
import fsspec
import pandas as pd
import json


def parse_bounds(arg):
    try:
        return [float(i) for i in arg.split(",")]
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Output bounds should be formatted as (xmin,ymin,xmax,ymax)"
        )


def get_pyinstrument_results(results_dir):
    fs = fsspec.filesystem("file")
    return fs.glob(f"{results_dir}/pyinstrument*.json")


def get_memray_summaries(results_dir):
    fs = fsspec.filesystem("file")
    return fs.glob(f"{results_dir}/memray*.json")


def get_common_name(dataset_name):
    return dataset_name.replace("C1996881146-POCLOUD", "MUR SST").replace(
        "C2723754850-GES", "GPM IMERG"
    )


def get_test_info_from_filename(filepath):
    results_base = filepath.split("/")[-1]
    if "GES_DISC" in results_base:
        df = pd.DataFrame.from_records(
            [results_base.split("_")],
            columns=["test_id", "dataset", "_", "run_id", "x", "y", "zoom"],
        )
        df = df.drop(columns=["_"])
    elif "GHRSST" in results_base:
        metadata = results_base.split("-")
        _, method, location = metadata[0:3]
        dataset = "MUR SST"
    return method, location, dataset


def load_data(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return data


def process_results(summary_dir):
    df = pd.DataFrame()
    files = get_memray_summaries(summary_dir)
    for ind, file in enumerate(files):
        df.loc[ind, "output_file"] = file
        df.loc[ind, "method"], df.loc[ind, "location"], df.loc[ind, "dataset"] = (
            get_test_info_from_filename(file)
        )
        memray_summary = load_data(file)
        df.loc[ind, "peak memory (GB)"] = (
            memray_summary["metadata"]["peak_memory"] * 1e-9
        )
        pyinstrument_file = file.replace("memray", "pyinstrument")
        pyinstrument_data = load_data(pyinstrument_file)
        df.loc[ind, "duration (s)"] = pyinstrument_data["duration"]
    return df
