import rioxarray as rx

import argparse
from utils import parse_bounds
from rasterio.warp import calculate_default_transform
import fsspec
import xarray as xr


def warp_resample(
    *,
    input_fp: str,
    srcSRS: str,
    width: int,
    height: int,
    dstSRS: str,
    outputBounds: tuple,
    write_netcdf: bool = False,
    virtualized: bool = False,
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
    if virtualized:
        input_fp = f"{input_fp.split(':')[1].split('.')[0]}.json"
        print(input_fp)
        fs = fsspec.filesystem("reference", fo=input_fp)
        m = fs.get_mapper("")
        ds = xr.open_dataset(
            m, engine="kerchunk", chunks={}
        )  # normal xarray.Dataset object, wrapping dask/numpy arrays etc.
        da = ds
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
    parser.add_argument(
        "--write-netcdf", default=False, type=bool, help="Write output to netcdf"
    )
    parser.add_argument(
        "--virtualized",
        default=False,
        type=bool,
        help="Input dataset has been virtualized",
    )

    args = parser.parse_args()
    warp_resample(
        input_fp=args.filename,
        srcSRS=args.srcSRS,
        dstSRS=args.dstSRS,
        width=args.tilesize,
        height=args.tilesize,
        outputBounds=args.outputBounds,
        write_netcdf=args.write_netcdf,
        virtualized=args.virtualized,
    )
