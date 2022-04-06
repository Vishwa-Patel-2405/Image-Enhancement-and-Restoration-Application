# Image Enhancement and Restoration Application (IERA)
- Developed a desktop software for enhancing the images and restoring the degraded images. Used NumPy, Tkinter for GUI, PIL and OpenCV for image processing. Provided various features of image processing such as grey-scale image colorizing, segmentation, sharpening, image denoising, low light enhancement, and super-resolution with Generative Adversarial Networks.
- Used deep learning to create a model, that converts RGB image to LAB colour space, which is capable to predict the AB channels from the given L channel of an input image.
- Lastly, the L and predicted AB channels are combined and form a resultant colorized image with LAB colour space, which is then transformed into RGB colour space.
- Image segmentation is used to remove background from any image, and for that DeepLabV3+ model was used to perform semantic segmentation. Achieved over 96.7% accuracy for all the features in this software.
