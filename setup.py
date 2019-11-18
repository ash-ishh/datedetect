import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="datedetect",
    version="1.0.0",
    description="Get possible string format codes of the given datetime object.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ash-ishh/datedetect",
    author="Ash-Ishh..",
    author_email="mr.akc@outlook.com",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    setup_requires=['wheel']
)
