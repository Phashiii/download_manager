from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move

from time import sleep
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

dest_dir_music = '/home/phashcentral/Music'
dest_dir_pictures = '/home/phashcentral/Pictures'
dest_dir_videos = '/home/phashcentral/Videos'
dest_dir_docs = '/home/phashcentral/Documents'
source_dir = "/home/phashcentral/Downloads"

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    while exists(f'{dest}/{name}'):
        name = f"{filename}({str(counter)}){extension}"
        counter +=1
    return name + ''

def move_file(dest, entry, name):
    file_exists = exists(dest + '/' + name)
    #Check wheteher file name is alreadytaken in destination folder
    if file_exists:
        unique_name = make_unique(dest, name)
        rename(entry, unique_name)
    move(entry, dest)

class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        #This goes through fies in the source_dir folder
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if name.endswith('.wav') or name.endswith('.mp3'):
                    dest = dest_dir_music
                    move_file(dest, entry, name)
                elif name.endswith('.mp4') or name.endswith('.mov'):
                    dest = dest_dir_videos
                    move_file(dest, entry, name)
                elif name.endswith('jpg') or name.endswith('.png') or name.endswith('.gif') or name.endswith('.jpeg'):
                    dest = dest_dir_pictures
                    move_file(dest, entry, name)
                else:
                    dest = dest_dir_docs
                    move_file(dest, entry, name)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()