# Inherit from a JupyterHub compatible Docker image
FROM quay.io/jupyter/base-notebook:2024-10-14


# Add conda packages
COPY binder/environment.yml /tmp/environment.yml
RUN mamba env update --prefix ${CONDA_DIR} --file /tmp/environment.yml

COPY binder/apt.txt /tmp/apt.txt

USER root

RUN apt-get update && \
    xargs -a /tmp/apt.txt apt install -y && \
    apt-get autoremove -y && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* && \
    rm /tmp/apt.txt

# Insall quarto
USER root
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.5.57/quarto-1.5.57-linux-amd64.deb
RUN dpkg -i quarto-1.5.57-linux-amd64.deb

USER ${NB_USER}

# Use solution from https://github.com/NASA-Openscapes/corn/blob/main/ci/Dockerfile
# for installing VS Code extensions.
COPY binder/install-vscode-ext.sh ${HOME}/.kernels/install-vscode-ext.sh

RUN bash ${HOME}/.kernels/install-vscode-ext.sh

# Install icechunk development packages (these steps required from https://github.com/earth-mover/icechunk/issues/197)
RUN python -m pip install icechunk xarray VirtualiZarr
RUN python -m pip install git+https://github.com/mpiannucci/kerchunk@v3
RUN python -m pip install git+https://github.com/zarr-developers/numcodecs@zarr3-codecs
RUN python -m pip install git+https://github.com/zarr-developers/zarr-python@main
RUN python -m pip install git+https://github.com/pydata/xarray@main
