# Releasing with `setuptools_scm`

This project uses dynamic versions derived from Git tags.

## One-time
```bash
git init
git add .
git commit -m "init"
git tag v0.1.0
```

## For each release
1. Bump tag (semantic): `git tag v0.2.0` (or `git tag v0.1.1` for patches).
2. Build: 
   ```bash
   python -m pip install --upgrade build twine
   python -m build
   ```
3. Upload (TestPyPI or PyPI):
   ```bash
   twine upload --repository testpypi dist/*
   # or
   twine upload dist/*
   ```

`setuptools_scm` will generate `src/azicure/_version.py` during builds and `__version__`
will be sourced from that file at runtime.
