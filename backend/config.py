import os

from backend.utils import iso_to_epoch

DROP_DB = os.environ.get('DROP_DB', 'false') == 'true'

TOTP_SECRET = os.environ.get('TOTP_SECRET', 'blopblopblop')
WS_HOST = 'https://trade-service.wealthsimple.com'
WS_ACCOUNT = os.environ.get('WS_ACCOUNT', 'test@bob.com:mypassword')
WS_TFSA_ID = os.environ.get('WS_TFSA_ID', 'blopblop')

SEEKING_ALPHA_HOST = 'seeking-alpha.p.rapidapi.com'
SEEKING_ALPHA_API_KEY = os.environ['SA_API_KEY']

ACTIVITY_START = iso_to_epoch('2022-10-21')
