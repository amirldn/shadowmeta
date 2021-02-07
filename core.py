import os
import time
import ntpath
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
import logging
import PySimpleGUI as sg

shadowplay_dir = "D:\Videos\Shadowplay"
poll_rate = 5

def detectChanges(dirSnapshopRef):
    # hold = input()
    dir_snapshot_new = DirectorySnapshot(path=shadowplay_dir, recursive=True)
    list_of_new_files = DirectorySnapshotDiff(ref=dirSnapshopRef, snapshot=dir_snapshot_new).files_created
    if list_of_new_files:
        logging.info(str(len(list_of_new_files)) + " new file(s) found!")
        for file in list_of_new_files:
            orig_file_name, file_extension = ntpath.splitext(file)
            if file_extension == ".mp4":
                # print("If you would like to rename it, please type a new name for it else leave it empty.")
                logging.info(ntpath.basename(file) + " - asking to rename")
                # rename_gui(file)
                rename_file(file)
            else:
                logging.info(ntpath.basename(file) + " was not a .mp4")
    else:
        logging.info("No new files found - polling in "+str(poll_rate)+" secs")
    return dir_snapshot_new


def rename_file(init_path):
    print("New Shadowplay Found: " + init_path)
    user_new_fn = input("New File Name (leave blank to keep the same)> ")
    new_path = ntpath.dirname(init_path) + "\\" + user_new_fn
    new_fn, user_new_file_ext = ntpath.splitext(new_path)

    if user_new_fn: #if user typed in a file name
        if user_new_file_ext != ".mp4":
            new_path = new_path + ".mp4"
        os.rename(init_path, new_path)
        logging.info("File was renamed from " + ntpath.basename(init_path) + " to " + ntpath.basename(new_path))
    else:
        logging.warning("File was not renamed")


def rename_gui(init_path):
    new_fn, file_ext = ntpath.splitext(init_path)
    form = sg.FlexForm("Rename File: "+new_fn)
    layout = [[sg.Text('New File Name:'), sg.InputText()],
              [sg.OK()]]

    button, (name,) = form.Layout(layout).Read()

def core():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    execute = True
    logging.info("Shadowmeta Launched")
    dir_snapshot_orig = DirectorySnapshot(path=shadowplay_dir, recursive=True)
    dir_snapshot_curr = dir_snapshot_orig
    try:
        while execute:
            time.sleep(poll_rate)
            dir_snapshot_curr = detectChanges(dir_snapshot_curr)
    except Exception as exp:
        logging.error(exp)
    logging.info("End of code reached")

core()

# print(ntpath.basename(init_path)) #gives filename
# print(ntpath.dirname(init_path)) #gives directory name