from setuptools import setup

setup(
    name='simple_aws',
    python_requires='>=3.6',
    version='0.1',
    description='Simplified AWS Functions',
    packages=['simple_aws'],
    install_requires=[
        'boto3',
    ],
)