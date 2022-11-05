from itertools import count
import os
import pickle

x1 = count()  # for crear_rotulo_html()
next(x1)

x2 = count() # for crear_rotulo_csv()
next(x2)

x4 = count()  # for descargar_objeto()
next(x4)

def descargar_csv(frame, dir_name="csv", prefix="db", suffix=None, fix=None):
    """Recibe un dataframe y los almacena en formato csv"""
    if fix:
        list_dir = os.listdir(dir_name)
        for file in list_dir:
            last_index = file[0]
            fix = str(int(last_index) +1)

    frame.to_csv(
        crear_directorio(dir_name)
        + "\\"
        + crear_rotulo_csv(prefix=prefix, suffix=suffix, fix=fix),
    ) 
    

# def descargar_imagen(obj, dir_name="html", prefix="img", suffix=None):
#     """Descarga una figure en formato HTML - Valido para plotly library"""
#     obj.write_html(
#         crear_directorio(dir_name)
#         + "\\"
#         + crear_rotulo_html(prefix=prefix, suffix=suffix),
#         full_html=True,
#     )


# def descargar_objeto(obj, dir_name="objects", prefix="obj", suffix=None):
#     """Descarga un objeto en formato pickle (Serializado)"""
#     global x4

#     path = f"{os.getcwd()}\\{dir_name}"
#     list_dir = os.listdir(path)
#     last_val = 0
#     for nombre in list_dir:
#         if nombre[0].isdigit():
#             last_val = int(nombre[0])
#     x = next(x4)
#     while last_val >= x:
#         x = next(x4)
#     file_name = f"{crear_directorio(dir_name)}\\{crear_rotulo_pickle(prefix=prefix, suffix=suffix, x=x)}"

#     with open(file_name, "wb") as f:
#         pickle.dump(obj, f)


# def cargar_objeto(file_name, dir_name="objects"):
#     """Levanta desde el directorio, un objeto pickle guardado"""
#     file_name = f"{crear_directorio(dir_name)}\\{file_name}"
#     with open(file_name, "rb") as f:
#         obj = pickle.load(f)
#     return obj


def crear_directorio(dir_name):
    if not dir_name.startswith("\\"):
        dir_name = "\\" + dir_name
    path = os.getcwd() + dir_name
    os.makedirs(path, exist_ok=True)
    return path


def string_replace_blank(string):
    return string.replace(" ", "_")


# def crear_rotulo_html(prefix, suffix):
#     global x1
#     if suffix is not None:
#         return f"{next(x1)}_{prefix}_{string_replace_blank(suffix)}.html"
#     return f"{next(x1)}_{prefix}.html"

def crear_rotulo_csv(prefix, suffix, fix=None):
    global x1
    if not fix:
        if suffix is not None:
            return f"{next(x2)}_{prefix}_{string_replace_blank(suffix)}.csv"
        return f"{next(x2)}_{prefix}.csv"
    else:
        if suffix is not None:
            return f"{fix}_{prefix}_{string_replace_blank(suffix)}.csv"
        return f"{fix}_{prefix}.csv"


# def crear_rotulo_pickle(prefix, suffix, x=1):
#     if suffix is not None:
#         return f"{x}_{prefix}_{string_replace_blank(suffix)}.pickle"
#     return f"{x}_{prefix}.pickle"