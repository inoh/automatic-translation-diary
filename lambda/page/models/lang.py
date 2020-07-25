from enum import (Enum, auto)


class Lang(Enum):
    Ja = auto()
    En = auto()


    @classmethod
    def value_of(cls, name):
        return [lang for lang in cls if lang.name == name][0]
