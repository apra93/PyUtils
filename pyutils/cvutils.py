# Image-Centric Helper Functions

import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

################################################################################
#                                Image Operations                              #
################################################################################

def to_uint8(image, mode="clip"):
    """*Correctly* converts an image to uint8 type.
    
    Args:
        image (np.ndarray): Image to be converted to uint8.
    Returns:
        np.ndarray. Converted Image.
        
    Running 'image.astype(np.uint8)' on its own applies a mod(256) to handle
    values over 256. The correct way is to either clip (implemented here) or
    normalize.
    """
    # Make sure the image is a numpy array
    if not isinstance(image, np.ndarray):
        image_array = np.array(image)
    else:
        image_array = np.copy(image)
    # Clip or normalize the image
    if mode.lower() == "clip":
        return cv2.convertScaleAbs(image_array)
    elif mode.lower() == "norm":
        type_min = np.iinfo(image_array.dtype).min
        type_max = np.iinfo(image_array.dtype).max
        return cv2.convertScaleAbs(image_array, alpha=255/(type_max-type_min))
    raise ValueError("Valid modes are 'clip' and 'norm'")

def rolling_average (values, window):
    weights = np.repeat(1.0, window)/window
    return np.convolve(values, weights, 'valid')

def plot_image(image,  msg = ""):
    """
    Plots an image with an optional message.
    """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(image)
    if msg:
        plt.text(0.95, 0.05, msg, ha='right', va='center', color='w',
                transform=ax.transAxes)
    plt.grid()
    plt.show()



################################################################################
#                                   Image I/O                                  #
################################################################################

def get_images_from_dir(target_dir, n_images=None, shuffle=False):
    """Crawls through the contents of inputted directory and saves files with 
    image extensions as images.
    """
    image_ext = set(["bmp", "jpeg", "jpg", "png", "tif", "tiff"])
    dir_files = os.walk(target_dir)
    dir_path, _, file_names = dir_files.next()
    full_path_files = [os.path.join(dir_path, name) for name in file_names]
    images = [cv2.imread(name, cv2.IMREAD_GRAYSCALE) for name in full_path_files
             if os.path.splitext(name)[-1][1:].lower() in image_ext]
    if shuffle:
        random.shuffle(images)
    if n_images:
        images = images[:n_images]
    return images

