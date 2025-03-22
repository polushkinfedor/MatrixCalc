## Description

Матричный калькулятор, реализующий библиотку для работы с типом данных матрицы в файле matrix_math.cpp и интерфейс для работы в MatrixCalc.py

## Start of work and usage

Для работы с калькулятором необходимо сгенерировать exe-файл из MatrixCalc.py 
(например при помощи средства Pyinstaller необходимо открыть командную строку и из директории, в которой находится 
MatrixCalc.py выполнить комманду "pyinstaller --noconsole --onefile MatrixCalc.py")
К сгенерированному exe-файлу в директорию необходимо положить matrixcalc_lib.dll

Пожалуйста, проверьте что в пути до директории с программой отсутствуют символы кириллицы

## Used dependences

-- Исходники c++ файлов, задействованных в динамической библиотеке находятся в директории Source\C:
   matrix_math.cpp
   matrixcalc_lib.cpp
-- Исходный файл интерфейса python находится в директории Source\py:
   MatrixCalc.py

Используемые py-библиотеки: tkinter, datetime, os и ctypes
Использованные заголовочные С++ файлы: Windows.h, vector, typeinfo и math.h

## author:  Полушкин Ф.Ю. 
