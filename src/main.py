import os
import subprocess
from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from loguru import logger

logger.add('./logs/info.log')


def compile_tex_to_pdf(tex_file):
    # 获取文件所在的目录
    tex_file_path = Path(tex_file)
    directory = tex_file_path.parent.absolute()
    # 保存当前工作目录，以便稍后恢复
    current_dir = os.getcwd()
    try:
        # 切换到文件所在的目录
        os.chdir(directory)

        command = ['latexmk', '-pdf', tex_file_path.name]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            logger.error(f"Error occurred while compiling {tex_file}: error code :{result.stderr}")
        else:
            logger.info(f"Successfully compiled {tex_file}")
    finally:
        # 恢复之前的工作目录
        os.chdir(current_dir)


class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_modified_time = {}

    def on_created(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith('.tex'):
            compile_tex_to_pdf(event.src_path)
            logger.info(f'File created: {event.src_path}')

    def on_modified(self, event):
        if event.is_directory:
            return
        elif event.src_path.endswith('.tex'):
            # 防抖
            current_time = time.time()
            last_modified_time = self.last_modified_time.get(event.src_path, 0)
            if current_time - last_modified_time > 2:  # Ignore modifications within 1 second
                logger.info(f'File modified: {event.src_path}')
                compile_tex_to_pdf(event.src_path)
                self.last_modified_time[event.src_path] = current_time


if __name__ == "__main__":
    path = "file"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
