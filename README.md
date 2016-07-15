[![Build Status](https://travis-ci.org/mariano-dagostino/AcmeTinyHelper.svg?branch=master)](https://travis-ci.org/mariano-dagostino/AcmeTinyHelper)

# AcmeTinyHelper

This project is a helper for [acme-tiny.py](https://github.com/diafygi/acme-tiny)
that automate the creation of the files required by letsencrypt and acme-tiny to
get a certificate.

# Example

```./AcmeTinyHelper new --path=/etc/letsencrypt/certs --domains='example.com'```

The result of running this script is:

```
mkdir -p /etc/letsencrypt/certs/example.com

openssl genrsa 4096 > /etc/letsencrypt/certs/example.com/account.key

openssl genrsa 4096 > /etc/letsencrypt/certs/example.com/domain.key

wget -O - https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem > /etc/letsencrypt/certs/example.com/intermediate.pem

openssl req -new -sha256 -key /etc/letsencrypt/certs/example.com/domain.key -subj "/CN=example.com" > /etc/letsencrypt/certs/example.com/domain.csr

python /bin/acme_tiny.py --account-key /etc/letsencrypt/certs/example.com/account.key --csr /etc/letsencrypt/certs/example.com/domain.csr --acme-dir /var/www/challenges > /etc/letsencrypt/certs/example.com/signed.crt

cat /etc/letsencrypt/certs/example.com/signed.crt /etc/letsencrypt/certs/example.com/intermediate.pem > /etc/letsencrypt/certs/example.com/chained.pem
```

# Mode of use


```./AcmeTinyHelper [action] [parameters]```

# Actions

- new: Prints or executes all the instructions to obtain a new certificate signed by letsencrypt.
- new: Prints or executes all the instructions to renew a certificate signed by letsencrypt.
- help: Displays the usage instrucctions.

# Parameters

- ```--path: Indicates where will be saved all the files.```
- ```--domains: A comma separated list of domains (example: 'example.com,www.example.com')```
- ```--acme-tiny-path: The path where acme-tiny.py is located (defaults to /bin/acme-tiny.py)```
- ```--challenge-path: The directory where acme-tiny.py will write the challenge to authenticate the domain with letscrypt.org (defaults to /var/www/challenges)```
- ```--execute: If present, the script will execute all the commands instead of output them in the terminal as text. The process will check first if the signed certificate is absent before start all the process.```
- ```--force: If present, the script will execute all the commands even if the signed certificate was already obtained.```
