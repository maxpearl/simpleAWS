import pathlib
from setuptools import setup

#  The Directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file

README = (HERE/"README.md").read_text()

setup(
    name='simple_AWS',
    python_requires='>=3.3',
    version='0.1.5',
    description='Simplified AWS Functions',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/maxpearl/simpleAWS",
    author="Max Pearl",
    author_email="code@maxwellpearl.com",
    license="GPLv3",
    packages=['simple_AWS'],
    include_package_data=True,
    install_requires=[
        'botocore',
        'boto3',
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
    ],
)