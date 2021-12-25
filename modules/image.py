import random
import time

from modules import timer
from modules.byte_reader import BReader

INF = 256


class Pixels:
    R_MAX = 0
    R_MIN = INF

    G_MAX = 0
    G_MIN = INF

    B_MAX = 0
    B_MIN = INF

    def __init__(self):
        self._columns = None
        self._rows = None
        self._max_val = None

        self._colors = []

    def set_size(self, columns, rows, max_val):
        self._columns = columns
        self._rows = rows
        self._max_val = max_val

    def save(self):
        raise


class PpmPixels(Pixels):
    @timer.work_time
    def parse(self, base, type_):
        if type_ == 'parallel':
            self.__parse_parallel(base)
        else:
            self.__parse_norm(base)

    def __parse_norm(self, base):
        ind = 0
        for x in range(self._rows):
            row = []
            for y in range(self._columns):
                col = [base[ind]]

                self.R_MIN = min(self.R_MIN, base[ind])
                self.R_MAX = max(self.R_MAX, base[ind])
                ind += 1

                col.append(base[ind])
                self.G_MIN = min(self.G_MIN, base[ind])
                self.G_MAX = max(self.G_MAX, base[ind])
                ind += 1

                col.append(base[ind])
                self.B_MIN = min(self.B_MIN, base[ind])
                self.B_MAX = max(self.B_MAX, base[ind])
                ind += 1

                row.append(col)
            self._colors.append(row)
        print(self.R_MIN, self.R_MAX, self.B_MIN, self.B_MAX, self.G_MIN, self.G_MAX)

    def __parse_parallel(self, base):
        import pymp
        # base = pymp.shared.array(base, dtype = 'uint8')

        with pymp.Parallel(4) as p:
            for index in p.range(0, 100):
                base[index] = 1
                # The parallel print function takes care of asynchronous output.
                p.print('Yay! {} done!'.format(index))

        ind = 0
        for x in range(self._rows):
            row = []
            for y in range(self._columns):
                col = [base[ind]]

                self.R_MIN = min(self.R_MIN, base[ind])
                self.R_MAX = max(self.R_MAX, base[ind])
                ind += 1

                col.append(base[ind])
                self.G_MIN = min(self.G_MIN, base[ind])
                self.G_MAX = max(self.G_MAX, base[ind])
                ind += 1

                col.append(base[ind])
                self.B_MIN = min(self.B_MIN, base[ind])
                self.B_MAX = max(self.B_MAX, base[ind])
                ind += 1

                row.append(col)
            self._colors.append(row)
        print(self.R_MIN, self.R_MAX, self.B_MIN, self.B_MAX, self.G_MIN, self.G_MAX)

    @timer.work_time
    def save(self):
        ret = []
        for row in self._colors:
            for color in row:
                ret.append(func(self.R_MIN, self.R_MAX, color[0]))
                ret.append(func(self.G_MIN, self.G_MAX, color[1]))
                ret.append(func(self.B_MIN, self.B_MAX, color[2]))

        return ret

def func(MIN, MAX, value):
    # if random.randint(0, 100) < 10:
    #     return value
    val = round((value - MIN) * (255 / (MAX - MIN)))
    if val <= 0:
        return 0
    if val >= 255:
        return 255
    return val


class PgmPixels(Pixels):
    def parse(self, base):
        ind = 0
        for x in range(self._rows):
            row = []
            for y in range(self._columns):
                row.append(base[ind])
                ind += 1
            self._colors.append(row)


class Image:
    def __init__(self, path):
        self.header = b''
        self.__matrix = Pixels()
        self.__read_image(path)

    def __read_image(self, path):
        with open(path, 'rb') as file:
            reader = BReader(file.read())
        strings = []
        while 1:
            wait = True
            if len(strings) >= 3:
                wait = False
            a = reader.next_row(wait_sep = wait)
            if a is None:
                break
            if wait:
                self.header += a
            strings.append(a)

        type_ = strings[0][:-1]
        if type_ == b'P6':
            self.__matrix = PpmPixels()
        elif type_ == b'P5':
            self.__matrix = PgmPixels()
        else:
            raise 'Cant encode'

        # skip comment
        ind_comment = 1
        while strings[ind_comment][0] == b'#':
            ind_comment += 1

        try:
            column, rows = map(int, str(strings[ind_comment][:-1])[2:-1].split())
            ind_comment += 1
        except:
            raise 'Cant encode'
        print(column, rows)
        try:
            # only 255
            max_val = int(str(strings[ind_comment][:-1])[2:-1])
        except:
            raise 'Cant encode'

        if max_val != 255:
            raise 'Max value should be 255'
        print(len(strings[-1]))
        self.__matrix.set_size(column, rows, max_val)
        self.__matrix.parse(strings[-1], 'parallel')
        self.save('output1.pnm')

    def save(self, path):
        with open(path, 'wb') as file:
            file.write(self.header)
            for byte in self.__matrix.save():
                # print(byte, bytes(str(byte)))
                file.write(byte.to_bytes(1, 'big'))

# def auto_contrast():
# img = Image(path)
