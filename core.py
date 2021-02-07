import os
import time
import ntpath
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot, DirectorySnapshotDiff
import sys
import logging

# Exclude .tmp files

shadowplay_dir = "D:\Videos\Shadowplay"


def detectChanges(dirSnapshopRef):
    # hold = input()
    time.sleep(2)
    dir_snapshot_new = DirectorySnapshot(path=shadowplay_dir, recursive=True)
    list_of_new_files = DirectorySnapshotDiff(ref=dirSnapshopRef, snapshot=dir_snapshot_new).files_created
    if list_of_new_files:
        logging.info(str(len(list_of_new_files))+" new file(s) found!")
        for file in list_of_new_files:
            orig_file_name, file_extension = ntpath.splitext(file)
            if file_extension == ".mp4":
                # print("If you would like to rename it, please type a new name for it else leave it empty.")
                logging.info(ntpath.basename(file)+" - asking to rename")
                rename_file(file)
            else:
                logging.info(ntpath.basename(file)+" was not a .mp4")

    else:
        logging.info("No new files found, rerunning...")
    return dir_snapshot_new


def rename_file(init_path):
    print("New Shadowplay Found: " + init_path)
    # print(ntpath.basename(init_path)) #gives filename
    # print(ntpath.dirname(init_path)) #gives directory name

    new_file_name = input("New File Name > ")
    new_path = ntpath.dirname(init_path) + "\\" + new_file_name

    new_file_name, new_file_extension = ntpath.splitext(new_path)
    print("New extension: ", new_file_extension)

    if new_file_name:
        if new_file_extension!=".mp4":
            new_path = new_path+".mp4"

        os.rename(init_path, new_path)
        logging.info("File was renamed from " + ntpath.basename(init_path) + " to " + ntpath.basename(new_path))
    else:
        logging.warning("File was not renamed")


def core():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    event_handler = LoggingEventHandler()
    execute = True
    logging.info("Code executed")
    dir_snapshot_orig = DirectorySnapshot(path=shadowplay_dir, recursive=True)
    dir_snapshot_curr = detectChanges(dir_snapshot_orig)
    try:
        while execute:
            dir_snapshot_curr = detectChanges(dir_snapshot_curr)
    except KeyboardInterrupt:
        execute = False
        logging.warning("Keyboard Interrupt")
    logging.info("End of code reached")


core()

# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO,
#                         format='%(asctime)s - %(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S')
#     event_handler = LoggingEventHandler()
#     observer = Observer()
#     observer.schedule(event_handler, path=shadowplay_dir, recursive=True)
#     observer.start()
#     try:
#         while observer.isAlive():
#             observer.join(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
