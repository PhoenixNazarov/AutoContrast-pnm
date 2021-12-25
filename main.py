from modules import image as im
from modules import timer


@timer.work_time
def main():
    image = im.Image('test/input/photo_2021-12-25_17-02-13.pnm')
    image.auto_contrast('test/output/photo_2021-12-25_17-02-13.pnm')


if __name__ == '__main__':
    main()
