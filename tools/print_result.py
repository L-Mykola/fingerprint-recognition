# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext


def print_result_comparison(image1, image2, matched_minuties):
    root = tk.Tk()
    root.title("Мінуції")

    fig, (ax1, ax2) = plt.subplots(1, 2)

    list1 = [item[0] for item in matched_minuties]
    list2 = [item[1] for item in matched_minuties]


    ax1.imshow(image1)
    for minutias in matched_minuties:
        min1, min2 = minutias
        x, y, minutia_type = min1
        ax1.plot(y, x, marker='o', markersize=5, color="g")

    ax1.axis('off')
    ax1.set_title('Еталоний шаблон')

    ax2.imshow(image2)
    for minutias in matched_minuties:
        min1, min2 = minutias
        x, y, minutia_type = min2
        ax2.plot(y, x, marker='o', markersize=5, color='g')

    ax2.axis('off')
    ax2.set_title('Контрольний шаблон')

    fig.suptitle('Результат порівняння')

    label1 = tk.Label(root, text="Еталоний шаблон", font=("Helvetica", 12))
    label1.grid(row=0, column=0)

    label2 = tk.Label(root, text="Контрольний шаблон", font=("Helvetica", 12))
    label2.grid(row=0, column=1)


    # Область з прокруткою для списку 1
    scroll_text1 = scrolledtext.ScrolledText(root, width=40, height=10)
    scroll_text1.grid(row=1, column=0)
    scroll_text1.insert(tk.END, "\n".join(str(item) for item in list1))

    # Область з прокруткою для списку 2
    scroll_text2 = scrolledtext.ScrolledText(root, width=40, height=10)
    scroll_text2.grid(row=1, column=1)
    scroll_text2.insert(tk.END, "\n".join(str(item) for item in list2))

    plt.show()
    # Запуск головного циклу tkinter
    return 0


def print_result_reg(img, minutiaes):
    root = tk.Tk()
    root.title("Мінуції")
    fig, ax = plt.subplots()

    ax.imshow(img)
    for minutia in minutiaes:
        x, y, _ = minutia
        ax.plot(y, x, marker='o', markersize=5, color='g')

    plt.axis('off')  # вимкнути вісі
    ax.set_title("Відображення мінуцій")

    # Створення області з прокруткою
    scroll_text = scrolledtext.ScrolledText(root, width=40, height=10)
    scroll_text.pack()

    # Додавання списку у область з прокруткою
    scroll_text.insert(tk.END, "\n".join(str(item) for item in minutiaes))

    plt.show()
    # Запуск головного циклу tkinter
    return 0
