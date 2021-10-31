import re

from rest_framework.exceptions import ValidationError


MIN_PASSWORD_LEN = 8

MIN_PHONE_LENGTH = 11
MAX_PHONE_LENGTH = 15

WALLET_ERC_20_PATTERN = r'^0x[a-fA-F0-9]{40}$'


def is_erc_20_wallet_valid(erc20_wallet: str) -> bool:
    """Checked the ERC-20 wallet"""
    return re.fullmatch(WALLET_ERC_20_PATTERN, erc20_wallet)

def PhoneValidator(value):

    if not value:
        return value

    if not value.isdigit():
        raise ValidationError('The phone should contain only digits')

    value_len = len(value)
    if (value_len < MIN_PHONE_LENGTH or value_len > MAX_PHONE_LENGTH):
        raise ValidationError(f'The phone should have length from {MIN_PHONE_LENGTH} to {MAX_PHONE_LENGTH}')

    return value

def ERC20Validator(value):
    if not value:
        return value

    if not is_erc_20_wallet_valid(value):
        raise ValidationError('wallet is invalid')

    return value

def PasswordValidator(value):
    if not value:
        return value

    if len(value) < MIN_PASSWORD_LEN:
        raise ValidationError(f'password should have at least {MIN_PASSWORD_LEN} symbols')

    return value
