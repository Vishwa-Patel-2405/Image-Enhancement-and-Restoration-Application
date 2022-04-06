import cv2

def sharpening_fun(num,image):
    if num == 1:
        new_img1 = sharpening_fun1(image)
        return new_img1
    elif num == 2:
        new_img2 = sharpening_fun2(image)
        return new_img2
    elif num == 3:
        new_img1, new_img2 = sharpening_fun1(image),sharpening_fun2(image)
        return new_img1,new_img2

def sharpening_fun1(image):
    gaussian_blur = cv2.GaussianBlur(image, (15,15), 2)
    sharpened1 = cv2.addWeighted(image,1.5, gaussian_blur, -0.5, 0)
    return sharpened1

def sharpening_fun2(image):
    gaussian_blur = cv2.GaussianBlur(image, (15,15), 2)
    sharpened2 = cv2.addWeighted(image,3.5, gaussian_blur, -2.5, 0)
    return sharpened2