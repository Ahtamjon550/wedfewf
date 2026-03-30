#pragma once
#include <vector>
#include <string>

void keyboard_input(std::vector<int>& arr);

void random_input(std::vector<int>& arr);

void load_from_file(std::vector<int>& arr);

void file_output(std::vector<int>& arr);

bool yes_no_menu(const std::string& message);


void keyboard_input(std::vector<int>& arr);

void random_input(std::vector<int>& arr);

void load_from_file(std::vector<int>& arr);

void file_output(std::vector<int>& arr);

bool yes_no_menu(const std::string& message);

// Добавляем вспомогательные функции для тестов
void print_array(std::vector<int>& array_to_print);
