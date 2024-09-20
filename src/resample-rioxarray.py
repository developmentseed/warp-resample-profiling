import rioxarray as rx

import argparse
from utils import parse_bounds
from rasterio.warp import calculate_default_transform
import fsspec
import xarray as xr
import os

# Env variables from titiler performance tuning
os.environ["GDAL_CACHEMAX"] = "75%"
os.environ["GDAL_INGESTED_BYTES_AT_OPEN"] = "32768"
os.environ["GDAL_DISABLE_READDIR_ON_OPEN"] = "EMPTY_DIR"
os.environ["GDAL_HTTP_MERGE_CONSECUTIVE_RANGES"] = "YES"
os.environ["GDAL_HTTP_MULTIPLEX"] = "YES"
os.environ["GDAL_HTTP_VERSION"] = "2"
os.environ["VSI_CACHE"] = "TRUE"
os.environ["VSI_CACHE_SIZE"] = "536870912"


def warp_resample(
    *,
    input_fp: str,
    srcSRS: str,
    width: int,
    height: int,
    dstSRS: str,
    outputBounds: tuple,
    write_netcdf: bool = False,
    backend: str = False,
    default_cache_type: str = None,
    variable: str = None,
    **kwargs,
):
    """Warp resample using GDAL

    Args:
        input_fp (str): path to input dataset
        format (str): format of the output dataset
        width (int): width of the output array
        height (int): height of the output array
        dstSRS (str): target SRS
        outputBounds (tuple): bounds of the output array as (xmin, ymin, xmax, ymax)
        write_netcdf (bool): store output array to a NetCDF file
    """
    if backend == "kerchunk":
        fs = fsspec.filesystem("reference", fo=input_fp)
        m = fs.get_mapper("")
        ds = xr.open_dataset(
            m, engine="kerchunk"
        )  # normal xarray.Dataset object, wrapping dask/numpy arrays etc.
        da = ds
    elif backend == "h5netcdf":
        fs = fsspec.filesystem("s3", default_cache_type=default_cache_type)
        fo = fs.open(input_fp)
        da = xr.open_dataset(fo, engine="h5netcdf", lock=False)[variable]
    else:
        da = rx.open_rasterio(input_fp)  # , mask_and_scale=True)
    da = da.rio.write_crs(srcSRS)
    da = da.rio.clip_box(
        *outputBounds,
        crs=dstSRS,
    )
    dst_transform, w, h = calculate_default_transform(
        srcSRS,
        dstSRS,
        da.rio.width,
        da.rio.height,
        *da.rio.bounds(),
        dst_width=width,
        dst_height=height,
    )
    resampled = da.rio.reproject(dstSRS, shape=(h, w), transform=dst_transform)
    if write_netcdf:
        print("writing")
        resampled.to_netcdf("output/rioxarray-resampled.nc4", mode="w")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", "-f", required=True, help="File to resample")
    parser.add_argument("--srcSRS", required=True, help="Source SRS")
    parser.add_argument(
        "--dstSRS", required=True, default="EPSG:3857", help="Output SRS"
    )
    parser.add_argument(
        "--tilesize", required=True, default=256, help="Tile size", type=int
    )
    parser.add_argument(
        "--outputBounds",
        required=True,
        help="Output bounds as (xmin,ymin,xmax,ymax)",
        type=parse_bounds,
        default=[
            -20037508.342789244,
            -20037508.34278925,
            20037508.34278925,
            20037508.342789244,
        ],
    )
    parser.add_argument("--write-netcdf", action=argparse.BooleanOptionalAction)
    parser.add_argument(
        "--backend", choices=["gdal", "kerchunk", "h5netcdf"], default="gdal"
    )
    parser.add_argument("--caching", choices=["readahead", "none"], default=None)
    parser.add_argument("--variable", type=str, default=None)

    args = parser.parse_args()
    warp_resample(
        input_fp=args.filename,
        srcSRS=args.srcSRS,
        dstSRS=args.dstSRS,
        width=args.tilesize,
        height=args.tilesize,
        outputBounds=args.outputBounds,
        write_netcdf=args.write_netcdf,
        backend=args.backend,
        default_cache_type=args.caching,
        variable=args.variable,
    )
