from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from skimage import exposure
from PIL import ImageTk, Image
from tkinter import messagebox
from screeninfo import get_monitors


import numpy as np
import cv2


# FUNCTIONS
def monitor_resolution():
    # GET INFO ABOUT MONITOR RESOLUTION
    monitors = get_monitors()
    str_first_mon = str(monitors[0])
    list_mon = str_first_mon.split(",")
    mon_width = list_mon[2]
    mon_height = list_mon[3]
    # mon_width = 'width=1280'
    # mon_height = 'height=720'

    splitted_w = mon_width.split("=")
    monitor_width = int(splitted_w[-1])

    splitted_h = mon_height.split("=")
    monitor_length = int(splitted_h[-1])

    app_width = str((monitor_width * 0.65) + 10) # WIDTH APP
    app_height = str((monitor_length * 0.75) + 10) # HEIGHT APP

    kk = app_width.split(".")
    ii = app_height.split(".")

    geom = kk[0] + 'x' + ii[0]

    square_side = int(ii[0])
    btns_width = (int(kk[0]) - int(ii[0])) / 2
    btns_height = int(ii[0]) / 25
    w_app = int(monitor_width * 0.65) + 10
    h_app = int(monitor_length * 0.75) + 10
    space = btns_height / 8
    fontt = 14

    return w_app, h_app, btns_width, btns_height, square_side, geom, space, fontt


def create_red_line():
    mat = np.zeros((3, 120))
    indices = mat == 0
    mat[indices] = 255
    r = mat
    g = np.zeros((3, 120))
    b = np.zeros((3, 120))
    red_line = cv2.merge((r, g, b))

    return red_line


def segment_logo():
    logo = 'CEITEC_CTLAB_zelena.jpg'
    image = cv2.imread(logo)
    (b, g, r) = cv2.split(image)
    indices_b = b > 220
    indices_g = g > 220
    indices_r = r > 220
    b[indices_b] = 0
    g[indices_g] = 0
    r[indices_r] = 0
    log_arr = cv2.merge((r, g, b))
    img_log = Image.fromarray(log_arr)
    [width_log, height_log] = img_log.size

    return img_log, width_log, height_log

# TAKE INFO ABOUT MONITOR RESOLUTION
[w_app, h_app, btns_width, btns_height, square_side, geom, space, fontt] = monitor_resolution()

# other parameters
global line
line = 10
w_app_def = w_app
h_app_def = h_app
w_app_start = w_app
h_app_start = h_app
w_app_max = w_app_def / 0.65
h_app_max = h_app_def / 0.75
log_wid = int(w_app_def / 4.5)
log_hei = int(h_app / 11.5)
global work_square_w, work_square_h
work_square_w = int((w_app_def - 10) - (btns_width * 2))
work_square_h = int((w_app_def - 10) - (btns_width * 2))


window = Tk()
window.title("CT app")
window.geometry(geom)
window.resizable(True, True)
window.iconbitmap('icon.ico')

# LOGICKE
logo_on = False
scale_on = False
opened = False
hist_on = False
roi_on = False
vxl_on = False
crop_on = False
crop_byl = False

# Create red line
red_line = create_red_line()

# Segment logo
[img_log, width_log, height_log] = segment_logo()

# Scale image
sc = "scale_white.png"
open_sc = Image.open(sc)

# Other variables
var_md = IntVar()
var_cr = IntVar()


# FUNKCI
def save_pct():
    y = filedialog.asksaveasfilename(title="Save file", defaultextension=".tif",
                                     filetypes=(("tif file", "*.tif"), ("png file", "*.png"), ("All Files", "*.*")))

    global x_canv_press, y_canv_press, x_canv_rel, y_canv_rel, line

    if logo_on:
        background = Image.new('RGBA', (work_square_w + line, work_square_h + log_hei + line), (0, 0, 0, 255))
        offset_2 = (coor_x - log_wid, coor_y - log_hei)
        background.paste(img_log, offset_2)
    else:
        background = Image.new('RGBA', (work_square_w + line, work_square_h + line), (0, 0, 0, 255))

    if opened:
        offset = (0, 0)
        background.paste(img3, offset)
    if scale_on:
        offset_1 = (posx, posy)
        background.paste(img_sc, offset_1)
    if roi_on:
        offset_3 = (new_width + line, 0)
        background.paste(roi_img, offset_3)

        if x_canv_press > x_canv_rel:
            [x_canv_press, x_canv_rel] = [x_canv_rel, x_canv_press]
        if y_canv_press > y_canv_rel:
            [y_canv_press, y_canv_rel] = [y_canv_rel, y_canv_press]

        rect_wid = abs(x_canv_press - x_canv_rel)
        rect_hei = abs(y_canv_press - y_canv_rel)

        if color == "red":
            j = 255
            k = 0
            l =  0
        elif color == "blue":
            j = 0
            k = 0
            l =  255
        elif color == "green":
            j = 0
            k = 255
            l =  0
        elif color == "yellow":
            j = 255
            k = 255
            l =  0
        elif color == "orange":
            j = 255
            k = 165
            l =  0
        # CREATE RECTANGULAR IN PICTURE
        cvet = (j,k,l)
        red_line_w_1 = Image.new('RGB', (rect_wid, 3), cvet)
        red_line_h_1 = Image.new('RGB', (3, rect_hei), cvet)
        red_line_h_2 = Image.new('RGB', (3, rect_hei + 3), cvet)

        background.paste(red_line_w_1, (x_canv_press, y_canv_press))
        background.paste(red_line_w_1, (x_canv_press, y_canv_rel))
        background.paste(red_line_h_1, (x_canv_press, y_canv_press))
        background.paste(red_line_h_2, (x_canv_rel, y_canv_press))

        # CREATE RECTANGULAR NEAR ROI
        red_line_wr_1 = Image.new('RGB', (roi_n_wid, 3), cvet)
        red_line_hr_1 = Image.new('RGB', (3, roi_n_height), cvet)
        red_line_hr_2 = Image.new('RGB', (3, roi_n_height + 3), cvet)

        background.paste(red_line_wr_1, (new_width + line, 0))
        background.paste(red_line_wr_1, (new_width + line, roi_n_height))
        background.paste(red_line_hr_1, (new_width + line, 0))
        background.paste(red_line_hr_2, (new_width + line + roi_n_wid, 0))


    # SAVE PARAMETERS IN .TXT
    name_txt = y[0:-4] + '.txt'

    if logo_on:
        pic_size = "Picture size: " + str(work_square_w + line) + "x" + str(work_square_h + line + log_hei)
    else:
        pic_size = "Picture size: " + str(work_square_w + line) + "x" + str(work_square_h + line)

    hist_low = "Histogram lower value: " + str(lower_limit)
    hist_up = "Histogram upper value: " + str(upper_limit)

    if vxl_on:
        vxl_str = "Voxel size: " + n + " " + str(voxel_unit_1)
    else:
        vxl_str = "Voxel size: " + "NO INFO"

    if scale_entry_var:
        image_scale = "Real width of the scale: " + p + " " + scale_size_1
        if roi_on:
            roi_scale_str = "Real width of the ROI: " + str(det_scl) + " " + str(voxel_unit_1)
        else:
            roi_scale_str = "Real width of the ROI: " + "NO INFO"
    else:
        image_scale = "Real width of the scale: " + "NO INFO"
        roi_scale_str = "Real width of the ROI: " + "NO INFO"

    if roi_on:
        zoom_detail_str = "Zoom of the detail: " + "X" + str(det_zoom)
    else:
        zoom_detail_str = "Zoom of the detail: " + "NO INFO"

    stroky = [pic_size, hist_low, hist_up, vxl_str, image_scale, roi_scale_str, zoom_detail_str]

    with open(name_txt, 'w', encoding="utf-8") as f:
        for stroka in stroky:
            f.write(stroka)
            f.write('\n')

    background.save(y)


def scl_pos_x(event):
    global posx
    posx = scale_pos_x.get()
    if scale_on:
        insert_scale()
    if logo_on:
        insert_logo()


def scl_pos_y(event):
    global posy
    posy = scale_pos_y.get()
    if scale_on:
        insert_scale()
    if logo_on:
        insert_logo()


def change_low_hist(event):
    global lower_limit
    lower_limit = scale.get()

    if opened:
        global img_ct, img_ph, img3, z
        img_ct = exposure.rescale_intensity(img2, in_range=(lower_limit, upper_limit))
        dst = np.zeros_like(img_ct)
        z_norm = cv2.normalize(img_ct, dst, 0, 255, cv2.NORM_MINMAX)
        z = z_norm.astype(np.uint8)
        img3 = Image.fromarray(z)
        img3 = img3.resize((new_width, new_height), Image.ANTIALIAS)
        img_ph = ImageTk.PhotoImage(img3)
        canv.create_image(0, 0, image=img_ph, anchor=NW)

    if scale_on:
        insert_scale()
    if logo_on:
        insert_logo()
    if hist_on:
        show_hist()
    if roi_on:
        show_roi(bigger=det_zoom)
        canv.create_rectangle(x_canv_press, y_canv_press, x_canv_rel, y_canv_rel, width=3, outline=color)  # "#fb0"


def change_high_hist(event):
    global upper_limit
    upper_limit = scale_2.get()

    if opened:
        global img_ph, img_ct, z, img3
        img_ct = exposure.rescale_intensity(img2, in_range=(lower_limit, upper_limit))
        dst = np.zeros_like(img_ct)
        z = cv2.normalize(img_ct, dst, 0, 255, cv2.NORM_MINMAX)
        z = z.astype(np.uint8)
        img3 = Image.fromarray(z)
        img3 = img3.resize((new_width, new_height), Image.ANTIALIAS)
        img_ph = ImageTk.PhotoImage(img3)
        canv.create_image(0, 0, image=img_ph, anchor=NW)


    if scale_on:
        insert_scale()
    if logo_on:
        insert_logo()
    if hist_on:
        show_hist()
    if roi_on:
        show_roi(bigger=det_zoom)
        canv.create_rectangle(x_canv_press, y_canv_press, x_canv_rel, y_canv_rel, width=3, outline=color)  # "#fb0"


def scale_units(event):
    global scale_size_1
    scale_size_1 = cb_scale_size.get()
    jednotka = scale_size_1[0]

    global scl_stepen
    if jednotka == "m":
        scl_stepen = 3
    elif jednotka == "\u03BC":
        scl_stepen = 6
    elif jednotka == "n":
        scl_stepen = 9


def voxel_units(event):
    global vxl_stepen, voxel_unit_1, vxl_on
    voxel_unit_1 = cb_voxel_size.get()
    voxel_unit = voxel_unit_1[0]

    if voxel_unit == "m":
        vxl_stepen = 3
    elif voxel_unit == "\u03BC":
        vxl_stepen = 6
    elif voxel_unit == "n":
        vxl_stepen = 9

    vxl_on = True


def give_size(event):
    global voxel_size, n
    n = entry_vxl_size.get()
    voxel_size = float(n)


def scale_entry(event):
    global scale_number, scale_entry_var, p
    p = entry_scl_size.get()
    scale_number = float(p)
    scale_entry_var = 1

    if scale_on:
        create_scale_widget()
        insert_scale()


def create_scale_widget():
    global width_widget, height_widget, img_sc_ph, img_sc, scale_size
    if crop_byl:
        new_voxel_size = (voxel_size * (10 ** -vxl_stepen)) / (new_zoom_w / 100)
    else:
        new_voxel_size = (voxel_size * (10 ** -vxl_stepen)) / (zoom / 100)

    scale_size = scale_number * (10 ** -scl_stepen)
    width_widget = int(scale_size / new_voxel_size)
    height_widget = int(width_widget / 20)
    img_sc = open_sc.resize((width_widget, height_widget), Image.ANTIALIAS)
    img_sc_ph = ImageTk.PhotoImage(img_sc)

    scale_pos_x.configure(to=new_width - 25 - width_widget)
    scale_pos_y.configure(to=new_height - 25 - height_widget)


def insert_scale():
    global scale_on, scale_photo
    canv.create_image(0, 0, image=img_ph, anchor=NW)

    if not scale_on:
        create_scale_widget()

    canv.create_image(posx, posy, image=img_sc_ph, anchor=NW)
    panel_sc = Label(second_frame, image=img_sc_ph)
    panel_sc.image = img_sc_ph

    scale_on = True

    if logo_on:
        canv.create_image(coor_x, coor_y, image=img_log_ph, anchor=SE)
        panel1 = Label(second_frame, image=img_log_ph)
        panel1.image = img_log_ph
        panel1.grid(row=0, column=1)
    if roi_on:
        canv.create_rectangle(x_canv_press, y_canv_press, x_canv_rel, y_canv_rel, width=3, outline=color)  # "#fb0"
        show_roi(bigger=det_zoom)


def insert_logo():

    global img_log, width_log, height_log
    global log_wid, log_hei, logo_on, prev_w, prev_h, prev_pos_x, prev_pos_y, coor_x, coor_y, img_log_ph

    # BLACK PREVIOUS LOGO
    if logo_on:
        back_im = Image.new('RGBA', (prev_w, prev_h), (0, 0, 0, 255))
        back_ph = ImageTk.PhotoImage(back_im)
        canv.create_image(prev_pos_x, prev_pos_y, image=back_ph, anchor=SE)
        panel_3 = Label(second_frame, image=back_ph)
        panel_3.image = back_ph
        panel_3.place(x=0, y=0)

        back = back_create(work_square_w + line, log_hei + line)
        back_place(kuda_x=0, kuda_y=work_square_h + line, back_ph=back)


    img_log = img_log.resize((log_wid, log_hei), Image.ANTIALIAS)
    img_log_ph = ImageTk.PhotoImage(img_log)

    if roi_on:
        if mode == 3:
            coor_x = log_wid
            coor_y = work_square_h + log_hei + line
            window.geometry("{width}x{height}".format(width=w_app, height=work_square_h + log_hei + line))
            frame_picture.configure(height=work_square_h + log_hei + line)
            canv.configure(height=work_square_h + log_hei + line)
        elif mode == 2:
            coor_x = log_wid
            coor_y = work_square_h + log_hei + line
            if coor_y < h_app_def:
                window.geometry("{width}x{height}".format(width=w_app, height=h_app_def))
            else:
                window.geometry("{width}x{height}".format(width=w_app, height=coor_y))
            frame_picture.configure(height=work_square_h + log_hei + line)
            canv.configure(height=work_square_h + log_hei + line)
        elif mode == 1:
            coor_x = work_square_w
            coor_y = work_square_h + log_hei + line
            if coor_y < h_app_def:
                window.geometry("{width}x{height}".format(width=w_app, height=h_app_def))
            else:
                window.geometry("{width}x{height}".format(width=w_app, height=coor_y))
            #window.geometry("{width}x{height}".format(width=w_app, height=h_app_def + log_hei))
            frame_picture.configure(height=work_square_h + log_hei + line)
            canv.configure(height=work_square_h + log_hei + line)
    else:
        coor_x = work_square_w
        coor_y = work_square_h + log_hei + line
        # START
        # if crop_byl:
        #     window.geometry("{width}x{height}".format(width=w_app, height=h_app_def))
        # else:
        #     window.geometry("{width}x{height}".format(width=w_app, height=work_square_h + log_hei + line))

        if crop_byl:
            if coor_y < h_app_def:
                window.geometry("{width}x{height}".format(width=w_app, height=h_app_def))
            else:
                window.geometry("{width}x{height}".format(width=w_app, height=coor_y))
        else:
            window.geometry("{width}x{height}".format(width=w_app, height=coor_y))

        frame_picture.configure(height=work_square_h + log_hei + line)
        canv.configure(height=work_square_h + log_hei + line)

    canv.create_image(coor_x, coor_y, image=img_log_ph, anchor=SE)

    panel1 = Label(second_frame, image=img_log_ph)
    panel1.image = img_log_ph
    panel1.grid(row=0, column=1)

    prev_w = log_wid
    prev_h = log_hei
    prev_pos_x = coor_x
    prev_pos_y = coor_y

    logo_on = True


def open_in_canv(x):
    # x = "Example_slice_1.tif"
    global img2, upper_limit, lower_limit, img_ct, width_img, height_img, zoom, new_width, new_height, z, img3, second_frame,\
        opened, img_ph, img_shh, var

    if not opened:
        img2 = cv2.imread(x, cv2.IMREAD_ANYDEPTH)
        img_shh = img2


    b = np.max(img2)
    upper_limit = 65536
    lower_limit = 0
    hist_high = upper_limit

    if opened:
        img_ct = exposure.rescale_intensity(img2, in_range=(lower_limit, upper_limit))
    else:
        img_ct = img2

    shapes = np.shape(img_ct)
    width_img = shapes[0]
    height_img = shapes[1]

    # ADAPTACE VELIKOSTI
    if not crop_byl:
        zoom = (work_square_h) / height_img * 100
        new_width = int(width_img * (zoom / 100))
        new_height = int(height_img * (zoom / 100))

    dst = np.zeros_like(img_ct)
    z_norm = cv2.normalize(img_ct, dst, 0, 255, cv2.NORM_MINMAX)
    z = z_norm.astype(np.uint8)
    img3 = Image.fromarray(z)
    # img3 = img3.resize((600, 600), Image.ANTIALIAS)
    img3.thumbnail([new_width, new_height], Image.ANTIALIAS)
    img_ph = ImageTk.PhotoImage(img3)

    if not opened:
        create_canv()
        # UPADTE SCALE OF HISTOGRAM
        scale_2.configure(to=hist_high)
        scale.configure(to=hist_high)
        scale_pos_x.configure(to=new_width - 25)
        scale_pos_y.configure(to=new_height - 25)
        scale_2.set(hist_high)

    canv.create_image(0, 0, image=img_ph, anchor=NW)

    opened = True
    var = var_md.get()


def show_hist():
    global hist_on, lower_limit, upper_limit, new_arr_1
    if not hist_on:
        hist_h = np.max(img_shh)
        velikost = int(np.around(hist_h / 256))
        h = np.zeros((120, 256, 3))
        bins = np.arange(velikost).reshape(velikost, 1)
        hist, bins_1 = np.histogram(img_shh, velikost, [0, hist_h])
        hist_res = np.float32(hist.reshape(velikost, 1))
        cv2.normalize(hist_res, hist_res, 0, 255, cv2.NORM_MINMAX)
        hist = np.int32(np.around(hist_res))
        pts = np.column_stack((bins, hist))
        cv2.polylines(h, [pts], False, (0, 0, 255), 7)
        h = np.flipud(h)
        new = h
        new_arr_1 = np.uint8(new)

    ind_1 = int(np.around(lower_limit / 256))
    ind_2 = int(np.around(upper_limit / 256))

    histogram = np.insert(new_arr_1, ind_1, red_line, axis=1)
    histogram_2 = np.insert(histogram, ind_2, red_line, axis=1)
    new_arr = histogram_2

    splitted_arr = np.array_split(new_arr, 2, axis=1)
    arr_1 = splitted_arr[0]
    arr_2 = splitted_arr[1]

    global img_hist_ph_1, img_hist_ph_2
    img_5 = Image.fromarray(arr_1)
    img_5 = img_5.resize((int(btns_width), int(btns_height) * 4), Image.ANTIALIAS)
    img_hist_ph_1 = ImageTk.PhotoImage(img_5)

    img_4 = Image.fromarray(arr_2)
    img_4 = img_4.resize((int(btns_width), int(btns_height) * 4), Image.ANTIALIAS)
    img_hist_ph_2 = ImageTk.PhotoImage(img_4)

    first_label.configure(image=img_hist_ph_1)
    first_label.image = img_hist_ph_1

    sec_label.configure(image=img_hist_ph_2)
    sec_label.image = img_hist_ph_2

    hist_on = True


def press(event):
    global x_coor_image_press, y_coor_image_press, x_canv_press, y_canv_press

    if crop_byl:
        x_coor_image_press = int(event.x / (new_zoom_w / 100))
        y_coor_image_press = int(event.y / (new_zoom_h / 100))
    else:
        x_coor_image_press = int(event.x / (zoom / 100))
        y_coor_image_press = int(event.y / (zoom / 100))

    x_canv_press = event.x
    y_canv_press = event.y


def release(event):

    global x_coor_image_rel, y_coor_image_rel, x_canv_rel, y_canv_rel, x_canv_press, y_canv_press, x_coor_image_press,\
        x_coor_image_rel, y_coor_image_press, y_coor_image_rel, crop_byl, new_zoom_w, new_zoom_h, crop_on, z,\
        work_square_h, work_square_w

    if crop_byl:
        x_coor_image_rel = int(event.x / (new_zoom_w / 100))
        y_coor_image_rel = int(event.y / (new_zoom_h / 100))
    else:
        x_coor_image_rel = int(event.x / (zoom / 100))
        y_coor_image_rel = int(event.y / (zoom / 100))

    x_canv_rel = event.x
    y_canv_rel = event.y


    if crop_on:
        global new_img, x_posun, y_posun, img_ph, img2, new_width, new_height, w_app, h_app, w_app_def, h_app_def,\
        minimum_zoom, new_zoom_w_2, work_square_w, work_square_h, upper_limit, lower_limit, new_zoom_h_2, img3

        canv.create_rectangle(x_canv_press, y_canv_press, x_canv_rel, y_canv_rel, width=3, outline="#fb0")  # "#fb0"
        if x_coor_image_press > x_coor_image_rel:
            [x_coor_image_press, x_coor_image_rel] = [x_coor_image_rel, x_coor_image_press]
        if y_coor_image_press > y_coor_image_rel:
            [y_coor_image_press, y_coor_image_rel] = [y_coor_image_rel, y_coor_image_press]

        new_img = img2[y_coor_image_press:y_coor_image_rel, x_coor_image_press:x_coor_image_rel]
        img2 = new_img

        x_posun = x_coor_image_press
        y_posun = y_coor_image_press
        back_ph = back_create(work_square_w + line, work_square_h + line)
        back_place(0, 0, back_ph)

        # PRO TEST
        img_ct = img2
        #img_ct = exposure.rescale_intensity(img2, in_range=(lower_limit, upper_limit))

        shapes = np.shape(img_ct)
        width_img = shapes[1]
        height_img = shapes[0]

        # NEW ZOOM CALCULATION
        new_zoom_w_2 = work_square_w / width_img * 100
        new_zoom_h_2 = work_square_h / height_img * 100
        minimum_zoom = min(new_zoom_w_2, new_zoom_h_2)
        new_zoom_w = minimum_zoom
        new_zoom_h = minimum_zoom

        new_width = int(width_img * (new_zoom_w / 100))
        new_height = int(height_img * (new_zoom_h / 100))

        # CONFIGURE APP RESOLUTION
        work_square_w = new_width
        work_square_h = new_height
        w_app = work_square_w + int(btns_width*2) + line
        w_app_def = w_app

        window.geometry("{width}x{height}".format(width=w_app, height=h_app_def))
        frame_picture.configure(height=work_square_h + line, width=work_square_w + line)
        canv.configure(height=work_square_h + line, width=work_square_w + line)

        img_ct = exposure.rescale_intensity(img2, in_range=(lower_limit, upper_limit))
        dst = np.zeros_like(img_ct)
        z_norm = cv2.normalize(img_ct, dst, 0, 255, cv2.NORM_MINMAX)
        z = z_norm.astype(np.uint8)
        img3 = Image.fromarray(z)
        img3 = img3.resize((new_width, new_height), Image.ANTIALIAS)
        img_ph = ImageTk.PhotoImage(img3)
        canv.create_image(0, 0, image=img_ph, anchor=NW)
        panel_3 = Label(second_frame, image=img_ph)
        panel_3.image = img_ph

        btn_crop_image.configure(state=DISABLED)

        crop_byl = True
        crop_on = False

        if opened:
            upper_limit = 65536
            lower_limit = 0

    if var:
        canv.create_image(0, 0, image=img_ph, anchor=NW)
        canv.create_rectangle(x_canv_press, y_canv_press, x_canv_rel, y_canv_rel, width=3, outline=color)  # "#fb0" "#FF0800"
        show_roi(bigger=det_zoom)
        bb = back_create(work_square_w, line)
        back_place(0, work_square_h, bb)

    if logo_on:
        insert_logo()
    if scale_on:
        insert_scale()


def motton(event):
    global x_canv_motion, y_canv_motion, maxim
    x_canv_motion = event.x
    y_canv_motion = event.y
    canv.create_image(0, 0, image=img_ph, anchor=NW)

    if crop_on:
        canv.create_rectangle(x_canv_press, y_canv_press, x_canv_motion, y_canv_motion, width=3, outline="#fb0")  # "#fb0"

    if var:
        canv.create_rectangle(x_canv_press, y_canv_press, x_canv_motion, y_canv_motion, width=3, outline=color)

    # if logo_on:
    #     insert_logo()


def back_create(sirka, vysota):
    back_im = Image.new('RGB', (sirka, vysota), (0, 0, 0))
    back_ph = ImageTk.PhotoImage(back_im)

    return back_ph


def back_place(kuda_x, kuda_y, back_ph):
    canv.create_image(kuda_x, kuda_y, image=back_ph, anchor=NW)
    panel_3 = Label(second_frame, image=back_ph)
    panel_3.image = back_ph
    panel_3.place(x=0, y=0)


def show_roi(bigger=1):
    global roi_on, x_coor_image_rel, x_coor_image_press, y_coor_image_press, y_coor_image_rel, roi_n_wid, roi_n_height,\
        roi_img, det_zoom, save_width, roi_ph, x_posun, y_posun, w_app, new_w, z, h_app, work_square_w, work_square_h,\
        mode

    # Adapt ROI coordinates
    det_zoom = bigger

    if x_coor_image_press > x_coor_image_rel:
        [x_coor_image_press, x_coor_image_rel] = [x_coor_image_rel, x_coor_image_press]
    if y_coor_image_press > y_coor_image_rel:
        [y_coor_image_press, y_coor_image_rel] = [y_coor_image_rel, y_coor_image_press]

    # Create Z array
    if crop_byl:
        roi_z = z[y_coor_image_press:y_coor_image_rel, x_coor_image_press:x_coor_image_rel]
        zoom_w = new_zoom_w
        zoom_h = new_zoom_h
    else:
        roi_z = z[y_coor_image_press + y_posun:y_coor_image_rel + y_posun,
                x_coor_image_press + x_posun:x_coor_image_rel + x_posun]
        zoom_w = zoom
        zoom_h = zoom

    # Get picture parameters
    shapes_roi = np.shape(roi_z)
    roi_wid = shapes_roi[1]
    roi_height = shapes_roi[0]

    # Create ROI image
    roi_img = Image.fromarray(roi_z)
    roi_n_wid = int(roi_wid * (zoom_w / 100)) * bigger
    roi_n_height = int(roi_height * (zoom_h / 100)) * bigger
    roi_img = roi_img.resize((roi_n_wid, roi_n_height), Image.ANTIALIAS)
    roi_ph = ImageTk.PhotoImage(roi_img)

    # PODMINKY MAXIMA
    work_square_w = new_width + roi_n_wid + line
    w_app = work_square_w + int(btns_width*2) + line

    if roi_n_height > (h_app_max - log_hei):
        messagebox.showerror("ERROR", "It is height over the maximum size, choose smaller zoom")
        return ()
    elif int(btns_width*2) + new_width + roi_n_wid + line > w_app_max:
        messagebox.showerror("ERROR", "It is width over the maximum size, choose smaller zoom")
        return ()

    if roi_n_height > new_height:
        work_square_h = roi_n_height
        if roi_n_height > h_app_def:
            mode = 3
            window.geometry("{width}x{height}".format(width=w_app, height=work_square_h + line))
            frame_picture.configure(width=work_square_w + line, height=work_square_h + line)
            canv.configure(width=work_square_w + line, height=work_square_h + line)

            frame_btns.configure(height=work_square_h + line)
            frame_help.configure(height=work_square_h + line)

            h_app = work_square_h
        else:
            mode = 2
            window.geometry("{width}x{height}".format(width=w_app, height=h_app_def))
            frame_picture.configure(width=work_square_w + line, height=work_square_h + line)
            canv.configure(width=work_square_w + line, height=work_square_h + line)

            frame_btns.configure(height=h_app_def)
            frame_help.configure(height=h_app_def)
            h_app = h_app_def
    else:
        mode = 1
        work_square_h = new_height
        window.geometry("{width}x{height}".format(width=w_app, height=h_app_def))
        frame_picture.configure(width=work_square_w + line, height=work_square_h + line)
        canv.configure(width=work_square_w + line, height=work_square_h + line)

        frame_btns.configure(height=h_app_def)
        frame_help.configure(height=h_app_def)
        h_app = h_app_def + line

    # Create black background and place
    if roi_on:
        back = back_create(roi_n_wid + 2*line, h_app + 2*line)
        back_place(kuda_x=new_width - 1, kuda_y=0, back_ph=back)

    # Add logo
    if logo_on:
        insert_logo()

    # Place ROI on black background
    canv.create_image(new_width + line, 0, image=roi_ph, anchor=NW)
    panel_3 = Label(second_frame, image=roi_ph)
    panel_3.image = roi_ph

    # Create rectangle near ROI
    canv.create_rectangle(new_width + line, 0, new_width + roi_n_wid + line, roi_n_height, width=3, outline=color)

    # Add ROI scale
    if vxl_on:
        global det_scl
        det_scl = np.around((roi_wid * (voxel_size)))
        lbl_det_scale.configure(text=str(det_scl) + " " + voxel_unit_1)

    roi_on = True


def create_canv(sirka=work_square_w):
    global canv, second_frame
    canv = Canvas(frame_picture, width=sirka + line, height=work_square_h + line, bg='black')
    canv.place(x=0, y=0)
    canv.bind("<Button-1>", press)
    canv.bind("<ButtonRelease-1>", release)
    canv.bind('<B1-Motion>', motton)
    second_frame = Frame(canv, width=work_square_w + line, height=work_square_h + line)


def roi_value():
    global w_app, h_app, var, roi_on
    var = var_md.get()

    if var:
        add = 200
        w_app = w_app_def + add
        window.geometry("{width}x{height}".format(width=w_app, height=h_app))
        canv.configure(cursor="tcross")
        back = back_create(200, h_app)
        back_place(square_side, 0, back)
        btn_crop_image.configure(state=DISABLED)
    else:
        add = 0
        w_app = w_app_def - 1
        window.geometry("{width}x{height}".format(width=w_app, height=h_app))
        canv.configure(cursor="arrow")
        roi_on = False
        btn_crop_image.configure(state=NORMAL)

    frame_picture.configure(width=work_square_w + add + line)
    canv.configure(width=work_square_w + add + line)


def clear_pic():
    # Create black background and place
    default()
    backk = back_create(w_app, h_app)
    back_place(kuda_x=0, kuda_y=0, back_ph=backk)


def default():
    global roi_on, logo_on, scale_on, opened, crop_on, hist_on, var, opened, crop_byl, color, mode

    if roi_on:
        check_make_detail.toggle()
        roi_value()

    # Clear histogram labels
    first_label.configure(image="")
    sec_label.configure(image="")

    # Clear histogram sliders
    scale.set(0)
    scale_2.set(65536)

    # Clear voxel and scale size, detail zoom
    entry_vxl_size.delete(0, 'end')
    entry_scl_size.delete(0, 'end')
    cb_scale_size.set("")
    cb_voxel_size.set("")
    lbl_det_scale.configure(text="")
    cb_zoom.set("")
    cb_make_detail.current(0)
    btn_crop_image.configure(state=NORMAL)

    # Clear scale slider positions
    scale_pos_x.set(0)
    scale_pos_y.set(0)

    if opened:
        global w_app, h_app, w_app_start, h_app_start, w_app_max, h_app_max, log_wid, log_hei, scale_entry_var
        # TAKE INFO ABOUT MONITOR RESOLUTION
        [w_app, h_app, btns_width, btns_height, square_side, geom, space, fontt] = monitor_resolution()
        # other parameters
        w_app_def = w_app
        h_app_def = h_app
        w_app_start = w_app
        h_app_start = h_app
        w_app_max = w_app_def / 0.65
        h_app_max = h_app_def / 0.75
        log_wid = int(w_app_def / 4.5)
        log_hei = int(h_app / 11.5)
        global work_square_w, work_square_h
        work_square_w = int((w_app_def - 10) - (btns_width * 2))
        work_square_h = int((w_app_def - 10) - (btns_width * 2))

        window.geometry("{width}x{height}".format(width=w_app, height=h_app))
        frame_picture.configure(height=work_square_h + line, width=work_square_w + line, bg='#0b1e21')
        canv.configure(height=work_square_h + line, width=work_square_w + line)
        frame_btns.configure(height=work_square_h + line)
        frame_help.configure(height=work_square_h + line)

    # Clear all checkpoints
    logo_on = False
    scale_on = False
    roi_on = False
    opened = False
    crop_on = False
    hist_on = False
    crop_byl = False
    scale_entry_var = 0

    global x_posun, y_posun, roi_n_wid, roi_n_height
    x_posun = 0
    y_posun = 0
    roi_n_wid = 0
    roi_n_height = 0
    mode = 1

    # Deafult color
    color = 'red'
    # Default parameters
    global det_zoom
    det_zoom = 1
    make_zoom()


def make_zoom():
    zoom_list = ["X1", "X2", "X3", "X4", "X8", "X16", "X32", "X64"]
    cb_zoom.configure(values=zoom_list)


def zoom_func(event):
    global det_zoom
    zoom_take = cb_zoom.get()
    zoom_det = zoom_take.split("X")
    zoom_detail = int(zoom_det[1])
    det_zoom = zoom_detail
    show_roi(bigger=det_zoom)


def get_color(event):
    global color
    color = cb_make_detail.get()


def fc_crop():
    global crop_on
    canv.configure(cursor="tcross blue")
    crop_on = True


def open_img():
    # x = "Example_slice_1.tif"
    global x
    x = filedialog.askopenfilename(title='Open file', filetypes=(("tif", "*.tif"), ("All Files", "*.*")))
    default()
    # roi_value()
    open_in_canv(x)


def black_past_logo():
    back_im = Image.new('RGBA', (prev_w, prev_h), (0, 0, 0, 255))
    back_ph = ImageTk.PhotoImage(back_im)
    canv.create_image(prev_pos_x, prev_pos_y, image=back_ph, anchor=SE)
    panel_3 = Label(second_frame, image=back_ph)
    panel_3.image = back_ph
    panel_3.place(x=0, y=0)


# NASTAVENI ROZHRANI A POLI
global frame_picture
frame_btns = Frame(window, bg='#0f282c', width=btns_width, height=h_app)
frame_btns.grid(row=0, column=0)
frame_help = Frame(window, bg='#0f282c', width=btns_width, height=h_app)
frame_help.grid(row=0, column=1)
frame_picture = Frame(window, bg='#0b1e21', width=work_square_w + line, height=work_square_h + line, relief=RAISED)
frame_picture.grid(row=0, column=2)

# LISTY PRO DROPDOWNBOXY
units_list = ["mm", "\u03BC" + "m", "nn"]
color_list = ["red", "blue", "green", "yellow", "orange"]

# VYTVORENI TLACITEK A JEJICH FUNKCI
btn_load = Button(frame_btns, text="Load slice", bg="light gray", font=fontt, command=open_img)
btn_clear = Button(frame_help, text="Clear all", bg="light gray", font=fontt, command=clear_pic)
lbl_vxl_size = Label(frame_btns, text="Voxel size", bg="white", pady=10, font=fontt, relief=RAISED)
entry_vxl_size = Entry(frame_help)
entry_vxl_size.bind("<Leave>", give_size)
entry_scl_size = Entry(frame_help)
entry_scl_size.bind("<Leave>", scale_entry)
lbl_scale_size = Label(frame_btns, text="Scale size", bg="white", pady=10, font=fontt, relief=RAISED)
cb_scale_size = ttk.Combobox(frame_help, values=units_list)
cb_scale_size.bind("<<ComboboxSelected>>", scale_units)
cb_voxel_size = ttk.Combobox(frame_help, values=units_list)
cb_voxel_size.bind("<<ComboboxSelected>>", voxel_units)
btn_crop_image = Button(frame_btns, text="Crop image", bg="light gray", pady=10, font=fontt, command=fc_crop)
btn_insert_scale = Button(frame_btns, text="Insert scale", bg="light gray", pady=10, font=fontt, command=insert_scale)
label_x = Label(frame_btns, text="Scale position X:", bg="white", pady=10, font=fontt, relief=RAISED)
label_y = Label(frame_btns, text="Scale position Y:", bg="white", pady=10, font=fontt, relief=RAISED)
scale_pos_x = Scale(frame_help, from_=25, to=5, resolution=1, orient=HORIZONTAL, sliderlength=5, showvalue=0,
                    command=scl_pos_x)
scale_pos_y = Scale(frame_help, from_=25, to=5, resolution=1, orient=HORIZONTAL, sliderlength=5, showvalue=0,
                    command=scl_pos_y)
btn_insert_logo = Button(frame_btns, text="Insert logo", bg="light gray", pady=10, font=fontt, command=insert_logo)
check_make_detail = Checkbutton(frame_btns, text="Make detail", font=fontt, variable=var_md, relief=RAISED,\
                                onvalue = True, offvalue = False, command=roi_value)
# check_crop = Checkbutton(frame_btns, text="Crop image", font=fontt, variable=var_cr, relief=RAISED, onvalue = True,\
#                          offvalue = False, command=fc_crop)


cb_make_detail = ttk.Combobox(frame_btns, values=color_list)
cb_make_detail.bind("<<ComboboxSelected>>", get_color)

lbl_detail_scale = Label(frame_btns, text="Detail scale:", bg="white", pady=10, font=fontt, relief=RAISED)
lbl_det_scale = Label(frame_help, text="", bg="white", pady=10, font=fontt, relief=RAISED)
lbl_detail_zoom = Label(frame_help, text="Zoom:", bg="white", pady=10, font=fontt, relief=RAISED)
cb_zoom = ttk.Combobox(frame_help)
cb_zoom.bind("<<ComboboxSelected>>", zoom_func)
cb_zoom.bind("<Return>", zoom_func)
btn_show_hist = Button(frame_btns, text="Show histogram", bg="light gray", pady=10, font=fontt, command=show_hist)
sec_label = Label(frame_help)
first_label = Label(frame_btns)
scale = Scale(frame_btns, from_=0, to=65536, resolution=1, orient=HORIZONTAL, sliderlength=5, showvalue=1,
              command=change_low_hist)
scale_2 = Scale(frame_help, from_=0, to=65536, resolution=1, orient=HORIZONTAL, sliderlength=5, showvalue=1,
                command=change_high_hist)
btn_save = Button(frame_btns, text="Save slice", bg="light gray", pady=10, font=fontt, command=save_pct)

# POLOHA A VELIKOST TLACITEK
btn_load.place(y=space*5, x=0, height=btns_height, width=btns_width)
lbl_vxl_size.place(y=(space*5 + space*2) + btns_height * 2, x=0, height=btns_height, width=btns_width)
lbl_scale_size.place(y=(space*5 + space*3) + btns_height * 3, x=0, height=btns_height, width=btns_width)
entry_vxl_size.place(y=(space*5 + space*2) + btns_height * 2, x=0, height=btns_height, width=btns_width * 0.66)
cb_voxel_size.place(y=(space*5 + space*2) + btns_height * 2, x=btns_width * 0.66, height=btns_height, width=btns_width * 0.33)
entry_scl_size.place(y=(space*5 + space*3) + btns_height * 3, x=0, height=btns_height, width=btns_width * 0.66)
cb_scale_size.place(y=(space*5 + space*3) + btns_height * 3, x=btns_width * 0.66, height=btns_height, width=btns_width * 0.33)

btn_crop_image.place(y=(space*5 + space) + btns_height, x=0, height=btns_height, width=btns_width)
btn_insert_scale.place(y=(space*5 + space*4) + btns_height * 4, x=0, height=btns_height, width=btns_width)
label_x.place(y=(space*5 + space*5) + btns_height * 5, x=0, height=btns_height, width=btns_width)
label_y.place(y=(space*5 + space*6) + btns_height * 6, x=0, height=btns_height, width=btns_width)
scale_pos_x.place(y=(space*5 + space*5) + btns_height * 5, x=0, width=btns_width, height=btns_height)
scale_pos_y.place(y=(space*5 + space*6) + btns_height * 6, x=0, width=btns_width, height=btns_height)
btn_insert_logo.place(y=(space*5 + space*7) + btns_height * 7, x=0, height=btns_height, width=btns_width)
check_make_detail.place(y=(space*5 + space*8) + btns_height * 8, x=0, height=btns_height, width=btns_width / 1.36)

cb_make_detail.place(y=(space*5 + space*8) + btns_height * 8, x=btns_width / 1.36, height=btns_height, width=btns_width / 3.75)
lbl_detail_zoom.place(y=(space*5 + space*8) + btns_height * 8, x=0, height=btns_height, width=btns_width / 2)
cb_zoom.place(y=(space*5 + space*8) + btns_height * 8, x=btns_width / 2, height=btns_height, width=btns_width / 2)
lbl_detail_scale.place(y=(space*5 + space*9) + btns_height * 9, x=0, height=btns_height, width=btns_width)
lbl_det_scale.place(y=(space*5 + space*9) + btns_height * 9, x=0, height=btns_height, width=btns_width)
btn_show_hist.place(y=(space*5 + space*10) + btns_height * 10, x=0, height=btns_height, width=btns_width)
sec_label.place(y=(space*5 + space*11) + btns_height * 11, x=0, height=btns_height * 4, width=btns_width)
first_label.place(y=(space*5 + space*11) + btns_height * 11, x=0, height=btns_height * 4, width=btns_width)
scale.place(y=(space*5 + space*15) + btns_height * 15, x=0, height=btns_height*1.5, width=btns_width)
scale_2.place(y=(space*5 + space*15) + btns_height * 15, x=0, height=btns_height*1.5, width=btns_width)
btn_save.place(y=(h_app - btns_height) - space*7, x=0, height=btns_height, width=btns_width)
btn_clear.place(y=(h_app - btns_height) - space*7, x=0, height=btns_height, width=btns_width)



window.mainloop()