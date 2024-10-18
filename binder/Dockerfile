# Inherit from a JupyterHub compatible Docker image
FROM quay.io/jupyter/base-notebook:2024-10-14


# Add conda packages
COPY binder/environment.yml /tmp/environment.yml
RUN mamba env update --prefix ${CONDA_DIR} --file /tmp/environment.yml

ENV ESMF_DIR="esmf"

# Download and compile ESMF
COPY binder/apt.txt /tmp/apt.txt

USER root

RUN apt-get update && \
    xargs -a /tmp/apt.txt apt install -y && \
    apt-get autoremove -y && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* && \
    rm /tmp/apt.txt

USER ${NB_USER}

RUN \
    mkdir esmf; \
    wget -qO- https://github.com/esmf-org/esmf/archive/refs/tags/v8.7.0.tar.gz \
        | tar xvz -C esmf --strip-components=1; cd esmf; \
        make; \
        cd ..; rm -rf esmf

RUN ls

# Install xesmf
RUN python -m pip install git+https://github.com/pangeo-data/xesmf.git
