import numpy as np

CELLS = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]


def apply_to_each_pixel(pixels, f):
    for i in range(0, len(pixels)):
        for j in range(0, len(pixels[i])):
            pixels[i][j] = f(pixels[i][j])


def calculate_minutiaes(skeleton_image):
    height, width = skeleton_image.shape[:2]
    minutiae = []

    apply_to_each_pixel(skeleton_image, lambda x: 1 if x == 255 else 0)

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            values = [skeleton_image[i + k][j + l] for k, l in CELLS]
            values = np.array(values, dtype=np.float64)

            crossings = 0
            for k in range(0, 8):
                crossings += abs(values[k] - values[k + 1])
            crossings /= 2

            if skeleton_image[i][j] == 1:
                if crossings == 1:
                    minutiae.append((i, j, "ending"))

                if crossings == 3:
                    minutiae.append((i, j, "bifurcation"))

    return minutiae

