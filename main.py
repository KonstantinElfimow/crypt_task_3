import numpy as np
import random
from hashlibrary import hash
import my_utils
import time


def compare_hashes(current: list, h: np.uint64, iv: np.uint64) -> bool:
    my_utils.save_list_in_file('./crypto_hash/input/input.txt', current)
    comparable: np.uint64 = hash('./crypto_hash/input/input.txt', iv)

    if h == comparable:
        my_utils.save_in_file('./crypto_hash/output/output.txt', comparable)
        print("h: ", h, "comparable:", comparable)
        return True
    return False


def gen_all_combo_and_compare_hashes(elements: list, current: list, next: int, used: list, h: np.uint64, iv: np.uint64) -> None:
    """ Рекурсивно создаются различные размещения в последовательности символов (сложность: O(n!)),
    затем получаем их хеш и сравниваем с требуемым хешем."""
    for i in range(len(elements)):
        if not used[i]:
            used[i] = True
            current[next] = elements[i]
            gen_all_combo_and_compare_hashes(elements, current, next + 1, used, h, iv)
            used[i] = False

            if next == len(elements) - 1:
                is_equal = compare_hashes(current, h, iv)
                if is_equal:
                    return


def factorial(n):
    f = 1
    for i in range(n, 1, -1):
        f = f * i
    return f


def boot_force(elements: list, h: np.uint64, iv: np.uint64) -> None:
    used = list()
    for i in range(len(elements)):
        used.append(False)

    start = time.perf_counter()
    gen_all_combo_and_compare_hashes(elements, np.copy(elements), 0, used, h, iv)
    per_sec = (time.perf_counter() - start) / factorial(len(elements))

    print("Общее среднее время (в днях), требуемое для рассчёта все возможных случаев хеша (2 ^ 64): ",
          (2 ** 64) * per_sec / 3600 / 24)


def task_hash() -> None:
    iv = np.uint64(random.randint(1, 18446744073709551616))
    print("Вектор инициализации:", iv)

    h: np.uint64 = hash('./crypto_hash/input/for_collision.txt', iv)
    print("Энтропия: ", my_utils.entropy(bytearray(my_utils.to_bits(h, 64), "UTF-8")))
    my_utils.save_in_file('./crypto_hash/output/output_collision.txt', h)

    data = list('abcde')
    boot_force(data, h, iv)


def main():
    task_hash()


if __name__ == '__main__':
    main()
