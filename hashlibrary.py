import numpy as np
from my_utils import cyclic_shift, xor_lists, cut_bits_of_number, collect_int_number, cut_uint64_num_into_list_uint16

_ROUNDS: int = 1  # количество проходов по сети Фейстеля


def _f1(m0: np.uint16, m1: np.uint16) -> np.uint16:
    """ (m0 <<< 4) + (m1 >> 2) """
    return (cyclic_shift(m0, 16, 4)) + (cyclic_shift(m1, 16, -2))


def _f2(m2: np.uint16, m3: np.uint16.numerator) -> np.uint16:
    """ (m2 <<< 7) ^ ~m3 """
    return cyclic_shift(m2, 16, 7) ^ (~m3)


def _Ek(message: list, round_keys: list) -> list:
    #  ...выполняем преобразование по раундам (сжимающая функция)
    cipher: list = np.copy(message)
    for i in range(_ROUNDS):
        cipher[0] = message[2] ^ (~round_keys[i])
        cipher[1] = _f1(message[0] ^ round_keys[i], message[1]) ^ message[3]
        cipher[2] = _f2(cipher[0], cipher[1]) ^ message[1]
        cipher[3] = message[0] ^ round_keys[i]
        message = np.copy(cipher)
    return cipher


def _create_round_keys(iv: np.uint64):
    round_keys: list = list()  # Создаём раундовые ключи
    for index in range(_ROUNDS):
        temp = cyclic_shift(iv, 64, -(index + 1)) ^ iv
        round_keys.append(np.uint16(cut_bits_of_number(temp, 64, 16)))
    return round_keys


def hash(path_from: str, iv: np.uint64) -> np.uint64:
    try:
        # Открываем файл, сообщение которого нужно захешировать
        with open(path_from, 'rb') as rfile:
            # h0, h1, ..., hi
            h: list = cut_uint64_num_into_list_uint16(iv)
            while True:
                # Проверка конца файла
                file_eof: bytes = rfile.read(1)
                rfile.seek(rfile.tell() - 1)
                if file_eof == b'':
                    break

                # Блок состоит из 4 частей
                message: list = list()
                for _ in range(4):
                    message.append(np.uint16(int.from_bytes(rfile.read(2), byteorder="little", signed=False)))

                # Создаём раундовые ключи
                round_keys: list = _create_round_keys(np.uint64(collect_int_number(h)))

                #  Хеширование
                h = xor_lists(xor_lists(_Ek(xor_lists(message, h), round_keys), h), message)

            result = np.uint64(collect_int_number(h))
            return result
    except FileNotFoundError:
        print("Невозможно открыть файл")
