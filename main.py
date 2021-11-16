import math
from typing import SupportsIndex
from PIL import Image, ImageOps
from bezier import bezier_points
from math import radians, sin, cos, pi, atan 
from random import randint, uniform
    
def rotate_curve(curve, angle):
    f = [curve[0]]
    origin = curve[0]
    for p in curve[1:]:

        xt = p[0] - origin[0]
        yt = p[1] - origin[1]

        xr = xt * cos(angle) + yt * sin(angle)
        yr =  xt * sin(angle) + yt* cos(angle)

        f.append((xr + origin[0],
                  yr + origin[1]))
    
    return f

def clear_artifacts(pixels, width, height):
    for y in range(height):
        for x in range(width):
            try:
                if pixels[x, y] == (0, 0, 0):
                    pixels[x, y] = pixels[x + 1, y]
            except:
                if pixels[x, y] == (0, 0, 0):
                    pixels[x, y] = pixels[x - 1, y]
    return pixels

def thicken_curve(curve, t):
    
    f = curve.copy()

    for i in range(len(curve) - 1):
        p1 = curve[i]
        p2 = curve[i + 1]

        fy = float(p2[1] - p1[1])
        fx = float(p2[0] - p1[0])

        slope = fy + 0.00001 / (fx + 0.0001)
        theta =  atan(-1 / slope)

        for j in range(t):
            f.append((int(p1[0] + cos(theta) * j), int(p1[1] + sin(theta) * j)))

    
    return f


def main():
    img = Image.open('tests/test13.jpg')
    img = ImageOps.exif_transpose(img)

    final = Image.new('RGB', img.size, 'black')
    
    img = img.resize((int(img.size[0] * 0.5), int(img.size[1] * 0.5)))
    img = img.resize(final.size)

    i_pixels = img.load()
    f_pixels = final.load()
    
    acc_x = int(final.size[0] * 0.05)
    acc_y = int(final.size[1] * 0.05)

    for y in range(0, final.size[1], 3):
        print(f'{y} / {final.size[1]}')
        for x in range(0, final.size[0], 3):
            color = i_pixels[x, y]
            curve = bezier_points([(x, y), 
                                   (x + (sin(radians(x)) * randint(0, acc_x)), y + (cos(radians(x)) * sin(radians(x)) * randint(0, acc_y))),
                                   (x + randint(0, acc_x), y + randint(0, acc_y)),
                                   (x + (cos(radians(y)) * sin(radians(y)) * randint(0, acc_x)), y + (cos(radians(x)) * sin(radians(x)) * randint(0, acc_y)))], numPoints=75)
            
            curve = rotate_curve(curve, uniform(0, 2*pi))
            curve = thicken_curve(curve, randint(1, 6))

            for p in curve:
                p = (int(p[0]), int(p[1]))
                if p[0] > 0 and p[0] < img.size[0] and p[1] > 0 and p[1] < img.size[1]:
                    f_pixels[p[0], p[1]] = color

    # final = final.resize((final.size[0] // 2, final.size[1] // 2), resample=Image.ANTIALIAS)
    # final.show()
    f_pixels = clear_artifacts(f_pixels, final.size[0], final.size[1])
    final.save('export/final6.jpg')
        

if __name__ == '__main__':
    main()