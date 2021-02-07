import os
import time
import ntpath
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.utils.dirsnapshot import DirectorySnapshot,DirectorySnapshotDiff
import sys
import logging

shadowplay_dir = "D:\Videos\Shadowplay"
execute = True


def rename_file(init_path):
    print("New Shadowplay Found: " + init_path)
    # print(ntpath.basename(init_path)) #gives filename
    # print(ntpath.dirname(init_path)) #gives directory name
    new_file_name=input("New File Name > ")
    new_path = ntpath.dirname(init_path)+"\\"+new_file_name
    print("New path: ",new_path)

    os.rename(init_path, new_path)



if __name__ == "__main__":
    while execute:
        dirSnapshotOrig = DirectorySnapshot(path=shadowplay_dir, recursive=True)
        # hold = input()
        time.sleep(2)
        dirSnapshotNew = DirectorySnapshot(path=shadowplay_dir, recursive=True)
        listOfNewFiles=DirectorySnapshotDiff(ref=dirSnapshotOrig, snapshot=dirSnapshotNew).files_created
        for file in listOfNewFiles:
            print("If you would like to rename it, please type a new name for it else leave it empty.")
            rename_file(file)










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
