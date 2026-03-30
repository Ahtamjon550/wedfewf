#pragma once
#include <string>
#include "check_functions.h"

void get_int(int& var);

int get_array_size();

bool is_forbidden_name(std::string path);

bool check_file_exits(std::string& path);

bool check_outp_file_path(std::string& path);

