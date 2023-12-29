import re

def convert_km_notation(amount: str) -> int:
    if amount.lower().endswith('k'):
        return int(amount[:-1])*1000
    if amount.lower().endswith('m'):
        return int(amount[:-1])*1000000
    raise Exception(f'Unknown notation: {amount}')

def format_int(amount: int) -> str:
    return f'{amount:,}'.replace(',',' ')