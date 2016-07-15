from AcmeTinyHelperConsole import AcmeTinyHelperConsole

class TestAcmeTinyHelper:

    def test_run(self, capsys):
        console = AcmeTinyHelperConsole()

        opts = [('--path', '/etc/letsencrypt/example.com'),
                ('--domains', 'example.com'),
                ('--acme-tiny-path', '/usr/src/acme-tiny.py'),
                ('--challenge-path', '/var/www/lets-encrypt-challenges')]

        console.run('new', opts)

        out, err = capsys.readouterr()

        expected = (
          'mkdir -p /etc/letsencrypt/example.com',
          'openssl genrsa 4096 > /etc/letsencrypt/example.com/account.key',
          'openssl genrsa 4096 > /etc/letsencrypt/example.com/domain.key',
          'wget -O - https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem > /etc/letsencrypt/example.com/intermediate.pem',
          'openssl req -new -sha256 -key /etc/letsencrypt/example.com/domain.key -subj "/CN=example.com" > /etc/letsencrypt/example.com/domain.csr',
          'python /usr/src/acme-tiny.py --account-key /etc/letsencrypt/example.com/account.key --csr /etc/letsencrypt/example.com/domain.csr --acme-dir /var/www/lets-encrypt-challenges > /etc/letsencrypt/example.com/signed.crt',
          'cat /etc/letsencrypt/example.com/signed.crt /etc/letsencrypt/example.com/intermediate.pem > /etc/letsencrypt/example.com/chained.pem'
        )

        for expected_line in expected:
            assert expected_line in out


