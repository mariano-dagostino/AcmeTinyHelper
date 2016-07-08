# usage: python letsencrypt-acme-tiny.py /etc/letsencrypt/certs "example.com,www.example.com"
import sys
import os
import re

class AcmeTinyHelper(object):

    def __init__(self, path, domains, acme_tiny_path, challenge_path, execute):
        self.path = path
        self.domains = domains
        self.acme_tiny_path = acme_tiny_path
        self.challenge_path = challenge_path
        self.execute = execute

        self.simulate = True
        self.force = False
        self.dhbits = 4096
        self.letsencrypt_x3_cross_signed_pem = 'https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem'


    def _signedCertNotFound(self):
        path = self.path
        return not os.path.isfile('{path}/signed.crt').format(**locals())

    def _makePath(self):
        return self._runCommand(
          'mkdir -p ' + self.path
        )

    def _callOpenSSL(self, fileName, bits=4096):
        path = self.path
        return self._runCommand(
          "openssl genrsa {bits} > {path}/{fileName}".format(**locals())
        )

    def _getSelfSignedCertificate(self):
        domains = self.domains
        path = self.path

        if len(domains) == 1:
            domain = domains[0]
            return self._runCommand(
                'openssl req -new -sha256 -key {path}/domain.key -subj "/CN={domain}" > {path}/domain.csr'.format(**locals())
            )
        else:
            domain_list = []
            for d in domains:
                domain_list.append('DNS:' + d)
            domain = ','.join(domain_list)
            return self._runCommand(
                'openssl req -new -sha256 -key {path}/domain.key -subj "/" -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName={domain}")) > domain.csr'.format(**locals())
            )

    def _getDiffieHellmanParams(self):
        path = self.path
        dhbits = self.dhbits

        return self._runCommand(
            'openssl dhparam -out {path}/dhparam.pem {dhbits}'.format(**locals())
        )

    def _runCommand(self, string):
        if self.simulate:
            print string
            print ""

        if self.execute:
            os.command(string)

        return string

    def _getIntermediateCertificate(self):
        path = self.path
        url = self.letsencrypt_x3_cross_signed_pem
        return self._runCommand(
          'wget -O - {url} > {path}/intermediate.pem'.format(**locals())
        )

    def _getSignedCertificate(self):
        path = self.path
        domains = self.domains
        acme_tiny_path = self.acme_tiny_path
        challenge_path = self.challenge_path

        return self._runCommand(
          ('python {acme_tiny_path} ' +
                  '--account-key {path}/account.key ' +
                  '--csr {path}/domain.csr ' +
                  '--acme-dir {challenge_path} > {path}/signed.crt').format(**locals())
        )


    def _chainCertificates(self):
        path = self.path
        return self._runCommand(
           'cat {path}/signed.crt {path}/intermediate.pem > {path}/chained.pem'.format(**locals())
        )


    def _checkParameters(self):
        return True

        valid_domain_regex = r'^[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63}).$'
        for domain in self.domains:
            if re.search(valid_domain_regex, domain) is None:
                return False

        return True

    def newCertificate(self):
        if self.simulate or self.force or self._signedCertNotFound():
            self._makePath()
            self._callOpenSSL('account.key')
            self._callOpenSSL('domain.key')
            self._getDiffieHellmanParams()
            self._getIntermediateCertificate()
            self._getSelfSignedCertificate()
            self._getSignedCertificate()
            self._chainCertificates()

    def renewCertificate(self):
        self._getIntermediateCertificate()
        self._getSelfSignedCertificate()
        self._getSignedCertificate()
        self._chainCertificates()
