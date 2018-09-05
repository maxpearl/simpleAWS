from setuptools import setup

setup(name='simple_aws',
      version='0.1',
      description='Simplified AWS Functions',
      packages=['simple_aws'],
      install_requires=[
          'boto3',
      ],
    )