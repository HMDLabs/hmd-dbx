import pathlib

from setuptools import find_packages, setup

repo_dir = pathlib.Path(__file__).absolute().parent.parent.parent
version_file = repo_dir / "meta-data" / "VERSION"
readme = (repo_dir / "README.md").read_text()

with open(version_file, "r") as vfl:
    version = vfl.read().strip()

setup(
    name="hmd-dbx",
    version=version,
    description="DataBase Extraction",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Brian Greene",
    author_email="brian.greene@hmdlabs.io",
    license="Apache 2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
)
