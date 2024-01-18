import cv2
import numpy as np
import math


def calculate_smoothness(diff):
    thresholds = [8, 16, 32, 64, 128, 255]
    classes = [0, 1, 2, 3, 4, 5]
    bit_counts = [3, 3, 4, 5, 6, 7]

    for threshold, smooth_class, bit_count in zip(thresholds, classes, bit_counts):
        if diff < threshold:
            return smooth_class, bit_count
        return classes[-1], bit_counts[-1]


def calculate_d_prime(differences, smoothness_classes, bit_counts, bit_stream):
    d_prime_matrix = []

    for i, row_diff in enumerate(differences):
        row_d_prime = []
        bit_index = 0

        for j, di in enumerate(row_diff):
            smoothness_class = smoothness_classes[i][j]
            ti = bit_counts[i][j]

            lj = 0 if smoothness_class == 0 else 2 * (smoothness_class - 1) * (2 ** 3)
            uj = 7 if smoothness_class == 0 else 2 * lj - 1

            bi_binary = bit_stream[bit_index:bit_index + ti]
            bit_index += ti
            bi = int(bi_binary, 2) if bi_binary else 0

            d_prime = abs(lj + bi)
            row_d_prime.append(d_prime)

        d_prime_matrix.append(row_d_prime)

    return d_prime_matrix


def calculate_m(differences, d_prime_matrix):
    m_matrix = []

    for i, row_diff in enumerate(differences):
        row_m = []

        for j, di in enumerate(row_diff):
            d_prime = d_prime_matrix[i][j]
            m = abs(d_prime - di)
            row_m.append(m)

        m_matrix.append(row_m)

    return m_matrix


def generate_stego_image(image, m_matrix, differences):
    stego_image = []

    for i, row_image in enumerate(image):
        row_stego = []

        for j in range(0, len(row_image), 2):
            pi = row_image[j]
            m = m_matrix[i][j // 2]
            di = differences[i][j // 2]

            if di % 2 == 0:
                p_prime_i = pi - math.ceil(m / 2)
                p_prime_i_plus_1 = pi + math.floor(m / 2)
            else:
                p_prime_i = pi + math.ceil(m / 2)
                p_prime_i_plus_1 = pi - math.floor(m / 2)

            row_stego.extend([p_prime_i, p_prime_i_plus_1])

        stego_image.append(row_stego)

    return np.array(stego_image, dtype=np.uint8)


def apply_diff(secret_image, support_image):
    original_image = cv2.imread(support_image)
    secret_image = cv2.imread(secret_image)
    image = np.array(original_image)
    pixel_values_flat = secret_image.flatten()
    bit_stream = ''.join(['{0:08b}'.format(pixel) for pixel in pixel_values_flat])

    # Display the new differences for the secret message
    differences = []  # New list to store differences
    smoothness_classes = []  # New list to store the "smoothness" classes
    bit_counts = []  # New list to store the number of bits for each difference

    # Populate differences, smoothness_classes, and bit_counts
    for ligne in image:
        row_diff = []
        row_classes = []
        row_bit_counts = []

        for i in range(0, len(ligne) - 1, 2):
            diff = abs(int(ligne[i][0]) - int(ligne[i + 1][0]))

            row_diff.append(diff)

            # Determine the "smoothness" class and the number of bits for each difference
            smooth_class, bit_count = calculate_smoothness(diff)
            row_classes.append(smooth_class)
            row_bit_counts.append(bit_count)

        differences.append(row_diff)
        smoothness_classes.append(row_classes)
        bit_counts.append(row_bit_counts)

    # Calculate the d' matrix
    d_prime_matrix = calculate_d_prime(differences, smoothness_classes, bit_counts, bit_stream)

    # Calculate the m matrix
    m_matrix = calculate_m(differences, d_prime_matrix)

    # Generate the stego image
    stego_image = generate_stego_image(image, m_matrix, differences)

    return stego_image