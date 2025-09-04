def level_str(level: dict):
    s = ""
    if level['artist']: s += f"{level['artist']} - "
    s += {level['level']}
    if level['creator']: s += f" (by {level['creator']})"
    s += f" ({level['exp']} EXP)"
    return s