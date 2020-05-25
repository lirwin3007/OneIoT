import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oneiot",
    version="0.1.0",
    author="Louis Irwin",
    author_email="coding@louisirwin.co.uk",
    description="OneIoT",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/lirwin3007/OneIoT",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
