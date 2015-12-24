from setuptools import setup

setup(
    name='aws-portknock',
    version='0.1',
    py_modules=['aws_portknock'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        aws-portknock=aws_portknock:cli
    ''',
)
