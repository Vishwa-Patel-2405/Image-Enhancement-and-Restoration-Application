import tkinter
from tkinter import *
from PIL import ImageTk, Image
from blackandwhite import colorizer_caffe
from sketch import sketch_fun
from BlurOperations import blur_fun
from Sharpening import sharpening_fun
import cv2
from tkinter import filedialog, messagebox
import os
from bg_remover import remover_bg_fun

def common_gui(name):
    common_gui_window = Toplevel(win)
    common_gui_window.grab_set()
    common_gui_window.geometry('690x450')
    common_gui_window.configure(bg='#C8EBE3')
    common_gui_window.title(name)
    common_gui_window.iconbitmap('Window Icon.ico')
    common_gui_window.resizable(0, 0)

    t1 = StringVar()
    w = StringVar()
    h = StringVar()
    perc = StringVar()

    def browseimg():
        global img, fln
        fln = filedialog.askopenfilename(initialdir=os.getcwd(),title='Browse Image File',filetypes=(("JPG Image","*.jpg"),("PNG Image","*.png"),("All Files","*.*")))
        t1.set(fln)
        img = cv2.imread(fln, cv2.IMREAD_UNCHANGED)
        w.set(img.shape[0])
        h.set(img.shape[1])

    def previewimg():
        cv2.imshow("Preview Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    common_gui_wrapper = LabelFrame(common_gui_window, text="Source File", bg="#C8EBE3")
    common_gui_wrapper.pack(fill='both', padx=10, pady=10)

    lbl = Label(common_gui_wrapper, text='Source File', bg='#C8EBE3', font='Bahnschrift 13')
    lbl.pack(side=LEFT, padx=10, pady=10)

    ent = Entry(common_gui_wrapper, textvariable=t1)
    ent.pack(side=LEFT, padx=10, pady=10)

    btn = Button(common_gui_wrapper, text='Browse', command=browseimg, bg='#206C92',
                 font='Courier 11 bold', fg='white', width=16, relief=FLAT, cursor='HAND1')
    btn.pack(side=LEFT, padx=10, pady=10)

    btn2 = Button(common_gui_wrapper, text='Preview', command=previewimg,
                  bg='#206C92', font='Courier 11 bold', fg='white', width=16, relief=FLAT, cursor='HAND1')
    btn2.pack(side=LEFT, padx=10, pady=10)

    var = IntVar()
    def radio_selection():
        selection = "You selected the option " + str(var.get())
        label.config(text=selection)

    if name == 'Colorizer':
        common_gui_wrapper2 = LabelFrame(common_gui_window, text='Actions', bg="#C8EBE3")
        common_gui_wrapper2.pack(fill='both', padx=10, pady=10)

        R1 = Radiobutton(common_gui_wrapper2, text="Colorizer Model 1", variable=var, value=1,
                         command=lambda: radio_selection(), background='#C8EBE3')
        R1.grid(row=0,column=0,padx=20,pady=20)

        R2 = Radiobutton(common_gui_wrapper2, text="Colorizer Model 2", variable=var, value=2,
                         command=lambda: radio_selection(), background='#C8EBE3')
        R2.grid(row=0,column=1,padx=20,pady=20)

        R3 = Radiobutton(common_gui_wrapper2, text="Both", variable=var, value=3,
                         command=lambda: radio_selection(), background='#C8EBE3')
        R3.grid(row=0,column=2,padx=20,pady=20)

        label = Label(common_gui_wrapper2,background='#C8EBE3')
        label.grid(row=0,column=3,padx=20,pady=20)

        btn3 = Button(common_gui_wrapper2, text='Colorize Image', command=lambda: fetch_colorizer(),
                      bg='#206C92', font='Courier 11 bold', fg='white', width=16, relief=FLAT, cursor='HAND1')
        btn3.grid(row=1,column=0,padx=20,pady=20)

        def fetch_colorizer():
            if var.get() == 3:
                global new_img1,new_img2
                new_img1,new_img2 = colorizer_caffe(var.get(), img, fln)
                return new_img1,new_img2
            else:
                global new_img
                new_img = colorizer_caffe(var.get(), img, fln)
                return new_img

    elif name == 'Resizer':
        def recalculate():
            p = int(perc.get())
            new_width = int(int(w.get()) * p / 100)
            new_height = int(int(h.get()) * p / 100)
            w.set(new_width)
            h.set(new_height)

        wrapper2 = LabelFrame(common_gui_window, text="Image Details", bg="#C8EBE3")
        wrapper2.pack(fill='both', padx=10, pady=10)

        lbl2 = Label(wrapper2, text='Dimension', bg='#C8EBE3', font='Bahnschrift 13')
        lbl2.pack(side=LEFT, padx=10, pady=10)

        ent2 = Entry(wrapper2, textvariable=w)
        ent2.pack(side=LEFT, padx=10, pady=10)

        lbl3 = Label(wrapper2, text='X', bg='#C8EBE3', font='Bahnschrift 13')
        lbl3.pack(side=LEFT, padx=5, pady=10)

        ent3 = Entry(wrapper2, textvariable=h)
        ent3.pack(side=LEFT, padx=5, pady=10)

        wrapper4 = LabelFrame(common_gui_window, text='Pixel Safe', bg="#C8EBE3")
        wrapper4.pack(fill='both', expand='yes', padx=10, pady=10)

        lbl4 = Label(wrapper4, text='Percentage', bg='#C8EBE3', font='Bahnschrift 13')
        lbl4.pack(side=LEFT, padx=10, pady=10)

        ent4 = Entry(wrapper4, textvariable=perc)
        ent4.pack(side=LEFT, padx=10, pady=10)

        btn3 = Button(wrapper4, text='Recalculate Dimension', command=recalculate,
                      bg='#206C92', font='Courier 11 bold', fg='white', width=26, relief=FLAT, cursor='HAND1')
        btn3.pack(side=LEFT, padx=10, pady=10)

    elif name == 'Sketch':
        common_gui_wrapper2 = LabelFrame(common_gui_window, text='Actions', bg="#C8EBE3")
        common_gui_wrapper2.pack(fill='both', padx=10, pady=10)

        btn3 = Button(common_gui_wrapper2, text='Make Sketch', command=lambda: fetch_sketch(),
                      bg='#206C92', font='Courier 11 bold', fg='white', width=16, relief=FLAT, cursor='HAND1')
        btn3.grid(row=0, column=0, padx=20, pady=20)

        def fetch_sketch():
            global new_img
            new_img = sketch_fun(img)
            return new_img

    elif name == 'Blur Operations':
        common_gui_wrapper2 = LabelFrame(common_gui_window, text='Actions', bg="#C8EBE3")
        common_gui_wrapper2.pack(fill='both', padx=10, pady=10)

        R1 = Radiobutton(common_gui_wrapper2, text="Gaussian Blur", variable=var, value=1,
                         command=lambda: radio_selection(), background='#C8EBE3')
        R1.grid(row=0,column=0,padx=20,pady=20)

        R2 = Radiobutton(common_gui_wrapper2, text="Median Blur", variable=var, value=2,
                         command=lambda: radio_selection(), background='#C8EBE3')
        R2.grid(row=0,column=1,padx=20,pady=20)

        R3 = Radiobutton(common_gui_wrapper2, text="Both", variable=var, value=3,
                         command=lambda: radio_selection(), background='#C8EBE3')
        R3.grid(row=0, column=2, padx=20, pady=20)

        label = Label(common_gui_wrapper2, background='#C8EBE3')
        label.grid(row=0, column=3, padx=20, pady=20)

        btn3 = Button(common_gui_wrapper2, text='Blur operations', command=lambda: fetch_blur(),
                      bg='#206C92', font='Courier 11 bold', fg='white', width=16, relief=FLAT, cursor='HAND1')
        btn3.grid(row=1, column=0, padx=20, pady=20)

        def fetch_blur():
            if var.get() == 3:
                global new_img1, new_img2
                new_img1, new_img2 = blur_fun(var.get(),img)
                return new_img1, new_img2
            else:
                global new_img
                new_img = blur_fun(var.get(),img)
                return new_img

    elif name == 'Background Remover':
        common_gui_wrapper2 = LabelFrame(common_gui_window, text='Actions', bg="#C8EBE3")
        common_gui_wrapper2.pack(fill='both', padx=10, pady=10)

        btn3 = Button(common_gui_wrapper2, text='Background Remover', command=lambda: fetch_bg_remover(),
                      bg='#206C92', font='Courier 11 bold', fg='white', width=20, relief=FLAT, cursor='HAND1')
        btn3.grid(row=0, column=0, padx=30, pady=20)

        def fetch_bg_remover():
            global new_img
            new_img = remover_bg_fun(fln)
            return new_img

    elif name == 'Image Sharpner':
        common_gui_wrapper2 = LabelFrame(common_gui_window, text='Actions', bg="#C8EBE3")
        common_gui_wrapper2.pack(fill='both', padx=10, pady=10)

        R1 = Radiobutton(common_gui_wrapper2, text="Level 1", variable=var, value=1,
                         command=lambda: radio_selection(), background='#C8EBE3')
        R1.grid(row=0, column=0, padx=20, pady=20)

        R2 = Radiobutton(common_gui_wrapper2, text="Level 2", variable=var, value=2,
                         command=lambda: radio_selection(), background='#C8EBE3')
        R2.grid(row=0, column=1, padx=20, pady=20)

        R3 = Radiobutton(common_gui_wrapper2, text="Both", variable=var, value=3,
                         command=lambda: radio_selection(), background='#C8EBE3')
        R3.grid(row=0, column=2, padx=20, pady=20)

        label = Label(common_gui_wrapper2, background='#C8EBE3')
        label.grid(row=0, column=3, padx=20, pady=20)

        btn3 = Button(common_gui_wrapper2, text='Image Sharpner', command=lambda: fetch_sharpner(),
                      bg='#206C92', font='Courier 11 bold', fg='white', width=20, relief=FLAT, cursor='HAND1')
        btn3.grid(row=1, column=0, padx=20, pady=20)

        def fetch_sharpner():
            if var.get() == 3:
                global new_img1, new_img2
                new_img1, new_img2 = sharpening_fun(var.get(), img)
                return new_img1, new_img2
            else:
                global new_img
                new_img = sharpening_fun(var.get(), img)
                return new_img

    def preview_img():
        if name == 'Resizer':
            nw = int(w.get())
            nh = int(h.get())
            resized_img = cv2.resize(img,(nw,nh),interpolation=cv2.INTER_AREA)
            cv2.imshow("Resized Image", resized_img)
        elif (name == 'Colorizer' or 'Blur Operations' or 'Image Sharpner') and (var.get() == 3):
            cv2.imshow(f'{name} 1', new_img1)
            cv2.imshow(f'{name} 2', new_img2)
        else:
            cv2.imshow(f'{name} Image',new_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def compare_image():
        if name == 'Resizer':
            nw = int(w.get())
            nh = int(h.get())
            resized_img = cv2.resize(img,(nw,nh),interpolation=cv2.INTER_AREA)
            cv2.imshow("Resized Image", resized_img)
            cv2.imshow('Original Image', img)
        elif (name == 'Colorizer' or 'Blur Operations' or 'Image Sharpner') and (var.get() == 3):
            cv2.imshow(f'{name} 1',new_img1)
            cv2.imshow(f'{name} 2',new_img2)
            cv2.imshow('Original Image', img)
        else:
            cv2.imshow(f'{name} Image',new_img)
            cv2.imshow('Original Image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_img():
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Save Image', defaultextension='.png',
                                           filetypes=(("JPG Image", "*.jpg"), ("PNG Image", "*.png"), ("All Files", "*.*")))
        if name == 'Resizer':
            nw = int(w.get())
            nh = int(h.get())
            resized_img = cv2.resize(img,(nw,nh),interpolation=cv2.INTER_AREA)
            cv2.imwrite(fln, resized_img)
        elif (name == 'Colorizer' or 'Blur Operations' or 'Image Sharpner') and (var.get() == 3):
            fln1 = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Save Image 2', defaultextension='.png',
                                                filetypes=(("JPG Image", "*.jpg"), ("PNG Image", "*.png"), ("All Files", "*.*")))

            cv2.imwrite(fln,new_img1)
            cv2.imwrite(fln1,new_img2)
        else:
            cv2.imwrite(fln,new_img)
        messagebox.showinfo("Image saved","Image has been saved successfully!")

    wrapper5 = LabelFrame(common_gui_window, text='View & Save Operation', bg="#C8EBE3")
    wrapper5.pack(fill='both', expand='yes', padx=10, pady=10)

    prvbtn = Button(wrapper5, text='Preview', command=preview_img,
                    bg='#206C92', font='Courier 11 bold', fg='white', width=15, relief=FLAT, cursor='HAND1')
    prvbtn.pack(side=LEFT, padx=10, pady=10)

    if name == 'Background Remover':
        pass
    else:
        savebtn = Button(wrapper5, text='Save', command=save_img,
                         bg='#206C92', font='Courier 11 bold', fg='white', width=15, relief=FLAT, cursor='HAND1')
        savebtn.pack(side=LEFT, padx=10, pady=10)

    compare_btn = Button(wrapper5, text='Compare Images', command=compare_image,
                     bg='#206C92', font='Courier 11 bold', fg='white', width=15, relief=FLAT, cursor='HAND1')
    compare_btn.pack(side=LEFT, padx=10, pady=10)

    common_gui_window.mainloop()


def help_gui():
    help_gui_window = Toplevel(win)
    help_gui_window.grab_set()
    help_gui_window.geometry('770x700')
    help_gui_window.configure(bg='#C8EBE3')
    help_gui_window.title('User Manual')
    help_gui_window.iconbitmap('Window Icon.ico')
    help_gui_window.resizable(0, 0)


    help_wrapper = LabelFrame(help_gui_window, text="Enhancement Tools", bg="#C8EBE3", width=770,height=400)
    help_wrapper_1 = LabelFrame(help_wrapper, text="Sketch", bg="#C8EBE3", width=750,height=50)
    help_wrapper_2 = LabelFrame(help_wrapper, text="Smoothing", bg="#C8EBE3", width=750,height=50)
    help_wrapper_3 = LabelFrame(help_wrapper, text="Resizer", bg="#C8EBE3", width=750,height=50)
    help_wrapper_4 = LabelFrame(help_wrapper, text="Sharpning", bg="#C8EBE3", width=750,height=50)
    help_wrapper_1.grid(row=0,column=0,padx=10, pady=10)
    help_wrapper_2.grid(row=1,column=0,padx=10, pady=10)
    help_wrapper_3.grid(row=2,column=0,padx=10, pady=10)
    help_wrapper_4.grid(row=3,column=0,padx=10, pady=10)
    help_wrapper.pack(padx=10, pady=10, fill='both')
    help_wrapper2 = LabelFrame(help_gui_window, text="Restoration Tools", bg="#C8EBE3", width=800)
    help_wrapper_2_1 = LabelFrame(help_wrapper2, text="Image Colorization", bg="#C8EBE3", width=750, height=50)
    help_wrapper_2_2 = LabelFrame(help_wrapper2, text="Background Remover", bg="#C8EBE3", width=750, height=50)
    help_wrapper_2_1.grid(row=0, column=0, padx=10, pady=10)
    help_wrapper_2_2.grid(row=1, column=0, padx=10, pady=10)
    help_wrapper2.pack(padx=10, pady=10, fill='both')


    lbl1 = Label(help_wrapper_1, text='IERA provides the best sketch tool to its users. Here, user can select any '
                                      'image from the device and then he/she can make the sketch\nout of the input '
                                      'image. User will select an image then several operations will be performed '
                                      'on the image such as conversion from\nBGR > Gray-scale, Inversion all so on. '
                                      'Lastly, the final output will be the sketch of the input image.', bg="#C8EBE3",justify= LEFT)
    lbl1.grid(padx=10, pady=10)
    lbl2 = Label(help_wrapper_2, text='This application provides the best smoothing tool to its users. Here, user can select any '
                                      'image from the device and then he/she can  \nsmooth the imagefrom the provided input.'
                                      'User will select an image then several operations will be performed '
                                      'on\nthe image to remove theunwanted noise from the image.'
                                      'Lastly, the final output will be the smoothing version of the input image.', bg="#C8EBE3",
                 justify=LEFT)
    lbl2.grid(padx=10, pady=10)
    lbl3 = Label(help_wrapper_3, text='IERA offers the best image resizer tool to its users. Here, user can select any '
                                      'images from the device and then he/she can resize the    \nimage according '
                                      'to their requirement. User will select an image then several operations '
                                      'will be performed on the image such as\nrecalculating the pixels by percentage'
                                      'and giving manual pixel values of an image. Hence, the output will be the '
                                      'resized image with\nlow size and it will not affect the image quality.', bg="#C8EBE3",
                 justify=LEFT)
    lbl3.grid(padx=10, pady=10)
    lbl4 = Label(help_wrapper_4, text='This application has one of the best sharpning feature. User can select any '
                                      'images from the device and then he/she can sharp the \ninput image to enhance the'
                                      'hidden details of any image. User will select an image then several operations will be performed'
                                      'on the    \nimage, and Lastly, the final outout will be the sketch of the input image.', bg="#C8EBE3",
                 justify=LEFT)
    lbl4.grid(padx=10, pady=10)

    lbl5 = Label(help_wrapper_2_1, text='This application has one of the best image colorizing tools. Users have an option to select the'
                                        'appropriate colorizing model, then he/\nshe can colorize the gray-scale or black & white image to convert it'
                                        'into the colored image.',bg="#C8EBE3", justify=LEFT)
    lbl5.grid(padx=10, pady=5)

    lbl6 = Label(help_wrapper_2_2, text='IERA has powerful image segmentation feature to extract the particular '
                                        'segment from the image such as any human object.              ',
                 bg="#C8EBE3",
                 justify=LEFT)
    lbl6.grid(padx=10, pady=10)
    help_gui_window.mainloop()


def about_gui():
    about_gui = Toplevel(win)
    about_gui.grab_set()
    about_gui.geometry('450x450')
    about_gui.configure(bg='#C8EBE3')
    about_gui.title('About IERA')
    about_gui.iconbitmap('Window Icon.ico')
    about_gui.resizable(0, 0)

    about_wrapper = LabelFrame(about_gui, text="About", bg="#C8EBE3", width=400, height=400)
    about_wrapper.pack(padx=10, pady=10, fill='both')

    logo = Image.open("TOP FRAME LOGO.png")
    resized_image = logo.resize((250, 140), Image.ANTIALIAS)
    new_image = ImageTk.PhotoImage(resized_image)
    test = ImageTk.PhotoImage(resized_image)
    image_label = tkinter.Label(about_wrapper, image=test)
    image_label.image = test
    image_label.grid(row=0, column=0, padx=85, pady=10)
    headline = Label(about_wrapper, text="The Best Image Enhancement and Restoration App", bg='#C8EBE3',font ='Bahnschrift 13')\
        .grid(row=1, column=0, padx=5, pady=10)
    headline1 = Label(about_wrapper, text="IERA - 2022.2.14 (Free Edition)", bg='#C8EBE3',
                     font='Fixedsys 13').grid(row=2, column=0, padx=5, pady=10)
    headline2 = Label(about_wrapper, text=":::: Developers ::::", bg='#C8EBE3',
                      font='Bahnschrift  14').grid(row=3, column=0, padx=5, pady=10)
    developers = Label(about_wrapper, text="Vishwa Patel, Yash Sanghani\nVasu Makwana, Shaswat Doshi", bg='#C8EBE3',
                     font='Bahnschrift 11').grid(row=4, column=0, padx=5, pady=10)
    copyright_label = Label(about_wrapper, text="Copyright © 2022-2023 IERA", bg='#C8EBE3',
                       font='Bahnschrift 10').grid(row=6, column=0, padx=5, pady=10)

    about_gui.mainloop()


#Main window code
win = Tk()
win.geometry('845x700')
win.configure(bg='#C8EBE3')
win.title('IERA - Image Enhancement and Restoration Application')
win.iconbitmap('Window Icon.ico')
win.resizable(0,0)


menubar = Menu(win)
enhancement_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Enhancement", menu=enhancement_menu)

enhancement_menu.add_command(label="Make Sketch", command=lambda: common_gui('Sketch'))
enhancement_menu.add_command(label="Smooth Image", command=lambda: common_gui('Blur Operations'))
enhancement_menu.add_command(label="Image Resizer", command=lambda: common_gui('Resizer'))
enhancement_menu.add_command(label="Sharpen Image", command=lambda: common_gui('Image Sharpner'))
enhancement_menu.add_separator()
enhancement_menu.add_command(label="Exit", command=win.quit)



restoration_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Restoration", menu=restoration_menu)

restoration_menu.add_command(label="Colorizer", command=lambda: common_gui('Colorizer'))
restoration_menu.add_command(label="Background Remover", command=lambda: common_gui('Background Remover'))


helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="User Manual", command=help_gui)
helpmenu.add_command(label="About IERA", command=about_gui)
menubar.add_cascade(label="Help", menu=helpmenu)

wrapper = LabelFrame(win, text = "IERA", bg="#C8EBE3", width=845, height=50)
wrapper2 = LabelFrame(win,text = "Enhancement Tools",bg="#C8EBE3")
wrapper.pack(padx=10,pady=10,fill='both')
wrapper2.pack(padx=10,pady=10,fill='both')
wrapper3 = LabelFrame(wrapper2,text = "Sketch Image",bg="#C8EBE3")
wrapper4 = LabelFrame(wrapper2,text = "Smooth Image",bg="#C8EBE3")
wrapper5 = LabelFrame(wrapper2,text = "Resize Image",bg="#C8EBE3")
wrapper9 = LabelFrame(wrapper2,text = "Sharpen Image",bg="#C8EBE3")
wrapper3.grid(row=0,column=0,padx=20,pady=20)
wrapper4.grid(row=0,column=1,padx=10,pady=20)
wrapper5.grid(row=0,column=2,padx=10,pady=20)
wrapper9.grid(row=0,column=3,padx=10,pady=20)

wrapper6 = LabelFrame(win,text = "Restoration Tools",bg="#C8EBE3")
wrapper6.pack(padx=10,pady=10)
wrapper7 = LabelFrame(wrapper6,text = "Image Colorizer",bg="#C8EBE3")
wrapper8 = LabelFrame(wrapper6,text = "Background Remover",bg="#C8EBE3")
wrapper7.pack(padx=20,pady=10,fill='both')
wrapper8.pack(padx=20,pady=20,fill='both')

wrapper10 = LabelFrame(win,text = "Copyright",bg="#C8EBE3")
wrapper10.pack(padx=10,pady=10,fill='both')


#wrappe1 components
logo = Image.open("TOP FRAME LOGO.png")
resized_image = logo.resize((250,140), Image.ANTIALIAS)
new_image = ImageTk.PhotoImage(resized_image)
test = ImageTk.PhotoImage(resized_image)
image_label = tkinter.Label(wrapper,image = test)
image_label.image = test
image_label.grid(row=0,column=0,padx=10,pady=10)
headline = Label(wrapper,text="The Best Image Enhancement and Restoration App",bg='#C8EBE3',font='Bahnschrift 17').grid(row=0,column=1,padx=5,pady=10)

#wrappe2_1 components
btn2 = Button(wrapper3,text='Make Sketch',bg='#206C92',
              command=lambda: common_gui('Sketch'),font='Courier 11 bold',fg='white',width=16,relief = FLAT)
btn2.grid(row=0,column=1,padx = 10,pady=10)

#wrappe2_2 components
btn3 = Button(wrapper4,text='Smooth Image',bg='#206C92',
              command=lambda: common_gui('Blur Operations'),font='Courier 11 bold',fg='white',width=16,relief = FLAT)
btn3.grid(row=0,column=2,padx = 10,pady=10)

#wrappe2_3 components
btn4 = Button(wrapper9,text='Sharpen Image',bg='#206C92',
              command=lambda: common_gui('Image Sharpner'),font='Courier 11 bold',fg='white',width=16,relief = FLAT)
btn4.grid(row=0,column=3,padx = 10,pady=10)


#wrappe2_4 components
btn7 = Button(wrapper5,text='Image Resizer',bg='#206C92',
              command=lambda: common_gui('Resizer'),font='Courier 11 bold',fg='white',width=16,relief = FLAT)
btn7.grid(row=0,column=4,padx = 10,pady=10)


#wrappe3_1 components
lbl5 = Label(wrapper7,text = 'Colorize any black and white image using our powerful colorizer',bg="#C8EBE3",font='Bahnschrift 12')
lbl5.grid(row=0,column=0,padx=10,pady=10)
btn5 = Button(wrapper7,text='Colorize Image',bg='#206C92',
              command=lambda: common_gui('Colorizer'),font='Courier 11 bold',fg='white',width=16,relief = FLAT)
btn5.grid(row=0,column=1,padx = 81,pady=10)

#wrappe3_2 components
lbl6 = Label(wrapper8,text = 'Remove background by the most powerful bg remover',bg="#C8EBE3",font='Bahnschrift 12')
lbl6.grid(row=1,column=0,padx=10,pady=10)
btn6 = Button(wrapper8,text='Remove BG',bg='#206C92',
              command=lambda: common_gui('Background Remover'),font='Courier 11 bold',fg='white',width=16,relief = FLAT)
btn6.grid(row=1,column=1,padx =153,pady=10)

#Wrapper10 components
lbl10 = Label(wrapper10,text = '© All Rights Reserved - IERA',bg="#C8EBE3",font='Bahnschrift 12')
lbl10.grid(row=0,column=0,padx=10,pady=10)
btn10 = Button(wrapper10,text='Exit',bg='#206C92',
               command=win.destroy,font='Courier 11 bold',fg='white',width=16,relief = FLAT)
btn10.grid(row=0,column=1,padx =363,pady=10)

win.config(menu=menubar)
win.mainloop()