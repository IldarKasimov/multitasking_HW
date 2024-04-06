# Задание №7
# � Напишите программу на Python, которая будет находить сумму элементов массива из 1000000 целых чисел.
# � Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
# � Массив должен быть заполнен случайными целыми числами от 1 до 100.
# � При решении задачи нужно использовать многопоточность, многопроцессорность и асинхронность.
# � В каждом решении нужно вывести время выполнения вычислений.

import threading
import multiprocessing
from random import randint
from time import time
import asyncio


def get_sum_thread(array):
    global total_sum_thread
    total_sum_thread += sum(array)


def get_sum_process(array, res):
    with res.get_lock():
        res.value += sum(array)


async def get_sum_asyncio(array):
    global total_sum_asyncio
    total_sum_asyncio += sum(array)


async def main_asyncio():
    tasks = [asyncio.create_task(get_sum_asyncio(array[part_aray * num:])) if
             num + 1 == COUNT_OPERATIONS and part_aray * (num + 1) != len(array) else
             asyncio.create_task(get_sum_asyncio(array[part_aray * num:part_aray * (num + 1)]))
             for num in range(COUNT_OPERATIONS)]
    await asyncio.gather(*tasks)


array = [randint(1, 100) for _ in range(1_000_000)]
COUNT_OPERATIONS = 50  # количество потоков/процессов/асинхронных запусков
part_aray = len(array) // COUNT_OPERATIONS  # обратная зависимость от COUNT_OPERATIONS, для подачи диапазона среза
total_sum_thread = 0  # глобальная переменная для подсчета суммы через потоки
total_sum_asyncio = 0  # глобальная переменная для подсчета суммы через асинхронность
result = multiprocessing.Value('i', 0)   # переменная для подсчета суммы через многопроцессорность

if __name__ == '__main__':

    # Запуск многопоточности

    threads = []
    start_time_threads = time()

    for num in range(COUNT_OPERATIONS):
        # проверка на последний цикл и на попадания всех элементов массива в список threads
        if num + 1 == COUNT_OPERATIONS and part_aray * (num + 1) != len(array):
            thread = threading.Thread(target=get_sum_thread(array[part_aray * num:]))
            threads.append(thread)
            thread.start()
        else:
            thread = threading.Thread(target=get_sum_thread(array[part_aray * num:part_aray * (num + 1)]))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()
        end_time_thread = time()
    print(f'Сумма элементов массива = {total_sum_thread}, подсчитана с использованием многопоточности за '
          f'{end_time_thread - start_time_threads:.2f} секунд')

    # Запуск многопроцессорности

    processes = []
    start_time_processes = time()
    for num in range(COUNT_OPERATIONS):
        if num + 1 == COUNT_OPERATIONS and part_aray * (num + 1) != len(array):
            process = multiprocessing.Process(target=get_sum_process, args=(array[part_aray * num:], result))
            processes.append(process)
            process.start()
        else:
            process = multiprocessing.Process(target=get_sum_process,
                                              args=(array[part_aray * num:part_aray * (num + 1)], result))
            processes.append(process)
            process.start()

    for process in processes:
        process.join()
        end_time_processes = time()
    print(f'Сумма элементов массива = {result.value}, подсчитана с использованием многопроцессорности за '
          f'{end_time_processes - start_time_processes:.2f} секунд')

# Запуск асинхронности

    start_time_asyncio = time()
    asyncio.run(main_asyncio())
    end_time_asyncio = time()
    print(f'Сумма элементов массива = {total_sum_asyncio}, подсчитана с использованием асинхронности за '
          f'{end_time_asyncio - start_time_asyncio:.2f} секунд')
