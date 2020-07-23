from dataclasses import dataclass


@dataclass(frozen=True)
class DiaryId:
    id: str

    def __eq__(self, other):
        return self.id == other.id
