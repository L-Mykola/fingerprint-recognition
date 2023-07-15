# -*- coding: utf-8 -*-
import fingerprint_enhancer

from tools.skeletonization import fingerprint_skeletonization
from tools.minuties_search import calculate_minutiaes
from json_handler import database_load
from tools.comparison_of_minutiae import match


TD = 20
TA = 0.90
TR = 15


def identification(fingerprint_image):
    result = ["user", 0, []]
    skeleton_img = None

    try:
        data = database_load()
    except FileNotFoundError:
        return result, skeleton_img, 0

    enhanced_img = fingerprint_enhancer.enhance_Fingerprint(fingerprint_image)
    skeleton_img = fingerprint_skeletonization(enhanced_img)
    minutiaes = calculate_minutiaes(skeleton_img)

    for key, value in data.items():
        matched = match(value, minutiaes, Td=TD, Ta=TA, Tr=TR)
        k = len(matched) / min(len(minutiaes), len(value)) * 100
        if k > result[1]:
            result[0], result[1], result[2] = key, k, matched

    return result, skeleton_img, 1


