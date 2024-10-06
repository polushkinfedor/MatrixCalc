#include <vector>

#ifndef MATRIXCALC_MATRIX_MATH_H
#define MATRIXCALC_MATRIX_MATH_H

template<typename val_type>
using matrix_body = vector<vector<val_type>>;
using vectoy_body = vector<val_type>;

class enum matrix_type {  // Перечисление стандартных типов матриц при создании
  no_type, zero_matrix, identity_matrix;
};

class matrix {
private:
    // СЛУЖЕБНАЯ ИНФОРМАЦИЯ
    type_info data_type;  // Тип данных, хранимый в матрице
    bool empty_matrix;  // Флаг пустой функции

    // ПЕРЕМЕННЫЕ КЛАССА
    matrix_body body;  // Данные, хранимые в матрице
    double determenant;  // Детерминант(определитель) матрицы
    int size_n;  // Размерность матрицы (количество строк)
    int size_m;  // Размерность матрицы (количество столбцов)

    // Служебная функция расчета определителя
    void calc_det();

public:
    // БЛОК КОНСТРУТОРОВ
    matrix();  // Конструктор по умолчанию, создающий пустую матрицу
    matrix(int n);  // Конструктор создания вектора
    matrix(int n, int m, matrix_type type = no_type);  // Создание матрицы заданного типа размером [n x m]
    matrix(const matrix_body& matrix_value);  // Создание матрицы с заданными значениями

    // GET функции
    type_info matrix_data_type();
    double det();
    int line_size();
    int column_size();

    // БЛОК ПЕРЕГРУЖЕННЫХ ОПЕРАТОРОВ
    // copy
    matrix operator = (const matrix& sec_matrix);
    // multiply
    matrix operator * (const val_type number);
    matrix operator * (const matrix& sec_matrix);
    // division
    matrix operator / (const val_type number);
    matrix operator / (const matrix& sec_matrix);
    // plus
    matrix operator + (const val_type number);
    matrix operator + (const matrix& sec_matrix);
    // subtraction
    matrix operator - (const val_type number);
    matrix operator - (const matrix& sec_matrix);

    // БЛОК ФУНКЦИЙ ОПЕРАЦИЙ С МАТРИЦАМИ
    matrix calc_inverse_matrix();

    // БЛОК ФУНКЦИЙ ПРОВЕРОК ДОПУСТИМОСТИ МАТ.ДЕЙСТВИЙ
    // Проверка для определения допустимости взятия обратной матрицы
    bool is_zero_determenant();
    // Проверка для определения допустимости арифметических операций (-, +)
    bool can_ariphmetic_op_matrix(const matrix& sec_matrix);
    // Проверка для определения допустимости алгебраических операций (*, /)
    bool can_algebra_op_matrix(const val_type sec_matrix);
    bool can_algebra_op_matrix(const matrix& sec_matrix);
};

// TODO: Блочная матрица, как наследник класса matrix
//       Информация о блочных матрицах:
//       https://ru.wikipedia.org/wiki/%D0%91%D0%BB%D0%BE%D1%87%D0%BD%D0%B0%D1%8F_%D0%BC%D0%B0%D1%82%D1%80%D0%B8%D1%86%D0%B0

#endif //MATRIXCALC_MATRIX_MATH_H