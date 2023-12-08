import subprocess
import sys
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class BotHandler(FileSystemEventHandler):
    def __init__(self, process_name):
        self.process_name = process_name

    def on_modified(self, event):
        if event.is_directory:
            return
        print(f'File {event.src_path} has been modified. Restarting bot...')
        self.restart_bot()

    def restart_bot(self):
        for process in psutil.process_iter(['pid', 'cmdline']):
            if self.process_name in process.info['cmdline']:
                process.terminate()
                break
        subprocess.run([sys.executable, self.process_name])


if __name__ == "__main__":
    main_bot_script = 'ride.py'

    event_handler = BotHandler(main_bot_script)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        subprocess.run([sys.executable, main_bot_script])
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
