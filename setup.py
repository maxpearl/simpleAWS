import pathlib
from setuptools import setup

#  The Directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file

README = (HERE/"README.md").read_text()

setup(
    name='simpleaws',
    python_requires='>=3.3',
    version='0.1',
    description='Simplified AWS Functions',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/maxpearl/simpleAWS",
    author="Max Pearl",
    license="GPLv3",
    packages=['simpleaws'],
    include_package_data=True,
    install_requires=[
        'boto3',
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
    ],
)