# TODO 1: CREATE INTERFACE

from tkinter import *
from tkinter import PhotoImage
from tkinter.filedialog import askopenfiles
from requests_html import HTML

WHITE = "#FFFFFF"
GRAY = "#A9A9A9"
LIGHT_PURPLE = "#A9A9C9"
JAFRA_PURPLE = "#460A66"
GRAY2 = "#A9A9B9"
BLACK = "#000000"
FONT_NAME = "Raleway"
WIDTH = 500
var_list = []

window = Tk()
window.title(f"JAFRANET ({window.winfo_width()}, {window.winfo_height()})")
window.config(bg=GRAY)


def center_window(size, wndw):
    window_width = size[0]
    window_height = size[1]
    window_x = int((wndw.winfo_screenwidth() / 2) - (window_width / 2))
    window_y = int((wndw.winfo_screenheight() / 2) - (window_height / 2))

    window_geometry = str(window_width) + 'x' + str(window_height) + '+' + str(
        window_x) + '+' + str(window_y)  # Creates a geometric string argument
    wndw.geometry(window_geometry)  # Sets the geometry accordingly.
    return


def confirm():
    pass


def cancelar():
    global window
    window.quit()


def display_listbox(content, list_to_scrape, ro, col, root):
    list_box = Listbox(root, listvariable=content)
    list_box.grid(column=col, row=ro, sticky=EW, padx=25, pady=60)

    confirm_button = Button(text="Crear Archivo", width=20)
    confirm_button.grid(column=0, row=2)

    retry_button = Button(text="Reintentar", width=20, command=command_execute)
    retry_button.grid(column=0, row=3)

    cancelar_button = Button(text="Salir", width=20, command=cancelar)
    cancelar_button.grid(column=0, row=4)


# TODO 2: ASK FOR FILES WITH TKINTER.DIALOG BOX
def get_filepaths():
    file_paths = []
    files = askopenfiles(parent=window, title="Selecciona los estados de cuenta", mode="r",
                         filetypes=[("HTML file", "*.html")])
    for f in files:
        file_paths.append(f.name)
    return file_paths


# TODO 3: PROCESS FILES FUNCTIONS FOR SCRAPING NAMES
def scrape_report(single_file):
    with open(file=single_file, errors="ignore") as html_file:
        source = html_file.read()
        html = HTML(html=source)
        html.render()

    report = html.find(".table-blk#reporte", first=True)
    return report


def scrape_name(file):
    report = scrape_report(file)

    # data or tbody
    table_body = report.find("tbody", first=True)
    table_data = table_body.find("td")
    return table_data[2].text


def scrape_tabla(file):
    report = scrape_report(file)

    # data or tbody
    table_body = report.find("tbody", first=True)
    table_data = table_body.find("td")

    # headers
    table_head = report.find(".head")
    header = []
    table_heads = []
    for i in range(0, 2):
        title = table_head[i].text
        title = str(title)
        title = title.splitlines()
        table_heads.append(title)
    header.append(table_heads)

    # counter
    directas = 0
    indirectas = 0
    total = 0

    for i in range(0, len(table_data)):
        table_data1 = table_data[i].text
        if table_data1 == "I":
            indirectas = indirectas + 1
            total = total + 1
        elif table_data1 == "D":
            directas = directas + 1
            total = total + 1
    print(header)


# TODO 4: PROCESS FILES WITH FULL REPORT SCRAPE
def command_execute():
    global var_list
    file_paths_list = get_filepaths()
    animadores = []
    for f in file_paths_list:
        name_in_animadores = scrape_name(f)
        animadores.append(name_in_animadores)
    var_list = animadores
    var = Variable(value=var_list)
    display_listbox(content=var, list_to_scrape=var_list, ro=1, col=0, root=window)


# Row 0 - Logo
canvas = Canvas(width=WIDTH + 20, height=200, bg=WHITE, highlightthickness=0)
backgrnd_img = PhotoImage(file="jafra_logo_negro.png")
canvas.create_image(260, 115, image=backgrnd_img)
canvas.grid(column=0, row=0)

# Row 1 - Purple Background
canvas_center = Canvas(width=WIDTH + 20, height=400, bg=JAFRA_PURPLE, highlightthickness=0)
canvas_center.grid(column=0, row=1, rowspan=4)

# Row 1 (inside) - Texto
center_title = Label(text=f"Bienvenido(a), comienza seleccionando \n un archivo para convertir a excel. ",
                     bg=JAFRA_PURPLE, fg=WHITE, font=(FONT_NAME, 14))
center_title.grid(column=0, row=1, sticky="N", pady=15)

# Row 1 - Sub_window Explorer/List
browse_text = "Comenzar"
comenzar = Button(width=20, text=browse_text, bg=JAFRA_PURPLE, fg=BLACK, command=command_execute, bd=0)
comenzar.grid(column=0, row=2)

# Row 2 - Button 2


# TODO 5: CREATE XLXS FILE WITH COMPLETE DATA
center_window(wndw=window, size=[WIDTH + 20, 700])
window.mainloop()
