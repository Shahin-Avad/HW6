"""
Задание 1.
Выполните профилирование памяти в скриптах
Проанализировать результат и определить программы с
наиболее эффективным использованием памяти.
Примечание: Для анализа возьмите любые 3-5 ваших РАЗНЫХ скриптов!
(хотя бы 3 разных для получения оценки отл).
На каждый скрипт вы должны сделать как минимум по две реализации.
Можно взять задачи с курса Основ
или с текущего курса Алгоритмов
Результаты профилирования добавьте в виде комментариев к коду.
Обязательно сделайте аналитику (что с памятью в ваших скриптах, в чем ваша оптимизация и т.д.)
ВНИМАНИЕ: ЗАДАНИЯ, В КОТОРЫХ БУДУТ ГОЛЫЕ ЦИФРЫ ЗАМЕРОВ (БЕЗ АНАЛИТИКИ)
БУДУТ ПРИНИМАТЬСЯ С ОЦЕНКОЙ УДОВЛЕТВОРИТЕЛЬНО
Попытайтесь дополнительно свой декоратор используя ф-цию memory_usage из memory_profiler
С одновременным замером времени (timeit.default_timer())!
"""
import memory_profiler
from timeit import default_timer


# 1)
def decor(func):
    def wrapper(*args):
        m1 = memory_profiler.memory_usage()
        start_time = default_timer()
        res = func(args[0])
        m2 = memory_profiler.memory_usage()
        mem_diff = m2[0] - m1[0]
        time_diff = default_timer() - start_time
        return res, mem_diff, time_diff
    return wrapper


@decor
def min_value(lst):
    min_v = lst[0]
    for i in lst:
        if i < min_v:
            min_v = i
    return min_v


res, mem_diff, time_diff = min_value(list(range(100000)))
print(f'выполнение заняло {mem_diff} MiB и {time_diff} секунд')


@decor
def min_value_two(lst):
    min_v = lst[0]
    for i in lst:
        if i < min_v:
            min_v = i
            yield min_v


res2, mem_diff2, time_diff2 = min_value(list(range(100000)))
print(f'выполнение заняло {mem_diff2} MiB и {time_diff2} секунд')

'''
Аналитика: по результатаим видно, что вторая реализация функции методом "ленивых вычичслений" с помощью генератора
расходует меньше память. Разницы по времени исполенния кода нет
'''

# 2)
@decor
def splitter(string):
    splitter_list = []
    for i in range(len(string)):
        for j in range(i + 1, len(string) + 1):
            if string[i:j] != string:
                splitter_list.append(hash(string[i:j]))
    return set(splitter_list)


res3, mem_diff3, time_diff3 = splitter('qwertyuiopasdfghjklzxcvbnmkdjfkdsafjkdashfkladsflkahsdfjasdfygldksnlcnvalkjfdasfhlksdaf')
print(f'выполнение заняло {mem_diff3} MiB и {time_diff3} секунд')


@decor
def splitter_two(string):
    splitter_list = []
    for i in range(len(string)):
        for j in range(i + 1, len(string) + 1):
            if string[i:j] != string:
                splitter_list.append(hash(string[i:j]))
                yield set(splitter_list)


res4, mem_diff4, time_diff4 = splitter('qwertyuiopasdfghjklzxcvbnmkdjfkdsafjkdashfkladsflkahsdfjasdfygldksnlcnvalkjfdasfhlksdaf')
print(f'выполнение заняло {mem_diff4} MiB и {time_diff4} секунд')

'''
Аналитика: по результатаим видно, что вторая реализация функции методом "ленивых вычичслений" с помощью генератора
расходует меньше память. Разницы по времени исполенния кода нет
'''

# 3)
import math
@memory_profiler.profile
def fact_sum(val):
    lst = [math.factorial(i) for i in range(1, val)]
    return sum(lst)


fact_sum(5000)


@memory_profiler.profile
def fact_sum_2(val):
    lst = (math.factorial(i) for i in range(1, val))
    return sum(lst)


fact_sum_2(1000)

'''
Аналитика: Во втором примере выполнения функции мы испольовали кортеж, вместо списка, что позволило сократить
использование памяти в 2 раза
'''