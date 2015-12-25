# aws-portknock #
Port knocking for AWS security groups

## "Port knocking" ##

Unlike the traditional port knocking utilities, this tool relies on
the caller having the rights, through Amazon Web Services' Identity
and Access Management roles, to modify a security group.

## Usage ##

```
$ aws-portknock --help
Usage: aws-portknock [OPTIONS]

Options:
  --port INTEGER  Port to open
  --profile TEXT  Configuration profile to use
  --sgid TEXT     Security group ID
  --help          Show this message and exit.
```

For repeated use, create `$HOME/.aws/portknock.ini` containing, for example:

```
[default]
sgid = sg-12abcdef
port = 22

[webprofile]
sgid = sg-12abcdef
port = 443
```
