from skimage import io, color, util
import numpy as np
import math

path = 'stimuli/baseImgs/shape01.png'




def rotate_image(img, angle):
    # Convert to LAB and correct format:
    img = img.astype(np.float64) / 255.0
    lab = color.rgb2lab(img)
    x = lab[:, :, 1]
    y = lab[:, :, 2]
    v = np.vstack((x.ravel(), y.ravel()))
    
    # Rotate:
    percent_rotation = angle / 360.0
    theta = 2 * np.pi * percent_rotation
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                [np.sin(theta), np.cos(theta)]])
    vo = rotation_matrix @ v
    
    # Reshape into correct format:
    lab[:, :, 1] = vo[0, :].reshape(img.shape[0], img.shape[1])
    lab[:, :, 2] = vo[1, :].reshape(img.shape[0], img.shape[1])
    
    # Convert back to RGB and scale:
    img = util.img_as_ubyte(color.lab2rgb(lab))
    return img
rgb = io.imread(path)[:,:,:3]



test = rotate_image(rgb, 180)
io.imshow(test)
io.show()