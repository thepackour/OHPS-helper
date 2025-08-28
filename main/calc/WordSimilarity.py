from difflib import SequenceMatcher


def most_similar(query: str, word_list: list):
    ratio_list = []
    for word in word_list:
        ratio = SequenceMatcher(None, query.lower(), word.lower()).ratio()
        ratio_list.append(ratio)
    max_ratio = max(ratio_list)
    if max_ratio > 0.35:
        idx = ratio_list.index(max_ratio)
        return word_list[idx]
    else: return None