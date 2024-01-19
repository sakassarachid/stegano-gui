import cv2
import numpy as np


def dct_disguise( secret_image,support_image, alpha=0.5):
    # Read images
    support = cv2.imread(support_image)
    secret = cv2.imread(secret_image)

    # Ensure images have the same size
    secret = cv2.resize(support, (support.shape[1], support.shape[0]))

    # Convert images to YCrCb color space
    lena_ycrcb = cv2.cvtColor(support, cv2.COLOR_BGR2YCrCb)
    baboon_ycrcb = cv2.cvtColor(secret, cv2.COLOR_BGR2YCrCb)

    # Split channels
    lena_y, _, _ = cv2.split(lena_ycrcb)
    baboon_y, _, _ = cv2.split(baboon_ycrcb)

    # Divide the Lena image into 8x8 blocks
    height, width = lena_y.shape
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = lena_y[i:i+8, j:j+8]

            # Apply DCT to the block
            block_dct = cv2.dct(np.float32(block))

            # Modify the DCT coefficients using secret image

            block_dct[4:, 4:] = alpha * baboon_y[i:i+4, j:j+4]

            # Apply inverse DCT to the modified block
            modified_block = cv2.idct(np.float32(block_dct))

            # Replace the original block with the modified one
            lena_y[i:i+8, j:j+8] = modified_block

    # Merge the modified Y channel with the Cr and Cb channels
    modified_image_ycrcb = cv2.merge([lena_y, lena_ycrcb[:,:,1], lena_ycrcb[:,:,2]])

    # Convert the modified image back to BGR color space
    modified_image = cv2.cvtColor(modified_image_ycrcb, cv2.COLOR_YCrCb2BGR)

    return modified_image
