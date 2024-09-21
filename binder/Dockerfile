# Inherit from a JupyterHub compatible Docker image
FROM quay.io/jupyter/base-notebook:2024-07-25

# Add conda packages
COPY binder/environment.yml /tmp/environment.yml
RUN mamba env update --prefix ${CONDA_DIR} --file /tmp/environment.yml

# Insall quarto

USER root
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.5.57/quarto-1.5.57-linux-amd64.deb
RUN dpkg -i quarto-1.5.57-linux-amd64.deb
USER ${NB_USER}

# Use solution from https://github.com/NASA-Openscapes/corn/blob/main/ci/Dockerfile
# for installing VS Code extensions.

COPY binder/install-vscode-ext.sh ${HOME}/.kernels/install-vscode-ext.sh

RUN bash ${HOME}/.kernels/install-vscode-ext.sh
