import tkinter as tk
from tkinter import ttk
import json

MATERIALS_FILE_PATH = r"C:\Users\ckbas\pricing_platform\pricing_platform\materials.json"

def calc_sheet_area(size: str):
    dims = size.split("x")
    return float(dims[0]) * float(dims[1])


def save_new_moulding():
    if moulding_type_var.get() != "" and moulding_price_var.get() != "":
        materials['moulding_type'][moulding_type_var.get()] = float(moulding_price_var.get())

        with open(MATERIALS_FILE_PATH, "w") as f:
            json.dump(materials, f, indent=4)


def show_entry(event):
    if moulding_type_var.get() == "Custom":
        custom_material_name_label.grid(row=1, column=0, pady=5)
        custom_material_name_entry.grid(row=1, column=1, pady=5)
        moulding_price_label.grid(row=2, column=0, pady=5)
        moulding_price_entry.grid(row=2, column=1, pady=5)
        save_custom_moulding_button.grid(row=3, column=1, pady=5)
    else:
        custom_material_name_label.grid_forget()
        custom_material_name_entry.grid_forget()
        moulding_price_entry.grid_forget()
        moulding_price_label.grid_forget()
        save_custom_moulding_button.grid_forget()


def calculate_glass_price(glass_long_side,
                          glass_short_side,
                          area_mm2,
                          glass_type):
    # Calculate glass price based on glass type

    if glass_long_side > 1120 or glass_short_side > 914:
        glass_price = (materials['glass']['jumbo_types']['jumbo']
                       / calc_sheet_area(materials['glass']['sizes']['jumbo']) * area_mm2)
    else:
        glass_price = (materials['glass']['standard_types'][glass_type]
                       / calc_sheet_area(materials['glass']['sizes']['standard']) * area_mm2)

    return glass_price


def calculate_price():
    with open(MATERIALS_FILE_PATH) as f:
        materials = json.load(f)
    long_side = float(long_side_entry.get())
    short_side = float(short_side_entry.get())

    perimeter_m = 2 * (long_side + short_side) / 1000
    area_mm2 = long_side * short_side

    # Calculate total glass price
    glass_total_price = calculate_glass_price(long_side,
                                              short_side,
                                              area_mm2,
                                              glass_type_var.get())

    # Calculate total moulding price
    moulding_type = moulding_type_var.get()

    if moulding_type == "Custom":
        moulding_total_price = float(moulding_price_entry.get()) * perimeter_m
    else:
        moulding_total_price = materials['moulding_type'][moulding_type] * perimeter_m

    # Calculate total mount board price
    if long_side > 1200 or short_side > 815:
        mountboard_total_price = materials['mountboard']['jumbo']['price'] / calc_sheet_area(
            materials['mountboard']['jumbo']['size']) * area_mm2
    else:
        mountboard_total_price = materials['mountboard']['standard']['price'] / calc_sheet_area(
            materials['mountboard']['standard']['size']) * area_mm2

    if box_frame_checkbox_var.get() == 1:

        # Calculate total foam board price
        if long_side > 1016 or short_side > 762:
            foamboard_total_price = materials['foamboard']['jumbo'][foamboard_type_var.get()] / calc_sheet_area(
                materials['foamboard']['jumbo']['size']) * area_mm2
        else:
            foamboard_total_price = materials['foamboard']['standard'][foamboard_type_var.get()] / calc_sheet_area(
                materials['foamboard']['standard']['size']) * area_mm2

        # Calculate fillets total price
        fillets_total_price = perimeter_m * materials['fillets'][fillet_type_var.get()]

    else:
        foamboard_total_price = 0.00
        fillets_total_price = 0.00

    # Calculate mdf total price
    if long_side > 1220 or short_side > 914:
        mdf_total_price = area_mm2 * (
                materials['mdf']['jumbo']['price'] / calc_sheet_area(materials['mdf']['jumbo']['size']))
    else:
        mdf_total_price = area_mm2 * (
                materials['mdf']['standard']['price'] / calc_sheet_area(materials['mdf']['standard']['size']))

    # Calculate total labour price
    hourly_rate = 40.00
    total_hours = float(hours_entry.get())
    total_labour_price = hourly_rate * total_hours

    if tray_frame_checkbox_var.get() == 1:
        total_price = moulding_total_price + total_labour_price
    elif box_frame_checkbox_var.get() == 1:
        total_price = (glass_total_price
                       + mdf_total_price
                       + moulding_total_price
                       + mountboard_total_price
                       + fillets_total_price
                       + foamboard_total_price
                       + total_labour_price)
    else:
        total_price = (glass_total_price
                       + mdf_total_price
                       + moulding_total_price
                       + mountboard_total_price
                       + total_labour_price)

    paint_output_frame(glass_total_price,
                       mdf_total_price,
                       mountboard_total_price,
                       fillets_total_price,
                       foamboard_total_price,
                       moulding_total_price,
                       total_labour_price,
                       total_price)


def paint_output_frame(glass_total_price,
                       mdf_total_price,
                       mount_board_total_price,
                       fillets_total_price,
                       foam_board_total_price,
                       moulding_total_price,
                       labour_total_price,
                       total_price):
    for widget in output_frame.winfo_children():
        widget.destroy()
    output_frame.config(width=180, height=400, bg='#aaaaaa')
    if tray_frame_checkbox_var.get() == 0:
        glass_label = tk.Label(output_frame, text=f"Glass Price: £{glass_total_price:.2f}", bg='#aaaaaa')
        glass_label.grid(row=0, column=0)
        mdf_label = tk.Label(output_frame, text=f"MDF Price: £{mdf_total_price:.2f}", bg='#aaaaaa')
        mdf_label.grid(row=1, column=0)
        mountboard_label = tk.Label(output_frame, text=f"Mountboard Price: £{mount_board_total_price:.2f}", bg='#aaaaaa')
        mountboard_label.grid(row=2, column=0)
        if box_frame_checkbox_var.get() == 1:
            foamboard_label = tk.Label(output_frame, text=f"Foamboard Price: £{foam_board_total_price:.2f}", bg='#aaaaaa')
            foamboard_label.grid(row=3, column=0)
            fillets_label = tk.Label(output_frame, text=f"Fillets Price: £{fillets_total_price:.2f}", bg='#aaaaaa')
            fillets_label.grid(row=4, column=0)
    moulding_label = tk.Label(output_frame, text=f"Moulding Price: £{moulding_total_price:.2f}", bg='#aaaaaa')
    moulding_label.grid(row=5, column=0)
    labour_label = tk.Label(output_frame, text=f"Labour Price: £{labour_total_price:.2f}", bg='#aaaaaa')
    labour_label.grid(row=6, column=0)
    # Create label to display the result
    result_label = tk.Label(output_frame, text=f"Total Price: £{total_price:.2f}", bg='#aaaaaa')
    result_label.grid(row=7, column=0)
    result_label.config(font=('bold'))


def enable_fillet_and_foamboard_type_dropdown():
    if box_frame_checkbox_var.get() == 1:
        fillet_type_combobox.configure(state="normal")
        foamboard_type_combobox.configure(state="normal")
    else:
        fillet_type_combobox.configure(state="disabled")
        foamboard_type_combobox.configure(state="disabled")


def apply_dark_theme(widget, dark_bg, dark_fg):
    if isinstance(widget, tk.Frame):
        widget.config(bg=dark_bg)
    elif isinstance(widget, tk.Checkbutton):
        widget.config(bg=dark_bg)
    elif not isinstance(widget, tk.Entry):
        widget.config(bg=dark_bg, fg=dark_fg)

    for child in widget.winfo_children():
        apply_dark_theme(child, dark_bg, dark_fg)

def deselect_tray_frame(event):
    tray_frame_checkbox_var.set(0)

def deselect_box_frame():
    box_frame_checkbox_var.set(0)


with open(MATERIALS_FILE_PATH) as f:
    materials = json.load(f)

# Create the main window
window = tk.Tk()
dark_bg = '#2d2d2d'
dark_fg = '#ffffff'

window.title("Livingstone Studios Quote Calculator")
window.option_add("*Font", "Verdana 10")

window.config(bg=dark_bg)

input_frame = tk.Frame(window, width=600, height=400)
input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, anchor=tk.CENTER, padx=10, pady=10)

glass_frame = tk.Frame(input_frame, width=590, height=100)
glass_frame.grid(row=0, column=0, padx=5, pady=5)

moulding_frame = tk.Frame(input_frame, width=590, height=100)
moulding_frame.grid(row=1, column=0, padx=5, pady=5)

frame_type_frame = tk.Frame(input_frame, width=590, height=100)
frame_type_frame.grid(row=2, column=0, padx=5, pady=5)

calculate_frame = tk.Frame(input_frame, width=590, height=100)
calculate_frame.grid(row=3, column=0, padx=5, pady=5)

# Create input labels and entry fields
long_side_label = tk.Label(glass_frame, text="Glass Long Side (mm):")
long_side_label.grid(row=0, column=0, sticky=tk.E, pady=5)
long_side_entry = tk.Entry(glass_frame)
long_side_entry.grid(row=0, column=1, pady=5)
long_side_entry.config(width=15)

short_side_label = tk.Label(glass_frame, text="Glass Short Side (mm):")
short_side_label.grid(row=1, column=0, sticky=tk.E, pady=5)
short_side_entry = tk.Entry(glass_frame)
short_side_entry.grid(row=1, column=1, pady=5)
short_side_entry.config(width=15)

glass_type_label = tk.Label(glass_frame, text="Glass Type:")
glass_type_label.grid(row=2, column=0, pady=5)

glass_type_var = tk.StringVar(glass_frame)
glass_type_var.set("Standard")
glass_type_options = list(materials['glass']['standard_types'].keys())
glass_type_combobox = ttk.Combobox(glass_frame, values=glass_type_options, textvariable=glass_type_var)
glass_type_combobox.current(0)  # set the default selected item
glass_type_combobox.config(width=10)
glass_type_combobox.grid(row=2, column=1, columnspan=1, pady=5)

moulding_type_label = tk.Label(moulding_frame, text="Moulding Type:")
moulding_type_label.grid(row=0, column=0, pady=5)

moulding_type_var = tk.StringVar(moulding_frame)
moulding_type_options = list(materials['moulding_type'].keys())
moulding_type_options.append("Custom")

moulding_type_combobox = ttk.Combobox(moulding_frame, textvariable=moulding_type_var, values=moulding_type_options)
moulding_type_combobox.grid(row=0, column=1, pady=5)
moulding_type_combobox.bind("<<ComboboxSelected>>", show_entry)
custom_material_name_label = tk.Label(moulding_frame, text="Custom Material Name:")
# glass_type_combobox.config(width)

custom_material_name_var = tk.StringVar(moulding_frame)
custom_material_name_entry = tk.Entry(moulding_frame, textvariable=custom_material_name_var)

moulding_price_label = tk.Label(moulding_frame, text="Moulding Price:")

moulding_price_var = tk.StringVar(moulding_frame)
moulding_price_entry = tk.Entry(moulding_frame, textvariable=moulding_price_var)

# BUTTON TO SAVE CUSTOM MOULDING
save_custom_moulding_button = tk.Button(moulding_frame, text="Save", command=save_new_moulding)

tray_frame_label = tk.Label(frame_type_frame, text="Tray Frame:")
tray_frame_label.grid(row=0, column=0, pady=5)
tray_frame_checkbox_var = tk.IntVar()
tray_frame_checkbox = tk.Checkbutton(frame_type_frame, variable=tray_frame_checkbox_var)
tray_frame_checkbox.grid(row=0, column=1, pady=5)

box_frame_label = tk.Label(frame_type_frame, text="Box Frame:")
box_frame_label.grid(row=1, column=0, pady=5)
box_frame_checkbox_var = tk.IntVar()
box_frame_checkbox = tk.Checkbutton(frame_type_frame, variable=box_frame_checkbox_var)
box_frame_checkbox.grid(row=1, column=1, pady=5)

fillet_type_label = tk.Label(frame_type_frame, text="Fillet Type:")
fillet_type_label.grid(row=2, column=0, pady=5)

fillet_type_var = tk.StringVar(frame_type_frame)
fillet_type_options = list(materials['fillets'].keys())

fillet_type_combobox = ttk.Combobox(frame_type_frame, textvariable=fillet_type_var, values=fillet_type_options)
fillet_type_combobox.configure(width=10)
fillet_type_combobox.configure(state="disabled")
fillet_type_combobox.grid(row=2, column=1, pady=5)

foamboard_type_label = tk.Label(frame_type_frame, text="Foamboard Type:")
foamboard_type_label.grid(row=3, column=0, pady=5)

foamboard_type_var = tk.StringVar(frame_type_frame)
foamboard_type_options = ["3mm", "5mm", "10mm"]  # Replace with actual foamboard types

foamboard_type_combobox = ttk.Combobox(frame_type_frame, textvariable=foamboard_type_var, values=foamboard_type_options)
foamboard_type_combobox.configure(width=10)
foamboard_type_combobox.configure(state="disabled")
foamboard_type_combobox.grid(row=3, column=1, pady=5)

box_frame_checkbox.configure(command=enable_fillet_and_foamboard_type_dropdown)

hours_label = tk.Label(calculate_frame, text="Total Hours:")
hours_label.grid(row=0, column=0, pady=5)
hours_entry = tk.Entry(calculate_frame)
hours_entry.grid(row=0, column=1, pady=5)
# Create calculate button
calculate_button = tk.Button(calculate_frame, text="Calculate", command=calculate_price)
calculate_button.grid(row=1, column=1, pady=5)

apply_dark_theme(input_frame, dark_bg, dark_fg)

output_frame = tk.Frame(window, width=180, height=400, bg='#aaaaaa')
output_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, anchor=tk.CENTER, padx=10, pady=10)

# Start the main event loop
window.mainloop()
