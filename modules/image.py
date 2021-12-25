from modules import timer
from modules.byte_reader import BReader

INF = 256


def func_normalize(MIN, MAX, value):
    # if random.randint(0, 100) < 10:
    #     return value
    val = round((value - MIN) * (255 / (MAX - MIN)))
    if val <= 0:
        return 0
    if val >= 255:
        return 255
    return val


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

    def parse(self, base):
        raise

    def save(self):
        raise

    def min_max_normalize(self):
        if self.R_MAX == INF:
            self.R_MAX = 250
        if self.R_MIN == 0:
            self.R_MIN = 5

        if self.G_MAX == INF:
            self.G_MAX = 250
        if self.G_MIN == 0:
            self.G_MIN = 5

        if self.B_MAX == INF:
            self.B_MAX = 250
        if self.B_MIN == 0:
            self.B_MIN = 5


class PpmPixels(Pixels):
    def parse(self, base, type_=None):
        if type_ == 'parallel':
            print('not work')
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

    def save(self):
        self.min_max_normalize()
        ret = []
        for row in self._colors:
            for color in row:
                ret.append(func_normalize(self.R_MIN, self.R_MAX, color[0]))
                ret.append(func_normalize(self.G_MIN, self.G_MAX, color[1]))
                ret.append(func_normalize(self.B_MIN, self.B_MAX, color[2]))

        return ret

    def print_val(self):
        # logging
        printable = {
            'R': [self.R_MIN, self.R_MAX],
            'B': [self.B_MIN, self.B_MAX],
            'G': [self.G_MIN, self.G_MAX],
        }
        print('Current value: [min. max]')
        for i in printable:
            print(f'channel {i}: [{printable[i][0]}, {printable[i][1]}]')
        print()


class PgmPixels(Pixels):
    def parse(self, base, type_=None):
        ind = 0
        for x in range(self._rows):
            row = []
            for y in range(self._columns):
                row.append(base[ind])
                self.R_MIN = min(self.R_MIN, base[ind])
                self.R_MAX = max(self.R_MAX, base[ind])
                ind += 1
            self._colors.append(row)

    def save(self):
        self.min_max_normalize()
        ret = []
        for row in self._colors:
            for color in row:
                ret.append(func_normalize(self.R_MIN, self.R_MAX, color[0]))
        return ret


class Image:
    def __init__(self, path_input):
        self.header = b''
        self.__matrix = Pixels()
        self.__read_image(path_input)

    def auto_contrast(self, path_save):
        self.__processing_and_save(path_save)

    @timer.work_time
    def __open_file(self, path):
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
        return strings

    def __read_image(self, path):
        strings = self.__open_file(path)

        print('Image data:')
        type_ = strings[0][:-1]
        if type_ == b'P6':
            print('Current format: P6(Ppm)')
            self.__matrix = PpmPixels()
        elif type_ == b'P5':
            print('P5 Not tested')
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
        try:
            # only 255
            max_val = int(str(strings[ind_comment][:-1])[2:-1])
        except:
            raise 'Cant encode'

        print('Width:', column)
        print('Height:', rows)
        print('Max value:', max_val)
        print()

        if max_val != 255:
            raise 'Max value should be 255'
        self.__matrix.set_size(column, rows, max_val)
        self.__load_channels(strings[-1])
        self.__matrix.print_val()

    @timer.work_time
    def __load_channels(self, row):
        self.__matrix.parse(row)

    @timer.work_time
    def __processing_and_save(self, path):
        with open(path, 'wb') as file:
            file.write(self.header)
            for byte in self.__matrix.save():
                file.write(byte.to_bytes(1, 'big'))

