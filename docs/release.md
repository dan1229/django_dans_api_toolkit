## Packaging

**IMPORTANT:** You MUST update your version number in `setup.cfg` before anything else as this is what actually determines the version!

### CD

Releases follow the standard flow in `.github/workflows/detect-version.yml` (`dan:release` drives it):

1. Bump `version` in `setup.cfg`.
2. Move the finished `### [X.X.X] - DATE` section from `TODO.md` to the top of `CHANGELOG.md`.
3. Commit those three files with the subject `release: [X.X.X]` and no body, then push to main.

CI then checks `setup.cfg` matches, builds and uploads to PyPI (`PYPI_PASSWORD` secret), tags `X.X.X`, pushes a `release/X.X.X` branch and creates the GitHub release with the CHANGELOG section as its notes.

To replay a release, run the "Detect Version" workflow from GitHub Actions with a version. PyPI rejects a version that's already uploaded, so a replay only helps when the upload never happened.

**NOTE:** a bracketed `[X.X.X]` in any other commit subject also triggers a release.

### Manual

To build run:

```bash
python setup.py sdist
python setup.py bdist_wheel
```

To release run:

```bash
python3 -m twine upload --repository pypi dist/*
```

This expects you to have the proper credentials in your `$HOME/.pypirc` file