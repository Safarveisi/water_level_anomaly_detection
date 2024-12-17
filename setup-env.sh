VENV=$(poetry env info -p)
[[ -d $VENV ]] && rm -rf $VENV

PYTHON_VERSION=$(pyenv version-name)
# Install the Python version in .python-version
pyenv install --skip-existing

poetry env use $HOME/.pyenv/versions/$PYTHON_VERSION/bin/python

poetry check
poetry install