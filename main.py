import tkinter as tk
from tkinter import ttk
GLASS_SHEET_SIZE = 1220*914
GLASS_SHEET_JUMBO_SHEET_SIZE = 1680*1040
MOUNTBOARD_STANDARD_SHEET_SIZE = 1200*815
MOUNTBOARD_JUMBO_SHEET_SIZE = 1525*1016
FOAM_BOARD_SHEET_SIZE = 1016*762
FOAM_BOARD_JUMBO_SHEET_SIZE = 1525*1016
STANDARD_GLASS_SHEET_PRICE = 10.50
JUMBO_GLASS_SHEET_PRICE = 18.67 * 2
AR70_GLASS_STANDARD_SHEET = (42.00 + 8.00) * 2
AR70_GLASS_MM2 = AR70_GLASS_STANDARD_SHEET / GLASS_SHEET_SIZE
AR92_GLASS_STANDARD_SHEET = (68.88 + 10.00) * 2
AR92_GLASS_MM2 = AR92_GLASS_STANDARD_SHEET / GLASS_SHEET_SIZE
AR99_GLASS_STANDARD_SHEET = (88.65 + 12.00) * 2
AR99_GLASS_MM2 = AR99_GLASS_STANDARD_SHEET / GLASS_SHEET_SIZE
MOULDING_0056LI_M = 7.26
MOULDING_2651BK_M = 13.84
F1_M = 1.66 * 2
F2_M = 1.50 * 2
F3_M = 1.61 * 2
FOAMBOARD_3MM_STANDARD = 6.66 * 2 / FOAM_BOARD_SHEET_SIZE
FOAMBOARD_5MM_STANDARD = 7.24 * 2 / FOAM_BOARD_SHEET_SIZE
FOAMBOARD_10MM_STANDARD = 12.42 * 2 / FOAM_BOARD_SHEET_SIZE
FOAMBOARD_3MM_JUMBO = 12.59 * 2 / FOAM_BOARD_JUMBO_SHEET_SIZE
FOAMBOARD_5MM_JUMBO = 16.83 * 2 / FOAM_BOARD_JUMBO_SHEET_SIZE
MOUNTBOARD_STANDARD_SHEET_PRICE = 8.61 * 2
MOUNTBOARD_JUMBO_SHEET_PRICE = 16.10 * 2
MDF_STANDARD_SHEET_SIZE = 1220 * 914
MDF_STANDARD_SHEET_PRICE = 2.61 * 2
MDF_JUMBO_SHEET_SIZE = 1830 * 1220
MDF_JUMBO_SHEET_PRICE = 8.83 * 2



def calculate_price():
    # Get user input
    glass_long_side = float(long_side_entry.get())
    glass_short_side = float(short_side_entry.get())
    area_mm2 = glass_long_side * glass_short_side
    total_hours = float(hours_entry.get())

    # Get selected glass type
    glass_type = glass_type_var.get()

    # Calculate glass price based on glass type
    if glass_type == "Standard":
        if glass_long_side > 1120 or glass_short_side > 914:
            glass_price = JUMBO_GLASS_SHEET_PRICE / GLASS_SHEET_JUMBO_SHEET_SIZE * area_mm2
        else:
            glass_price = STANDARD_GLASS_SHEET_PRICE / GLASS_SHEET_SIZE * area_mm2
    elif glass_type == "AR70":
        glass_price = AR70_GLASS_MM2 * area_mm2
    elif glass_type == "AR92":
        glass_price = AR92_GLASS_MM2 * area_mm2
    elif glass_type == "AR99":
        glass_price = AR99_GLASS_MM2 * area_mm2
    else:
        glass_price = 0.00  # Default to 0 if glass type is not recognized

    moulding_type = moulding_type_var.get()

    if moulding_type == "0056LI":
        moulding_total_price = MOULDING_0056LI_M * (2*(glass_long_side + glass_short_side) / 1000)
    elif moulding_type == "2651BK":
        moulding_total_price = MOULDING_2651BK_M * (2*(glass_long_side + glass_short_side) / 1000)
    else:
        moulding_total_price = float(moulding_price_var_entry.get()) * (2*(glass_long_side + glass_short_side) / 1000)


    if glass_long_side > 1200 or glass_short_side > 815:
        mount_board_unit_price = MOUNTBOARD_STANDARD_SHEET_PRICE / MOUNTBOARD_STANDARD_SHEET_SIZE
    else:
        mount_board_unit_price = MOUNTBOARD_JUMBO_SHEET_PRICE / MOUNTBOARD_JUMBO_SHEET_SIZE


    if foamboard_type_var.get() == "3mm":
        if glass_long_side > 1016 or glass_short_side > 762:
            foam_board_price = FOAMBOARD_3MM_JUMBO
        else:
            foam_board_price = FOAMBOARD_3MM_STANDARD
    elif foamboard_type_var.get() == "5mm":
        if glass_long_side > 1016 or glass_short_side > 762:
            foam_board_price = FOAMBOARD_5MM_JUMBO
        else:
            foam_board_price = FOAMBOARD_5MM_STANDARD
    elif foamboard_type_var.get() == "10mm":
        foam_board_price = FOAMBOARD_10MM_STANDARD
    else:
        foam_board_price = 0.00

    hourly_rate = 40.00  # Replace with actual hourly rate


    glass_total_price = glass_price 

    if glass_long_side > 1220 or glass_short_side > 914:
        mdf_total_price = area_mm2  * (MDF_JUMBO_SHEET_PRICE / MDF_JUMBO_SHEET_SIZE)
    else:
        mdf_total_price = area_mm2  * (MDF_STANDARD_SHEET_PRICE / MDF_STANDARD_SHEET_SIZE)

    if fillet_type_var.get() == "F1":
        fillets_total_price = (2*(glass_long_side + glass_short_side) / 1000) * F1_M
    elif fillet_type_var.get() == "F2":
        fillets_total_price = (2*(glass_long_side + glass_short_side) / 1000) * F2_M
    elif fillet_type_var.get() == "F3":
        fillets_total_price = (2*(glass_long_side + glass_short_side) / 1000) * F3_M

    mount_board_total_price = area_mm2 * mount_board_unit_price
    foam_board_total_price = (glass_long_side * glass_short_side) * foam_board_price
    labour_total_price = hourly_rate * total_hours
    

    if tray_frame_checkbox_var.get() == 1:
        total_price = moulding_total_price + labour_total_price
    elif box_frame_checkbox_var.get() == 1:
        total_price = glass_total_price + mdf_total_price + moulding_total_price + mount_board_total_price + fillets_total_price + foam_board_total_price + labour_total_price
        glass_label.config(text=f"Glass Price: £{glass_total_price:.2f}")
        mdf_label.config(text=f"MDF Price: £{mdf_total_price:.2f}")
        mountboard_label.config(text=f"Mountboard Price: £{mount_board_total_price:.2f}")
        fillets_label.config(text=f"Fillets Price: £{fillets_total_price:.2f}")
        foamboard_label.config(text=f"Foamboard Price: £{foam_board_total_price:.2f}")
    else:
        total_price = glass_total_price + mdf_total_price + moulding_total_price + mount_board_total_price + labour_total_price
        glass_label.config(text=f"Glass Price: £{glass_total_price:.2f}")
        mdf_label.config(text=f"MDF Price: £{mdf_total_price:.2f}")
        mountboard_label.config(text=f"Mountboard Price: £{mount_board_total_price:.2f}")
    # Display the result
    
    moulding_label.config(text=f"Moulding Price: £{moulding_total_price:.2f}")
    
    labour_label.config(text=f"Labour Price: £{labour_total_price:.2f}")
    result_label.config(text=f"Total Price: £{total_price:.2f}")

# Create the main window
window = tk.Tk()
window.title("Material Price Calculator")
window.geometry("800x600")


# Create input labels and entry fields
long_side_label = tk.Label(window, text="Glass Long Side (mm):")
long_side_label.grid(row=0, column=0)
long_side_entry = tk.Entry(window)
long_side_entry.grid(row=0, column=1)

short_side_label = tk.Label(window, text="Glass Short Side (mm):")
short_side_label.grid(row=1, column=0)
short_side_entry = tk.Entry(window)
short_side_entry.grid(row=1, column=1)

hours_label = tk.Label(window, text="Total Hours:")
hours_label.grid(row=2, column=0)
hours_entry = tk.Entry(window)
hours_entry.grid(row=2, column=1)

glass_type_label = tk.Label(window, text="Glass Type:")
glass_type_label.grid(row=3, column=0)

glass_type_var = tk.StringVar(window)
glass_type_var.set("Standard")  # Set default value

glass_type_options = ["Standard", "AR70", "AR92", "AR99"]  # Replace with actual glass types

glass_type_dropdown = tk.OptionMenu(window, glass_type_var, *glass_type_options)
glass_type_dropdown.configure(width=10)
glass_type_dropdown.grid(row=3, column=1)

# def enable_moulding_type_dropdown():
#     if enable_moulding_type_dropdown_bool.get():
#         moulding_type_dropdown.configure(state="normal")
#         moulding_price_var_entry.configure(state="disabled")
#     else:
#         moulding_type_dropdown.configure(state="disabled")
#         moulding_price_var_entry.configure(state="normal")



# enable_moulding_type_dropdown_bool = tk.BooleanVar()
# moulding_type_radiobutton = tk.Radiobutton(window, text="Dropdown", variable=enable_moulding_type_dropdown, value=True, command=enable_moulding_type_dropdown, state="normal")
# moulding_price_radiobutton = tk.Radiobutton(window, text="Custom", variable=enable_moulding_type_dropdown, value=False, command=enable_moulding_type_dropdown, state="active")
# moulding_type_radiobutton.pack()
# moulding_price_radiobutton.pack()


moulding_type_label = tk.Label(window, text="Moulding Type:")
moulding_type_label.grid(row=4, column=0)

moulding_type_var = tk.StringVar(window)

moulding_type_options = ["0056LI", "2651BK"]  # Replace with actual glass types

moulding_type_dropdown = tk.OptionMenu(window, moulding_type_var, *moulding_type_options)
moulding_type_dropdown.configure(width=10)
moulding_type_dropdown.grid(row=4, column=1)

moulding_price_label = tk.Label(window, text="Moulding Price per metre:")
moulding_price_label.grid(row=4, column=2)

moulding_price_var_entry = tk.Entry(window)  # Set default value
moulding_price_var_entry.grid(row=4, column=3)

moulding_price_options = ["Dropdown", "Custom"]




tray_frame_label = tk.Label(window, text="Tray Frame:")
tray_frame_label.grid(row=5, column=0)
tray_frame_checkbox_var = tk.IntVar()
tray_frame_checkbox = tk.Checkbutton(window, variable=tray_frame_checkbox_var)
tray_frame_checkbox.grid(row=5, column=1)


box_frame_label = tk.Label(window, text="Box Frame:")
box_frame_label.grid(row=5, column=3)
box_frame_checkbox_var = tk.IntVar()
box_frame_checkbox = tk.Checkbutton(window, variable=box_frame_checkbox_var)
box_frame_checkbox.grid(row=5, column=4)

fillet_type_label = tk.Label(window, text="Fillet Type:")
fillet_type_label.grid(row=6, column=3)

fillet_type_var = tk.StringVar(window)
fillet_type_options = ["F1", "F2", "F3"]

fillet_type_dropdown = tk.OptionMenu(window, fillet_type_var, *fillet_type_options)
fillet_type_dropdown.configure(width=10)
fillet_type_dropdown.configure(state="disabled")
fillet_type_dropdown.grid(row=6, column=4)

foamboard_type_label = tk.Label(window, text="Foamboard Type:")
foamboard_type_label.grid(row=7, column=3)

foamboard_type_var = tk.StringVar(window)
foamboard_type_options = ["3mm", "5mm", "10mm"]  # Replace with actual foamboard types

foamboard_type_dropdown = tk.OptionMenu(window, foamboard_type_var, *foamboard_type_options)
foamboard_type_dropdown.configure(width=10)
foamboard_type_dropdown.configure(state="disabled")
foamboard_type_dropdown.grid(row=7, column=4)

def enable_fillet_and_foamboard_type_dropdown():
    if box_frame_checkbox_var.get() == 1:
        fillet_type_dropdown.configure(state="normal")
        foamboard_type_dropdown.configure(state="normal")
    else:
        fillet_type_dropdown.configure(state="disabled")
        fillets_label.config(text="")
        foamboard_type_dropdown.configure(state="disabled")
        foamboard_label.config(text="")

box_frame_checkbox.configure(command=enable_fillet_and_foamboard_type_dropdown)




# Create calculate button
calculate_button = tk.Button(window, text="Calculate", command=calculate_price)
calculate_button.grid(row=8, column=0)

glass_label = tk.Label(window, text="")
glass_label.grid(row=9, column=0)
moulding_label = tk.Label(window, text="")
moulding_label.grid(row=10, column=0)
mdf_label = tk.Label(window, text="")
mdf_label.grid(row=11, column=0)
mountboard_label = tk.Label(window, text="")
mountboard_label.grid(row=12, column=0)
foamboard_label = tk.Label(window, text="")
foamboard_label.grid(row=13, column=0)
fillets_label = tk.Label(window, text="")
fillets_label.grid(row=14, column=0)
labour_label = tk.Label(window, text="")
labour_label.grid(row=15, column=0)
# Create label to display the result
result_label = tk.Label(window, text="")
result_label.grid(row=16, column=0)

# Start the main event loop
window.mainloop()