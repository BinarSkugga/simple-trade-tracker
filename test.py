import pyotp

totp = pyotp.totp.TOTP('JDRSMBJVAXDLHKLD').provisioning_uri(name='Wealthsimple:binarskugga@gmail.com', issuer_name='Wealthsimple')
totp = pyotp.parse_uri(totp)
print(totp.now())


