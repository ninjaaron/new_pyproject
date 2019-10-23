# -*- coding: utf-8 -*-
from distutils.core import setup

packages = ["new_pyproject"]

package_data = {"": ["*"], "new_pyproject": ["templates/*"]}

install_requires = ["easyproc>=0.5.1,<0.6.0", "lazycli>=0.2.2,<0.3.0"]

entry_points = {"console_scripts": ["pyproject = new_pyproject:script.run"]}

setup_kwargs = {
    "name": "new-pyproject",
    "version": "0.2.0",
    "description": "automation for my personal projects",
    "long_description": None,
    "author": "Aaron Christianson",
    "author_email": "ninjaaron@gmail.com",
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.5,<4.0",
}


setup(**setup_kwargs)
