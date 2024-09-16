# Inherit from a JupyterHub compatible Docker image
FROM quay.io/pangeo/pangeo-notebook:2024.09.11

# Add conda packages
COPY environment.yml /tmp/environment.yml
RUN mamba env update --prefix ${NB_PYTHON_PREFIX} --file /tmp/environment.yml

# Use solution from https://github.com/NASA-Openscapes/corn/blob/main/ci/Dockerfile
# for installing VS Code extensions.

COPY --chown=${NB_USER}:${NB_USER} install-vscode-ext.sh ${HOME}/.kernels/install-vscode-ext.sh

RUN bash ${HOME}/.kernels/install-vscode-ext.sh
