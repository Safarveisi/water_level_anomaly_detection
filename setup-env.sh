# Remove the virtual env created by devbox (after running `devbox shell`) 
rm -rf .venv/

# Get the required python version in .python-version (e.g., 3.9.1)
PYTHON_VERSION=$(pyenv version-name)

# Install the python version if not present
pyenv install --skip-existing

# Configure poetry to use the installed python version
poetry env use $HOME/.pyenv/versions/$PYTHON_VERSION/bin/python
poetry config virtualenvs.in-project true
poetry check
poetry install