#!/bin/bash

# Install VSCode extensions.
# These get installed to $CONDA_PREFIX/envs/notebook/share/code-server/extensions/

extensions=("ms-python.python" "ms-toolsai.jupyter" "ms-toolsai.vscode-jupyter-powertoys" "ms-python.debugpy" "eamodio.gitlens" "wholroyd.jinja" "esbenp.prettier-vscode" "njpwerner.autodocstring" "quarto.quarto")

for EXT in "${extensions[@]}"; do
    code-server --install-extension "${EXT}"
done
