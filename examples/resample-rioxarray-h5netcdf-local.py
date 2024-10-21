# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## Resampling with Rioxarray (Local storage, NetCDF file, H5NetCDF driver)

# %%
import argparse

import fsspec
import rasterio as rio  # noqa
import xarray as xr
from rasterio.warp import calculate_default_transform


# %%
def warp_resample(dataset):
    from common import earthaccess_args
    from common import target_extent as te

    # Define filepath, driver, and variable information
    args = earthaccess_args[dataset]
    src = f'earthaccess_data/{args["filename"]}'
    # Define source and target projection
    dstSRS = "EPSG:3857"
    srcSRS = "EPSG:4326"
    width = height = 256

    # Specify fsspec caching since default options don't work well for raster data
    fsspec_caching = {
        "cache_type": "none",
    }
    fs = fsspec.filesystem("file")
    with fs.open(src, **fsspec_caching) as f:
        # Open dataset
        da = xr.open_dataset(f, engine="h5netcdf", mask_and_scale=True)[
            args["variable"]
        ]
        if dataset == "gpm_imerg":
            # Transpose and rename dims to align with rioxarray expectations
            da = da.rename({"lon": "x", "lat": "y"}).transpose("time", "y", "x")
        # Set input dataset projection
        da = da.rio.write_crs(srcSRS)
        da = da.rio.clip_box(
            *te,
            crs=dstSRS,
        )
        # Define affine transformation from input to output dataset
        dst_transform, w, h = calculate_default_transform(
            srcSRS,
            dstSRS,
            da.rio.width,
            da.rio.height,
            *da.rio.bounds(),
            dst_width=width,
            dst_height=height,
        )
        # Reproject dataset
        return da.rio.reproject(dstSRS, shape=(h, w), transform=dst_transform)


# %%
if __name__ == "__main__":
    if "get_ipython" in dir():
        # Just call warp_resample if running as a Jupyter Notebook
        da = warp_resample("gpm_imerg")
    else:
        # Configure dataset via argpase if running via CLI
        parser = argparse.ArgumentParser(description="Set environment for the script.")
        parser.add_argument(
            "--dataset",
            default="mursst",
            help="Dataset to resample.",
            choices=["gpm_imerg", "mursst"],
        )
        user_args = parser.parse_args()
        da = warp_resample(user_args.dataset)

# %%
