#include "check_functions.h"
#include <iostream>
#include <limits>
#include <algorithm>
#include <fstream>

using namespace std;

// проверка на ввод числа
void get_int(int& var) {

    while (!(cin >> var)) {
        cout << "Некорректный ввод." << endl
            << "Введите число: ";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

// проверка на ввод размера массива
int get_array_size() {
    int size = 0;
    do {
        cout << "Введите размер массива: ";
        get_int(size);

        if (size >= 1)
            return size;
        else
            cout << "Некорректный размер массива." << endl;

    } while (true);
}


// проверка на запрещенные названия для windows
bool is_forbidden_name(string path) {
    const string forbidden_names[] = { "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6",
    "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9" };

    if (path.find_last_of('\\') != string::npos)
        path = path.substr(path.find_last_of('\\') + 1);

    transform(path.begin(), path.end(), path.begin(), [](unsigned char c) { return static_cast<unsigned char>(toupper(c)); });

    for (const string& name : forbidden_names)
        if (path == name)
            return true;

    return false;
}

// проверка пути файла на ввод данных
bool check_file_exits(string& path) {
    ifstream file;

    file.open(path);

    if (!file.is_open())
        return false;

    file.close();

    return true;
}

// проверка пути файла на вывод данных
bool check_outp_file_path(string& path) {

    if (is_forbidden_name(path))
        return false;

    ofstream file;
    file.open(path, ios::app);
    if (!file.is_open())
        return false;
    file.close();

    return true;
}