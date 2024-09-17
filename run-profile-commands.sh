#!/usr/bin/env bash

# File parameters
data_dir="earthaccess_data"
results_dir="results"
bucket="podaac-ops-cumulus-protected/MUR-JPL-L4-GLOB-v4.1"
input_file_base="20020601090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1"


# Common processing parameters
srcSRS="EPSG:4326"
dstSRS="EPSG:3857"
tilesize=256
output_bounds="-20037508.342789244,-20037508.34278925,20037508.34278925,20037508.342789244"


# Processing methods
local=true
remote=true
virtual=true

# shellcheck disable=SC2086 # We want to expand arguments
run_pyinstrument() {
    local output_base=$1
    local command=$2
    echo "Running pyinstrument on: ${command}"
    pyinstrument --outfile "${output_base}.json" -r json ${command}
    pyinstrument --outfile "${output_base}.html" -r html --timeline ${command}
}

# shellcheck disable=SC2086 # We want to expand arguments
run_memray() {
    local output_base=$1
    local command=$2
    echo "Running memray on: ${command}"
    memray run --force --output "${output_base}.bin"  ${command}
    memray stats --force --json --output "${output_base}.json" "${output_base}.bin"
    memray flamegraph --force --output "${output_base}.html" "${output_base}.bin"
}

common_args() {
    local input_dataset=$1
    echo "--filename ${input_dataset} --srcSRS ${srcSRS} --dstSRS ${dstSRS} --tilesize ${tilesize}  --outputBounds=${output_bounds}"
}

profile() {
    local suffix=$1
    local command=$2
    # Run pyinstrument for timing performance
    pyinstrument_ouput_base="${results_dir}/pyinstrument-${suffix}"
    run_pyinstrument "${pyinstrument_ouput_base}" "${command}"

    # Run memray for profiling memory
    memray_ouput_base="${results_dir}/memray-${suffix}"
    run_memray "${memray_ouput_base}" "${command}"
}

if [ "$local" = true ] ; then
    methods=("gdal" "rioxarray")
    # Format arguments to python scripts
    input_file="${data_dir}/${input_file_base}.nc"
    input_dataset="NETCDF:${input_file}:analysed_sst"
    args=$(common_args "${input_dataset}")
    echo
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
        python_command="${module} ${method_args}"
        results_suffix="${method}-${input_file_base}"
        profile "${results_suffix}" "${python_command}"

    done
fi

if [ "$remote" = true ] ; then
    methods=("gdal" "rioxarray")
    # Format arguments to python scripts
    input_file="/vsis3/${bucket}/${input_file_base}.nc"
    input_dataset="NETCDF:${input_file}:analysed_sst"
    args=$(common_args "${input_dataset}")
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
        python_command="${module} ${method_args}"
        results_suffix="${method}-remote-${input_file_base}"
        profile "${results_suffix}" "${python_command}"
    done
fi

if [ "$virtual" = true ] ; then
    # Format arguments to python scripts
    input_reference_file="${data_dir}/${input_file_base}.json"
    args=$(common_args "${input_reference_file}")
    # Profile rioxarray for a virual dataset
    method="rioxarray"
    module="src/resample-${method}.py"
    method_args="${args} --virtualized"
    python_command="${module} ${method_args}"
    results_suffix="${method}-virtual-${input_file_base}"
    profile "${results_suffix}" "${python_command}"
fi
