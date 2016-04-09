from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup

setup(
    name='aws-portknock',
    version='0.1',
    py_modules=['aws_portknock'],
    description='Port knocking for AWS security groups',
    author='Michel Alexandre Salim',
    author_email='michel@michel-slm.name',
    url='https://github.com/michel-slm/aws-portknock',
    download_url='https://github.com/michel-slm/aws-portknock/tarball/0.1',
    keywords=['aws'],
    classifiers=[],
    install_requires=[str(r.req)
                      for r in parse_requirements(
                        'requirements.txt',
                        session=PipSession())],
    entry_points='''
        [console_scripts]
        aws-portknock=aws_portknock:cli
    ''',
)
