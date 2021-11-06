import re
from django.core import validators
from django.core.exceptions import ValidationError


MIN_PASSWORD_LEN = 8

MIN_PHONE_LENGTH = 11
MAX_PHONE_LENGTH = 15

WALLET_ERC_20_PATTERN = r'^0x[a-fA-F0-9]{40}$'


def is_erc_20_wallet_valid(erc20_wallet: str) -> bool:
    """Checked the ERC-20 wallet"""
    return re.fullmatch(WALLET_ERC_20_PATTERN, erc20_wallet)


def is_phone_valid(phone: str) -> bool:
    if not phone.isdigit():
        return False
    phone_len = len(phone)
    if phone_len < MIN_PHONE_LENGTH or phone_len > MAX_PHONE_LENGTH:
        return False
    return True


def PhoneValidator(value):
    if not value:
        return value

    if not is_phone_valid(value):
        raise ValidationError('phone is invalid')

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


def is_url_valid(value: str) -> bool:
    validator = validators.URLValidator()
    try:
        validator(value)
    except ValidationError:
        return False
    return True


def URLValidator(value):
    if not value:
        return value

    if not is_url_valid(value):
        raise ValidationError('URL is invalid')
    return value


def is_email_valid(value: str) -> bool:
    validator = validators.EmailValidator()
    try:
        validator(value)
    except ValidationError:
        return False
    return True


def EmailValidator(value):
    if not value:
        return value

    if not is_email_valid(value):
        raise ValidationError('Email is invalid')
    return value
