#!/usr/bin/env bash

# File parameters
data_dir="earthaccess_data"
results_dir="results"
input_file_base="20020601090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1"
input_file="${data_dir}/${input_file_base}.nc"
input_dataset="NETCDF:${input_file}:analysed_sst"

# Processing methods
methods=("gdal")

# Common processing parameters
srcSRS="EPSG:4326"
dstSRS="EPSG:3857"
tilesize=256
output_bounds="-20037508.342789244,-20037508.34278925,20037508.34278925,20037508.342789244"

# Method specific processing parameters
gdal_format="MEM"

# Format arguments to python scripts
args="--filename ${input_dataset} --srcSRS ${srcSRS} --dstSRS ${dstSRS} --tilesize ${tilesize}  --outputBounds=${output_bounds}"

for method in "${methods[@]}"; do
    # Format arguments for specific method
    module="src/resample-${method}.py"
    if [ "$method" = "gdal" ]; then
        method_args="${args} --format ${gdal_format}"
    else
        method_args=${args}
    fi
    # Run pyinstrument for timing performance
    pyinstrument --outfile "${results_dir}/pyinstrument-${method}-${input_file_base}.json" -r json "${module}" "${method_args}"
    pyinstrument --outfile "${results_dir}/pyinstrument-${method}-${input_file_base}.html" -r html --timeline "${module}" "${method_args}"
    # Run memray for profiling memory
    memray run --force --output "${results_dir}/memray-${method}-${input_file_base}.bin" "${module}" "${method_args}"
    memray stats --force --json --output "${results_dir}/memray-${method}-${input_file_base}.json" "${results_dir}/memray-${method}-${input_file_base}.bin"
    memray flamegraph --force --output "${results_dir}/memray-${method}-${input_file_base}.html" "${results_dir}/memray-${method}-${input_file_base}.bin"
done
