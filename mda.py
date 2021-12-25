from modules import image as im


if __name__ == '__main__':
    # pth = 'test/input/images_1_.pnm'
    pth = 'test/input/918452.pnm'
    # pth = 'output.pnm'
    with open(pth, 'rb') as file:
        base = file.read()
    #     print(base[0], base[1], base[2])
    #     print(base[3], base[4], base[5], base[6])
    for i in base[:100]:
        if i == 10:
            print(10)
            continue
        print(i, chr(i))
    # print(len(base))

    img = im.Image(pth)
