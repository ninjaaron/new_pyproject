# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import pathlib
import lazycli
import easyproc
import shutil
import os

PROJDIR = pathlib.Path(__file__).parent
TEMPLATES = PROJDIR / "templates"
here = pathlib.Path()
script = lazycli.script()


@script.subcommand
def addhooks(path: pathlib.Path = here):
    with (TEMPLATES / "pre-commit.sh").open() as fh:
        precommit = fh.read().format(src_dir=path)
    with (path / ".git" / "hooks" / "pre-commit").open("w") as fh:
        fh.write(precommit)
        os.chmod(fh.name, 0o755)


@script.subcommand
def new(path: pathlib.Path):
    easyproc.run(["poetry", "new", path])
    easyproc.run(["git", "init", path])
    addhooks(path)
    # add license and .gitignore
    shutil.copy2(PROJDIR / "LICENSE", path)
    shutil.copy2(PROJDIR / ".gitignore", path)
