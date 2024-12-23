import numpy as np
from telebot import *
import random

bot = telebot.TeleBot('7768681005:AAE7RASaIpE-BxVkwh4omQzjzsz9r9GO8pM')

# Глобальная переменная для хранения матрицы
matrix = None

# Функция для поворота матрицы по часовой стрелке
def rotate_clockwise(mat):
    return [list(row) for row in zip(*mat[::-1])]

# Функция для поворота матрицы против часовой стрелки
def rotate_counterclockwise(mat):
    return [list(row) for row in zip(*mat)][::-1]

# Функция для нахождения обратной матрицы
def inverse_matrix(mat):
    try:
        mat = np.array(mat)
        inv_mat = np.linalg.inv(mat)
        return inv_mat.tolist()
    except np.linalg.LinAlgError:
        return None

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global matrix
    matrix = None
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Ввести матрицу вручную")
    btn2 = types.KeyboardButton("Сгенерировать случайную матрицу")
    btn3 = types.KeyboardButton("Вывести матрицу")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Привет! Выберите способ ввода матрицы:", reply_markup=markup)

# Обработчик для выбора способа ввода матрицы
@bot.message_handler(func=lambda message: message.text in ["Ввести матрицу вручную", "Сгенерировать случайную матрицу", "Вывести матрицу"])
def handle_matrix_input_choice(message):
    if message.text == "Ввести матрицу вручную":
        bot.send_message(message.chat.id, "Введите матрицу через пробел, строки разделяйте точкой с запятой. Пример: 1 2; 3 4")
        bot.register_next_step_handler(message, process_manual_matrix_input)
    elif message.text == "Сгенерировать случайную матрицу":
        bot.send_message(message.chat.id, "Введите размер матрицы в формате 'rows columns' (например, 3 3 для 3x3 матрицы):")
        bot.register_next_step_handler(message, process_random_matrix_input)
    elif message.text == "Вывести матрицу":
        if matrix is not None:
            matrix_str = '\n'.join([' '.join(map(str, row)) for row in matrix])
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Повернуть по часовой стрелке", callback_data='rotate_clockwise')
            btn2 = types.InlineKeyboardButton("Повернуть против часовой стрелки", callback_data='rotate_counterclockwise')
            btn3 = types.InlineKeyboardButton("Ввести новую матрицу", callback_data='new_matrix')
            btn4 = types.InlineKeyboardButton("Найти обратную матрицу", callback_data='inverse_matrix')
            markup.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, f"Текущая матрица:\n{matrix_str}", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Матрица еще не была введена или сгенерирована.")

# Обработчик для ввода матрицы вручную
def process_manual_matrix_input(message):
    global matrix
    try:
        matrix_str = message.text
        rows = matrix_str.split(';')
        matrix = [list(map(int, row.split())) for row in rows]
        bot.send_message(message.chat.id, "Матрица успешно введена. Используйте кнопку 'Вывести матрицу', чтобы увидеть её.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при вводе матрицы: {e}")

# Обработчик для генерации случайной матрицы
def process_random_matrix_input(message):
    global matrix
    try:
        size_str = message.text
        rows, cols = map(int, size_str.split())
        if rows <= 0 or cols <= 0:
            raise ValueError("Размеры матрицы должны быть положительными числами.")
        matrix = [[random.randint(1, 9) for _ in range(cols)] for _ in range(rows)]
        bot.send_message(message.chat.id, "Матрица успешно сгенерирована. Используйте кнопку 'Вывести матрицу', чтобы увидеть её.")
    except ValueError as ve:
        bot.send_message(message.chat.id, f"Ошибка при вводе размера матрицы: {ve}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при генерации матрицы: {e}")

# Обработчик для поворота матрицы и нахождения обратной матрицы
@bot.callback_query_handler(func=lambda call: call.data in ['rotate_clockwise', 'rotate_counterclockwise', 'new_matrix', 'inverse_matrix'])
def handle_rotate_matrix(call):
    global matrix
    if call.data == 'new_matrix':
        bot.send_message(call.message.chat.id, "Введите новую матрицу через пробел, строки разделяйте точкой с запятой. Пример: 1 2; 3 4")
        bot.register_next_step_handler(call.message, process_manual_matrix_input)
    elif call.data == 'inverse_matrix':
        inv_matrix = inverse_matrix(matrix)
        if inv_matrix is not None:
            inv_matrix_str = '\n'.join([' '.join(map(str, row)) for row in inv_matrix])
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Повернуть по часовой стрелке", callback_data='rotate_clockwise')
            btn2 = types.InlineKeyboardButton("Повернуть против часовой стрелки", callback_data='rotate_counterclockwise')
            btn3 = types.InlineKeyboardButton("Ввести новую матрицу", callback_data='new_matrix')
            btn4 = types.InlineKeyboardButton("Найти обратную матрицу", callback_data='inverse_matrix')
            markup.add(btn1, btn2, btn3, btn4)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Обратная матрица:\n{inv_matrix_str}", reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "Матрица не имеет обратной.")
    elif matrix is not None:
        if call.data == 'rotate_clockwise':
            matrix = rotate_clockwise(matrix)
        elif call.data == 'rotate_counterclockwise':
            matrix = rotate_counterclockwise(matrix)
        matrix_str = '\n'.join([' '.join(map(str, row)) for row in matrix])
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Повернуть по часовой стрелке", callback_data='rotate_clockwise')
        btn2 = types.InlineKeyboardButton("Повернуть против часовой стрелки", callback_data='rotate_counterclockwise')
        btn3 = types.InlineKeyboardButton("Ввести новую матрицу", callback_data='new_matrix')
        btn4 = types.InlineKeyboardButton("Найти обратную матрицу", callback_data='inverse_matrix')
        markup.add(btn1, btn2, btn3, btn4)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Матрица после поворота:\n{matrix_str}", reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "Матрица еще не была введена или сгенерирована.")

# Запуск бота
bot.polling()