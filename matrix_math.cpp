#include "matrix_math.h"

// --------------------------------------------------------------------------------------------------------------------
// Служебная функция расчета определителя
// --------------------------------------------------------------------------------------------------------------------
template<typename val_type>
void matrix<val_type>::calc_det() {
    ;
}


// --------------------------------------------------------------------------------------------------------------------
// БЛОК КОНСТРУТОРОВ
// --------------------------------------------------------------------------------------------------------------------
template<typename val_type>
matrix<val_type>::matrix() {}

template<typename val_type>
matrix<val_type>::matrix(int n) {
    ;
}

template<typename val_type>
matrix<val_type>::matrix(int n, int m, matrix_type type) {
    ;
}

template<typename val_type>
matrix<val_type>::matrix(const matrix_body<val_type> &matrix_value) {
    ;
}


// --------------------------------------------------------------------------------------------------------------------
// GET функции
// --------------------------------------------------------------------------------------------------------------------
template<typename val_type>
type_info matrix<val_type>::matrix_data_type() {
    ;
}

template<typename val_type>
double matrix<val_type>::det() {
    ;
}

template<typename val_type>
int matrix<val_type>::line_size() {
    ;
}

template<typename val_type>
int matrix<val_type>::column_size() {
    ;
}


// --------------------------------------------------------------------------------------------------------------------
// БЛОК ПЕРЕГРУЖЕННЫХ ОПЕРАТОРОВ
// --------------------------------------------------------------------------------------------------------------------
// ------------------------------------------------------
// copy
template<typename val_type>
matrix<val_type>& matrix<val_type>::operator = (const matrix<val_type>& sec_matrix) {
    ;
}
// ------------------------------------------------------

// ------------------------------------------------------
// multiply
template<typename val_type>
matrix<val_type>& matrix<val_type>::operator * (const val_type number) {
    ;
}

template<typename val_type>
matrix<val_type>& matrix<val_type>::operator * (const matrix<val_type>& sec_matrix) {
    ;
}
// ------------------------------------------------------

// ------------------------------------------------------
// division
template<typename val_type>
matrix<val_type>& matrix<val_type>::operator / (const val_type number) {
    ;
}

template<typename val_type>
matrix<val_type>& matrix<val_type>::operator / (const matrix<val_type>& sec_matrix) {
    ;
}
// ------------------------------------------------------

// ------------------------------------------------------
// plus
template<typename val_type>
matrix<val_type>& matrix<val_type>::operator + (const val_type number) {
    ;
}

template<typename val_type>
matrix<val_type>& matrix<val_type>::operator + (const matrix<val_type>& sec_matrix) {
    ;
}
// ------------------------------------------------------

// ------------------------------------------------------
// subtraction
template<typename val_type>
matrix<val_type>& matrix<val_type>::operator - (const val_type number) {
    ;
}

template<typename val_type>
matrix<val_type>& matrix<val_type>::operator - (const matrix& sec_matrix) {
    ;
}
// ------------------------------------------------------


// --------------------------------------------------------------------------------------------------------------------
// БЛОК ФУНКЦИЙ ОПЕРАЦИЙ С МАТРИЦАМИ
// --------------------------------------------------------------------------------------------------------------------
template<typename val_type>
matrix<val_type>& matrix<val_type>::calc_inverse_matrix() {
    ;
}


// --------------------------------------------------------------------------------------------------------------------
// БЛОК ФУНКЦИЙ ПРОВЕРОК ДОПУСТИМОСТИ МАТ.ДЕЙСТВИЙ
// --------------------------------------------------------------------------------------------------------------------
template<typename val_type>
bool is_zero_determenant() {
    // Проверка для определения допустимости взятия обратной матрицы
    ;
}

template<typename val_type>
bool can_ariphmetic_op_matrix(const matrix<val_type>& sec_matrix) {
    // Проверка для определения допустимости арифметических операций (-, +)
    ;
}

template<typename val_type>
bool can_algebra_op_matrix(const val_type sec_matrix) {
    // Проверка для определения допустимости алгебраических операций (*, /)
}

template<typename val_type>
bool can_algebra_op_matrix(const matrix<val_type>& sec_matrix) {
    // Проверка для определения допустимости алгебраических операций (*, /)
}