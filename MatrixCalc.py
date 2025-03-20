import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from ctypes import *
from datetime import datetime

matrix_lib = cdll.LoadLibrary('./matrixcalc_lib')
help_menu = True  # Флаг выставленного поля предпросмотра способа записи

# define'ы
MATRIX1, MATRIX2, BACK_UP_MATRIX = (1, 2, 3)
MATRIX_MAX_SIZE = 1002  # Работа с матрицами меньше чем 32x32 (избыточная размерность)


# класс для взаимодействия с dll
class tu_matrix:
    """
    Назначение: Класс для перевода данных из python в c_types данные с сохранением служебной информации
    """

    def __init__(self):
        """
        Назначение: Конструктор, создающий принадлежащее классу поле

        self.body -- массив из MATRIX_MAX_SIZE элементов c_double
        """
        self.body = (c_double * MATRIX_MAX_SIZE)(c_double(0))

    def load(self, data=list(list())) -> None:
        """
        Назначение: Загрузка данных для подготовки к их переводу в dll

        :param data: список списков, содержащий информацию о данных матрицы (по умолчанию пустой)
        """
        self.data = data
        self.n_size = len(data)
        self.m_size = len(data[0])
        self.body[0] = c_double(self.n_size)
        self.body[1] = c_double(self.m_size)
        for i in range(self.n_size):
            for j in range(self.m_size):
                self.body[2 + i * self.m_size + j] = c_double(data[i][j])

    def send(self) -> (c_double * MATRIX_MAX_SIZE):
        """
        Назначение: выдача данных для отправки в dll библиотеку

        :return: self.body -- массив из MATRIX_MAX_SIZE элементов c_double
        """
        return self.body


class Settings:
    def __init__(self):
        self.out_matrix = MATRIX1
        self.precession = 2
        self.log_need = True

    def set_precession(self, precession):
        self.precession = precession

    def set_out_matrix(self, num_out_matrix):
        self.out_matrix = num_out_matrix

    def set_log_need(self, log_need):
        self.log_need = log_need


# Матрицы python-представления
matrix1 = list(list())
matrix2 = list(list())
back_up_matrix = list(list())

# Юниты трансляции данных из python в dll
tu_matrix1 = tu_matrix()
tu_matrix2 = tu_matrix()

# Настройки
setting = Settings()


def init_library() -> None:
    # Определение типов аргументов для функции matrix_ariphmetic
    matrix_lib.matrix_ariphmetic.argtypes = [POINTER(c_double * MATRIX_MAX_SIZE),  # Массив arr1
                                             POINTER(c_double * MATRIX_MAX_SIZE)]  # Массив arr2
    # Определение возвращаемого значения для функции matrix_ariphmetic
    matrix_lib.matrix_ariphmetic.restype = int  # Число-флаг

    # Определение типов аргументов для функции matrix_algo
    matrix_lib.matrix_inv_ready.argtypes = [POINTER(c_double * MATRIX_MAX_SIZE)]  # Массив arr1
    # Определение возвращаемого значения для функции matrix_algo
    matrix_lib.matrix_inv_ready.restype = int  # Число-флаг

    # Определение типов аргументов для функции matrix_algo
    matrix_lib.matrix_algo.argtypes = [POINTER(c_double * MATRIX_MAX_SIZE),  # Массив arr1
                                       POINTER(c_double * MATRIX_MAX_SIZE)]  # Массив arr2
    # Определение возвращаемого значения для функции matrix_algo
    matrix_lib.matrix_algo.restype = int  # Число-флаг

    # Определение типов аргументов для функции calc_det
    matrix_lib.calc_det.argtypes = [POINTER(c_double * MATRIX_MAX_SIZE)]  # Массив arr1
    # Определение возвращаемого значения для функции calc_det
    matrix_lib.calc_det.restype = c_double  # Значение детерминанта

    # Определение типов аргументов для функции matrix_sum
    matrix_lib.matrix_sum.argtypes = [POINTER(c_double * MATRIX_MAX_SIZE),  # Массив arr1
                                      POINTER(c_double * MATRIX_MAX_SIZE)]  # Массив arr2
    # Определение возвращаемого значения для функции matrix_sum
    matrix_lib.matrix_sum.restype = POINTER(c_double * MATRIX_MAX_SIZE)  # Указатель на массив double

    # Определение типов аргументов для функции matrix_mul
    matrix_lib.matrix_mul.argtypes = [POINTER(c_double * MATRIX_MAX_SIZE),  # Массив arr1
                                      POINTER(c_double * MATRIX_MAX_SIZE)]  # Массив arr2
    # Определение возвращаемого значения для функции matrix_mul
    matrix_lib.matrix_mul.restype = POINTER(c_double * MATRIX_MAX_SIZE)  # Указатель на массив double

    # Определение типов аргументов для функции matrix_sub
    matrix_lib.matrix_sub.argtypes = [POINTER(c_double * MATRIX_MAX_SIZE),  # Массив arr1
                                      POINTER(c_double * MATRIX_MAX_SIZE)]  # Массив arr2
    # Определение возвращаемого значения для функции matrix_sub
    matrix_lib.matrix_sub.restype = POINTER(c_double * MATRIX_MAX_SIZE)  # Указатель на массив double

    # Определение типов аргументов для функции matrix_div
    matrix_lib.matrix_div.argtypes = [POINTER(c_double * MATRIX_MAX_SIZE),  # Массив arr1
                                      POINTER(c_double * MATRIX_MAX_SIZE)]  # Массив arr2
    # Определение возвращаемого значения для функции matrix_div
    matrix_lib.matrix_div.restype = POINTER(c_double * MATRIX_MAX_SIZE)  # Указатель на массив double

    # Определение типов аргументов для функции matrix_T
    matrix_lib.matrix_T.argtypes = [POINTER(c_double * MATRIX_MAX_SIZE)]  # Массив arr1
    # Определение возвращаемого значения для функции matrix_T
    matrix_lib.matrix_T.restype = POINTER(c_double * MATRIX_MAX_SIZE)  # Указатель на массив double

    # Определение типов аргументов для функции matrix_inv
    matrix_lib.matrix_inv.argtypes = [POINTER(c_double * MATRIX_MAX_SIZE)]  # Массив arr1
    # Определение возвращаемого значения для функции matrix_inv
    matrix_lib.matrix_inv.restype = POINTER(c_double * MATRIX_MAX_SIZE)  # Указатель на массив double


def preset_delete(event) -> None:
    """
    Назначение: очистка окна предварительного объяснения

    """
    global help_menu, matrix1, back_up_matrix

    if (help_menu):
        entry_matrix1.delete("1.0", tk.END)
        matrix1 = back_up_matrix
        fill_result(matrix1, MATRIX1)
        help_menu = False


def fill_preset() -> None:
    """
    Назначение: представление полученных данных в поле пользовательского ввода первой матрицы

    :param list_of_lists: представление матрицы, которое будет установлено в поле пользовательского ввода первой матрицы
    """
    text = ("Пример заполнения матрицы\n1.2 7\n2\nСтроки автоматически дополняются до максимальной длины "
            "нулями(0).\nПолученная матрица:\n|1.2, 7 |\n| 2,  0 |\n\n-- При активном меню помощи нажатие на кнопки "
            "показывает информацию\nо них. При наличии данного теста меню помощи активировано\n-- Для выхода "
            "установите курсор в поле матрица1\n\n"
            "Текущие настройки:\n"
            f"Точность(кол-во знаков, использующихся для вычислений): {setting.precession}\n"
            f"Запись результатов производится в матрицу{setting.out_matrix}\n"
            f"Статус логирования (True-включено, False-отключено): {setting.log_need}"
            
            "\n\nДоступные операции:\nX   -- умножение матриц. (Бинарная операция М1 X М2)."
            "\n/   -- деление матриц. (Бинарная операция М1 / М2)."
            "\n+   -- сложение матриц. (Бинарная операция М1 + М2)."
            "\n-   -- вычитание матриц. (Бинарная операция М1 - М2)."
            "\nT   -- транспонирование матрицы. (Унарная операция T(М1))."
            "\n^-1 -- вычисление обратной матрицы. (Унарная операция М1^(-1)).")
    entry_matrix1.delete("1.0", tk.END)
    entry_matrix1.insert("1.0", text)


"""
# ---------------------------------------------------------
#   Блок работы с dll-библиотекой для вычисления значений
# ---------------------------------------------------------
"""


def get_matrix() -> None:
    """
    Назначение: получает данные из полей пользовательского ввода в matrix1 и matrix2

    """
    # установка видимости для переменных
    global matrix1, matrix2

    list_matrix = [entry_matrix1, entry_matrix2]

    for matrixn in list_matrix:
        # Получаем текст из текстового поля и убираем лишние пробелы
        user_input = matrixn.get("1.0", tk.END).strip()

        # Разделяем текст на строки
        lines = user_input.splitlines()

        # Инициализируем массив массивов
        array_of_arrays = []

        # Находим максимальное количество чисел в строках
        max_length = 0
        for line in lines:
            # Убираем пробелы в конце строки и разбиваем её, сохраняя только числовые значения
            numbers = [float(num) for num in line.strip().split() \
                       if num.replace('.', '', 1).replace('-', '', 1).isdigit()]
            array_of_arrays.append(numbers)  # Добавляем массив чисел для этой строки
            max_length = max(max_length, len(numbers))  # Обновляем максимальную длину

        # Дополняем каждую строку нулями до максимальной длины
        for i in range(len(array_of_arrays)):
            while len(array_of_arrays[i]) < max_length:
                array_of_arrays[i].append(0)

        if matrixn == entry_matrix1:  # Устанавливаем полученные данные в матрицу, на которой находится итератор
            matrix1 = array_of_arrays
        elif matrixn == entry_matrix2:
            matrix2 = array_of_arrays


def c_matrix() -> (POINTER(c_double * MATRIX_MAX_SIZE), POINTER(c_double * MATRIX_MAX_SIZE)):
    """
    Назначение: загрузка глобальных matrix1 и matrix2 в тип данных tu_matrix, для работы с dll библиотекой и получение
                указателей на массивы (c_double * MATRIX_MAX_SIZE)

    :return: ptr1 -- указатель на первый массив, заполненный данными matrix1
             ptr2 -- указатель на второй массив, заполненный данными matrix2
    """
    # установка видимости для переменных
    global matrix1, matrix2

    if matrix1: tu_matrix1.load(matrix1)
    if matrix2: tu_matrix2.load(matrix2)

    # Получение указателей на массивы
    ptr1 = pointer(tu_matrix1.send())  # Получаем указатель на первый массив
    ptr2 = pointer(tu_matrix2.send())  # Получаем указатель на второй массив

    return ptr1, ptr2


def able_matrix_op(ptr1: POINTER(c_double * MATRIX_MAX_SIZE), ptr2: POINTER(c_double * MATRIX_MAX_SIZE)) -> bool:
    """
    Назначение: проверка возможности выполнения выбранной пользователем операции над введенными матрицами

    :param ptr1: указатель на массив, передающий информацию о матрице1 в dll библиотеку
    :param ptr2: указатель на массив, передающий информацию о матрице2 в dll библиотеку
    :return: true -- если операция возможна, false -- если операция невозможна
    """
    result = True

    selected_action = option_var.get()  # Выбранный пользователем вид операции над матрицами

    # Проверка на возможность арифметических действий над матрицами
    if selected_action in ['+', '-']:
        if not matrix1 or not matrix2: return False

        # Информация от c++ о возможности произведения арифметических действий
        # 1 -- операция возможна; 0 -- операция невозможна
        c_answer = matrix_lib.matrix_ariphmetic(ptr1, ptr2)

        if c_answer == 1:
            result = True
        else:
            show_message(f"""
            Пожалуйста, измените размерности Ваших матриц, 
            чтобы они были одинаковы
            текущие размерности:
            Матрица1 [{len(matrix1)} X {len(matrix1[0])}]
            Матрица2 [{len(matrix2)} X {len(matrix2[0])}]
            """)
            result = False

    # Проверка на возможность умножения матриц
    elif selected_action in ['X']:
        if not matrix1 or not matrix2: return False

        # Информация от c++ о возможности умножения матриц
        # 1 -- операция возможна; 0 -- операция невозможна
        c_answer = matrix_lib.matrix_algo(ptr1, ptr2)

        if c_answer == 1:
            result = True
        else:
            show_message(f"""
                    -- Пожалуйста, измените размерности Ваших 
                    матриц, чтобы количество столбцов матрицы1 
                    соответствовало количеству строк матрицы2
                    текущие размерности:
                    Матрица1 [{len(matrix1)} X {len(matrix1[0])}]
                    Матрица2 [{len(matrix2)} X {len(matrix2[0])}]
                    """)
            result = False

    elif selected_action in ['/']:
        if not matrix1 or not matrix2: return False
        if len(matrix2) == 1 and len(matrix2[0]) == 1: return True

        if len(matrix1) == len(matrix1[0]) and len(matrix2) == len(matrix2[0]):
            # Информация от c++ о возможности нахождения обратной матрицы для матрицы2
            # 1 -- операция возможна; 0 -- операция невозможна
            c_answer = matrix_lib.matrix_inv_ready(ptr2)
            if c_answer == 1:
                result = True
            else:
                show_message(f"""
                        -- Ваша матрица2 не имеет возможности 
                        вычислить обратную матрицу, т.к ее 
                        определитель равен 0. Измените матрицу 2""")
                result = False
        else:
            show_message(f"""
                            -- Деление матриц доступно только  
                            только для квадратных матриц (кол-во  
                            столбцов соответствует количеству строк)
                            Текущие размерности:
                            Матрица1 [{len(matrix1)} X {len(matrix1[0])}]
                            Матрица2 [{len(matrix2)} X {len(matrix2[0])}]
                            """)
            result = False


    elif selected_action in ['^-1']:
        if not matrix1: return False

        # Информация от c++ о возможности нахождения обратной матрицы
        # 1 -- операция возможна; 0 -- операция невозможна
        c_answer = matrix_lib.matrix_inv_ready(ptr1)

        if len(matrix1) == len(matrix1[0]):
            if c_answer == 1:
                result = True
            else:
                show_message(f"""
                        -- Ваша матрица1 не имеет возможности 
                        вычислить обратную матрицу, т.к ее 
                        определитель равен 0. Измените матрицу 1""")
                result = False
        else:
            show_message(f"-- Ваша матрица2 не имеет возможности вычислить обратную матрицу. Обратная матрица может "
                         f"быть найдена только для квадратной матрицы. Текущая размерность матрицы: [{len(matrix1)},"
                         f"{len(matrix1[0])}]")

    elif selected_action in ['T']:
        if not matrix1: return False

    return result


def op_by_matrix(ptr1: POINTER(c_double * MATRIX_MAX_SIZE), ptr2: POINTER(c_double * MATRIX_MAX_SIZE)) \
        -> POINTER(c_double * MATRIX_MAX_SIZE):
    """
    Назначение: произведение операций dll-библиотекой над введенными пользователем матрицами, преобразованными в
                указатели на массивы

    :param ptr1: указатель на массив, передающий информацию о матрице1 в dll библиотеку
    :param ptr2: указатель на массив, передающий информацию о матрице2 в dll библиотеку
    :return: result_ptr -- указатель на массив, являющийся представлением матрицы после произведенных над ней операций
    """
    selected_action = option_var.get()
    if (selected_action == '+'):
        result_ptr = matrix_lib.matrix_sum(ptr1, ptr2)

    elif (selected_action == '-'):
        result_ptr = matrix_lib.matrix_sub(ptr1, ptr2)

    elif (selected_action == 'X'):
        result_ptr = matrix_lib.matrix_mul(ptr1, ptr2)

    elif (selected_action == '/'):
        result_ptr = matrix_lib.matrix_div(ptr1, ptr2)

    elif (selected_action == 'T'):
        result_ptr = matrix_lib.matrix_T(ptr1)

    elif (selected_action == '^-1'):
        result_ptr = matrix_lib.matrix_inv(ptr1)

    return result_ptr


def convert_result(result_ptr: POINTER(c_double * MATRIX_MAX_SIZE)) -> list(list()):
    """
    Назначение: обратный перевод данных из одномерного массива (c_types) в список списков (python-style)

    :param result_ptr: указатель на массив, являющийся результатом операций над матрицами
    :return: list_of_lists -- матрица в python представлении
    """
    # Преобразование результата в массив c_double
    result_array = result_ptr.contents  # Теперь у вас есть доступ к содержимому указателя

    n = int(result_array[0])
    m = int(result_array[1])

    # for i in range(MATRIX_MAX_SIZE): print(result_array[i])

    list_of_lists = []
    for i in range(0, n):  # Предположим, что вы хотите получить подсписки по 10 элементов
        sublist = []
        for j in range(0, m):
            sublist.append(result_array[2 + i * m + j])
        list_of_lists.append(sublist)

    return list_of_lists


def fill_result(list_of_lists, num_matrix_fill) -> None:
    """
    Назначение: представление полученных данных в поле пользовательского ввода первой матрицы

    :param list_of_lists: представление матрицы, которое будет установлено в поле пользовательского ввода первой матрицы
    """
    get_matrix()
    # Получение значения длины максимального числа
    max_len_num = 0
    first_column_max_len = 0

    for i in range(0, len(list_of_lists)):
        for j in range(0, len(list_of_lists[0])):
            list_of_lists[i][j] = round(float(list_of_lists[i][j]), setting.precession) if \
                (abs(float(list_of_lists[i][j])) > 0.000001) else 0
            cur_num = list_of_lists[i][j]
            str_num = f"{cur_num:.{setting.precession}f}"
            max_len_num = max(len(f"{str_num}  "), max_len_num)
            if j == 0:
                first_column_max_len = max(len(str_num), first_column_max_len)

    # Вывод отформатированного значения
    text = str()
    for i in range(0, len(list_of_lists)):
        for j in range(0, len(list_of_lists[0])):
            probels = ""  # Пробелы для выравнивания
            if j!=0: # Для значений не из первого столбца
                for y in range((max_len_num - len(f"{float(list_of_lists[i][j]):.{setting.precession}f}"))):
                    probels += " "  # Установка значения пробелов для форматированного вывода
            else:
                for y in range((first_column_max_len - len(f"{float(list_of_lists[i][j]):.{setting.precession}f}"))):
                    #if y != 0:
                    probels += " "  # Установка значения пробелов для форматированного вывода
            cur_num = round(float(list_of_lists[i][j]), setting.precession)
            text += f"{probels}{cur_num:.{setting.precession}f}"

            # text+=f"{str(float(list_of_lists[i][j]))} "
        text += "\n"

    if num_matrix_fill == MATRIX1:
        entry_matrix1.delete("1.0", tk.END)
        entry_matrix1.insert("1.0", str(text))
    elif num_matrix_fill == MATRIX2:
        entry_matrix2.delete("1.0", tk.END)
        entry_matrix2.insert("1.0", str(text))


"""
# -------------------------------------------------------
#   Блок вычисление детерминантов для матриц
# -------------------------------------------------------
"""


def get_det(num_of_matrix: int):
    """
    Назначение: получение значения детерминанта через dll-библиотеку

    :param num_of_matrix: номер матрицы, для которой происходит вычисление
    """

    def calc_det_c(ptr) -> float:
        """
        Назначение: получение результата из dll-библиотеки
        :param ptr: указатель на память с вычисляемой матрицей
        """
        return matrix_lib.calc_det(ptr)

    # Получение матриц из окон для ввода
    get_matrix()

    # Проверка возможности вычисления определителя для матрицы1
    if num_of_matrix == MATRIX1 and matrix1:
        able_det_1 = (len(matrix1) == len(matrix1[0]))
    else:
        able_det_1 = False

    # Проверка возможности вычисления определителя для матрицы1
    if num_of_matrix == MATRIX2 and matrix2:
        able_det_2 = (len(matrix2) == len(matrix2[0]))
    else:
        able_det_2 = False

    if help_menu:
        show_message(
            f"Для вычисления определителя введите квадратную матрицу (кол-во строк соответствует кол-ву столбцов)",
            False
        )
    elif able_det_1 or able_det_2:
        ptr1, ptr2 = c_matrix()
        # Выбор обрабатываемой матрицы
        if num_of_matrix == MATRIX1:
            input_arr = ptr1
        elif num_of_matrix == MATRIX2:
            input_arr = ptr2
        show_message(f"Детерминант матрицы{num_of_matrix} равен {calc_det_c(input_arr):.2f}", False)
    else:
        show_message(f"Вычисление детерминанта для матрицы{num_of_matrix} невозможно\nУбедитесь, что матрица "
                     f"квадратная (количество строк соответствует количеству столбцов)")


"""
# -------------------------------------------------------
#   Блок получения/сохранения информации в файл 
# -------------------------------------------------------
"""


def in_file(num_of_matrix: int) -> None:
    """
    Назначение: загрузка матрицы в файл из поля ввода

    :param num_of_matrix: номер загружаемой матрицы
    """

    def matrix_to_string(list_of_lists: list(list())) -> str:
        max_len_num = 0
        first_column_max_len = 0

        for i in range(0, len(list_of_lists)):
            for j in range(0, len(list_of_lists[0])):
                list_of_lists[i][j] = round(float(list_of_lists[i][j]), setting.precession) if \
                    (abs(float(list_of_lists[i][j])) > 0.000001) else 0
                cur_num = list_of_lists[i][j]
                str_num = f"{cur_num:.{setting.precession}f}"
                max_len_num = max(len(f"{str_num}  "), max_len_num)
                if j == 0:
                    first_column_max_len = max(len(str_num), first_column_max_len)

        # Вывод отформатированного значения
        text = str()
        for i in range(0, len(list_of_lists)):
            for j in range(0, len(list_of_lists[0])):
                probels = ""  # Пробелы для выравнивания
                if j != 0:  # Для значений не из первого столбца
                    for y in range((max_len_num - len(f"{float(list_of_lists[i][j]):.{setting.precession}f}"))):
                        probels += " "  # Установка значения пробелов для форматированного вывода
                else:
                    for y in range(
                            (first_column_max_len - len(f"{float(list_of_lists[i][j]):.{setting.precession}f}"))):
                        # if y != 0:
                        probels += " "  # Установка значения пробелов для форматированного вывода
                cur_num = round(float(list_of_lists[i][j]), setting.precession)
                text += f"{probels}{cur_num:.{setting.precession}f}"

                # text+=f"{str(float(list_of_lists[i][j]))} "
            text += "\n"
        return text

    # Открываем диалог для выбора файла
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"),
                                                        ("All files", "*.*")])
    get_matrix()  # Получение текущих значений в матрице

    if not file_path:
        pass
    elif help_menu and num_of_matrix == MATRIX1:
        show_message("Не возможно сохранить служебную информацию в файл")
    elif (not matrix1 and num_of_matrix == MATRIX1) or (not matrix2 and num_of_matrix == MATRIX2):
        show_message("Заполните матрицу перед ее сохранением в файл")
    else:
        # Вводим информацию для сохранения
        info = str()
        if num_of_matrix == MATRIX1:
            info = matrix_to_string(matrix1)
        elif num_of_matrix == MATRIX2:
            info = matrix_to_string(matrix2)

        try:
            with open(file_path, 'w') as file:
                file.write(info)
            show_message(f"Информация успешно сохранена в файл {file_path}", False)
        except Exception as e:
            show_message(f"Ошибка при сохранении файла: {e}")


def from_file(num_of_matrix: int) -> None:
    """
    Назначение: загрузка матрицы в поле ввода из матрицы

    :param num_of_matrix:
    """

    def is_file_correct(file_path):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Разделяем строку по пробелам
                    values = line.split()

                    for value in values:
                        # Пытаемся преобразовать значение в число
                        try:
                            float(value)
                        except ValueError:
                            return False  # Если не удалось преобразовать, возвращаем False

        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
            return False

        # Если все значения успешно преобразованы, возвращаем True
        return True

    # Открываем диалог для выбора файла
    file_path = filedialog.askopenfile(filetypes=[("Text files", "*.txt"),
                                                  ("All files", "*.*")])

    if not file_path:
        pass
    elif is_file_correct(file_path.name):
        # Вводим информацию для сохранения
        info = str()

        info = file_path.read()
        show_message(f"Информация успешно получена из файла {file_path.name}", False)

        if num_of_matrix == MATRIX1:
            clear_m1()
            entry_matrix1.insert("1.0", str(info))
        elif num_of_matrix == MATRIX2:
            clear_m2()
            entry_matrix2.insert("1.0", str(info))
    else:
        show_message(f"Ошибка при открытии файла. Проверьте, что файл содержит только числовые значения и не имеет "
                     f"служебных символов внутри.")


"""
# -------------------------------------------------------
#   Action-действия для кнопок
# -------------------------------------------------------
"""


def show_message(message: str, is_error=True) -> None:
    """
    Назначение: уведомление пользователя через всплывающее окно

    :param is_error: является ли сообщение ошибкой (по умолчанию да)
    :param message: текст сообщения
    """
    # Показать всплывающее окно с сообщением
    if is_error:
        title = "Ошибка"
        messagebox.showerror(title, message)
    else:
        title = "Сообщение"
        messagebox.showinfo(title, message)


def logging() -> None:
    """
    Назначение: логирование операций с матрицами

    """
    get_matrix()

    def matrix_to_string(list_of_lists: list(list())) -> str:
        """
        Назначение: перевод матрицы в текст

        :param list_of_lists: матрица, переводимая в строку
        :return: итоговый текст
        """
        max_len_num = 0
        for i in range(0, len(list_of_lists)):
            for j in range(0, len(list_of_lists[0])):
                max_len_num = max(len(f"{float(list_of_lists[i][j]):.{setting.precession}f} "), max_len_num)

        # Вывод отформатированного значения
        text = str()
        for i in range(0, len(list_of_lists)):
            for j in range(0, len(list_of_lists[0])):
                probels = ""  # Пробелы для выравнивания
                for y in range((max_len_num - len(f"{float(list_of_lists[i][j]):.{setting.precession}f}"))):
                    probels += " "  # Установка значения пробелов для форматированного вывода
                text += f"{float(list_of_lists[i][j]):.{setting.precession}f}{probels}"
                # text+=f"{str(float(list_of_lists[i][j]))} "
            text += "\n"
        return text

    def generate_log_path() -> str:
        """
        Назначение: создания имени лог-файла, основываясь на текущем времени
        :return: имя файла лога
        """
        now = datetime.now()
        # Формируем имя файла в нужном формате
        file_name = f"matrix_result_{now.strftime('%H_%M_%S')}-{now.strftime('%d-%m-%Y')}"
        return file_name

    if setting.out_matrix == MATRIX1:
        info = matrix_to_string(matrix1)
    elif setting.out_matrix == MATRIX2:
        info = matrix_to_string(matrix2)

    file_name = generate_log_path()
    with open(os.path.join("Logs", f"{file_name}.txt"), 'w') as file:
        file.write(info)
    return file_name


def calc_button_res() -> None:
    """
    Назначение: реакция на нажатие кнопки отправить:
                1. Получение данных из окон пользовательского ввода;
                2. Преобразование полученных данных в указатели на c_types массивы;
                3. Проверка возможности выполнения выбранного действия над матрицами;
                4. Произведение выбранной операции dll-библиотекой;
                5. Конвертация полученного результата в python-style;
                6. Установка полученного результата в поле пользовательского ввода.

    """
    if help_menu:
        show_message(
            f"При нажатии будет произведено выбранное действие,\nрезультат будет записан в поле "
            f"матрица{setting.out_matrix}",
            False
        )
        return

    entry_matrix2.configure(state="normal")
    get_matrix()
    selected_action = option_var.get()
    ptr1, ptr2 = c_matrix()
    if able_matrix_op(ptr1, ptr2):
        result_ptr = op_by_matrix(ptr1, ptr2)
        list_of_lists = convert_result(result_ptr)
        fill_result(list_of_lists, setting.out_matrix)
        log_info = f""
        if setting.log_need:
            log_info = f"\nРезультат вычисления записан в файл {logging()}.\nФайл находится в директории Logs"
        show_message(
            f"Результат действия {selected_action} успешно сохранен в матрица{setting.out_matrix}.{log_info}",
            False
        )
    #if selected_action in ["T", "^-1"]:
        #entry_matrix2.configure(state="disabled")


def clear_m1() -> None:
    """
    Назначение: очистка окна пользовательского ввода для матрицы1

    """
    global help_menu, matrix1

    if help_menu:
        entry_matrix1.delete("1.0", tk.END)
        matrix1 = back_up_matrix
        fill_result(matrix1, MATRIX1)
        help_menu = False
    else:
        entry_matrix1.delete("1.0", tk.END)
        matrix1.clear()
        get_matrix()


def alligment_m1() -> None:
    """
    Назначение: выравнивание форматирования для матрицы1

    """
    if help_menu:
        show_message(f"""
                При нажатии данной кнопки, произойдет
                выравнивание элементов матрицы по столбцам
                для матрицы 1. Точность ниже выбранной 
                в настройках ({setting.precession}) будет потеряна""",
                     False)
    else:
        get_matrix()
        fill_result(matrix1, MATRIX1)


def from_file_m1() -> None:
    """
    Назначение: получение данных о матрице1 из файла

    """
    if help_menu:
        show_message("""
При нажатии данной кнопки, будет открыто диалоговое окно представленное в виде «Проводник Windows (explorer.exe)».
В появившемся диалоговом окне, стандартными средствами навигации по проводнику необходимо найти файл, информация из которого будет записана в поле матрица 1, хранящий в себе данные о матрице с расширением .txt (информация в файле должна иметь возможность быть представлена в виде набора чисел, разделенных запятой и не содержать символы кроме цифр, запятых, пробелов и символов переноса строки).
После нахождения файла, необходимо выбрать его (левой кнопкой мыши) и подтвердить открытие повторным ЛКМ/нажатием кнопки открыть""",
                     False)
    else:
        from_file(MATRIX1)


def in_file_m1() -> None:
    """
    Назначение: отправка данных о матрице1 в файл

    """

    if help_menu:
        show_message("""
При нажатии данной кнопки, будет открыто диалоговое окно представленное в виде «Проводник Windows (explorer.exe)».
В появившемся диалоговом окне, стандартными средствами навигации по проводнику необходимо найти каталог, в котором должен быть создан файл с информацией о матрице1
Далее необходимо ввести желаемое имя файла в поле имя файла и нажать кнопку \"Сохранить\"""",
                     False)
    else:
        alligment_m1()
        in_file(MATRIX1)


def clear_m2() -> None:
    """
    Назначение: очистка окна пользовательского ввода для матрицы2

    """
    entry_matrix2.configure(state="normal")
    entry_matrix2.delete("1.0", tk.END)
    matrix2.clear()
    get_matrix()
    #entry_matrix2.configure(state="disabled")


def alligment_m2() -> None:
    """
    Назначение: выравнивание форматирования для матрицы2

    """
    if help_menu:
        show_message(f"""
                При нажатии данной кнопки, произойдет
                выравнивание элементов матрицы по столбцам
                для матрицы 2 Точность ниже выбранной 
                в настройках ({setting.precession}) будет потеряна""",
                     False)
    else:
        get_matrix()
        fill_result(matrix2, MATRIX2)


def from_file_m2() -> None:
    """
    Назначение: получение данных о матрице2 из файла

    """
    if help_menu:
        show_message("""
При нажатии данной кнопки, будет открыто диалоговое окно представленное в виде «Проводник Windows (explorer.exe)».
В появившемся диалоговом окне, стандартными средствами навигации по проводнику необходимо найти файл, информация из которого будет записана в поле матрица 2, хранящий в себе данные о матрице с расширением .txt (информация в файле должна иметь возможность быть представлена в виде набора чисел, разделенных запятой и не содержать символы кроме цифр, запятых, пробелов и символов переноса строки).
После нахождения файла, необходимо выбрать его (левой кнопкой мыши) и подтвердить открытие повторным ЛКМ/нажатием кнопки открыть""",
                     False)
    else:
        from_file(MATRIX2)


def in_file_m2() -> None:
    """
    Назначение: отправка данных о матрице2 в файл

    """

    if help_menu:
        show_message("""
При нажатии данной кнопки, будет открыто диалоговое окно представленное в виде «Проводник Windows (explorer.exe)».
В появившемся диалоговом окне, стандартными средствами навигации по проводнику необходимо найти каталог, в котором должен быть создан файл с информацией о матрице2
Далее необходимо ввести желаемое имя файла в поле имя файла и нажать кнопку \"Сохранить\"""",
                     False)
    else:
        alligment_m2()
        in_file(MATRIX2)


def calc_matrix_size(matrix_num) -> None:
    """
    Назначение: демонстрация размерности матрицы пользователю

    :param matrix_num: Номер матрицы, для которой производится проверка размерностей
    """
    if not help_menu:
        get_matrix()
        cur_matrix = matrix1 if (matrix_num == 1) else matrix2
        show_message(f"""
                Текущая размерность матрицы{matrix_num}:
                [{len(cur_matrix)} X {len(cur_matrix[0])}]""", False)
    else:
        show_message(f"""
                При нажатии данной кнопки, выведется
                сообщение о размерности матрицы{matrix_num}""", False)


def det_marix1() -> None:
    """
    Назначение: вычисление детерминанта для матрицы 1

    """
    get_det(MATRIX1)


def det_marix2() -> None:
    """
    Назначение: вычисление детерминанта для матрицы 2

    """
    get_det(MATRIX2)


def switch_matrix() -> None:
    """
    Назначение: функция меняет местами матрицы 1 и 2

    """
    if not help_menu:
        get_matrix()
        fill_result(matrix1, MATRIX2)
        fill_result(matrix2, MATRIX1)
    else:
        show_message("""
        При нажатии данной кнопки, произойдет
        установка значения матрицы 1 в поле
        матрица2, а значение матрицы 2 будет
        установлено в поле матрица1""", False)


def help_call() -> None:
    """
    Назначение: вызов вспомогательной информации по способу заполнения матриц

    """
    global help_menu, back_up_matrix, matrix1

    show_message("""
            Текущее значение матрицы 1 сохранено
            в буфер и будет установлено в поле
            матрицы 1 после выхода из режима помощи.
            Для выхода установите курсор в поле ввода
            матрица 1 или нажмите кнопку \"Очистить\"""", False)

    get_matrix()
    if not help_menu:
        back_up_matrix = matrix1

    help_menu = True
    fill_preset()
    root.focus_set()


def on_logging_option_change(logging_var) -> None:
    """
    Назначение: Сохранение настроек логирования

    :param logging_var: устанавливаемое значение логирования
    """
    global setting

    if logging_var.get() == 1:
        setting.set_log_need(True)
    else:
        setting.set_log_need(False)


def on_settings_select(combo_var) -> None:
    """
    Назначение: Сохранение настроек поля сохранения результата

    :param combo_var: устанавливаемое значение поля сохранения
    """
    global setting

    selected_value = combo_var.get()
    if selected_value:
        if selected_value == "Матрица1":
            setting.set_out_matrix(MATRIX1)
        elif selected_value == "Матрица2":
            setting.set_out_matrix(MATRIX2)


# Функция для открытия окна настроек
def open_settings_window() -> None:
    """
    Назначение: отрисовка и отработка окна настроек работы программы
                (настраивается: точность, поле вывода и потребность логирования)
    :return:
    """
    global setting

    def safe_set(combo_var, logging_var):
        setting.set_precession(accuracy_var.get())
        on_settings_select(combo_var)
        on_logging_option_change(logging_var)
        settings_window.destroy()
        if help_menu:
            fill_preset()

    settings_window = tk.Toplevel(root)
    settings_window.title("Настройки")

    # Настройка точности (от 0 до 7)
    accuracy_label = ttk.Label(settings_window, text="Точность\n(кол-во знаков после запятой):")
    accuracy_label.grid(row=0, column=0, padx=10, pady=5)

    accuracy_var = tk.IntVar(value=setting.precession)  # Значение по умолчанию
    accuracy_spinbox = ttk.Spinbox(settings_window, from_=0, to=7, textvariable=accuracy_var)
    accuracy_spinbox.grid(row=0, column=1, padx=10, pady=5)

    # Выпадающий список для выбора поля (Поле1 или Поле2)
    settings_label = ttk.Label(settings_window, text="Выбор поля, куда будет\nсохранен результат выражения:")
    settings_label.grid(row=1, column=0, padx=10, pady=5)

    combo_var = tk.StringVar()
    combo_choices = ["Матрица1", "Матрица2"]
    combo_box = ttk.Combobox(settings_window, textvariable=combo_var, values=combo_choices)
    combo_box.current(setting.out_matrix - 1)  # Устанавливаем начальное значение
    combo_box.grid(row=1, column=1, padx=10, pady=5)

    # Переменная для хранения состояния чекбокса
    logging_var = tk.IntVar()

    # Создаем чекбокс с меткой "Логирование"
    if setting.log_need:
        logging_var.set(1)
    else:
        logging_var.set(0)
    logging_checkbox = tk.Checkbutton(settings_window, text="Логирование", variable=logging_var)
    logging_checkbox.grid(row=1, column=2, padx=10, pady=20)

    # Привязка события выбора в выпадающем списке
    combo_box.bind("<<ComboboxSelected>>")

    # Кнопка для применения настроек (если нужно)
    apply_button = ttk.Button(settings_window, text="Применить",
                              command=lambda: safe_set(combo_var, logging_var))
    apply_button.grid(row=2, column=0, columnspan=2, pady=10)


def on_key_press(event):
    """
    Назначение: функция для проверки ввода (для ввода доступны операции перевода коретки, числа и точки)

    :param event:
    """
    # Разрешаем ввод цифр, пробелов, переносов строки и разрешенных клавиш
    able_keys = {"BackSpace", "Delete", "Return", "Tab", "space", "Up", "Down", "Left", "Right"}
    if event.char.isdigit() or event.char in ['.', '-'] or event.keysym in able_keys:
        return  # Пропускаем, все разрешено
    return "break"  # Отменить ввод для других символов


# ------------------------------------------------
#  Служебные элементы интерфейса
# ------------------------------------------------

# Создаем основное окно
root = tk.Tk()
root.title("Matrix Calculator")
root.geometry("1250x600")  # Устанавливаем начальный размер окна
root.minsize(1300, 650)  # Минимальный размер окна
# Настраиваем строки и столбцы для масштабирования
root.grid_rowconfigure(0, weight=1)  # Верхний ряд (help/settings)
root.grid_rowconfigure(1, weight=1)  # Ряд с матрицами
root.grid_rowconfigure(2, weight=0)  # Ряд с кнопками под матрицами
root.grid_columnconfigure(0, weight=1)  # Матрица 1
root.grid_columnconfigure(1, weight=0)  # Центральные элементы (операции)
root.grid_columnconfigure(2, weight=1)  # Матрица 2

# ------------------------------------------------
# Кнопка help
# ------------------------------------------------
help_button = tk.Button(root, text="help", command=help_call)
help_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

# Кнопка "Настройки"
settings_button = ttk.Button(root, text="Настройки", command=open_settings_window)
settings_button.grid(row=0, column=2, sticky="ne", padx=10, pady=10)

# ------------------------------------------------
# Элементы интерфейса для матрицы 1
# ------------------------------------------------
matrix1_frame = tk.Frame(root)
matrix1_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
matrix1_frame.grid_rowconfigure(1, weight=1)
matrix1_frame.grid_columnconfigure(0, weight=1)

matrix1_label = tk.Label(matrix1_frame, text="Матрица 1")
matrix1_label.grid(row=0, column=0, sticky="w")

entry_matrix1 = tk.Text(matrix1_frame, wrap="none")
entry_matrix1.grid(row=1, column=0, sticky="nsew")
entry_matrix1.bind("<KeyPress>", on_key_press)  # Привязываем событие нажатия клавиш
entry_matrix1.bind("<FocusIn>", preset_delete)  # Привязываем событие выбора поля
fill_preset()

scrollbar_x_m1 = tk.Scrollbar(matrix1_frame, orient=tk.HORIZONTAL, command=entry_matrix1.xview)
scrollbar_x_m1.grid(row=2, column=0, sticky="ew")
scrollbar_y_m1 = tk.Scrollbar(matrix1_frame, orient=tk.VERTICAL, command=entry_matrix1.yview)
scrollbar_y_m1.grid(row=1, column=1, sticky="ns")
entry_matrix1.config(xscrollcommand=scrollbar_x_m1.set, yscrollcommand=scrollbar_y_m1.set)

matrix1_buttons_frame = tk.Frame(matrix1_frame)
matrix1_buttons_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
matrix1_buttons = [
    ("Записать из файла", lambda: from_file_m1()),
    ("Сохранить в файл", lambda: in_file_m1()),
    ("Очистить", lambda: clear_m1()),
    ("det", lambda: det_marix1()),
    ("Выровнять", lambda: alligment_m1()),
    ("Размер матрицы", lambda: calc_matrix_size(MATRIX1)),
]

for i, (text, command) in enumerate(matrix1_buttons):
    tk.Button(matrix1_buttons_frame, text=text, command=command).grid(row=0, column=i, padx=5)

# ------------------------------------------------
# Центральные элементы (операции над матрицами)
# ------------------------------------------------
center_frame = tk.Frame(root)
center_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

operation_label = tk.Label(center_frame, text="Выберите операцию,\nпроизводимую над\nматрицами")
operation_label.grid(row=0, column=0, pady=20)

option_var = tk.StringVar(root)
option_var.set("X")
options = ["X", "/", "+", "-", "T", "^-1"]
option_menu = tk.OptionMenu(center_frame, option_var, *options)
option_menu.grid(row=1, column=0, pady=10)

reverse_button = tk.Button(center_frame, text="<=>", command=switch_matrix)
reverse_button.grid(row=2, column=0, pady=10)

calc_button = tk.Button(center_frame, text="Рассчитать", command=calc_button_res)
calc_button.grid(row=3, column=0, pady=10)

# ------------------------------------------------
# Элементы интерфейса для матрицы 2
# ------------------------------------------------
matrix2_frame = tk.Frame(root)
matrix2_frame.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
matrix2_frame.grid_rowconfigure(1, weight=1)
matrix2_frame.grid_columnconfigure(0, weight=1)

matrix2_label = tk.Label(matrix2_frame, text="Матрица 2")
matrix2_label.grid(row=0, column=0, sticky="w")

entry_matrix2 = tk.Text(matrix2_frame, wrap="none")
entry_matrix2.grid(row=1, column=0, sticky="nsew")
entry_matrix2.bind("<KeyPress>", on_key_press)  # Привязываем событие нажатия клавиш

scrollbar_x_m2 = tk.Scrollbar(matrix2_frame, orient=tk.HORIZONTAL, command=entry_matrix2.xview)
scrollbar_x_m2.grid(row=2, column=0, sticky="ew")
scrollbar_y_m2 = tk.Scrollbar(matrix2_frame, orient=tk.VERTICAL, command=entry_matrix2.yview)
scrollbar_y_m2.grid(row=1, column=1, sticky="ns")
entry_matrix2.config(xscrollcommand=scrollbar_x_m2.set, yscrollcommand=scrollbar_y_m2.set)

matrix2_buttons_frame = tk.Frame(matrix2_frame)
matrix2_buttons_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
matrix2_buttons = [
    ("Записать из файла", lambda: from_file_m2()),
    ("Сохранить в файл", lambda: in_file_m2()),
    ("Очистить", lambda: clear_m2()),
    ("det", lambda: det_marix2()),
    ("выровнять", lambda: alligment_m2()),
    ("Размер матрицы", lambda: calc_matrix_size(MATRIX2)),
]

for i, (text, command) in enumerate(matrix2_buttons):
    tk.Button(matrix2_buttons_frame, text=text, command=command).grid(row=0, column=i, padx=5)

if __name__ == "__main__":
    init_library()
    # Запуск главного цикла
    root.mainloop()
