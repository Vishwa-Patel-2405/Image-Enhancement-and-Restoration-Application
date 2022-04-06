import cv2

def sketch_fun(image):
    grey_img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(grey_img)
    blur = cv2.GaussianBlur(invert,(21,21),15,15)
    blur_invert = cv2.bitwise_not(blur)
    sketch = cv2.divide(grey_img,blur_invert, scale=256.0)

    return sketch

if __name__ == '__main__':
    sketch_fun()