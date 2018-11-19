__version__ = "0.1.0"
import pathlib
import lazycli
import easyproc
import shutil

PROJDIR = pathlib.Path(__file__).parent
TEMPLATES = PROJDIR / "templates"


@lazycli.script
def add_hooks(path: pathlib.Path):
    with (TEMPLATES / "pre-commit.sh").open() as fh:
        precommit = fh.read().format(src_dir=path)
    with (path / ".git" / "hooks" / "pre-commit").open("w") as fh:
        fh.write(precommit)


@lazycli.script
def setup(path: pathlib.Path):
    easyproc.run(["poetry", "new", path])
    easyproc.run(["git", "init", path])
    add_hooks(path)
    # add black to pyproject.toml
    with (path / "pyproject.toml").open() as fh:
        pyprojectlines = fh.readlines()
    with (TEMPLATES / "black.toml").open() as fh:
        blacklines = fh.readlines()
    blacklines.append("\n")
    blacklines += pyprojectlines
    with (path / "pyproject.toml").open("w") as fh:
        fh.writelines(blacklines)
    # add license and .gitignore
    shutil.copy2(PROJDIR / "LICENSE", path)
    shutil.copy2(PROJDIR / ".gitignore", path)
