#!/usr/bin/env bash

# File parameters
data_dir="earthaccess_data"
results_dir="results"
input_file_base="20020601090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1"


# Common processing parameters
srcSRS="EPSG:4326"
dstSRS="EPSG:3857"
tilesize=256
output_bounds="-20037508.342789244,-20037508.34278925,20037508.34278925,20037508.342789244"


# Processing methods
local=true
virtual=true

# shellcheck disable=SC2086 # We want to expand arguments
if [ "$local" = true ] ; then
    echo "Profiling local"
    methods=("gdal" "rioxarray")
    # Format arguments to python scripts
    input_file="${data_dir}/${input_file_base}.nc"
    input_dataset="NETCDF:${input_file}:analysed_sst"
    args="--filename ${input_dataset} --srcSRS ${srcSRS} --dstSRS ${dstSRS} --tilesize ${tilesize}  --outputBounds=${output_bounds}"
    # Method specific processing parameters
    gdal_opts="--format MEM"

    for method in "${methods[@]}"; do
        # Format arguments for specific method
        module="src/resample-${method}.py"
        if [ "$method" = "gdal" ]; then
            method_args="${args} ${gdal_opts}"
        else
            method_args=${args}
        fi
        # Run pyinstrument for timing performance
        echo ${module} ${method_args}
        pyinstrument --outfile "${results_dir}/pyinstrument-${method}-${input_file_base}.json" -r json ${module} ${method_args}
        pyinstrument --outfile "${results_dir}/pyinstrument-${method}-${input_file_base}.html" -r html --timeline ${module} ${method_args}
        # Run memray for profiling memory
        memray run --force --output "${results_dir}/memray-${method}-${input_file_base}.bin"  ${module} ${method_args}
        memray stats --force --json --output "${results_dir}/memray-${method}-${input_file_base}.json" "${results_dir}/memray-${method}-${input_file_base}.bin"
        memray flamegraph --force --output "${results_dir}/memray-${method}-${input_file_base}.html" "${results_dir}/memray-${method}-${input_file_base}.bin"
    done
fi

# shellcheck disable=SC2086 # We want to expand arguments
if [ "$virtual" = true ] ; then
    echo "Profiling virtual"

    # Format arguments to python scripts
    input_file="${data_dir}/${input_file_base}.json"
    args="--filename ${input_file} --srcSRS ${srcSRS} --dstSRS ${dstSRS} --tilesize ${tilesize}  --outputBounds=${output_bounds}"

    # Profile rioxarray for a virual dataset
    method="rioxarray"
    module="src/resample-${method}.py"
    method_args="${args} --virtualized"

    echo ${module} ${method_args}
    # Run pyinstrument for timing performance
    pyinstrument --outfile "${results_dir}/pyinstrument-${method}-virtual-${input_file_base}.json" -r json ${module} ${method_args}
    pyinstrument --outfile "${results_dir}/pyinstrument-${method}-virtual-${input_file_base}.html" -r html --timeline ${module} ${method_args}

    # Run memray for profiling memory
    memray run --force --output "${results_dir}/memray-${method}-virtual-${input_file_base}.bin" ${module} ${method_args}
    memray stats --force --json --output "${results_dir}/memray-virtual-${method}-${input_file_base}.json" "${results_dir}/memray-${method}-${input_file_base}.bin"
    memray flamegraph --force --output "${results_dir}/memray-virtual-${method}-${input_file_base}.html" "${results_dir}/memray-${method}-${input_file_base}.bin"
fi
