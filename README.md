## Overview

This repository and the accompanying Quarto book contains examples of using warp resampling / reprojection methods in Python, along with memory and statistical wall-time profiling results.

## Memory and time profiling

Resampling and reprojection (i.e., warp resampling) are essential steps for generating raster tiles for browser based visualization. Further, warp resampling is often one of the most time consuming and memory intensive portions of the tile generation process. The importance and complexity of this step motivates an exploration of different warp resampling options.

### Goals

Compare memory and time performance for generating Web Mercator Quad Tree raster tiles from one timestep and variable of the MUR SST and GPM IMERG dataset using the following approaches:

- [osgeo.warp](https://gdal.org/en/latest/api/python/utilities.html#osgeo.gdal.Warp)
- [rasterio.warp.reproject](https://rasterio.readthedocs.io/en/stable/api/rasterio.warp.html#rasterio.warp.reproject)
- [rioxarray.reproject](https://corteva.github.io/rioxarray/html/rioxarray.html#rioxarray.raster_array.RasterArray.reproject)
- [pyresample.resample_blocks](https://pyresample.readthedocs.io/en/stable/api/pyresample.html#pyresample.resampler.resample_blocks)
- [xesmf.Regridder](https://xesmf.readthedocs.io/en/stable/user_api.html#xesmf.frontend.Regridder)
- [geoutils.Raster.reproject](https://geoutils.readthedocs.io/en/stable/gen_modules/geoutils.Raster.reproject.html#geoutils.Raster.reproject)
- [raster_tools.warp.reproject](https://um-rmrs.github.io/raster_tools/reference/generated/raster_tools.warp.reproject.html)
- [odc.geo.xr.xr_reproject](https://odc-geo.readthedocs.io/en/latest/_api/odc.geo.xr.xr_reproject.html)
- [xcube.resampling](https://xcube.readthedocs.io/en/latest/api.html#cube-resampling)
- [geowombat.config.update](https://geowombat.readthedocs.io/en/latest/tutorial-crs.html#transforming-a-crs-on-the-fly)
- [xcdat.regridder.regrid2.Regrid2Regridder](https://xcdat.readthedocs.io/en/latest/generated/xcdat.regridder.regrid2.Regrid2Regridder.html#xcdat.regridder.regrid2.Regrid2Regridder)

Out-of-scope:

- [xarray-regrid](https://github.com/EXCITED-CO2/xarray-regrid/) - only regrids within the same rectilinear coordinate system
- [weatherbench2/regridding](https://github.com/google-research/weatherbench2/blob/main/weatherbench2/regridding.py) - only seems to regrid within the same rectilinear coordinate system
- [dinosaur](https://github.com/google-research/dinosaur/blob/67c686945a8e4dd24ab23bcee806ce69c8d4f853/dinosaur/horizontal_interpolation.py#L241) - only seems to regrid within the same rectilinear coordinate system
- [pygmt.grdproject](https://www.pygmt.org/latest/api/generated/pygmt.grdproject.html#pygmt.grdproject) - [web mercator not amongst supported projections](https://www.pygmt.org/latest/projections/index.html)
- [verde](https://www.fatiando.org/verde/latest/) - not used for raster -> raster resampling (only points -> raster)

These methods will be run on the full resolution dataset. Nearest neighbor interpolation will be used for the first comparison. For simplicity, the amount of time necessary to generate a resampled array and the maximum amount of heap memory allocated will be measured. We also compare results when using a virtual dataset (e.g., VRT, Kerchunk reference file), when reading from a dataset stored locally versus in cloud object storage, and when using a cloud-optimized dataset (Zarr.)

### Possible extensions

- Compare other resampling methods (e.g., bilinear, conservative).
- Compare with methods that don't rely on existing packages (e.g., [Conservative regridding with Xarray, GeoPandas, and Sparse](https://discourse.pangeo.io/t/conservative-region-aggregation-with-xarray-geopandas-and-sparse/2715) and [KDTree wrappers](https://github.com/arctic-carbon/eddy-footprint/blob/46935785ced10f24263cd740f81b0aaf02d9bf33/eddy_footprint/spatial.py#L38-L45)).

### Environment Setup

The notebooks can be run on a JupyterHub environment using the docker image `quay.io/developmentseed/warp-resample-profiling:latest`, which is created using `repo2docker` using the Dockerfile contained within the `binder` directory.

### Acknowledgements

This work was made possible through support from [NASA IMPACT](https://impact.earthdata.nasa.gov/). Numerous people have guided development, especially Aimee Barciauskas ([@abarciauskas-bgse](https://github.com/abarciauskas-bgse)), Justus Magin ([@keewis](https://github.com/keewis)), and Michael Sumner ([@mdsumner](https://github.com/mdsumner)). The resources page contains references for source information. Quarto configuration based on [Cloud Native Geospatial Formats Guide](https://github.com/cloudnativegeo/cloud-optimized-geospatial-formats-guide) and the Tile Benchmarking(https://developmentseed.org/tile-benchmarking/). All mistakes my own.
