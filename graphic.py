import tkinter as tk
import colorsys

from tkinter import filedialog, Label
from PIL import Image, ImageTk

from typing import Tuple


def submit(event):
    try:
        if not img_rgb:
            return

        width, height = img.size

        entry_value = color_coord.get()

        coords = entry_value.split(" ")

        if not entry_value or len(coords) != 2:
            return

        x, y = [int(c) for c in coords]

        if x > width or y > height:
            color_coord.set("")
            return

        r, g, b = img_rgb.getpixel((x, y))

        to_hsl = rgb_to_hsl(r, g, b)
        to_hsv = rgb_to_hsv(r, g, b)
        to_hex = rgb_to_hex(r, g, b)

        update_labels([
            f"RGB: ({r}, {g}, {b})",
            f"HSL: ({to_hsl[0]}, {to_hsl[1]}, {to_hsl[2]})",
            f"HSV: ({to_hsv[0]}, {to_hsv[1]}, {to_hsv[2]})",
            f"HEX: {to_hex}",
            f"COORDS: ({x}) ({y})",
        ])

        color_coord.set("")
    except NameError:
        return


def open_image():
    filepath = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )

    if not filepath:
        return

    global img, img_tk, img_rgb

    img = Image.open(filepath)
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)

    image_mouse_binder.config(image=img_tk)
    image_mouse_binder.image = img_tk

    img_rgb = img.convert('RGB')

    width, height = img.size
    rgb_value_table.delete(1.0, tk.END)

    rgb_values = ""
    for y in range(height):
        for x in range(width):
            r, g, b = img_rgb.getpixel((x, y))
            rgb_values += f"({r:3}, {g:3}, {b:3}) | "
        rgb_values += "\n"

    rgb_value_table.insert(tk.END, rgb_values)


def show_color_info(event):
    try:
        if img_rgb:
            x, y = event.x, event.y

            # ensure the coordinates are within the image bounds
            if 0 <= x < img.width and 0 <= y < img.height:
                r, g, b = img_rgb.getpixel((x, y))

                to_hsl = rgb_to_hsl(r, g, b)
                to_hsv = rgb_to_hsv(r, g, b)
                to_hex = rgb_to_hex(r, g, b)

                update_labels([
                    f"RGB: ({r}, {g}, {b})",
                    f"HSL: ({to_hsl[0]}, {to_hsl[1]}, {to_hsl[2]})",
                    f"HSV: ({to_hsv[0]}, {to_hsv[1]}, {to_hsv[2]})",
                    f"HEX: {to_hex}",
                    f"COORDS: ({x}) ({y})",
                ])
    except NameError:
        return


def rgb_to_hex(r: int, g: int, b: int) -> str:
    def to_hex(val):
        first_digit = val // 16
        second_digit = val % 16

        # convert 10-15 to 'A'-'F' and 0-9 to '0'-'9'
        hex_digits = '0123456789ABCDEF'
        return hex_digits[first_digit] + hex_digits[second_digit]

    r_hex = to_hex(r)
    g_hex = to_hex(g)
    b_hex = to_hex(b)

    # Combine into hex color string
    hex_color = f"#{r_hex}{g_hex}{b_hex}".upper()

    print(f'#{r:02x}{g:02x}{b:02x}'.upper())

    return hex_color

    # need to do it manually, gotta change later
    # return f'#{r:02x}{g:02x}{b:02x}'.upper()


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[int, int, int]:
    # normalize the RGB values to range [0, 1]
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0

    cMax = max(r_norm, g_norm, b_norm)
    cMin = min(r_norm, g_norm, b_norm)
    delta = cMax - cMin

    # calculate saturation (S)
    s = 0 if cMax == 0 else delta / cMax

    # calculate hue (H)
    if delta == 0:
        h = 0
    else:
        if cMax == r_norm:
            h = 60 * (((g_norm - b_norm) / delta) % 6)
        elif cMax == g_norm:
            h = 60 * (2 + (b_norm - r_norm) / delta)
        elif cMax == b_norm:
            h = 60 * (4 + (r_norm - g_norm) / delta)

    # scale h, s and v
    h = int(h)
    s = int(s * 100)
    v = int(cMax * 100)
    # print(f"hsv:{h, s, v}")

    # norm_a, norm_b, norm_c = r / 255.0, g / 255.0, b / 255.0
    # h1, s1, v1 = colorsys.rgb_to_hsv(norm_a, norm_b, norm_c)

    # h1 = int(h1 * 360)
    # s1 = int(s1 * 100)
    # v1 = int(v1 * 100)

    # return (h1, s1, v1)
    return (h, s, v)


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    # normalize the RGB values to range [0, 1]
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0

    cMax = max(r_norm, g_norm, b_norm)
    cMin = min(r_norm, g_norm, b_norm)

    delta = cMax - cMin
    l = (cMax + cMin) / 2

    if cMax == cMin:
        s = 0
    elif l <= 0.5:
        s = delta / (cMax + cMin)
    elif l > 0.5:
        s = delta / (2 - cMax - cMin)

    # calculate hue (H)
    if delta == 0:
        h = 0
    else:
        if cMax == r_norm:
            h = 60 * (((g_norm - b_norm) / delta) % 6)
        elif cMax == g_norm:
            h = 60 * (2 + (b_norm - r_norm) / delta)
        elif cMax == b_norm:
            h = 60 * (4 + (r_norm - g_norm) / delta)

    # scale h, s and v
    h = int(h)
    s = int(s * 100)
    l = int(l * 100)

    return (h, s, l)


def rgb_to_hsl2(r: int, g: int, b: int) -> Tuple[int, int, int]:
    # need to do it manually, gotta change later
    norm_r, norm_g, norm_b = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(norm_r, norm_g, norm_b)

    h = int(h * 360)
    s = int(s * 100)
    l = int(l * 100)

    a, b, c = rgb_to_hsl2(r, g, b)
    print(f"hsl:{a, b, c}")

    return (h, s, l)


root = tk.Tk()
root.title("Coursework")

label_list = []


def create_horizontal_frame_list(parent, num_frames):
    horizontal_frame = tk.Frame(parent)
    horizontal_frame.grid(row=0, column=1, sticky='ew',
                          pady=(10, 0), padx=(10, 20))

    labels = [
        f"RGB: (x, x, x)",
        f"HSL: (x, x, x)",
        f"HSV: (x, x, x)",
        f"HEX: (xxxxxx)",
        f"COORDS: (x) (y)",
        None
    ]

    for i in range(num_frames):
        frame = tk.Frame(horizontal_frame, borderwidth=2)

        frame.pack(side=tk.LEFT)

        if labels[i]:
            label = tk.Label(
                frame,
                text=labels[i],
                width=20,
                anchor='w',
            )

            label.pack(padx=0, pady=0)

            label_list.append(label)
        else:
            global entry_coord, color_coord

            color_coord = tk.StringVar()

            entry_coord = tk.Entry(frame, textvariable=color_coord)
            entry_coord.pack(padx=0, pady=0)
            entry_coord.bind("<Return>", submit)


def update_labels(new_texts):
    for label, new_text in zip(label_list, new_texts):
        label.config(text=new_text)


create_horizontal_frame_list(root, 6)

rgb_value_frame = tk.Frame(root, padx=10, pady=10)
rgb_value_frame.grid(row=1, column=1, sticky='nsew')

rgb_value_table = tk.Text(rgb_value_frame, wrap=tk.NONE,
                          width=107, height=24, bg='white')
rgb_value_table.grid(row=0, column=0, sticky='nsew')

# add a vertical scrollbar for the RGB table
scrollbar_y = tk.Scrollbar(
    rgb_value_frame, orient="vertical", command=rgb_value_table.yview)
scrollbar_y.grid(row=0, column=1, sticky='ns')
rgb_value_table.config(yscrollcommand=scrollbar_y.set)

# add a horizontal scrollbar for the RGB table
scrollbar_x = tk.Scrollbar(
    rgb_value_frame, orient="horizontal", command=rgb_value_table.xview)
scrollbar_x.grid(row=1, column=0, sticky='ew')
rgb_value_table.config(xscrollcommand=scrollbar_x.set)

image_mouse_binder = tk.Label(root)
image_mouse_binder.grid(row=0, column=0, rowspan=2,
                        padx=10, pady=(10, 0), sticky='new')
image_mouse_binder.bind("<Motion>", show_color_info)

root.grid_rowconfigure(2, weight=0)

open_button = tk.Button(root, text="Open Image",
                        command=open_image)
open_button.grid(row=2, column=0, padx=10, pady=(0, 10), sticky='ew')

root.mainloop()
