import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
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
    install_requires=[
        'regex==2017.4.29',
        'nltk==3.2.4',
        'PyNLPl==1.1.8',
    ],
    include_package_data=True,
)