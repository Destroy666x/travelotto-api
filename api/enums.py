from enum import Enum


class GameQuestionStatus(Enum):
    TO_ANSWER = "TO_ANSWER"
    ANSWERED_CORRECTLY = "ANSWERED_CORRECTLY"
    ANSWERED_INCORRECTLY = "ANSWERED_INCORRECTLY"

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)
