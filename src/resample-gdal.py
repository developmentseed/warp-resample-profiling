from osgeo import gdal
from pyproj.crs import CRS

import argparse
from utils import parse_bounds

gdal.UseExceptions()


def warp_resample(
    *,
    input_fp: str,
    output_format: str,
    width: int,
    height: int,
    dstSRS: str,
    outputBounds: tuple,
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
    """
    if output_format == "MEM":
        output = ""
    elif output_format == "netCDF":
        output = "output/gdal-resampled.nc4"
    else:
        output = f"output/gdal-resampled.{output_format}"
    ds = gdal.GetDriverByName(output_format).Create(
        output, width, height, 1, gdal.GDT_Float32
    )
    gt = [
        outputBounds[0],
        (outputBounds[2] - outputBounds[0]) / width,
        0,
        outputBounds[3],
        0,
        -(outputBounds[3] - outputBounds[1]) / height,
    ]
    crs = CRS(dstSRS).to_wkt()
    ds.SetProjection(crs)
    ds.SetGeoTransform(gt)
    gdal.Warp(ds, input_fp, **kwargs)


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
    parser.add_argument("--format", required=True, help="Output format")
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
    args = parser.parse_args()
    warp_resample(
        input_fp=args.filename,
        srcSRS=args.srcSRS,
        dstSRS=args.dstSRS,
        width=args.tilesize,
        height=args.tilesize,
        output_format=args.format,
        outputBounds=args.outputBounds,
    )
