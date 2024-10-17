# Inherit from a JupyterHub compatible Docker image
FROM quay.io/jupyter/base-notebook:2024-10-14


# Add conda packages
COPY binder/environment.yml /tmp/environment.yml
RUN mamba env update --prefix ${CONDA_DIR} --file /tmp/environment.yml


ENV ESMF_DIR="esmf"

# Download and compile ESMF

RUN apt-get update && \
    xargs -a /tmp/apt.txt apt install -y && \
    apt-get autoremove -y && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* && \
    rm /tmp/apt.txt

RUN \
    mkdir esmf; \
    wget https://github.com/esmf-org/esmf/archive/refs/tags/v8.7.0.tar.gz \
        | xvz -C esmf --strip-components=1; cd esmf; \
    make; \
    cd ..; rm -rf esmf

# Install xesmf
RUN python -m pip install git+https://github.com/pangeo-data/xesmf.git

# Install icechunk development packages (three steps required from https://github.com/earth-mover/icechunk/issues/197)
RUN python -m pip install icechunk git+https://github.com/earth-mover/Virtualizarr@icechunk
RUN python -m pip install git+https://github.com/pydata/xarray@zarr-v3 git+https://github.com/mpiannucci/kerchunk@v3
RUN python -m pip install git+https://github.com/zarr-developers/numcodecs@zarr3-codecs

# Insall quarto
USER root
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.5.57/quarto-1.5.57-linux-amd64.deb
RUN dpkg -i quarto-1.5.57-linux-amd64.deb

# Install apt packages
COPY binder/apt.txt /tmp/apt.txt

USER ${NB_USER}

# Use solution from https://github.com/NASA-Openscapes/corn/blob/main/ci/Dockerfile
# for installing VS Code extensions.
COPY binder/install-vscode-ext.sh ${HOME}/.kernels/install-vscode-ext.sh

RUN bash ${HOME}/.kernels/install-vscode-ext.sh
