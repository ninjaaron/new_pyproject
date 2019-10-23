# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import pathlib
import lazycli
import easyproc
import shutil
import tarfile
import os

PROJDIR = pathlib.Path(__file__).parent
TEMPLATES = PROJDIR / "templates"
here = pathlib.Path().absolute()
script = lazycli.script()


@script.subcommand
def addhooks(path: pathlib.Path = here):
    with (TEMPLATES / "pre-commit.sh").open() as fh:
        precommit = fh.read().format(src_dir=path)
    with (path / ".git" / "hooks" / "pre-commit").open("w") as fh:
        fh.write(precommit)
        os.chmod(fh.name, 0o755)


@script.subcommand
def license(path: pathlib.Path = here):
    shutil.copy2(PROJDIR / "LICENSE", path)


@script.subcommand
def gitignore(path: pathlib.Path = here):
    shutil.copy2(PROJDIR / ".gitignore", path)


@script.subcommand
def init(path: pathlib.Path = here):
    for func in (addhooks, license, gitignore):
        func(path)


@script.subcommand
def extract_setupfile(path: pathlib.Path = here):
    path = path.absolute()
    os.chdir(path)
    try:
        os.remove(path / "setup.py")
    except FileNotFoundError:
        pass
    easyproc.run("poetry build")
    archive_name = sorted((path / "dist").glob("*.tar.gz"))[-1]
    with tarfile.open(archive_name) as archive:
        for filename in archive.getnames():
            if filename.endswith("/setup.py"):
                break
        archive.extract(filename)

    extracted = pathlib.Path(filename)
    extracted.rename(path / "setup.py")
    extracted.parent.rmdir()
    os.chdir(here)


@script.subcommand
def new(path: pathlib.Path):
    easyproc.run(["poetry", "new", path])
    easyproc.run(["git", "init", path])
    init(path)
