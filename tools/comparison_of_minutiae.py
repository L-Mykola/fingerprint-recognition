# -*- coding: utf-8 -*-
import numpy as np


def distance(m1, m2):
    return np.sqrt((m1[0] - m2[0])**2 + (m1[1] - m2[1])**2)


def angle(m1, m2):
    a = np.array([m1[0], m1[1]])
    b = np.array([m2[0], m2[1]])
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    acc = dot / (norm_a * norm_b)
    if acc >= 1:
        acc = 0.9999999999999999
    if acc <= -1:
        acc = -0.9999999999999999
    return np.arccos(acc)


def center(points):
    return tuple(np.mean(np.array(points), axis=0))


def match(minutiae1, minutiae2, Td, Ta, Tr):
    # Initialize the list of matched pairs
    matched = []

    # Compute the centers of the minutiae arrays
    coords1 = [m[:2] for m in minutiae1]
    coords2 = [m[:2] for m in minutiae2]
    center1 = center(coords1)
    center2 = center(coords2)

    # Translate the minutiae arrays to the origin
    tminutiae1 = [(m[0]-center1[0], m[1]-center1[1], m[2]) for m in minutiae1]
    tminutiae2 = [(m[0]-center2[0], m[1]-center2[1], m[2]) for m in minutiae2]

    # Iterate over all pairs of minutiae
    for i, m1 in enumerate(tminutiae1):
        for j, m2 in enumerate(tminutiae2):
            # Compute the Euclidean distance and angle between the minutiae
            dist = distance(m1, m2)
            ang = angle(m1, m2)

            # Check if the minutiae match
            if dist < Td and ang < Ta:
                # Compute the score for the match
                score = (Td - dist) / Td + (Ta - ang) / Ta + Tr * (m1[2] == m2[2])

                # Add the match to the list of matches
                matched.append((i, j, score))

    # Sort the matches by score
    matched.sort(key=lambda x: x[2], reverse=True)

    # Initialize sets to keep track of which minutiae have been matched
    used1 = set()
    used2 = set()

    # Iterate over the matches and add them to the list of final matches
    final_matches = []
    for m in matched:
        i, j, score = m
        if i not in used1 and j not in used2:
            final_matches.append((minutiae1[i], minutiae2[j]))
            used1.add(i)
            used2.add(j)

    # Return the list of final matches
    return final_matches




