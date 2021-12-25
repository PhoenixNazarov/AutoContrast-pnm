class BReader:
    def __init__(self, file):
        self.__file = file
        self.__ind = 0

    def next_row(self, wait_sep=True):
        if self.__ind >= len(self.__file):
            return None

        start_ind = self.__ind = self.__ind
        if wait_sep:
            while self.__file[self.__ind] != 10 and self.__ind + 1 < len(self.__file):
                self.__ind += 1
        else:
            while self.__ind + 1 < len(self.__file):
                self.__ind += 1

        self.__ind += 1
        return self.__file[start_ind: self.__ind]
