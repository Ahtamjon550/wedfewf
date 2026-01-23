import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, simpledialog
import sqlite3
import random
import time
import json


class SimpleArraySorter:
    def __init__(self, root):
        self.root = root
        self.root.title("Array Sorter")
        self.root.geometry("800x500")  # Меньший размер при запуске
        
        # Текущий пользователь
        self.current_user = None
        self.user_id = None
        
        # Настройки темы (по умолчанию светлая)
        self.dark_mode = False
        
        # Подключение к базе данных
        self.conn = sqlite3.connect('simple_arrays.db')
        self.setup_database()
        
        # Показать окно входа
        self.show_login_screen()

    def get_colors(self):
        """Возвращает цвета для текущей темы"""
        if self.dark_mode:
            return {
                'bg': '#2b2b2b',
                'fg': '#ffffff',
                'entry_bg': '#3c3c3c',
                'entry_fg': '#ffffff',
                'button_bg': '#505050',
                'button_fg': '#ffffff',
                'frame_bg': '#3c3c3c',
                'label_bg': '#2b2b2b',
                'text_bg': '#3c3c3c',
                'text_fg': '#ffffff',
                'accent': '#4CAF50',
                'tree_bg': '#3c3c3c',
                'tree_fg': '#ffffff',
                'tree_heading_bg': '#404040',
                'tree_heading_fg': '#ffffff'
            }
        else:
            return {
                'bg': '#f0f0f0',
                'fg': '#000000',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'button_bg': '#e0e0e0',
                'button_fg': '#000000',
                'frame_bg': '#ffffff',
                'label_bg': '#f0f0f0',
                'text_bg': '#ffffff',
                'text_fg': '#000000',
                'accent': '#4CAF50',
                'tree_bg': '#ffffff',
                'tree_fg': '#000000',
                'tree_heading_bg': '#e0e0e0',
                'tree_heading_fg': '#000000'
            }

    def apply_theme_to_widget(self, widget, colors):
        """Применяет тему к виджету и всем его дочерним виджетам"""
        widget_type = widget.winfo_class()
        
        # Применяем цвета в зависимости от типа виджета
        if widget_type in ('TFrame', 'Frame', 'Labelframe', 'LabelFrame'):
            try:
                widget.configure(bg=colors['bg'])
            except:
                pass
                
        elif widget_type in ('Entry', 'Text', 'ScrolledText'):
            try:
                widget.configure(
                    bg=colors['entry_bg'],
                    fg=colors['entry_fg'],
                    insertbackground=colors['entry_fg']
                )
            except:
                pass
                
        elif widget_type == 'Label':
            try:
                widget.configure(bg=colors['label_bg'], fg=colors['fg'])
            except:
                pass
                
        elif widget_type == 'Button':
            # Не меняем цвет кнопок, чтобы сохранить их стиль
            pass
                
        elif widget_type == 'Radiobutton':
            try:
                widget.configure(
                    bg=colors['frame_bg'],
                    fg=colors['fg'],
                    selectcolor=colors['frame_bg']
                )
            except:
                pass
                
        # Рекурсивно применяем к дочерним виджетам
        for child in widget.winfo_children():
            self.apply_theme_to_widget(child, colors)

    def setup_database(self):
        """Создаем простую базу данных"""
        cursor = self.conn.cursor()
        
        # Таблица пользователей (простая)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        
        # Таблица массивов (простая)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS arrays (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                name TEXT,
                original TEXT,
                sorted TEXT,
                created TEXT
            )
        ''')
        
        self.conn.commit()

    def show_login_screen(self):
        """Показать экран входа"""
        self.clear_window()
        colors = self.get_colors()
        
        # Применяем тему ко всему окну
        self.root.configure(bg=colors['bg'])
        
        # Заголовок
        tk.Label(self.root, text="Array Sorter", font=("Arial", 20, "bold"),
                bg=colors['bg'], fg=colors['fg']).pack(pady=20)
        
        # Фрейм для ввода
        frame = tk.Frame(self.root, bg=colors['frame_bg'], padx=20, pady=20)
        frame.pack(pady=10)
        
        # Логин
        tk.Label(frame, text="Логин:", font=("Arial", 11),
                bg=colors['frame_bg'], fg=colors['fg']).grid(row=0, column=0, pady=5, sticky='w')
        self.login_entry = tk.Entry(frame, font=("Arial", 11), width=20,
                                   bg=colors['entry_bg'], fg=colors['entry_fg'],
                                   insertbackground=colors['fg'])
        self.login_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Пароль
        tk.Label(frame, text="Пароль:", font=("Arial", 11),
                bg=colors['frame_bg'], fg=colors['fg']).grid(row=1, column=0, pady=5, sticky='w')
        self.password_entry = tk.Entry(frame, font=("Arial", 11), width=20, show="*",
                                      bg=colors['entry_bg'], fg=colors['entry_fg'],
                                      insertbackground=colors['fg'])
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Кнопки
        button_frame = tk.Frame(self.root, bg=colors['bg'])
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Войти", font=("Arial", 11), width=12,
                 command=self.login, bg="#4CAF50", fg="white",
                 activebackground="#45a049").pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Регистрация", font=("Arial", 11), width=12,
                 command=self.register, bg="#2196F3", fg="white",
                 activebackground="#1976D2").pack(side=tk.LEFT, padx=5)
        
        # Фокус на поле логина
        self.login_entry.focus()
        
        # Привязка Enter
        self.root.bind('<Return>', lambda e: self.login())

    def login(self):
        """Простой вход"""
        username = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Ошибка", "Введите логин и пароль")
            return
        
        cursor = self.conn.cursor()
        
        # Ищем пользователя
        cursor.execute("SELECT id FROM users WHERE username=? AND password=?", 
                      (username, password))
        result = cursor.fetchone()
        
        if result:
            self.current_user = username
            self.user_id = result[0]
            self.show_main_window()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def register(self):
        """Простая регистрация"""
        username = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username:
            messagebox.showwarning("Ошибка", "Введите логин")
            return
        
        if not password:
            messagebox.showwarning("Ошибка", "Введите пароль")
            return
        
        if len(username) < 2:
            messagebox.showwarning("Ошибка", "Логин должен быть минимум 2 символа")
            return
        
        cursor = self.conn.cursor()
        
        try:
            # Проверяем, есть ли уже такой пользователь
            cursor.execute("SELECT id FROM users WHERE username=?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Ошибка", "Пользователь уже существует")
                return
            
            # Добавляем нового пользователя
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                          (username, password))
            self.conn.commit()
            
            messagebox.showinfo("Успех", "Регистрация успешна! Теперь войдите.")
            
            # Очищаем поля
            self.login_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка регистрации: {str(e)}")

    def show_main_window(self):
        """Показать главное окно"""
        self.clear_window()
        colors = self.get_colors()
        
        # Применяем тему ко всему окну
        self.root.configure(bg=colors['bg'])
        
        # Создаем меню
        menubar = tk.Menu(self.root)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Выйти", command=self.logout)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        # Меню "Настройки"
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Светлая тема", 
                                command=lambda: self.toggle_theme(False))
        settings_menu.add_command(label="Темная тема", 
                                command=lambda: self.toggle_theme(True))
        menubar.add_cascade(label="Настройки", menu=settings_menu)
        
        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Справка", menu=help_menu)
        
        self.root.config(menu=menubar)
        
        # Заголовок с информацией о пользователе
        header = tk.Frame(self.root, bg=colors['bg'])
        header.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(header, text=f"Пользователь: {self.current_user}", 
                font=("Arial", 11, "bold"),
                bg=colors['bg'], fg=colors['fg']).pack(side=tk.LEFT)
        
        tk.Button(header, text="Выйти", font=("Arial", 10),
                 command=self.logout, bg="#f44336", fg="white",
                 activebackground="#d32f2f").pack(side=tk.RIGHT)
        
        # Вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Создаем вкладки
        self.create_array_tab()
        self.create_manager_tab()
        
        # По умолчанию показываем вкладку с массивом
        self.notebook.select(0)
        
        # Применяем тему ко всем виджетам
        self.apply_theme_to_widget(self.root, colors)

    def create_array_tab(self):
        """Создать вкладку работы с массивом"""
        colors = self.get_colors()
        
        tab = tk.Frame(self.notebook, bg=colors['bg'])
        self.notebook.add(tab, text="Работа с массивом")
        
        # Левая часть - ввод данных
        left_frame = tk.LabelFrame(tab, text="Ввод массива", padx=10, pady=10,
                                  bg=colors['frame_bg'], fg=colors['fg'],
                                  font=("Arial", 10, "bold"))
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5), pady=5)
        
        # Выбор метода
        tk.Label(left_frame, text="Метод создания:", font=("Arial", 10),
                bg=colors['frame_bg'], fg=colors['fg']).pack(anchor='w', pady=(0, 5))
        
        self.method_var = tk.StringVar(value="random")
        
        tk.Radiobutton(left_frame, text="Случайные числа", variable=self.method_var,
                      value="random", command=self.update_method,
                      bg=colors['frame_bg'], fg=colors['fg'],
                      selectcolor=colors['frame_bg']).pack(anchor='w')
        
        tk.Radiobutton(left_frame, text="Ввести вручную", variable=self.method_var,
                      value="manual", command=self.update_method,
                      bg=colors['frame_bg'], fg=colors['fg'],
                      selectcolor=colors['frame_bg']).pack(anchor='w')
        
        # Параметры для случайных чисел
        self.random_frame = tk.Frame(left_frame, bg=colors['frame_bg'])
        
        tk.Label(self.random_frame, text="Количество:",
                bg=colors['frame_bg'], fg=colors['fg']).grid(row=0, column=0, sticky='w', pady=2)
        self.count_entry = tk.Entry(self.random_frame, width=8,
                                   bg=colors['entry_bg'], fg=colors['entry_fg'],
                                   insertbackground=colors['fg'])
        self.count_entry.grid(row=0, column=1, padx=5, pady=2)
        self.count_entry.insert(0, "10")
        
        tk.Label(self.random_frame, text="От:",
                bg=colors['frame_bg'], fg=colors['fg']).grid(row=1, column=0, sticky='w', pady=2)
        self.min_entry = tk.Entry(self.random_frame, width=8,
                                 bg=colors['entry_bg'], fg=colors['entry_fg'],
                                 insertbackground=colors['fg'])
        self.min_entry.grid(row=1, column=1, padx=5, pady=2)
        self.min_entry.insert(0, "1")
        
        tk.Label(self.random_frame, text="До:",
                bg=colors['frame_bg'], fg=colors['fg']).grid(row=2, column=0, sticky='w', pady=2)
        self.max_entry = tk.Entry(self.random_frame, width=8,
                                 bg=colors['entry_bg'], fg=colors['entry_fg'],
                                 insertbackground=colors['fg'])
        self.max_entry.grid(row=2, column=1, padx=5, pady=2)
        self.max_entry.insert(0, "100")
        
        # Поле для ручного ввода
        self.manual_frame = tk.Frame(left_frame, bg=colors['frame_bg'])
        tk.Label(self.manual_frame, text="Числа через пробел:",
                bg=colors['frame_bg'], fg=colors['fg']).pack(anchor='w')
        
        self.manual_entry = tk.Entry(self.manual_frame, width=25,
                                    bg=colors['entry_bg'], fg=colors['entry_fg'],
                                    insertbackground=colors['fg'])
        self.manual_entry.pack(fill=tk.X, pady=2)
        self.manual_entry.insert(0, "5 2 8 1 9 3 7 4 6")
        
        # Кнопки управления
        button_frame = tk.Frame(left_frame, bg=colors['frame_bg'])
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Создать", font=("Arial", 10), width=10,
                 command=self.create_array, bg="#2196F3", fg="white",
                 activebackground="#1976D2").pack(side=tk.LEFT, padx=2)
        
        tk.Button(button_frame, text="Сортировать", font=("Arial", 10), width=10,
                 command=self.sort_array, bg="#4CAF50", fg="white",
                 activebackground="#45a049").pack(side=tk.LEFT, padx=2)
        
        tk.Button(button_frame, text="Сохранить", font=("Arial", 10), width=10,
                 command=self.save_array, bg="#FF9800", fg="white",
                 activebackground="#f57c00").pack(side=tk.LEFT, padx=2)
        
        # Правая часть - отображение
        right_frame = tk.LabelFrame(tab, text="Результаты", padx=10, pady=10,
                                   bg=colors['frame_bg'], fg=colors['fg'],
                                   font=("Arial", 10, "bold"))
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        
        # Исходный массив
        tk.Label(right_frame, text="Исходный массив:", font=("Arial", 10, "bold"),
                bg=colors['frame_bg'], fg=colors['fg']).pack(anchor='w')
        
        self.original_text = scrolledtext.ScrolledText(right_frame, height=6, width=35,
                                                      bg=colors['text_bg'], fg=colors['text_fg'],
                                                      insertbackground=colors['fg'])
        self.original_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Отсортированный массив
        tk.Label(right_frame, text="Отсортированный массив:", font=("Arial", 10, "bold"),
                bg=colors['frame_bg'], fg=colors['fg']).pack(anchor='w')
        
        self.sorted_text = scrolledtext.ScrolledText(right_frame, height=6, width=35,
                                                    bg=colors['text_bg'], fg=colors['text_fg'],
                                                    insertbackground=colors['fg'])
        self.sorted_text.pack(fill=tk.BOTH, expand=True)
        
        # Инициализация
        self.current_array = []
        self.update_method()

    def update_method(self):
        """Обновить вид в зависимости от метода"""
        method = self.method_var.get()
        
        if method == "random":
            self.random_frame.pack(fill=tk.X, pady=10)
            self.manual_frame.pack_forget()
        else:
            self.random_frame.pack_forget()
            self.manual_frame.pack(fill=tk.X, pady=10)

    def create_array(self):
        """Создать массив"""
        method = self.method_var.get()
        
        try:
            if method == "random":
                # Создаем случайный массив
                count = int(self.count_entry.get())
                min_val = int(self.min_entry.get())
                max_val = int(self.max_entry.get())
                
                if count <= 0:
                    messagebox.showerror("Ошибка", "Количество должно быть больше 0")
                    return
                
                if min_val > max_val:
                    messagebox.showerror("Ошибка", "Минимум не может быть больше максимума")
                    return
                
                self.current_array = [random.randint(min_val, max_val) for _ in range(count)]
                
            else:  # manual
                # Читаем ручной ввод
                text = self.manual_entry.get().strip()
                if not text:
                    messagebox.showerror("Ошибка", "Введите числа")
                    return
                
                try:
                    self.current_array = list(map(int, text.split()))
                except:
                    messagebox.showerror("Ошибка", "Введите только числа через пробел")
                    return
            
            # Показываем массив
            self.original_text.delete(1.0, tk.END)
            self.original_text.insert(1.0, str(self.current_array))
            
            # Очищаем отсортированный
            self.sorted_text.delete(1.0, tk.END)
            
            messagebox.showinfo("Успех", f"Массив создан ({len(self.current_array)} элементов)")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка создания массива: {str(e)}")

    def msd_sort(self, arr):
        """Простая реализация MSD сортировки"""
        if not arr:
            return arr
        
        # Разделяем отрицательные и положительные
        negatives = [x for x in arr if x < 0]
        positives = [x for x in arr if x >= 0]
        
        # Сортируем отдельно
        negatives = sorted(negatives, reverse=True)
        positives = sorted(positives)
        
        return negatives + positives

    def sort_array(self):
        """Сортировать массив"""
        if not self.current_array:
            messagebox.showwarning("Внимание", "Сначала создайте массив")
            return
        
        try:
            # Сортируем
            self.sorted_array = self.msd_sort(self.current_array)
            
            # Показываем результат
            self.sorted_text.delete(1.0, tk.END)
            self.sorted_text.insert(1.0, str(self.sorted_array))
            
            messagebox.showinfo("Успех", "Массив отсортирован")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сортировки: {str(e)}")

    def save_array(self):
        """Сохранить массив в БД"""
        if not self.current_user:
            messagebox.showerror("Ошибка", "Вы не вошли в систему")
            return
        
        if not self.current_array:
            messagebox.showwarning("Внимание", "Нет массива для сохранения")
            return
        
        # Запрашиваем название
        name = simpledialog.askstring("Сохранение", "Введите название массива:")
        if not name:
            return
        
        try:
            cursor = self.conn.cursor()
            
            # Сохраняем оригинальный массив
            original_str = json.dumps(self.current_array)
            
            # Если есть отсортированный, сохраняем его тоже
            if hasattr(self, 'sorted_array'):
                sorted_str = json.dumps(self.sorted_array)
            else:
                sorted_str = None
            
            cursor.execute('''
                INSERT INTO arrays (user_id, name, original, sorted, created)
                VALUES (?, ?, ?, ?, datetime('now'))
            ''', (self.user_id, name, original_str, sorted_str))
            
            self.conn.commit()
            
            messagebox.showinfo("Успех", "Массив сохранен")
            
            # Обновляем список в менеджере
            if hasattr(self, 'tree'):
                self.load_arrays()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")

    def create_manager_tab(self):
        """Создать вкладку менеджера массивов"""
        colors = self.get_colors()
        
        tab = tk.Frame(self.notebook, bg=colors['bg'])
        self.notebook.add(tab, text="Мои массивы")
        
        # Таблица с массивами
        frame = tk.Frame(tab, bg=colors['bg'])
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем таблицу
        columns = ("ID", "Название", "Исходный", "Отсортированный", "Дата")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        
        # Настраиваем стиль для дерева
        style = ttk.Style()
        
        # Настраиваем колонки
        for col in columns:
            self.tree.heading(col, text=col)
            if col == "ID":
                self.tree.column(col, width=40, anchor='center')
            elif col == "Дата":
                self.tree.column(col, width=120, anchor='center')
            elif col == "Название":
                self.tree.column(col, width=100)
            else:
                self.tree.column(col, width=150)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопки управления
        button_frame = tk.Frame(tab, bg=colors['bg'])
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Button(button_frame, text="Обновить", font=("Arial", 9), width=8,
                 command=self.load_arrays, bg="#2196F3", fg="white",
                 activebackground="#1976D2").pack(side=tk.LEFT, padx=2)
        
        tk.Button(button_frame, text="Загрузить", font=("Arial", 9), width=10,
                 command=self.load_selected, bg="#4CAF50", fg="white",
                 activebackground="#45a049").pack(side=tk.LEFT, padx=2)
        
        tk.Button(button_frame, text="Удалить", font=("Arial", 9), width=8,
                 command=self.delete_selected, bg="#f44336", fg="white",
                 activebackground="#d32f2f").pack(side=tk.LEFT, padx=2)
        
        # Загружаем массивы
        self.load_arrays()

    def load_arrays(self):
        """Загрузить массивы пользователя"""
        if not self.user_id:
            return
        
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT id, name, original, sorted, created 
                FROM arrays 
                WHERE user_id = ? 
                ORDER BY created DESC
            ''', (self.user_id,))
            
            for row in cursor.fetchall():
                # Форматируем массивы
                try:
                    original = json.loads(row[2])
                    if len(original) > 8:
                        original_str = str(original[:8]) + "..."
                    else:
                        original_str = str(original)
                    
                    if row[3]:
                        sorted_arr = json.loads(row[3])
                        if len(sorted_arr) > 8:
                            sorted_str = str(sorted_arr[:8]) + "..."
                        else:
                            sorted_str = str(sorted_arr)
                    else:
                        sorted_str = "-"
                except:
                    original_str = "Ошибка"
                    sorted_str = "Ошибка"
                
                self.tree.insert("", tk.END, values=(
                    row[0], row[1], original_str, sorted_str, row[4]
                ))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}")

    def load_selected(self):
        """Загрузить выбранный массив"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите массив")
            return
        
        try:
            item = self.tree.item(selected[0])
            array_id = item['values'][0]
            
            cursor = self.conn.cursor()
            cursor.execute("SELECT original, sorted FROM arrays WHERE id = ?", (array_id,))
            result = cursor.fetchone()
            
            if result:
                # Загружаем оригинальный массив
                self.current_array = json.loads(result[0])
                
                # Показываем в основном окне
                self.original_text.delete(1.0, tk.END)
                self.original_text.insert(1.0, str(self.current_array))
                
                # Если есть отсортированный
                self.sorted_text.delete(1.0, tk.END)
                if result[1]:
                    self.sorted_array = json.loads(result[1])
                    self.sorted_text.insert(1.0, str(self.sorted_array))
                
                # Переключаемся на вкладку работы с массивом
                self.notebook.select(0)
                
                messagebox.showinfo("Успех", "Массив загружен")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}")

    def delete_selected(self):
        """Удалить выбранный массив"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите массив")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранный массив?"):
            try:
                item = self.tree.item(selected[0])
                array_id = item['values'][0]
                
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM arrays WHERE id = ?", (array_id,))
                self.conn.commit()
                
                self.load_arrays()
                messagebox.showinfo("Успех", "Массив удален")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка удаления: {str(e)}")

    def toggle_theme(self, dark_mode):
        """Переключение темы - теперь работает корректно"""
        if self.dark_mode != dark_mode:
            self.dark_mode = dark_mode
            
            # Получаем новые цвета
            colors = self.get_colors()
            
            # Применяем тему ко всему окну и всем виджетам
            if self.current_user:
                # Сохраняем текущую вкладку
                current_tab = self.notebook.index(self.notebook.select())
                
                # Пересоздаем главное окно с новой темой
                self.show_main_window()
                
                # Восстанавливаем вкладку
                if current_tab < self.notebook.index("end"):
                    self.notebook.select(current_tab)
            else:
                # Пересоздаем окно входа
                self.show_login_screen()

    def show_about(self):
        """Показать окно 'О программе'"""
        colors = self.get_colors()
        
        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("500x350")
        about_window.configure(bg=colors['bg'])
        about_window.resizable(False, False)
        
        # Центрируем окно
        about_window.transient(self.root)
        about_window.grab_set()
        
        # Заголовок
        tk.Label(about_window, text="Array Sorter", 
                font=("Arial", 18, "bold"),
                bg=colors['bg'], fg=colors['fg']).pack(pady=15)
        
        # Информация о программе
        info_frame = tk.Frame(about_window, bg=colors['bg'])
        info_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        info_text = """
Добро пожаловать в справку!
Здесть находится все информация о программе.
Программа для сортировки массивов
Версия: 1.0
Основатель: Акрамжон Бобоклонов 
Функционал:
• Регистрация и авторизация пользователей
• Создание массивов:
  - Генерация случайных чисел
  - Ручной ввод
• Сортировка массивов методом MSD
• Сохранение массивов в базу данных
• Управление сохраненными массивами
Программа предоставляет возможность создания
личного кабинета, за которым можно пользоваться
программой без вход, но все сохраненные массивы
под аккаунтом гостя будут удалены после выхода
из программы.

            """
        
        text_widget = scrolledtext.ScrolledText(info_frame, width=55, height=15,
                                               bg=colors['text_bg'], fg=colors['text_fg'],
                                               insertbackground=colors['fg'],
                                               font=("Arial", 9))
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(1.0, info_text)
        text_widget.config(state=tk.DISABLED)
        
        # Кнопка закрытия
        tk.Button(about_window, text="Закрыть", font=("Arial", 10), width=10,
                 command=about_window.destroy, bg="#f44336", fg="white",
                 activebackground="#d32f2f").pack(pady=10)
        
        # Центрируем окно
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = (about_window.winfo_screenwidth() // 2) - (width // 2)
        y = (about_window.winfo_screenheight() // 2) - (height // 2)
        about_window.geometry(f'{width}x{height}+{x}+{y}')

    def logout(self):
        """Выйти из системы"""
        self.current_user = None
        self.user_id = None
        self.show_login_screen()

    def clear_window(self):
        """Очистить окно"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        """Запустить приложение"""
        self.root.mainloop()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleArraySorter(root)
    app.run()
