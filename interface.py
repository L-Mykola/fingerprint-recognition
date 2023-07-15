import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
from PIL import ImageTk, Image

from system_training import demonstration_and_save_data
from authentication import authorization
from identification import identification
from tools.print_result import print_result_comparison

image = None


def confirm_reg():
    login = frame1_entry_login.get().strip()
    file_path = frame1_label_path['text']

    if not login or not file_path:
        messagebox.showerror("Помилка", "Будь ласка, заповніть усі поля")
        return

    is_user_exist = demonstration_and_save_data(login, image)
    if is_user_exist:
        messagebox.showerror("Помилка", "Користувач вже існує")
        frame1_entry_login.delete(0, tk.END)
        frame1_label_path.configure(text="")
        frame1_photo_label.configure(image=initial_photo)
        frame1_photo_label.image = initial_photo
        return

    frame1_entry_login.delete(0, tk.END)
    frame1_label_path.configure(text="")
    frame1_photo_label.configure(image=initial_photo)
    frame1_photo_label.image = initial_photo


def confirm_ind():
    file_path = frame2_label_path['text']

    if not file_path:
        messagebox.showerror("Помилка", "Будь ласка, заповніть усі поля")
        return

    result, sample, is_database_exist = identification(image)

    if not is_database_exist:
        messagebox.showerror("Помилка", "Бази даних не існує")
        frame2_label_status.configure(text="Статус: ")
        frame2_label_result.configure(text=f"Результат: ")
        frame2_label_path.configure(text="")
        frame2_photo_label.configure(image=initial_photo)
        frame2_photo_label.image = initial_photo
        return

    if result[1] > 65:
        frame2_label_status.configure(text=f"Статус: Ви {result[0]}")
        frame2_label_result.configure(text=f"Результат: {result[1]}")
        benchmark = cv2.imread(f'processed_images/{result[0]}.tif', cv2.IMREAD_GRAYSCALE)
        print_result_comparison(benchmark, sample, result[2])

        frame2_label_status.configure(text="Статус: ")
        frame2_label_result.configure(text=f"Результат: ")
        frame2_label_path.configure(text="")
        frame2_photo_label.configure(image=initial_photo)
        frame2_photo_label.image = initial_photo

    else:
        frame2_label_status.configure(text=f"Статус: Ви невідомий")
        frame2_label_result.configure(text=f"Результат: {result[1]}")


def confirm_aut():
    login = frame3_entry_login.get().strip()
    file_path = frame3_label_path['text']

    if not login or not file_path:
        messagebox.showerror("Помилка", "Будь ласка, заповніть усі поля")
        return

    result, benchmark, sample, matched, is_database_exist, is_user_exist = authorization(login, image)

    if not is_database_exist:
        messagebox.showerror("Помилка", "Бази даних не існує")
        frame3_label_status.configure(text="Статус: ")
        frame3_label_result.configure(text=f"Результат: ")
        frame3_label_path.configure(text="")
        frame3_photo_label.configure(image=initial_photo)
        frame3_photo_label.image = initial_photo
        return
    if not is_user_exist:
        messagebox.showerror("Помилка", "Користувача не існує")
        frame3_label_status.configure(text="Статус: ")
        frame3_label_result.configure(text=f"Результат: ")
        frame3_label_path.configure(text="")
        frame3_photo_label.configure(image=initial_photo)
        frame3_photo_label.image = initial_photo
        return

    if result >= 65:
        frame3_label_status.configure(text="Статус: Автентифікацію пройдено")
        frame3_label_result.configure(text=f"Результат: {result}")
    else:
        frame3_label_status.configure(text="Статус: Автентифікацію не пройдено")
        frame3_label_result.configure(text=f"Результат: {result}")

    print_result_comparison(benchmark, sample, matched)
    frame3_entry_login.delete(0, tk.END)
    frame3_label_status.configure(text="Статус: ")
    frame3_label_result.configure(text=f"Результат: ")
    frame3_label_path.configure(text="")
    frame3_photo_label.configure(image=initial_photo)
    frame3_photo_label.image = initial_photo


def choose_file_reg():
    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.tif")])
    frame1_label_path.configure(text=filename)
    display_image_reg(filename)


def display_image_reg(filename):
    global image
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    photo = cv2.resize(image, (300, 300))
    photo = Image.fromarray(photo)
    photo = ImageTk.PhotoImage(photo)

    # Відображення зображення у вікні
    frame1_photo_label.configure(image=photo)
    frame1_photo_label.image = photo


def choose_file_ind():

    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.tif")])
    frame2_label_path.configure(text=filename)
    display_image_ind(filename)


def display_image_ind(filename):
    global image
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    photo = cv2.resize(image, (300, 300))
    photo = Image.fromarray(photo)
    photo = ImageTk.PhotoImage(photo)

    # Відображення зображення у вікні
    frame2_photo_label.configure(image=photo)
    frame2_photo_label.image = photo


def choose_file_aut():
    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.tif")])
    frame3_label_path.configure(text=filename)
    display_image_aut(filename)


def display_image_aut(filename):
    global image
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    photo = cv2.resize(image, (300, 300))
    photo = Image.fromarray(photo)
    photo = ImageTk.PhotoImage(photo)

    # Відображення зображення у вікні
    frame3_photo_label.configure(image=photo)
    frame3_photo_label.image = photo


window = tk.Tk()
window.title("Демонстраційний комплекс")
window.geometry("700x500")

style = ttk.Style()
style.configure("TNotebook", background="white")
style.configure("TNotebook.Tab",
                background="lightgray",
                foreground="black",
                padding=[10, 5],
                font=("Helvetica", 12),
                compound='center',
                width=200)


notebook = ttk.Notebook(window, style="TNotebook")

style.configure("TButton", font=("Helvetica", 12, "bold"))

# Вкладка 1
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text="Навчання системи")

frame1_block = ttk.Frame(frame1)
frame1_block.pack(anchor="w")

# Блок лівої частини елементів
frame1_left_block = ttk.Frame(frame1_block)
frame1_left_block.pack(side="left", padx=(25, 0))

# Текст "Login"
frame1_label_login = ttk.Label(frame1_left_block, text="Login", font=("Helvetica", 12, "bold"))
frame1_label_login.pack(anchor="w")

frame1_entry_login = ttk.Entry(frame1_left_block)
frame1_entry_login.config(width=30, font=("Helvetica", 12))
frame1_entry_login.pack(anchor="w", pady=5)

# Рядок з кнопкою "Обрати" та пустим полем
frame1_file_row = ttk.Frame(frame1_left_block)
frame1_file_row.pack(anchor="w", pady=5)

frame1_button_choose = ttk.Button(frame1_file_row, text="Обрати", command=choose_file_reg)
frame1_button_choose.pack(side="left", )

frame1_label_path = ttk.Label(frame1_file_row, text="", font=("Helvetica", 9, "bold"))
frame1_label_path.pack(side="left", padx=5)

# Кнопка "Підтвердити"
frame1_button_confirm = ttk.Button(frame1_left_block, text="Підтвердити", command=confirm_reg)
frame1_button_confirm.configure(width=30)
frame1_button_confirm.pack(pady=10)

# Місце для фото
frame1_photo_frame = ttk.Frame(frame1_block, width=300, height=300, relief="solid")
frame1_photo_frame.pack(side="left", padx=(50, 0), pady=(50, 0))

initial_image = Image.open("init_image.jpg")
initial_image = initial_image.resize((300, 300))
initial_photo = ImageTk.PhotoImage(initial_image)

frame1_photo_label = ttk.Label(frame1_photo_frame, image=initial_photo)
frame1_photo_label.image = initial_photo
frame1_photo_label.pack()


# Вкладка 2
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text="Ідентифікація")

frame2_block = ttk.Frame(frame2)
frame2_block.pack(anchor="w")

# Блок лівої частини елементів
frame2_left_block = ttk.Frame(frame2_block)
frame2_left_block.pack(side="left", padx=(25, 0))

# Рядок з кнопкою "Обрати" та пустим полем
frame2_file_row = ttk.Frame(frame2_left_block)
frame2_file_row.pack(anchor="w", pady=5)

frame2_button_choose = ttk.Button(frame2_file_row, text="Обрати", command=choose_file_ind)
frame2_button_choose.pack(side="left", )

frame2_label_path = ttk.Label(frame2_file_row, text="", font=("Helvetica", 9, "bold"))
frame2_label_path.pack(side="left", padx=5)

# Кнопка "Підтвердити"
frame2_button_confirm = ttk.Button(frame2_left_block, text="Підтвердити", command=confirm_ind)
frame2_button_confirm.configure(width=30)
frame2_button_confirm.pack(pady=10)

frame2_label_status = ttk.Label(frame2_left_block, text="Статус: ", font=("Helvetica", 12, "bold"))
frame2_label_status.pack(anchor="w", pady=10)

frame2_label_result = ttk.Label(frame2_left_block, text="Результат: ", font=("Helvetica", 12, "bold"))
frame2_label_result.pack(anchor="w", pady=10)

# Місце для фото
frame2_photo_frame = ttk.Frame(frame2_block, width=300, height=300, relief="solid")
frame2_photo_frame.pack(side="left", padx=(50, 0), pady=(50, 0))

frame2_photo_label = ttk.Label(frame2_photo_frame, image=initial_photo)
frame2_photo_label.image = initial_photo
frame2_photo_label.pack()


# Вкладка 3
frame3 = ttk.Frame(notebook)
notebook.add(frame3, text="Автентифікація")

notebook.pack(fill="both", expand=True)

frame3_block = ttk.Frame(frame3)
frame3_block.pack(anchor="w")

# Блок лівої частини елементів
frame3_left_block = ttk.Frame(frame3_block)
frame3_left_block.pack(side="left", padx=(25, 0))

# Текст "Login"
frame3_label_login = ttk.Label(frame3_left_block, text="Login", font=("Helvetica", 12, "bold"))
frame3_label_login.pack(anchor="w")

frame3_entry_login = ttk.Entry(frame3_left_block)
frame3_entry_login.config(width=30, font=("Helvetica", 12))
frame3_entry_login.pack(anchor="w", pady=5)

# Рядок з кнопкою "Обрати" та пустим полем
frame3_file_row = ttk.Frame(frame3_left_block)
frame3_file_row.pack(anchor="w", pady=5)

frame3_button_choose = ttk.Button(frame3_file_row, text="Обрати", command=choose_file_aut)
frame3_button_choose.pack(side="left", )

frame3_label_path = ttk.Label(frame3_file_row, text="", font=("Helvetica", 9, "bold"))
frame3_label_path.pack(side="left", padx=5)

# Кнопка "Підтвердити"
frame3_button_confirm = ttk.Button(frame3_left_block, text="Підтвердити", command=confirm_aut)
frame3_button_confirm.configure(width=30)
frame3_button_confirm.pack(pady=10)

frame3_label_status = ttk.Label(frame3_left_block, text="Статус:", font=("Helvetica", 12, "bold"))
frame3_label_status.pack(anchor="w", pady=10)

frame3_label_result = ttk.Label(frame3_left_block, text="Результат:", font=("Helvetica", 12, "bold"))
frame3_label_result.pack(anchor="w")

# Місце для фото
frame3_photo_frame = ttk.Frame(frame3_block, width=300, height=300, relief="solid")
frame3_photo_frame.pack(side="left", padx=(50, 0), pady=(50, 0))

frame3_photo_label = ttk.Label(frame3_photo_frame, image=initial_photo)
frame3_photo_label.image = initial_photo
frame3_photo_label.pack()


window.mainloop()
