import numpy as np
import colorsys
from skimage.color import lab2rgb

outfile = './colors.json'

def lab_angle_to_rgb(angle: float, l: float = 75, c: float = 100) -> tuple:
    """
    Converts an LAB hue angle to an RGB color.

    :param angle: The hue-like angle in LAB color space (in degrees, 0-360).
    :param l: Lightness value (0-100, default: 50 for mid-tone colors).
    :param c: Chroma value (default: 50, controls color saturation).
    :return: Tuple of (R, G, B) values in the range [0, 255].
    """
    # Convert angle to a/b values
    rad = np.radians(angle)
    a = c * np.cos(rad)
    b = c * np.sin(rad)
    
    # Convert LAB to RGB
    lab_color = np.array([[[l, a, b]]], dtype=np.float32)  # Shape for skimage
    rgb_color = lab2rgb(lab_color)[0][0]  # Convert and extract first pixel
    
    # Scale to 0-255 range
    return tuple((rgb_color * 255).astype(int))

with open('colors.json', 'w') as the_file:
    the_file.write('[\n')
    for i in range(359):
        color = lab_angle_to_rgb(i)
        the_file.write('\t[' + str(color[0]) + ', ' + str(color[1]) + ', ' + str(color[2]) + '],\n')
    color = lab_angle_to_rgb((359 - i) % 360)
    the_file.write('\t[' + str(color[0]) + ', ' + str(color[1]) + ', ' + str(color[2]) + ']\n]')
        
    



