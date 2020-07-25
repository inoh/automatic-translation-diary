from abc import ABCMeta, abstractmethod


class DiaryRepository(metaclass=ABCMeta):
    @abstractmethod
    def diaries(self):
        pass
