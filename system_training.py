# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import cv2
import fingerprint_enhancer

from tools.skeletonization import fingerprint_skeletonization
from tools.minuties_search import calculate_minutiaes
from json_handler import database_update, database_load
from tools.print_result import print_result_reg


def show_image(img, index):
    tiltle_list = ["Нормалізоване зображення", "Скелетонізоване зображення"]
    fig, ax = plt.subplots()

    # Виведення фото
    ax.imshow(img)
    ax.axis('off')
    ax.set_title(tiltle_list[index])

    plt.show()


def demonstration_and_save_data(username, fingerprint_image):
    try:
        data = database_load()
    except FileNotFoundError:
        pass
    else:
        if username in data:
            return 1

    enhanced_img = fingerprint_enhancer.enhance_Fingerprint(fingerprint_image)
    show_image(enhanced_img, 0)

    skeleton_img = fingerprint_skeletonization(enhanced_img)
    show_image(skeleton_img, 1)

    minutiaes = calculate_minutiaes(skeleton_img)
    database_update(minutiaes, username)
    cv2.imwrite(f'processed_images/{username}.tif', skeleton_img)

    print_result_reg(skeleton_img, minutiaes)

    return 0


