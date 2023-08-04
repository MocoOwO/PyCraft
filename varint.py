def de_varint(num):
    res = 0
    offset, size = 0, len(num)
    for i in range(size):
        if (num[i] & 0x80) == 0x80:
            res |= (num[i] & 0x7f) << offset
        else:
            res |= num[i] << offset
            break
        offset += 7
    return res


def varint(num):
    res = []
    temp = ''
    while num:
        if (num >> 7) != 0:
            res.append(0x80 | (num & 0x7F))
            num = num >> 7
        else:
            res.append(num & 0x7F)
            break
    for i in res:
        if len(hex(i)[2:]) == 1:
            temp += '0' + hex(i)[2:]
        else:
            temp += hex(i)[2:]
    if num == 0:
        temp = '00'
    return bytes.fromhex(temp)


def MCString(string):
    data = b''
    data += varint(len(string))
    data += bytes(string, encoding='utf-8')
    return data


if __name__ == "__main__":
    s = varint(128)
    print(s)
    num = de_varint(s)
    print(num)
