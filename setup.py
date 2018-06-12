import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyVitk",
    version="0.0.1",
    author="Ted Chen",
    author_email="shapable.ted@gmail.com",
    description="A python version Vietnamese text processing toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/u8621011/pyVitk",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)