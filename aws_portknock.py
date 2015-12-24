#!/usr/bin/env python
import atexit
import click
try:
    import configparser
except:
    import ConfigParser as configparser
import os
import sys
import time


def close_port(sgid, port):
    click.echo("Closing {} {}".format(sgid, port))


def open_port(sgid, port):
    click.echo("Opening {} {}".format(sgid, port))


def keep_open(sgid, port):
    # check if we need to open port
    if True:
        open_port(sgid, port)
        atexit.register(close_port, sgid=sgid, port=port)
    while True:
        time.sleep(5)
        click.echo("Sleeping")

@click.command()
@click.option('--port', help='Port to open')
@click.option('--sgid', help='Security group ID')
@click.option('--profile', default='default')
def portknock(sgid, profile, port):
    config = configparser.ConfigParser()
    cfg_file = os.path.join(os.path.expanduser('~'),
                            '.config',
                            'aws-portknock.ini')
    if os.path.exists(cfg_file):
        config.read(cfg_file)
        if not sgid:
            if profile in config and 'sgid' in config[profile]:
                sgid = config[profile]['sgid']
            else:
                click.echo("Cannot determine security group ID", err=True)
                sys.exit(1)
        if not port:
            if profile in config and 'port' in config[profile]:
                port = config[profile]['port']
            else:
                port = 22
    keep_open(sgid, port)


if __name__ == '__main__':
    portknock()
