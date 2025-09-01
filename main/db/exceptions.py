class InvalidDict(Exception):
    def __str__(self):
        return "Necessary keys are not found"

class InvalidDetailsDict(Exception):
    def __str__(self):
        return "Necessary keys for DetailsDict are not found"

class NoSuchUser(Exception):
    def __str__(self):
        return "No such user"

class ExistingUser(Exception):
    def __str__(self):
        return "Existing user"

class NoSuchLevel(Exception):
    def __str__(self):
        return "No such level"

class NoSuchQuest(Exception):
    def __str__(self):
        return "No such quest"

class InvalidStars(Exception):
    def __str__(self):
        return "Invalid stars"

class NoSuchDifficulty(Exception):
    def __str__(self):
        return "No such difficulty, maybe the value is not between 1~5."