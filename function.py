import random
# Функции для поворота матрицы
def rotate_matrix_clockwise(matrix):
    """
    Функция для поворота матрицы на 90 градусов по часовой стрелке.

    :param matrix: Исходная матрица
    :return: Повернутая матрица
    """
    rows = len(matrix)
    cols = len(matrix[0])
    rotated_matrix = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            rotated_matrix[j][rows - 1 - i] = matrix[i][j]
    return rotated_matrix

def rotate_matrix_counterclockwise(matrix):
    """
    Функция для поворота матрицы на 90 градусов против часовой стрелки.

    :param matrix: Исходная матрица
    :return: Повернутая матрица
    """
    rows = len(matrix)
    cols = len(matrix[0])
    rotated_matrix = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            rotated_matrix[cols - 1 - j][i] = matrix[i][j]
    return rotated_matrix

def matrix_to_string(matrix):
    """
    Функция для преобразования матрицы в строку для отправки в Telegram.

    :param matrix: Матрица
    :return: Строка, представляющая матрицу
    """
    return '\n'.join([' '.join(map(str, row)) for row in matrix])

def generate_random_matrix(rows, cols):
    """
    Функция для генерации случайной матрицы.

    :param rows: Количество строк
    :param cols: Количество столбцов
    :return: Случайная матрица
    """
    return [[random.randint(0, 9) for _ in range(cols)] for _ in range(rows)]