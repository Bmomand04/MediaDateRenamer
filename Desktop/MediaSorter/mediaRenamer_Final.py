import os
import os.path
import exiftool
import json

#Brishna Momand
#----------------------------------------------------------------------------------------------------------------------------------------
#Media Renamer Script
#This script renames each picture or video to the date it was originally taken/filmed by reading it's EXIF tag
#For example, 'image1' was originally taken May 2, 2025 - 'image1' will be titled 'MAY2_2025' or 'DEC14_2004'. Format : (MONTHDAY_YEAR)
#Makes it a lot more easy and clear to see date of media when scrolling through large folders
#----------------------------------------------------------------------------------------------------------------------------------------

# GUI for mediasorter program
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
import exiftool
import json

selected_files = []
files_count = 0

def open_windows_explorer():
    global selected_files
    global files_count
    tk.Tk().withdraw()
    selected_files = filedialog.askopenfilenames(
        initialdir="C://", title="Select medias"
    )
    files_count = len(selected_files)
    if selected_files:
        status_label.config(text=f"{files_count} files selected")
    else:
        status_label.config(text="No files selected")


def renaming():
    if not selected_files:
        print("No files selected. Please choose files first.")
        return

    files_done = 0
    files_skip = 0

    with exiftool.ExifToolHelper() as et:
        for file_path in selected_files:

            if not os.path.isfile(file_path):
                files_skip += 1
                continue

            filename = os.path.basename(file_path)
            folder_path = os.path.dirname(file_path)
            old_path = file_path

            metadata_str = et.execute("-j", old_path)
            metadata_list = json.loads(metadata_str)

            if not metadata_list:
                files_skip += 1
                print(f"{filename}: No metadata found, skipping")
                continue

            metadata = metadata_list[0]

            date = (
                metadata.get("EXIF:DateTimeOriginal")
                or metadata.get("QuickTime:CreateDate")
            )

            if not date:
                files_skip += 1
                print(f"{filename}: No original date found, skipping")
                continue

            split = date.split(':')

            months_short = {
                '01': 'JAN', '02': 'FEB', '03': 'MAR', '04': 'APR',
                '05': 'MAY', '06': 'JUN', '07': 'JUL', '08': 'AUG',
                '09': 'SEP', '10': 'OCT', '11': 'NOV', '12': 'DEC'
            }

            new_name = ""
            DAY = ""
            UNDERSCORE = "_"

            MONTH = str(split[1])

            DAY_PREV = str(split[2])
            i = 0
            while i < 2:
                DAY += DAY_PREV[i]
                i += 1

            YEAR = str(split[0])

            base_name, EXT = os.path.splitext(filename)
            base_name = base_name.strip()

            new_name += months_short[MONTH]
            new_name += DAY
            new_name += UNDERSCORE
            new_name += YEAR
            new_name += EXT

            new_path = os.path.join(folder_path, new_name)

            base_name = new_name
            count = 1

            while os.path.exists(new_path):
                new_name = f"{base_name}({count}){EXT}"
                new_path = os.path.join(folder_path, new_name)
                count += 1

            if new_path != old_path:
                os.rename(old_path, new_path)
                files_done += 1

    if files_done + files_skip == files_count:
        completion_label.config(
            text=f"Done! Renamed {files_done}, skipped {files_skip}"
        )


window = Tk()
window.geometry("500x500")
window.title("Media Date Namer")

header_title = Label(window, text='This is the Media Date Renamer program!')
header_title.place(x=140, y=30)

header_title2 = Label(window, text='Renamed in format : MONTHDAY_YEAR')
header_title2.place(x=140, y=50)

browse_files = tk.Button(
    window, text='Choose Pictures to Rename',
    width=25, command=open_windows_explorer
)
browse_files.place(x=160, y=120)

status_label = Label(window, text="No files selected")
status_label.place(x=200, y=160)

completion_label = Label(window, text="")
completion_label.place(x=175, y=250)

initiate_renaming = tk.Button(
    window, text='Initiate Renaming!',
    width=25, command=renaming
)
initiate_renaming.place(x=160, y=200)

window.mainloop()

