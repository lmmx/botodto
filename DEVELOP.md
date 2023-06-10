To set up a development environment, clone this repo and run:

```sh
conda create -n botodto python
conda activate botodto
pip install -e .[dev]
```

This will install the library and development dependencies (pytest, mypy etc.)

There is a tox suite you can run by simply calling `tox` in the main folder.
It uses `tox-conda` because that's how I manage my Python environments.

You can run the test suite on its own with `pytest tests/` (this is faster than the full tox suite
but will not include pre-commit hooks, linting, etc.)
