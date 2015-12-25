#!/usr/bin/env python
import atexit
import boto3
import botocore.exceptions
import click
try:
    import configparser
except:
    import ConfigParser as configparser
import os
import sys
import time
from urllib2 import urlopen


def close_port(sgid, cidr_ip, port):
    ec2_client = boto3.client('ec2')
    ec2_client.revoke_security_group_ingress(
        GroupId=sgid,
        IpProtocol='tcp',
        CidrIp=cidr_ip,
        FromPort=port,
        ToPort=port
    )
    click.echo("Closed {} to {}-tcp-{}-{}".format(sgid, cidr_ip, port, port))


def get_ip():
    return "{}/32".format(urlopen('http://ip.42.pl/raw').read())


def open_port(sgid, cidr_ip, port):
    ec2_client = boto3.client('ec2')
    ec2_client.authorize_security_group_ingress(
        GroupId=sgid,
        IpProtocol='tcp',
        CidrIp=cidr_ip,
        FromPort=port,
        ToPort=port
    )
    click.echo("Opened {} to {}-tcp-{}-{}".format(sgid, cidr_ip, port, port))


def keep_open(sgid, port):
    # check if we need to open port
    try:
        _cidr_ip = get_ip()
        open_port(sgid, _cidr_ip, port)
        # no exception means we added a new rule
        # so clean up afterwards
        atexit.register(close_port,
                        sgid=sgid,
                        cidr_ip=_cidr_ip,
                        port=port)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidPermission.Duplicate':
            click.echo(e.response['Error']['Message'])
        else:
            raise e
    while True:
        time.sleep(5)
        click.echo("Sleeping")


@click.command()
@click.option('--port', type=int, help='Port to open.')
@click.option('--profile', default='default', help='Configuration profile to use.')
@click.option('--sgid', help='Security group ID.')
def cli(sgid, profile, port):
    config = configparser.ConfigParser()
    cfg_file = os.path.join(os.path.expanduser('~'),
                            '.aws',
                            'portknock.ini')
    if os.path.exists(cfg_file):
        config.read(cfg_file)
    if not sgid:
        if config.has_option(profile, 'sgid'):
            sgid = config.get(profile, 'sgid')
        else:
            click.echo("Cannot determine security group ID", err=True)
            sys.exit(1)
    if not port:
        if config.has_option(profile, 'port'):
            port = config.getint(profile, 'port')
        else:
            port = 22
    keep_open(sgid, port)


if __name__ == '__main__':
    cli()
