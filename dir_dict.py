"""
Нужно написать класс, который полностью повторяет интерфейс обычного dict,
но хранит все данные на диске в указанной директории. Причем все ключи — это файлы,
а значения — их содержимое. Значения — юникодные строки, при попытке записать
что-то другое, просто записывать строковое представление.

Кеша быть не должно, все изменения на диске должны мгновенно отражаться в объекте.
"""

from collections.abc import MutableMapping
import os


class DirDict(MutableMapping):

    def __init__(self, directory):
        if not os.path.exists(directory):
            os.mkdir(directory)
        self._root_dir = directory

    def __len__(self):
        return len(os.listdir(self._root_dir))

    def __getitem__(self, filename):
        if not filename:
            raise SyntaxError
        keypath = os.path.join(self._root_dir, filename)
        if os.path.exists(keypath):
            answer = ""
            with open(keypath, 'r') as f:
                for line in f:
                    answer += line
            return answer
        else:
            raise IndexError

    def __setitem__(self, filename, info):
        if not filename:
            raise SyntaxError
        keypath = os.path.join(self._root_dir, filename)
        with open(keypath, 'w') as f:
            f.write(str(info))

    def __delitem__(self, filename):
        os.remove(os.path.join(self._root_dir, filename))

    def __iter__(self):
        keys = os.listdir(self._root_dir)
        for key in keys:
            yield key

    def items(self):
        keys = os.listdir(self._root_dir)
        for key in keys:
            yield (key, self.__getitem__(key))


if __name__ == "__main__":
    pass
