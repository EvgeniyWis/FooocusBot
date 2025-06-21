import random
from collections.abc import MutableSequence

from bot.logger import logger


class VariableValuesIsNull(Exception):
    """
    Вызывается, если переданный список значений пуст.
    """
    pass


def random_choice_variables_for_images(variable_values: MutableSequence[str]):
    """
    Функция рандомно выбирает значения переменных для имен переменных (key:value),
    с гарантией, что они не будут повторяться в течение заданного количества итераций и все будут использоваться.

    :param variable_values: Список значений переменных.
    :return: Генератор, который возвращает переменные по одному, случайным образом перемешивая их.
    :raises VariableValuesIsNull: Если переданный список значений пуст.
    """

    if not variable_values:
        logger.error(
            "Список значений переменных для генерации изображений пуст.",
        )
        raise VariableValuesIsNull("Список значений пуст.")

    while True:
        pool = variable_values[:]
        random.shuffle(pool)
        for variable_name in pool:
            yield variable_name
