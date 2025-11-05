# Publishing Azicure to TestPyPI / PyPI

## 1) Build
```bash
python -m pip install --upgrade build
python -m build
```

## 2) Upload to TestPyPI
```bash
python -m pip install --upgrade twine
twine upload --repository testpypi dist/*
```

## 3) Install from TestPyPI (example)
```bash
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps azicure==0.1.0
```

## 4) Upload to PyPI (when ready)
```bash
twine upload dist/*
```

> Tip: keep `version` in `pyproject.toml` in sync with release tags.


---

## Versioning (Important)
Versions are derived from Git tags using `setuptools_scm`. Create a tag like `v0.1.0` before building:
```bash
git tag v0.1.0  # or vX.Y.Z
python -m build
```
