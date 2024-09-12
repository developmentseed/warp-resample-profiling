# Overview

Resampling and reprojection (i.e., warp resampling) are essential steps for generating raster tiles for browser based visualization. Further, warp resampling is often one of the most time consuming and memory intensive portions of the tile generation process. The importance and complexity of this step motivates an exploration of different warp resampling options.

## Goals

Compare memory and time performance for generating a zoom level 0 256 x 256 raster from one timestep and variable of the MUR SST dataset using the following approaches:

- [osgeo.warp](https://gdal.org/en/latest/api/python/utilities.html#osgeo.gdal.Warp)
- [rasterio.warp.reproject](https://rasterio.readthedocs.io/en/stable/api/rasterio.warp.html#rasterio.warp.reproject)
- [rioxarray.reproject](https://corteva.github.io/rioxarray/html/rioxarray.html#rioxarray.raster_array.RasterArray.reproject)
- [pyresample.resample_blocks](https://pyresample.readthedocs.io/en/stable/api/pyresample.html#pyresample.resampler.resample_blocks)
- [xesmf.Regridder](https://xesmf.readthedocs.io/en/stable/user_api.html#xesmf.frontend.Regridder)
- [geoutils.Raster.reproject](https://geoutils.readthedocs.io/en/stable/gen_modules/geoutils.Raster.reproject.html#geoutils.Raster.reproject)
- [raster_tools.warp.reproject](https://um-rmrs.github.io/raster_tools/reference/generated/raster_tools.warp.reproject.html)
- [odc.geo.xr.xr_reproject](https://odc-geo.readthedocs.io/en/latest/_api/)

Out-of-scope:

- [xarray-regrid](https://github.com/EXCITED-CO2/xarray-regrid/) - only regrids within the same rectilinear coordinate system
- [weatherbench2/regridding](https://github.com/google-research/weatherbench2/blob/main/weatherbench2/regridding.py) - only seems to regrid within the same rectilinear coordinate system

These methods will be run on the full resolution dataset as well as a 2x and 4x downsampled versions to better understand the time and memory complexity. Nearest neighbor interpolation will be used for the first comparison. For simplicity, the amount of time necessary to generate a resampled array and the maximum amount of heap memory allocated will be measured.

## Planned extensions

- Compare to results when using a virtual dataset (e.g., VRT, Kerchunk reference file).
- Compare results when reading from a dataset stored locally versus in cloud object storage.

## Possible extensions

- Compare other resampling methods (e.g., bilinear, conservative).
- Compare with methods that don't rely on existing packages (e.g., [Conservative regridding with Xarray, GeoPandas, and Sparse](https://discourse.pangeo.io/t/conservative-region-aggregation-with-xarray-geopandas-and-sparse/2715) and [KDTree wrappers](https://github.com/arctic-carbon/eddy-footprint/blob/46935785ced10f24263cd740f81b0aaf02d9bf33/eddy_footprint/spatial.py#L38-L45)).

## References

- [What's Next - Software - Regridding](https://discourse.pangeo.io/t/whats-next-software-regridding/3896)
- [Lazy regridding discussion](https://discourse.pangeo.io/t/can-a-reprojection-change-of-crs-operation-be-done-lazily-using-rioxarray/4468)
