import sys
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from PIL import Image

BACKGROUND_COLOR = '#bbbbbb'

def listbox_init():
    listbox.insert(END, f'No files selected')
    listbox.config(state=DISABLED)

def add_files():
    img_path_list = fd.askopenfilenames(filetypes=[('Images', '*.jpg *.jpeg *.png')])

    if listbox['state'] == DISABLED and img_path_list:
        listbox.config(state=NORMAL)
        listbox.delete(0)

    for img_path in img_path_list:
        listbox.insert(END, f'{img_path}')

def delete_files():
    if not listbox.curselection():
        warning('No files selected!')
        return

    if not askokcancel('Do you want to delete selected files?'):
        return

    while listbox.curselection():
        listbox.delete(listbox.curselection()[0])

    if listbox['state'] == NORMAL and not listbox.size():
        listbox_init()

def save_pdf():
    if listbox['state'] == DISABLED:
        warning('No files to convert!')
        return

    images = []
    for img_path in listbox.get(0, END):
        images.append(Image.open(img_path).convert('RGB'))

    out_fname = fd.asksaveasfilename(defaultextension='pdf', filetypes=[('PDF file', '*.pdf')])
    if not out_fname:
        return

    images[0].save(out_fname, save_all = True, quality=100, append_images = images[1:])

    info('File succesfully generated!')

def center_app(width, height):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (width/2))
    y_cordinate = int((screen_height/2) - (height/2))
    return f'{width}x{height}+{x_cordinate}+{y_cordinate}'

def askokcancel(message) -> bool:
    return messagebox.askokcancel('Are you sure?', message)

def info(message):
    messagebox.showinfo('Info', message)

def warning(message):
    messagebox.showwarning('Warning', message)

def error(message):
    messagebox.showerror('Error', message)

app = Tk()
# App
app.config(bg=BACKGROUND_COLOR)
app.title('Converter img2pdf')
app.geometry(center_app(500, 250))
app.minsize(250, 250)

# Frames
controls_frame = Frame(app, bg=BACKGROUND_COLOR)
text_frame = Frame(app, bg=BACKGROUND_COLOR)
bottom_frame = Frame(app, bg=BACKGROUND_COLOR)

# Buttons
open_button = Button(controls_frame, text='Add image / images', command=add_files)
delete_button = Button(controls_frame, text='Delete selected images', command=delete_files)
convert_button = Button(bottom_frame, text='Convert all files to PDF', command=save_pdf)
exit_button = Button(bottom_frame, text='Exit', command=sys.exit)

# Texts
listbox = Listbox(text_frame, selectmode=EXTENDED, height=10, bg='#dddddd')
scrollbar = Scrollbar(text_frame, orient=VERTICAL, command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)

# Packing
controls_frame.pack()
text_frame.pack(fill='x')
bottom_frame.pack()

open_button.pack(side=LEFT, padx=5)
delete_button.pack(side=LEFT, padx=5)

listbox.pack(side=LEFT, fill='x', expand=True)
scrollbar.pack(side=LEFT, fill='y')

convert_button.pack()
exit_button.pack()

if __name__ == '__main__':
    listbox_init()
    app.mainloop()
