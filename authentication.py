# -*- coding: utf-8 -*-
import fingerprint_enhancer
import cv2

from tools.skeletonization import fingerprint_skeletonization
from tools.minuties_search import calculate_minutiaes
from json_handler import database_load
from tools.comparison_of_minutiae import match

TD = 20
TA = 0.90
TR = 15


def authorization(username, fingerprint_image):
    benchmark_img = None
    skeleton_img = None
    matched = 0
    k = 0

    try:
        data = database_load()
    except FileNotFoundError:
        return k, benchmark_img, skeleton_img, matched, 0, 1
    if username not in data:
        return k, benchmark_img, skeleton_img, matched, 1, 0


    benchmark_minuties = data[username]

    enhanced_img = fingerprint_enhancer.enhance_Fingerprint(fingerprint_image)
    skeleton_img = fingerprint_skeletonization(enhanced_img)
    minutiaes = calculate_minutiaes(skeleton_img)


    benchmark_img = cv2.imread(f'processed_images/{username}.tif', cv2.IMREAD_GRAYSCALE)

    matched = match(benchmark_minuties, minutiaes, Td=TD, Ta=TA, Tr=TR)
    k = len(matched) / min(len(minutiaes), len(benchmark_minuties)) * 100

    return k, benchmark_img, skeleton_img, matched, 1, 1



