#include "input_output.h"
#include "check_functions.h"
#include <iostream>
#include <fstream>
#include <ctime> // Для srand(time(0))
#include <iomanip> // Для std::setw
#include <cmath>   // Для статистики

// Функция для вывода таблицы
void print_table(std::vector<int>& array_to_print) {
    if (array_to_print.empty()) return;

    std::cout << "\nТаблица результатов:\n";
    std::cout << "Индекс | Значение\n";
    std::cout << "-----------------\n";
    for (size_t i = 0; i < array_to_print.size(); i++) {
        std::cout << std::setw(6) << i + 1 << " | "
            << std::setw(8) << array_to_print[i] << "\n";
    }
}

// Функция для вывода статистики
void print_statistics(std::vector<int>& array_to_print) {
    if (array_to_print.empty()) return;

    int sum = 0;
    int min_val = array_to_print[0];
    int max_val = array_to_print[0];

    for (int num : array_to_print) {
        sum += num;
        if (num < min_val) min_val = num;
        if (num > max_val) max_val = num;
    }

    double average = static_cast<double>(sum) / array_to_print.size();

    std::cout << "\nСтатистика:\n";
    std::cout << "Количество элементов: " << array_to_print.size() << "\n";
    std::cout << "Минимальное значение: " << min_val << "\n";
    std::cout << "Максимальное значение: " << max_val << "\n";
    std::cout << "Среднее значение: " << std::fixed << std::setprecision(2) << average << "\n";
    std::cout << "Сумма элементов: " << sum << "\n";
}
using namespace std;

// ввод с клавиатуры
void keyboard_input(vector<int>& arr) {
    int size = get_array_size();
    int element;
    for (size_t i = 0; i < size; i++) {
        cout << "Введите " << i + 1 << " элемент массива: ";
        get_int(element);
        arr.push_back(element);
    }
}

enum range_input { without_range = 1, with_range };
// заполнение рандомными числами
void random_input(vector<int>& arr) {
    srand(time(0)); // Инициализация генератора случайных чисел

    int size = get_array_size();
    int user_choice = 0;
    do {
        cout << "Выберите способ случайного заполнения: " << endl
            << "1 - Заполнение случайными числами без диапазона;" << endl
            << "2 - Заполнение случайными числами в выбранном диапазоне." << endl;
        cout << "Введите число: ";
        get_int(user_choice);

        if (user_choice == without_range || user_choice == with_range) {
            switch (user_choice) {
            case without_range:
                for (size_t i = 0; i < size; i++)
                    arr.push_back(rand());
                return;
            case with_range:
            {
                int first_range_num, second_range_num;
                do {
                    cout << "Введите первое число диапазона: ";
                    get_int(first_range_num);
                    cout << "Введите второе число диапазона: ";
                    get_int(second_range_num);
                    if (first_range_num > second_range_num)
                        cout << "Некорректный диапазон." << endl;
                } while (first_range_num > second_range_num);

                int range_size = second_range_num - first_range_num + 1;
                for (size_t i = 0; i < size; i++)
                    arr.push_back(rand() % range_size + first_range_num);
                return;
            }
            }
        }
        else
            cout << "Некорректный пункт меню." << endl;
    } while (true);
}


void load_from_file(vector<int>& arr) {
    ifstream file;
    string path;
    do {
        cout << "Введите путь к файлу: ";
        getline(cin, path);
        if (check_file_exits(path))
            break;
        else
            cout << "Файл не найден." << endl;
    } while (true);

    file.open(path);
    if (!file.is_open()) {
        cout << "Ошибка: не удалось открыть файл. Проверьте путь и права доступа." << endl;
        return;
    }

    int element;
    while (file >> element) {
        arr.push_back(element);
    }

    if (file.fail() && !file.eof()) {
        cout << "Ошибка при чтении данных из файла. Корректно загружено: " << arr.size() << " элементов." << endl;
    }
    file.close();
}

enum menu_items { yes = 1, no };
// меню ответа да/нет для передаваемого сообщения
bool yes_no_menu(const string& message) {
    int user_choice = 0;
    cout << message << endl
        << "1 - Да" << endl
        << "2 - Нет" << endl;
    do {
        cout << "Введите число: ";
        get_int(user_choice);
        switch (user_choice) {
        case yes:
            return true;
        case no:
            return false;
        default:
            cout << "Некорректный пункт меню." << endl;
        }
    } while (true);
    return false;
}

// сохранение файла в лбом месте
void file_output(vector<int>& arr) {
    ofstream file;
    string path;

    while (true) {
        cout << "Введите полный путь для сохранения файла (например, C:/data.txt или ./results.txt): ";
        getline(cin, path);

        // Проверяем, существует ли файл с таким именем
        if (check_file_exits(path)) {
            if (!yes_no_menu("Файл уже существует. Перезаписать?")) {
                continue; // Просим ввести путь заново
            }
        }

        // Пробуем открыть файл для записи
        file.open(path);
        if (file.is_open()) {
            break; // Успешное открытие
        }

        cout << "Ошибка: невозможно создать файл по указанному пути. Проверьте:" << endl
            << "- Права на запись в папку" << endl
            << "- Корректность имени файла (недопустимые символы: \\ / : * ? \" < > |)" << endl
            << "- Существование родительских папок (например, C:/nonexistent_folder/file.txt не сработает)" << endl;
    }

    // Запись данных
    for (size_t i = 0; i < arr.size(); i++) {
        file << arr[i];
        if (i < arr.size() - 1) file << " ";
    }

    file.close();

    if (file.good()) {
        cout << "Данные успешно сохранены в " << path << endl;
    }
    else {
        cout << "Ошибка при записи данных. Файл мог быть поврежден." << endl;
    }
}