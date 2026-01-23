#include <iostream>
#include <vector>
#include <clocale>
#include "input_output.h"
#include "check_functions.h"


using namespace std;


void print_array(std::vector<int>& array_to_print) {
    std::cout << std::endl;
    for (int num : array_to_print)
        std::cout << num << " ";
    std::cout << std::endl;
}

// Вспомогательная функция для слияния двух подмассивов
void merge(vector<int>& arr, int left, int mid, int right) {
    int needto = mid - left + 1;
    int nicestway = right - mid;

    // Создаем временные массивы
    vector<int> Let(needto), Rely(nicestway);

    // Копируем данные во временные массивы
    for (int i = 0; i < needto; i++)
        Let[i] = arr[left + i];
    for (int j = 0; j < nicestway; j++)
        Rely[j] = arr[mid + 1 + j];

    // Слияние временных массивов обратно в основной
    int i = 0, j = 0, k = left;
    while (i < needto && j < nicestway) {
        if (Let[i] <= Rely[j]) {
            arr[k] = Let[i];
            i++;
        }
        else {
            arr[k] = Rely[j];
            j++;
        }
        k++;
    }

    // Копируем оставшиеся элементы Let[]
    while (i < needto) {
        arr[k] = Let[i];
        i++;
        k++;
    }

    // Копируем оставшиеся элементы Rely[]
    while (j < nicestway) {
        arr[k] = Rely[j];
        j++;
        k++;
    }
}

// Рекурсивная сортировка слиянием
void merge_sort_helper(vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;

        // Сортируем левую и правую части
        merge_sort_helper(arr, left, mid);
        merge_sort_helper(arr, mid + 1, right);

        // Сливаем отсортированные части
        merge(arr, left, mid, right);
    }
}

// Основная функция сортировки (сохраняет ваш интерфейс)
void merge_sort(vector<int>& arr) {
    if (!arr.empty()) {
        merge_sort_helper(arr, 0, arr.size() - 1);
    }
}

// ввод разными методами, обработка результатов
void results(void (*input) (vector<int>& arr)) {
    vector<int> array_to_sort;

    input(array_to_sort);

    if (array_to_sort.size() == 0)
        return;

    cout << endl << "Исходный массив: ";
    print_array(array_to_sort);

    merge_sort(array_to_sort);  
    cout << "Отсортированный массив: ";
    print_array(array_to_sort);
    cout << endl;

    if (yes_no_menu("Сохранить результат сортировки в файл?")) {
        file_output(array_to_sort);
        cout << "Данные сохранены в файл." << endl << endl;
    }

    array_to_sort.clear();
}

// главное меню
enum menu_items { keyboard = 1, random_items, file, prog_exit };

int main() {
    setlocale(LC_ALL, "");

    srand(0);

    int user_choice = 0; 

    do {
        if (user_choice == 0) {
            cout << "---------------------------" << endl
                << "|  Бобокалонов Акрамжон    |" << endl 
                << "|  Сортировка слиянием     |" << endl  
                <<  "---------------------------" << endl
                << "Выберите способ заполнения массива:" << endl
                << "1 - Заполнение с клавиатуры;" << endl
                << "2 - Заполнение случайными числами;" << endl
                << "3 - Загрузка данных из файла;" << endl
                << "4 - Выход." << endl; 
             
        }

        cout << "Введите число: ";
        get_int(user_choice);
        cout << endl;

        switch (user_choice) {
        case keyboard:
            results(keyboard_input);
            user_choice = 0;
            break;

        case random_items:
            results(random_input);
            user_choice = 0;
            break;

        case file:
            results(load_from_file);
            user_choice = 0;
            break;

        case prog_exit:
            return 0;

        default:
            cout << "Некорректный пункт меню." << endl;
            break;
        }

    } while (true);
}