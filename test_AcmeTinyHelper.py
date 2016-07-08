from AcmeTinyHelper import SSLManager

class TestAcmeTinyHelper:



    def setup_method(self, method):
        self.manager = SSLManager('/my/path', ['example.com'], '/bin/acme_tiny.py', '/var/www/challenges', False)
        self.manager.returnString = True



    def test_makePath(self):
        assert self.manager._makePath() == 'mkdir -p /my/path'



    def test_callOpenSSL(self):
        assert self.manager._callOpenSSL('account.key') == 'openssl genrsa 4096 > /my/path/account.key'
        assert self.manager._callOpenSSL('domain.key')  == 'openssl genrsa 4096 > /my/path/domain.key'



    def test_DiffieHellmanParams(self):
        expected = 'openssl dhparam -out /my/path/dhparam.pem 4096'
        assert self.manager._getDiffieHellmanParams() == expected



    def test_getIntermediateCertificate(self):
        expected = 'wget -O - https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem > /my/path/intermediate.pem'
        assert self.manager._getIntermediateCertificate() == expected



    def test_getSelfSignedCertificate(self):
        expected = 'openssl req -new -sha256 -key /my/path/domain.key -subj "/CN=example.com" > /my/path/domain.csr'
        assert self.manager._getSelfSignedCertificate() == expected

        self.manager.domains = ['www.example.com', 'example.com', 'subdomain.example.com']
        expected = 'openssl req -new -sha256 -key /my/path/domain.key -subj "/" -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:www.example.com,DNS:example.com,DNS:subdomain.example.com")) > domain.csr'
        assert self.manager._getSelfSignedCertificate() == expected



    def test_getSignedCertificate(self):
        assert self.manager._getSignedCertificate() == 'python /bin/acme_tiny.py --account-key /my/path/account.key --csr /my/path/domain.csr --acme-dir /var/www/challenges > /my/path/signed.crt'

        self.manager.acme_tiny_path = '/usr/bin/acme_tiny.py'
        assert self.manager._getSignedCertificate() == 'python /usr/bin/acme_tiny.py --account-key /my/path/account.key --csr /my/path/domain.csr --acme-dir /var/www/challenges > /my/path/signed.crt'

        self.manager.challenge_path = '/tmp/challenges'
        assert self.manager._getSignedCertificate() == 'python /usr/bin/acme_tiny.py --account-key /my/path/account.key --csr /my/path/domain.csr --acme-dir /tmp/challenges > /my/path/signed.crt'



    def test_chainCertificates(self):
        expected = 'cat /my/path/signed.crt /my/path/intermediate.pem > /my/path/chained.pem'
        assert self.manager._chainCertificates() == expected

