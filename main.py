import numpy as np
import random
from hashlibrary import hash
import my_utils
import time

IV: np.uint64 = np.uint64(random.randint(1, 18446744073709551616))
# IV: np.uint64 = np.uint64(5128838431977526119)


def compare_hashes(current: list, for_collision: np.uint64) -> bool:
    my_utils.save_list_in_file('./crypto_hash/input/input.txt', current)
    comparable: np.uint64 = hash(IV, path_from='./crypto_hash/input/input.txt')
    my_utils.save_in_file('./crypto_hash/output/output.txt', comparable)

    if for_collision == comparable:
        print("h: ", for_collision, "comparable:", comparable)
        return True
    return False


def gen_all_combo_and_compare_hashes(elements: list, current: list, next: int, used: list,
                                     for_collision: np.uint64) -> bool:
    """ Рекурсивно создаются различные размещения в последовательности символов (сложность: O(n!)),
    затем получаем хеш последовательностей и сравниваем с требуемым хешем. Возвращаем bool значение равенства хешей.
    Нужный хеш записывается в output.txt, а входное сообщение в input.txt. """
    for i in range(len(elements)):
        if not used[i]:
            used[i] = True
            current[next] = elements[i]
            gen_all_combo_and_compare_hashes(elements, current, next + 1, used, for_collision)
            used[i] = False

            if next == len(elements) - 1:
                if compare_hashes(current, for_collision):
                    return True
    return False


def factorial(n) -> int:
    f = 1
    for i in range(n, 1, -1):
        f = f * i
    return f


def brute_force(input: list, for_collision: np.uint64) -> None:
    used = list()
    for i in range(len(input)):
        used.append(False)

    # В теории забрутфорсить можно, но времени уйдёт овермного, а шанс равен 1 / (2 ** 64),
    # поэтому просто посчитаем, сколько времени в теории уйдёт на поиск коллизии
    start = time.perf_counter()
    value = gen_all_combo_and_compare_hashes(input, np.copy(input), 0, used,
                                             for_collision)
    per_sec = (time.perf_counter() - start) / factorial(len(input))

    # Вряд ли найдёт, но проверка есть
    print("Требуемая коллизия найдена? ", value)

    print("Общее среднее время (в днях), требуемое для рассчёта все возможных случаев хеша (2 ^ 64): ",
          (2 ** 64) * per_sec / 3600 // 24)


def determine_the_avalanche_effect_of_hash():
    """ Зависимость всех выходных битов от каждого входного бита. Отличие выходных битов для хорошего криптографического
    алгоритма хеширования должно составлять в среднем 50% при разнице в один бит (что оно и делает). """

    m1: bytes = bytes("aaaaaaaaaaaaaaaa", "UTF-8")
    m2: bytes = bytes("baaaaaaaaaaaaaaa", "UTF-8")

    h1 = hash(IV, message=m1)
    h2 = hash(IV, message=m2)

    my_utils.save_in_file('crypto_hash/output/output_1.txt', h1)
    my_utils.save_in_file('crypto_hash/output/output_2.txt', h2)

    width: int = 64
    h1 = my_utils.to_bits(h1, width)
    h2 = my_utils.to_bits(h2, width)

    coincidence = 0
    for i in range(width):
        if h1[i] == h2[i]:
            coincidence += 1

    return coincidence / width


def task_hash() -> None:
    print("Вектор инициализации:", IV)

    print("Лавинный эффект (вероятность совпадения битов): ", determine_the_avalanche_effect_of_hash())

    # Ищем кеш для коллизии
    h: np.uint64 = hash(IV, path_from='./crypto_hash/input/for_collision.txt')
    print("Энтропия: ", my_utils.entropy(bytearray(my_utils.to_bits(h, 64), "UTF-8")))
    my_utils.save_in_file('./crypto_hash/output/output_collision.txt', h)

    # Создаём различные комбинации букв латинского алфавита, чтобы получить (навряд ли) коллизию ф-ии хеширования,
    # когда h1 == h2 и m1 != m2.
    data = list("abcdef")
    brute_force(data, h)


def main():
    task_hash()


if __name__ == '__main__':
    main()
