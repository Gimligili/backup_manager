import os
import shutil
import filecmp
from multiprocessing import Pool, cpu_count
import customtkinter
from tkinter import filedialog as fd

########################################################################################################################
#######################################################   DATA   #######################################################
########################################################################################################################

class DecryptError(Exception):
    def __init__(self, message="decryption process error"):
        self.message = message
        super().__init__(self.message)


customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('700x700')
root.title('Gestionnaire de sauvegarde pour Papilou')


source_folder = ""
destination_folder=""
########################################################################################################################
#######################################################   UTILS   ######################################################
########################################################################################################################

def on_quit():
    root.destroy()

def copy_file(args):
    source_path, relative_path, destination_path = args

    if os.path.exists(destination_path) and filecmp.cmp(source_path, destination_path, shallow=False):
        print(f"Skipping {relative_path} (already exists and is identical)")
        return

    shutil.copy2(source_path, destination_path)
    print(f"Copied {relative_path}")

def copy_files(source_folder, destination_folder):
    if not os.path.exists(source_folder) or not os.path.exists(destination_folder):
        print("Source or destination folder does not exist.")
        return

    pool = Pool(processes=cpu_count())  # Use the maximum number of cores available

    tasks = []

    for root, _, files in os.walk(source_folder):
        for file in files:
            source_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_path, source_folder)
            destination_path = os.path.join(destination_folder, relative_path)

            tasks.append((source_path, relative_path, destination_path))

    pool.map(copy_file, tasks)

    pool.close()
    pool.join()


########################################################################################################################
######################################################   PROCESS  ######################################################
########################################################################################################################


def select_folder_src():
    global source_folder
    try:
        user_home = os.path.expanduser("~")  # Get the user's home directory
        image_folder = os.path.join(user_home, "Pictures")
        initial_dir = image_folder if os.path.exists(image_folder) else user_home
        folder_path = fd.askdirectory(title="Dossier source", mustexist=True, initialdir=initial_dir)
        if folder_path:
            source_folder = folder_path
            root.update()
            print("Selected Folder:", folder_path)
    

    except Exception as e:
        output_label.configure(text="Une erreur s'est produite : {}".format(e), text_color='darkred', font=('Roboto', 24))
        root.update()
        print("Une erreur s'est produite : {}".format(e))

def select_folder_dst():
    global destination_folder
    try:
        user_home = os.path.expanduser("~")  # Get the user's home directory
        image_folder = os.path.join(user_home, "Pictures")
        initial_dir = image_folder if os.path.exists(image_folder) else user_home
        folder_path = fd.askdirectory(title="Dossier destination", mustexist=True, initialdir=initial_dir   )
        if folder_path:
            destination_folder = folder_path
            root.update()
            print("Selected Folder:", folder_path)
    

    except Exception as e:
        output_label.configure(text="Une erreur s'est produite : {}".format(e), text_color='darkred', font=('Roboto', 24))
        root.update()
        print("Une erreur s'est produite : {}".format(e))

def help_window(message):
    alert_window = customtkinter.CTkToplevel(root)
    alert_window.title("Mode d'emploi")
    alert_window.overrideredirect(True)
    alert_window.transient(root)
    root_x, root_y = root.winfo_x(), root.winfo_y()
    root_width, root_height = root.winfo_width(), root.winfo_height()
    alert_width, alert_height = 400, 400  # Set your desired width and height
    center_x = root_x + (root_width - alert_width) // 2
    center_y = root_y + (root_height - alert_height) // 2
    alert_window.geometry(f"{alert_width}x{alert_height}+{center_x}+{center_y}")
    alert_window.configure(bd=4, relief=customtkinter.GROOVE)  # You can adjust the bd and relief values
    
    
    label = customtkinter.CTkLabel(alert_window, text=message)
    label.pack(padx=20, pady=20)
    
    ok_button = customtkinter.CTkButton(alert_window, text="OK", command=alert_window.destroy)
    ok_button.pack(pady=10)


########################################################################################################################
########################################################   UI   ########################################################
########################################################################################################################

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=10, padx=60, fill='both', expand=True)


frame_title = customtkinter.CTkLabel(master=frame, text="Gestionnaire de sauvegarde", text_color='#1B8DCF',font=('Roboto', 40))
frame_title.pack(pady=15, padx=10)


source_label_title = customtkinter.CTkLabel(master=frame, text="Choisissez un dossier source 📤", font=('Roboto', 20))
source_label_title.pack(pady=10, padx=10)


source_folder_button = customtkinter.CTkButton(master=frame, text='Parcourir les fichiers', command=select_folder_src)
source_folder_button.pack(pady=10)

destination_label_title = customtkinter.CTkLabel(master=frame, text="Choisissez un dossier destination 📥", font=('Roboto', 20))
destination_label_title.pack(pady=10, padx=10)

destination_folder_button = customtkinter.CTkButton(master=frame, text='Parcourir les fichiers', command=select_folder_dst)
destination_folder_button.pack(pady=10)

file_path_label = customtkinter.CTkLabel(master=frame, text='Dossiers selectionnés :\n\nSource : {0}\nDestination : {1}'.format(source_folder, destination_folder), font=('Roboto', 20))
file_path_label.pack(pady=20)

output_label = customtkinter.CTkLabel(master=frame, text="\n\n", font=('Roboto', 24))
output_label.pack(pady = 10)


backup_button = customtkinter.CTkButton(master=root, text='Effectuer la sauvegarde', command=on_quit, state=customtkinter.DISABLED, fg_color='darkgreen')
backup_button.pack(pady = 10)

custom_alert_button = customtkinter.CTkButton(root, text="Mode d'Emploi", command=lambda: help_window("This is a custom alert!"))
custom_alert_button.pack(side='left', padx=10, pady=10, anchor='sw')

quit_button = customtkinter.CTkButton(master=root, text='Quitter', command=on_quit, fg_color='darkred', hover_color='#CC0000')
quit_button.pack(side='right', padx=10, pady=10, anchor='se')

root.mainloop()

