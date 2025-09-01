def official_str(official: dict):
    return f"{official['song']} ({official['exp']} EXP) \n"


def is_official(level: dict):
    if level['artist'] == "OFFICIAL" and level['creator'] == "OFFICIAL":
        return True
    return False