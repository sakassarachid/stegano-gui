import pywt
import cv2
import numpy as np

def embed_dhwt(support_image, secret_image):
    # Perform Haar DWT on the support image
    support_image = cv2.imread(support_image, cv2.IMREAD_GRAYSCALE)
    secret_image = cv2.imread(secret_image, cv2.IMREAD_GRAYSCALE)
    if len(support_image.shape) != 2:
        raise ValueError("Input array 'support_image' must be a two-dimensional array")

    coeffs_support = pywt.dwt2(support_image, 'haar')
    LL_support, (LH_support, HL_support, HH_support) = coeffs_support

    # Perform Haar DWT on the secret image
    coeffs_secret = pywt.dwt2(secret_image, 'haar')
    LL_secret, _ = coeffs_secret

    # Embed the LL coefficients of the secret image into the LL coefficients of the support image
    embedded_LL = LL_support + 0.1 * LL_secret


    # Reconstruct the new coefficients
    embedded_coeffs = (embedded_LL, (LH_support, HL_support, HH_support))
    embedded_image = pywt.idwt2(embedded_coeffs, 'haar')

    # Ensure pixel values are within the valid range [0, 255]
    embedded_image = np.clip(embedded_image, 0, 255)

    # Convert to uint8 for proper image representation
    #embedded_image = embedded_image.astype(np.uint8)
    return embedded_image