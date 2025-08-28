from difflib import SequenceMatcher


def most_similar(query: str, word_list: list):
    ratio_list = []
    for word in word_list:
        ratio = SequenceMatcher(None, query, word.lower()).ratio()
        print(ratio, end=" ")
        ratio_list.append(ratio)
    max_ratio = max(ratio_list)
    if max_ratio < 0.35: return "Too low!"
    else:
        idx = ratio_list.index(max_ratio)
        return word_list[idx]

lst = [
    "It's beginning!",
    "It's beginning!!!",
    "Triangular Phobia",
    "Peaceful & Healing",
    "Mini Bosses",
    "Swingggg",
    "Assemble! (Easy)",
    "Assemble! (Hard)",
    "Gimmicks!"
]

print("\n")

while True:
    print(most_similar(input().lower(), lst))