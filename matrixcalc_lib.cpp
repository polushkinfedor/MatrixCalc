#include "Windows.h"
#include "matrix_math.cpp"

#ifndef MATRIX_DRIVER
#define MATRIX_DRIVER

const int MAX_MATRIX_SIZE = 1002; // Максимальный размер 31x31

static double result[MAX_MATRIX_SIZE];

extern "C" __declspec(dllexport) int det_able(double arr1[MAX_MATRIX_SIZE]);  // Вызов проверки возможности вычисления детерменантра для python c-types данных
extern "C" __declspec(dllexport) int matrix_ariphmetic(double[MAX_MATRIX_SIZE], double[MAX_MATRIX_SIZE]);  // Вызов проверки арифметических действий для python c-types данных
extern "C" __declspec(dllexport) int matrix_algo(double[MAX_MATRIX_SIZE], double[MAX_MATRIX_SIZE]);  // Вызов проверки возможности суммы для python c-types данных
extern "C" __declspec(dllexport) int matrix_inv_ready(double[MAX_MATRIX_SIZE]);  // Вызов проверки нахождения обратной суммы для python c-types данных

extern "C" __declspec(dllexport) double calc_det(double arr1[MAX_MATRIX_SIZE]);  // Вычисление детерменанта для python c-types данных
extern "C" __declspec(dllexport) double* matrix_sum(double[MAX_MATRIX_SIZE], double[MAX_MATRIX_SIZE]);  // Вызов суммы для python c-types данных
extern "C" __declspec(dllexport) double* matrix_sub(double[MAX_MATRIX_SIZE], double[MAX_MATRIX_SIZE]);  // Вызов деления для python c-types данных
extern "C" __declspec(dllexport) double* matrix_mul(double[MAX_MATRIX_SIZE], double[MAX_MATRIX_SIZE]);  // Вызов умножения для python c-types данных
extern "C" __declspec(dllexport) double* matrix_div(double[MAX_MATRIX_SIZE], double[MAX_MATRIX_SIZE]);  // Вызов деления для python c-types данных
extern "C" __declspec(dllexport) double* matrix_T(double[MAX_MATRIX_SIZE]);    // Вызов транспонирования для python c-types данных
extern "C" __declspec(dllexport) double* matrix_inv(double[MAX_MATRIX_SIZE]);  // Вызов вычисления обратной матрицы для python c-types данных


extern "C" __declspec(dllexport) int det_able(double arr1[MAX_MATRIX_SIZE]) {
    // Вызов проверки возможности вычисления детерменантра для python c-types данных
    int status = 0; // Если статус 0, то операция не возможна, если 1 -- возможна 

    matrix<double> m1;

    m1.arr_to_matrix(arr1);

    bool is_able = m1.is_determenant();
    (is_able) ? status = 1 : status = 0;

    return status;
}

extern "C" __declspec(dllexport) int matrix_ariphmetic(double arr1[MAX_MATRIX_SIZE], double arr2[MAX_MATRIX_SIZE]) {
    // Вызов проверки арифметических действий для python c-types данных
    int status = 0; // Если статус 0, то операция не возможна, если 1 -- возможна

    matrix<double> m1;
    matrix<double> m2;

    m1.arr_to_matrix(arr1);
    m2.arr_to_matrix(arr2);

    bool is_able = m1.can_ariphmetic_op_matrix(m2);
    (is_able) ? status = 1 : status = 0;

    return status;
}

extern "C" __declspec(dllexport) int matrix_algo(double arr1[MAX_MATRIX_SIZE], double arr2[MAX_MATRIX_SIZE]) {
    // Вызов проверки возможности суммы для python c-types данных
    int status = 0; // Если статус 0, то операция не возможна, если 1 -- возможна

    matrix<double> m1;
    matrix<double> m2;

    m1.arr_to_matrix(arr1);
    m2.arr_to_matrix(arr2);

    bool is_able = m1.can_algebra_op_matrix(m2);
    (is_able) ? status = 1 : status = 0;

    return status;
}

extern "C" __declspec(dllexport) int matrix_inv_ready(double arr1[MAX_MATRIX_SIZE]) {
    // Вызов проверки нахождения обратной суммы для python c-types данных
    int status = 1; // Если статус 0, то операция не возможна, если 1 -- возможна

    matrix<double> m1;

    m1.arr_to_matrix(arr1);

    try {
        m1.calc_inverse_matrix();
    }
    catch (...) {
        status = 0;
    }

    return status;
}

extern "C" __declspec(dllexport) double calc_det(double arr1[MAX_MATRIX_SIZE]) {
    // Вызов суммы для python c-types данных
    matrix<double> m1;

    m1.arr_to_matrix(arr1);

    return m1.det();
}

extern "C" __declspec(dllexport) double* matrix_sum(double arr1[MAX_MATRIX_SIZE], double arr2[MAX_MATRIX_SIZE]) {
    // Вызов суммы для python c-types данных
    matrix<double> m1;
    matrix<double> m2;

    m1.arr_to_matrix(arr1);
    m2.arr_to_matrix(arr2);

    m1 += m2;

    int n = m1.line_size();
    int m = m1.column_size();

    result[0] = n;
    result[1] = m;

    // Копирование значений в результат
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            result[2 + i * m + j] = m1.val(i, j);
        }
    }

    return result;
}

extern "C" __declspec(dllexport) double* matrix_sub(double arr1[MAX_MATRIX_SIZE], double arr2[MAX_MATRIX_SIZE]) {
    // Вызов вычитания для python c-types данных
    matrix<double> m1;
    matrix<double> m2;

    m1.arr_to_matrix(arr1);
    m2.arr_to_matrix(arr2);

    m1 -= m2;

    int n = m1.line_size();
    int m = m1.column_size();

    result[0] = n;
    result[1] = m;

    // Копирование значений в результат
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            result[2 + i * m + j] = m1.val(i, j);
        }
    }

    return result;
}

extern "C" __declspec(dllexport) double* matrix_mul(double arr1[MAX_MATRIX_SIZE], double arr2[MAX_MATRIX_SIZE]) {
    // Вызов умножения для python c-types данных
    matrix<double> m1;
    matrix<double> m2;

    m1.arr_to_matrix(arr1);
    m2.arr_to_matrix(arr2);

    m1 *= m2;

    int n = m1.line_size();
    int m = m1.column_size();

    result[0] = n;
    result[1] = m;

    // Копирование значений в результат
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            result[2 + i * m + j] = m1.val(i, j);
        }
    }

    return result;
}

extern "C" __declspec(dllexport) double* matrix_div(double arr1[MAX_MATRIX_SIZE], double arr2[MAX_MATRIX_SIZE]) {
    // Вызов деления для python c-types данных
    matrix<double> m1;
    matrix<double> m2;

    if (arr2[0] == 1 && arr2[1] == 1) {
        m1.arr_to_matrix(arr1);
        m1 = m1 / arr2[2];
    }
    else {
        m1.arr_to_matrix(arr1);
        m2.arr_to_matrix(arr2);
        m1 /= m2;
    }
    

    int n = m1.line_size();
    int m = m1.column_size();

    result[0] = n;
    result[1] = m;

    // Копирование значений в результат
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            result[2 + i * m + j] = m1.val(i, j);
        }
    }

    return result;
}

extern "C" __declspec(dllexport) double* matrix_T(double arr1[MAX_MATRIX_SIZE]) {
    // Вызов транспонирования для python c-types данных
    matrix<double> m1;
    m1.arr_to_matrix(arr1);

    m1.T();

    int n = m1.line_size();
    int m = m1.column_size();

    result[0] = n;
    result[1] = m;

    // Копирование значений в результат
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            result[2 + i * m + j] = m1.val(i, j);
        }
    }

    return result;
}

extern "C" __declspec(dllexport) double* matrix_inv(double arr1[MAX_MATRIX_SIZE]) {
    // Вызов вычисления обратной матрицы для python c-types данных
    matrix<double> m1;

    m1.arr_to_matrix(arr1);

    m1 = m1.calc_inverse_matrix();

    int n = m1.line_size();
    int m = m1.column_size();

    result[0] = n;
    result[1] = m;

    // Копирование значений в результат
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            result[2 + i * m + j] = m1.val(i, j);
        }
    }

    return result;
}

#endif // MATRIX_DRIVER