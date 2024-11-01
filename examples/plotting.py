# Load results
import hvplot.pandas  # noqa
from utils import process_results
from typing import Literal
import pandas as pd

pd.options.mode.chained_assignment = None

df = process_results("results")


def subset_dataset(
    dataset: Literal["mursst", "gpm_imerg"],
    local: bool = True,
    format: Literal["netcdf", "zarr"] = "netcdf",
):
    subset = df[df["format"] == format]
    subset = subset[subset["dataset"] == dataset]
    if local:
        subset = subset[subset["virtual"] == "local"]
    else:
        subset = subset[subset["virtual"] != "local"]
    return subset.copy()


def plot_time(
    dataset: Literal["mursst", "gpm_imerg"],
    local: bool,
    format: Literal["netcdf", "zarr"] = "netcdf",
):
    subset = subset_dataset(dataset, local, format)
    subset = subset.groupby(["zoom", "method"])["duration (s)"].mean(numeric_only=True)
    if dataset == "mursst":
        dataset_title = "MUR SST"
    else:
        dataset_title = "GPM IMERG"
    if local:
        location = "(local file)"
    else:
        location = "(remote file on s3)"
    title = f"Duration for resampling {dataset_title} {location} (s)"
    plt = subset.hvplot.bar(
        width=1000,
        rot=90,
        color="teal",
        title=title,
        ylabel="Duration (s)",
        xlabel="Zoom level, Resampling library",
    )
    return plt


def plot_memory(
    dataset: Literal["mursst", "gpm_imerg"],
    local: bool,
    format: Literal["netcdf", "zarr"] = "netcdf",
):
    subset = subset_dataset(dataset, local, format)
    subset = subset.groupby(["zoom", "method"])["peak memory (GB)"].mean(
        numeric_only=True
    )
    if dataset == "mursst":
        dataset_title = "MUR SST"
    else:
        dataset_title = "GPM IMERG"
    if local:
        location = "(local file)"
    else:
        location = "(remote file on s3)"
    title = f"Peak memory allocation for resampling {dataset_title} {location}"
    plt = subset.hvplot.bar(
        width=1000,
        rot=90,
        color="teal",
        title=title,
        ylabel="'Peak memory (GB)",
        xlabel="Zoom level, Resampling library",
    )
    return plt


def plot_time_by_format(dataset: Literal["mursst", "gpm_imerg"], method: str = "odc"):
    subset = df[df["dataset"] == dataset]
    subset = subset[subset["virtual"] != "local"]
    subset = subset[subset["method"] == method]
    subset["format"] = subset.apply(
        lambda x: (
            f"{x['format']} (via icechunk)"
            if x["virtual"] == "icechunk"
            else x["format"]
        ),
        axis=1,
    )
    subset = subset.groupby(["zoom", "format"])["duration (s)"].mean(numeric_only=True)
    if dataset == "mursst":
        dataset_title = "MUR SST"
    else:
        dataset_title = "GPM IMERG"
    title = f"Duration for resampling {dataset_title}"
    plt = subset.hvplot.bar(
        width=1000,
        rot=90,
        color="teal",
        title=title,
        ylabel="Duration (s)",
        xlabel="Zoom level, Storage format",
    )
    return plt


def plot_memory_by_format(dataset: Literal["mursst", "gpm_imerg"], method: str = "odc"):
    subset = df[df["dataset"] == dataset]
    subset = subset[subset["virtual"] != "local"]
    subset = subset[subset["method"] == method]
    subset["format"] = subset.apply(
        lambda x: (
            f"{x['format']} (via icechunk)"
            if x["virtual"] == "icechunk"
            else x["format"]
        ),
        axis=1,
    )
    subset = subset.groupby(["zoom", "format"])["peak memory (GB)"].mean(
        numeric_only=True
    )
    if dataset == "mursst":
        dataset_title = "MUR SST"
    else:
        dataset_title = "GPM IMERG"
    title = f"Peak memory allocation for resampling {dataset_title}"
    plt = subset.hvplot.bar(
        width=1000,
        rot=90,
        color="teal",
        title=title,
        ylabel="'Peak memory (GB)",
        xlabel="Zoom level, Resampling library",
    )
    return plt


def plot_duration_by_weboptimization():
    subset = df[
        (df["dataset"] == "mursst")
        & ((df["method"] == "rasterio") | (df["method"] == "rioxarray"))
        & (df["driver"] != "h5netcdf")
        & (df["virtual"] != "local")
        & (df["format"] != "netcdf")
    ]
    subset["format"] = subset["format"].replace(
        {"cog": "COG", "weboptimizedzarr": "Web-Optimized Zarr", "zarr": "Zarr"}
    )
    subset["ID"] = subset.apply(
        lambda x: f"{x['format']} (resampled with {x['method']})", axis=1
    )
    subset = subset.groupby(["zoom", "ID"])["duration (s)"].mean(numeric_only=True)
    title = "Duration for resampling MUR SST"
    plt = subset.hvplot.bar(
        width=1000,
        height=500,
        rot=90,
        color="teal",
        title=title,
        ylabel="Duration (s)",
        xlabel="Zoom level, Format (resampling method)",
    )
    return plt


def plot_memory_by_weboptimization():
    subset = df[
        (df["dataset"] == "mursst")
        & ((df["method"] == "rasterio") | (df["method"] == "rioxarray"))
        & (df["driver"] != "h5netcdf")
        & (df["virtual"] != "local")
        & (df["format"] != "netcdf")
    ]
    subset["format"] = subset["format"].replace(
        {"cog": "COG", "weboptimizedzarr": "Web-Optimized Zarr", "zarr": "Zarr"}
    )
    subset["ID"] = subset.apply(
        lambda x: f"{x['format']} (resampled with {x['method']})", axis=1
    )
    subset = subset.groupby(["zoom", "ID"])["peak memory (GB)"].mean(numeric_only=True)
    title = "Peak memory allocation for resampling MUR SST"
    plt = subset.hvplot.bar(
        width=1000,
        height=500,
        rot=90,
        color="teal",
        title=title,
        ylabel="'Peak memory (GB)",
        xlabel="Zoom level, Format (resampling method)",
    )
    return plt
