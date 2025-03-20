#include <vector>
#include <typeinfo>
#include <math.h>

#ifndef MATRIXCALC_MATRIX_MATH_H
#define MATRIXCALC_MATRIX_MATH_H

using std::vector;
using std::type_info;

template<typename val_type>
using matrix_body = vector<vector<val_type>>;

enum class matrix_type {  // Перечисление стандартных типов матриц при создании
    no_type, value, identity, triangle
};
using enum matrix_type;

enum class matrix_errors {
    no_det, zero_det, size_err
};

template<typename val_type>
class matrix {
private:
    // СЛУЖЕБНАЯ ИНФОРМАЦИЯ
    // type_info data_type;  // Тип данных, хранимый в матрице
    bool empty_matrix = false;  // Флаг пустой матрицы
    bool zero_matrix = false;  // Флаг нулевой матрицы
    bool was_calc_det = false;  // Флаг вычисленности определителя

    // ПЕРЕМЕННЫЕ КЛАССА
    matrix_body<val_type> body;  // Данные, хранимые в матрице
    double determenant;  // Детерминант(определитель) матрицы
    int size_n;  // Размерность матрицы (количество строк)
    int size_m;  // Размерность матрицы (количество столбцов)

    // Служебная функция расчета определителя
    void calc_det();

public:
    // БЛОК КОНСТРУКТОРОВ
    matrix();  // Конструктор по умолчанию, создающий пустую матрицу
    matrix(int n);  // Конструктор создания вектора
    matrix(const vector<val_type>&);  // Конструктор создания вектора со значениями
    matrix(int n, int m, matrix_type type = no_type, int val = 1);  // Создание матрицы заданного типа
    // размером [n x m]
    matrix(const matrix_body<val_type>& matrix_value);  // Создание матрицы с заданными значениями

    // БЛОК ДЕСТРУКТОРОВ
    ~matrix();

    // GET функции
    // type_info matrix_data_type();
    double det();
    val_type val(int n, int m) const;
    matrix_body<val_type> get_body() const;
    int line_size() const;
    int column_size() const;

    // БЛОК ПЕРЕГРУЖЕННЫХ ОПЕРАТОРОВ
    void operator = (const matrix<val_type>& sec_matrix);
    // multiply
    matrix<val_type> operator * (const val_type number);
    matrix<val_type> operator *= (const val_type number);
    matrix<val_type> operator * (const matrix<val_type>& sec_matrix);
    matrix<val_type> operator *= (const matrix<val_type>& sec_matrix);
    // division
    matrix<val_type> operator / (const val_type number);
    matrix<val_type> operator /= (const val_type number);
    matrix<val_type> operator/ (matrix<val_type>& sec_matrix);
    matrix<val_type> operator /= (matrix<val_type>& sec_matrix);
    // plus
    matrix<val_type> operator + (const matrix<val_type>& sec_matrix);
    matrix<val_type> operator += (const matrix<val_type>& sec_matrix);
    // subtraction
    matrix<val_type> operator - (const matrix<val_type>& sec_matrix);
    matrix<val_type> operator -= (const matrix<val_type>& sec_matrix);
    // pow
    matrix<val_type> matrix_pow(const val_type number);

    // БЛОК ФУНКЦИЙ ОПЕРАЦИЙ С МАТРИЦАМИ
    matrix<val_type> calc_minor(int n, int m); // Вычисление минора для элемента [n, m]
    matrix<val_type> calc_inverse_matrix();  // Вычисление обратной матрицы
    matrix<val_type> T(bool self = true);  // Транспонирование матрицы

    // БЛОК ФУНКЦИЙ ПРОВЕРОК ДОПУСТИМОСТИ МАТ.ДЕЙСТВИЙ
    // Проверка для определения допустимости нахождения определителя
    bool is_determenant();
    // Проверка для определения допустимости нахождения обратной матрицы
    bool is_zero_determenant();
    // Проверка для определения допустимости арифметических операций (-, +)
    bool can_ariphmetic_op_matrix(const matrix<val_type>& sec_matrix);
    // Проверка для определения допустимости алгебраических операций (*, /)
    bool can_algebra_op_matrix(const matrix<val_type>& sec_matrix);
    // перевод массива в матрицу
    void arr_to_matrix(double[102]); // Перевод данных из массива в вектор
};

// TODO: Блочная матрица, как наследник (или шаблон?) класса matrix.
//       Информация о блочных матрицах:
//       https://ru.wikipedia.org/wiki/%D0%91%D0%BB%D0%BE%D1%87%D0%BD%D0%B0%D1%8F_%D0%BC%D0%B0%D1%82%D1%80%D0%B8%D1%86%D0%B0


// --------------------------------------------------------------------------------------------------------------------
// Служебная функция расчета определителя
// --------------------------------------------------------------------------------------------------------------------
template<typename val_type>
void matrix<val_type>::calc_det() {
    determenant = 0;
    if (zero_matrix) determenant = 0; // Для матрицы нулей не производим вычисления, т.к. лишняя нагрузка по времени
    if (size_n == 1) {
        // определитель матрицы из одного элемента -- вырожденный случай
        determenant = body[0][0];
        return;
    }
    else if (size_n == 2) {
        // Определитель матрицы [2x2] -- базовый случай рекурсии
        determenant = body[0][0] * body[1][1] - body[0][1] * body[1][0];
        return;
    }
    else {
        for (int i = 0; i < size_m; i++) {
            int line_n = 0; // Разложение по 0 строке
            // Инициализируем матрицу, являющуюся минором, которая вычислит свой детерминант
            matrix<val_type> minor = calc_minor(line_n, i);
            // прибавляем ко значению определителя определитель минора со знаком четности элемента разложения умноженном
            // на элемент, по которому проводилось разложение.
            this->determenant += pow(-1, i % 2) * body[0][i] * minor.det();
        }
    }
    was_calc_det = true;
}


// --------------------------------------------------------------------------------------------------------------------
// БЛОК КОНСТРУКТОРОВ
// --------------------------------------------------------------------------------------------------------------------
template<typename val_type>
matrix<val_type>::matrix() {
    empty_matrix = true;
    size_n = 0;
    size_m = 0;
}

template<typename val_type>
matrix<val_type>::matrix(int n) {
    size_n = n;
    size_m = 1;
}

template<typename val_type>
matrix<val_type>::matrix(const vector<val_type>& values) {
    size_n = values.size();
    size_m = 1;
    body.resize(size_n);
    for (int i = 0; i < values.size(); i++) {
        vector<val_type> curr_line{ values[i] };
        body[i] = curr_line;
    }
}

template<typename val_type>
matrix<val_type>::matrix(int n, int m, matrix_type type, int val) {
    size_n = n;
    size_m = m;
    body.resize(n);
    for (int i = 0; i < n; i++) {
        vector<val_type> curr_line(m);
        body[i] = curr_line;
    }

    switch (type) {
    case no_type:
        zero_matrix = true;
        break;
    case value: // Заполнение матрицы значением
        if (val == 0) zero_matrix; // Пустую матрицу не надо заполнять значениями
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                body[i][j] = val;
            }
        }
        break;
    case identity: // Заполнение единичной матрицы
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (i == j) body[i][j] = val;
            }
        }
        break;
    case triangle: // Заполнение треугольной матрицы
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (j >= i) body[i][j] = val;
            }
        }
        break;
    }
}

template<typename val_type>
matrix<val_type>::matrix(const matrix_body<val_type>& matrix_value) {
    size_n = matrix_value.size();
    size_m = matrix_value[0].size();
    body = matrix_value;
}


// --------------------------------------------------------------------------------------------------------------------
// БЛОК ДЕСТРУКТОРОВ
// --------------------------------------------------------------------------------------------------------------------
template<typename val_type>
matrix<val_type>::~matrix() {
    ;
}


// --------------------------------------------------------------------------------------------------------------------
// GET функции
// --------------------------------------------------------------------------------------------------------------------
/*
TODO: Подумать над типизацией данных
template<typename val_type>
type_info matrix<val_type>::matrix_data_type() {
    ;
}
*/

template<typename val_type>
double matrix<val_type>::det() {
    if (is_determenant()) {
        if (not was_calc_det) calc_det();
        return determenant;
    }
    else {
        throw matrix_errors::no_det;
    }
}

template<typename val_type>
val_type matrix<val_type>::val(int n, int m) const {
    return this->body[n][m];
}

template<typename val_type>
matrix_body<val_type> matrix<val_type>::get_body() const {
    return this->body;
}

template<typename val_type>
int matrix<val_type>::line_size() const {
    return this->size_n;
}

template<typename val_type>
int matrix<val_type>::column_size() const {
    return this->size_m;
}


// --------------------------------------------------------------------------------------------------------------------
// БЛОК ПЕРЕГРУЖЕННЫХ ОПЕРАТОРОВ
// --------------------------------------------------------------------------------------------------------------------
template<typename val_type>
void matrix<val_type>::operator = (const matrix<val_type>& sec_matrix) {
    this->body = sec_matrix.body;
    this->size_n = sec_matrix.size_n;
    this->size_m = sec_matrix.size_m;
    this->empty_matrix = sec_matrix.empty_matrix;
    this->zero_matrix = sec_matrix.zero_matrix;
    this->was_calc_det = sec_matrix.was_calc_det;
}

// ------------------------------------------------------
// multiply
template<typename val_type>
matrix<val_type> matrix<val_type>::operator * (const val_type number) {
    matrix<val_type> result(this->body);
    for (int i = 0; i < result.line_size(); i++) {
        for (int j = 0; j < result.column_size(); j++) {
            result.body[i][j] *= number;
        }
    }
    return result;
}

template<typename val_type>
matrix<val_type> matrix<val_type>::operator *= (const val_type number) {
    for (int i = 0; i < this->line_size(); i++) {
        for (int j = 0; j < this->column_size(); j++) {
            this->body[i][j] *= number;
        }
    }
    return *(this);
}

template<typename val_type>
matrix<val_type> matrix<val_type>::operator * (const matrix<val_type>& sec_matrix) {
    if (not can_algebra_op_matrix(sec_matrix)) throw matrix_errors::size_err;

    // Выделения места для новой матрицы
    int new_n = this->size_n;
    int new_m = sec_matrix.size_m;
    matrix<val_type> result(new_n, new_m);

    // перемножение матриц
    for (int new_i = 0; new_i < new_n; new_i++) {
        for (int new_j = 0; new_j < new_m; new_j++) {
            for (int line_counter = 0; line_counter < this->size_m; line_counter++)
                result.body[new_i][new_j] += this->body[new_i][line_counter] * sec_matrix.body[line_counter][new_j];
        }
    }

    return result;
}

template<typename val_type>
matrix<val_type> matrix<val_type>::operator *= (const matrix<val_type>& sec_matrix) {
    if (not can_algebra_op_matrix(sec_matrix)) throw matrix_errors::size_err;

    // Выделения места для новой матрицы
    int new_n = this->size_n;
    int new_m = sec_matrix.size_m;
    matrix<val_type> result(new_n, new_m);

    // перемножение матриц
    for (int new_i = 0; new_i < new_n; new_i++) {
        for (int new_j = 0; new_j < new_m; new_j++) {
            for (int line_counter = 0; line_counter < this->size_m; line_counter++)
                result.body[new_i][new_j] += this->body[new_i][line_counter] * sec_matrix.body[line_counter][new_j];
        }
    }

    // Заменяем текущую матрицу на полученную
    this->body = result.body;
    this->size_n = result.size_n;
    this->size_m = result.size_m;
    was_calc_det = false;

    return result;
}
// ------------------------------------------------------

// ------------------------------------------------------
// division
template<typename val_type>
matrix<val_type> matrix<val_type>::operator / (const val_type number) {
    matrix<val_type> result(this->body);
    for (int i = 0; i < result.line_size(); i++) {
        for (int j = 0; j < result.column_size(); j++) {
            result.body[i][j] /= number;
        }
    }
    return result;
}

template<typename val_type>
matrix<val_type> matrix<val_type>::operator /= (const val_type number) {
    for (int i = 0; i < this->line_size(); i++) {
        for (int j = 0; j < this->column_size(); j++) {
            this->body[i][j] /= number;
        }
    }
    return *(this);
}

template<typename val_type>
matrix<val_type> matrix<val_type>::operator / (matrix<val_type>& sec_matrix) {
    matrix<val_type> inv_sec_matrix;
    inv_sec_matrix = sec_matrix.calc_inverse_matrix();
    return (*this) * inv_sec_matrix;
}

template<typename val_type>
matrix<val_type> matrix<val_type>::operator /= (matrix<val_type>& sec_matrix) {
    matrix<val_type> inv_sec_matrix;
    inv_sec_matrix = sec_matrix.calc_inverse_matrix();
    return ((*this) *= inv_sec_matrix);
}
// ------------------------------------------------------

// ------------------------------------------------------
// plus
template<typename val_type>
matrix<val_type> matrix<val_type>::operator + (const matrix<val_type>& sec_matrix) {
    if (not can_ariphmetic_op_matrix(sec_matrix)) throw matrix_errors::size_err;

    matrix<val_type> result(this->body);
    for (int i = 0; i < sec_matrix.line_size(); i++) {
        for (int j = 0; j < sec_matrix.column_size(); j++) {
            result.body[i][j] += sec_matrix.body[i][j];
        }
    }
    return result;
}

template<typename val_type>
matrix<val_type> matrix<val_type>::operator += (const matrix<val_type>& sec_matrix) {
    if (not can_ariphmetic_op_matrix(sec_matrix)) throw matrix_errors::size_err;

    for (int i = 0; i < sec_matrix.line_size(); i++) {
        for (int j = 0; j < sec_matrix.column_size(); j++) {
            this->body[i][j] += sec_matrix.body[i][j];
        }
    }
    return *(this);
}
// ------------------------------------------------------

// ------------------------------------------------------
// subtraction
template<typename val_type>
matrix<val_type> matrix<val_type>::operator - (const matrix& sec_matrix) {
    if (not can_ariphmetic_op_matrix(sec_matrix)) throw matrix_errors::size_err;

    matrix<val_type> result(this->body);
    for (int i = 0; i < sec_matrix.line_size(); i++) {
        for (int j = 0; j < sec_matrix.column_size(); j++) {
            result.body[i][j] -= sec_matrix.body[i][j];
        }
    }
    return result;
}

template<typename val_type>
matrix<val_type> matrix<val_type>::operator -= (const matrix& sec_matrix) {
    if (not can_ariphmetic_op_matrix(sec_matrix)) throw matrix_errors::size_err;

    for (int i = 0; i < sec_matrix.line_size(); i++) {
        for (int j = 0; j < sec_matrix.column_size(); j++) {
            this->body[i][j] -= sec_matrix.body[i][j];
        }
    }
    return *(this);
}
// ------------------------------------------------------

// ------------------------------------------------------
// subtraction
template<typename val_type>
matrix<val_type> matrix<val_type>::matrix_pow(const val_type number) {
    matrix<val_type> result(this->body);
    for (int i = 0; i < number; i++) {
        result *= result;
    }
    return result;
}

// --------------------------------------------------------------------------------------------------------------------
// БЛОК ФУНКЦИЙ ОПЕРАЦИЙ С МАТРИЦАМИ
// --------------------------------------------------------------------------------------------------------------------
template<typename val_type>
matrix<val_type> matrix<val_type>::calc_minor(int n, int m) {
    // Вычисление минора для элемента [n, m]
    matrix_body<val_type> minor_body(size_n - 1);
    int i_dec = 0;
    for (int minor_i = 0; minor_i < size_m; minor_i++) {
        for (int minor_j = 0; minor_j < size_m; minor_j++) {
            val_type el = body[minor_i][minor_j];
            if (minor_j != m and minor_i != n) minor_body[minor_i - i_dec].push_back(el);
        }
        if (minor_i == n) i_dec = 1;
    }
    matrix<val_type> minor(minor_body);
    return minor;
}

template<typename val_type>
matrix<val_type> matrix<val_type>::calc_inverse_matrix() {
    // Вычисление обратной матрицы
    if (not is_determenant()) throw matrix_errors::no_det;
    if (is_zero_determenant()) throw matrix_errors::zero_det;

    // Расчет матрицы алебраических дополнений
    matrix<val_type> algbro_matrix(this->body);
    for (int i = 0; i < size_n; i++) {
        for (int j = 0; j < size_m; j++) {
            algbro_matrix.body[i][j] = pow(-1, (i + j) % 2) * (this->calc_minor(i, j)).det();
        }
    }

    // Транспонирование матрицы алгебраических дополнений
    algbro_matrix.T();

    // Вычисление обратной матрицы по формуле
    matrix<val_type> inverse_matrix = algbro_matrix * 1 / this->det();
    return  inverse_matrix;
}

template<typename val_type>
matrix<val_type> matrix<val_type>::T(bool self) {
    // Транспонирование матрицы

    // Выделяем место под транспонированную матрицу
    matrix<val_type> T_matrix(this->size_m, this->size_n);

    // Транспонируем матрицу
    for (int i = 0; i < size_n; i++) {
        for (int j = 0; j < size_m; j++) {
            val_type val = this->body[i][j];
            T_matrix.body[j][i] = this->body[i][j];
        }
    }

    // Заменяем матрицу
    if (self) {
        this->body = T_matrix.body;
        this->size_n = T_matrix.size_n;
        this->size_m = T_matrix.size_m;
        was_calc_det = false;
    }

    // Выдача результата во внешнюю среду
    return T_matrix;
}

// --------------------------------------------------------------------------------------------------------------------
// БЛОК ФУНКЦИЙ ПРОВЕРОК ДОПУСТИМОСТИ МАТ.ДЕЙСТВИЙ
// --------------------------------------------------------------------------------------------------------------------
template<typename val_type>
bool matrix<val_type>::is_determenant() {
    // Проверка для определения допустимости нахождения определителя
    if (empty_matrix) return false;
    return size_n == size_m;
}

template<typename val_type>
bool matrix<val_type>::is_zero_determenant() {
    // Проверка для определения допустимости нахождения обратной матрицы
    bool ans;
    if (was_calc_det) ans = determenant > -0.00000001 and determenant < 0.00000001;
    else if (is_determenant()) {
        calc_det();
        ans = (determenant > -0.00000001 and determenant < 0.00000001);
    }
    else throw matrix_errors::no_det;
    return ans;
}

template<typename val_type>
bool matrix<val_type>::can_ariphmetic_op_matrix(const matrix<val_type>& sec_matrix) {
    // Проверка для определения допустимости арифметических операций (-, +)
    return (this->size_n == sec_matrix.size_n and this->size_m == sec_matrix.size_m);
}

template<typename val_type>
bool matrix<val_type>::can_algebra_op_matrix(const matrix<val_type>& sec_matrix) {
    // Проверка для определения допустимости алгебраических операций (*, /)
    return (this->size_m == sec_matrix.size_n);
}

template<typename val_type>
void matrix<val_type>::arr_to_matrix(double arr[102]) {
    // Перевод данных из массива в вектор
    this->body.clear();
    for (int i = 0; i < (int)arr[0]; i++) {
        vector<double> line;
        for (int j = 0; j < (int)arr[1]; j++) {
            // vec[i][m] = arr[i * m + j];
            line.push_back(arr[2 + i * (int)arr[1] + j]);
        }
        this->body.push_back(line);
    }

    this->size_n = (int)arr[0];
    this->size_m = (int)arr[1];
    this->empty_matrix = false;
    this->zero_matrix = false;
    this->was_calc_det = false;
}

#endif //MATRIXCALC_MATRIX_MATH_H