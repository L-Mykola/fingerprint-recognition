# -*- coding: utf-8 -*-

import numpy as np
from skimage.morphology import skeletonize


def fingerprint_skeletonization(sample):
    skeleton = skeletonize(sample / 255)
    skeleton = (skeleton * 255).astype(np.uint8)

    return skeleton

