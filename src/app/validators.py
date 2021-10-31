import re

from rest_framework.exceptions import ValidationError


def PhoneValidator(value):
    MIN_PHONE_LENGTH = 11
    MAX_PHONE_LENGTH = 15

    if not value:
        return value

    if not value.isdigit():
        raise ValidationError('The phone should contain only digits')

    value_len = len(value)
    if (value_len < MIN_PHONE_LENGTH or value_len > models.User.MAX_PHONE_LENGTH):
        raise ValidationError(f'The phone should have length from {MIN_PHONE_LENGTH} to {MAX_PHONE_LENGTH}')

    return value


def is_erc_20_wallet_valid(erc20_wallet: str) -> bool:
    """Checked the ERC-20 wallet"""
    WALLET_ERC_20_PATTERN = r'^0x[a-fA-F0-9]{40}$'
    return re.fullmatch(WALLET_ERC_20_PATTERN, erc20_wallet)


def ERC20Validator(value):
    if not value:
        return value

    if not is_erc_20_wallet_valid(value):
        raise ValidationError(f'wallet is invalid')

    return value
