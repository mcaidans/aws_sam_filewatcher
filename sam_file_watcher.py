import sys
import os
import time
import shutil
import argparse
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

class SamHandler(FileSystemEventHandler):

    IGNORED_DIRS = [
        '.idea',
        '.aws-sam'
    ]

    def __init__(self, target_path=None, sam_path=None):
        super().__init__()
        self.sam_path = sam_path.rstrip('\\').rstrip('/') + '/'

        self.target_path = target_path

    def on_modified(self, event):
        if not event.is_directory and not event.src_path[-1] == '~':
            if event.src_path.split('\\')[1] not in self.IGNORED_DIRS:
                dest_path = self.sam_path + event.src_path.replace(self.target_path, '').lstrip('\\')
                print("Copying File: \n\tSource:{src} \n\tDest:{dest} ".format(src=event.src_path, dest=dest_path))
                shutil.copy(event.src_path, dest_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', help='Relative Path to the directory to watch. Defaults to directory run in.')
    parser.add_argument('--sam_path', help='Relative path to sam build folder')
    parser.add_argument('--proj_name', help='Name of the folder in the SAM build directory. Defaults to name of directory --target points to.')

    args = parser.parse_args()

    # Configure SAM Build Folder Path
    path = args.target if args.target else '.'
    print(args.proj_name)
    print(path)
    if args.proj_name:
        project_name = args.proj_name
    elif path == '.':
        file_path = os.path.realpath(__file__)
        project_name = os.getcwd().split('\\')[-1]
        print(os.getcwd())
    else:
        print('here')
        project_name = path.split('\\')[-1]
        print(project_name)

    sam_build_folder = args.sam_path if args.sam_path else './.aws-sam'
    sam_build_folder += '/build/'+project_name

    print("Watching folder: \n\t{folder}. \nSam Directory: \n\t{sam}".format(folder=os.path.abspath(path), sam=os.path.abspath(sam_build_folder)))

    event_handler = SamHandler(sam_path=sam_build_folder, target_path=path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
