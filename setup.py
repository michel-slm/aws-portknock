from pip.req import parse_requirements
from setuptools import setup

setup(
    name='aws-portknock',
    version='0.1',
    py_modules=['aws_portknock'],
    install_requires=[str(r.req)
                      for r in parse_requirements('requirements.txt')],
    entry_points='''
        [console_scripts]
        aws-portknock=aws_portknock:cli
    ''',
)
