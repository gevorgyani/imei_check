def is_valid_imei(imei: str) -> bool:
    if not imei.isdigit() or len(imei) not in (14, 15):
        return False
    total = 0
    for i, digit in enumerate(reversed(imei)):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0