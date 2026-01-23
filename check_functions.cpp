#include <direct.h> // Для Windows
#include <sys/stat.h> // Для проверки директорий
#include <string>
#include "check_functions.h"

// Функция для проверки существования директории
bool directory_exists(const std::string& path) {
    struct stat info;
    if (stat(path.c_str(), &info) != 0)
        return false;
    return (info.st_mode & S_IFDIR) != 0;
}

// Функция для проверки пути вывода
bool validate_output_path(const std::string& path) {
    // Проверяем запрещенные имена
    if (is_forbidden_name(path))
        return false;

    // Проверяем недопустимые символы
    std::string invalid_chars = "<>:\"|?*";
    for (char c : invalid_chars) {
        if (path.find(c) != std::string::npos)
            return false;
    }

    return true;
}