import cv2
import numpy as np

def calculate_mse_psnr(original_img, stega_image):
    original_img=cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    mse = np.mean((original_img - stega_image)**2)
    psnr = 10 * np.log10((255**2) / mse)
   # print(' MSE : ' ,mse,'PNSR : ',psnr)
    return mse,psnr

def decimal_to_binary(n):
    binary_representation = format(n, '08b')
    return binary_representation

def embed_secret_message(image, secret, k):
    image=cv2.imread(image)
    secret=cv2.imread(secret)
    if len(image.shape or secret.shape) == 3:  # Check if the image is color
        # Convert color image to grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        secret = cv2.cvtColor(secret, cv2.COLOR_BGR2GRAY)
        secret = cv2.resize(secret, (150, 150))
    # Convert pixel values to binary
    secret = [i for j in secret for i in j]
    secret_to_binary = [decimal_to_binary(i) for i in secret]

    # Concatenate binary values
    secret_concatenated = "".join(secret_to_binary)

    # Divide binary secret into chunks of size k
    secret_chunks = [secret_concatenated[i:i + k] for i in range(0, len(secret_concatenated), k)]

    # Flatten the image pixel values
    image_flattened = [i for j in image for i in j]

    # Embed binary values into image
    image_stega = [i - (i % 2 + int(j)) for (i, j) in zip(image_flattened, secret_chunks)]

    # Handle remaining pixels in image
    rest_of_image = image_flattened[-(len(image_flattened) - len(secret_chunks)):]
    image_stega.extend(rest_of_image)

    # Convert the list to a matrix
    list_to_matrix = [image_stega[i:i + len(image[0])] for i in range(0, len(image_stega), len(image[0]))]
    arr = np.array(list_to_matrix)
    image_stega = cv2.convertScaleAbs(arr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return image_stega

