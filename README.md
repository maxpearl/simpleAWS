# SimpleAWS

Version 0.1

Simplified Libraries for some of the most common AWS resources. The purpose of SimpleAWS is to add one layer of abstraction, and remove a lot of the guess-work from interfacing with some AWS resources.

The options are limited on purpose - this is not designed to replace boto3, but to provide an easier entry into using AWS resources with python.

## Installation

```
pip install .
```

## AWS Requirements

SimpleAWS uses profiles and secret/access keys. Put a file called 'credentials' inside the .aws directory in your home directory (the home of the user running this code.) The format of the file is:
[profilename]
aws_access_key_id = <key>
aws_secret_access_key = <key>

(If you only have one profile, you can name it 'Default' - that is the code's default profile.)
