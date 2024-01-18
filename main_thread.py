import argparse
import logging
import time
from pathlib import Path
from shutil import copyfile
from threading import Thread

start_time = time.time()
"""
python main.py --source -s picture
python main.py --output -o dist
"""

parser = argparse.ArgumentParser(description='App for sort deka')

parser.add_argument('-s', '--source', required=True)
parser.add_argument('-o', '--output', default='dist')
args = vars(parser.parse_args())
source = args.get("source")
output = args.get("output")

folders = []


def scan_folder(path: Path):
    for element in path.iterdir():
        if element.is_dir():
            folders.append(element)
            scan_folder(element)


def sort_file(path: Path):
    for el in path.iterdir():
        if el.is_file():
            sfx = el.suffix
            new_path = output_folder / sfx
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as e:
                logging.error(e)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    base_folder = Path(source)
    output_folder = Path(output)
    folders.append(base_folder)
    scan_folder(base_folder)
    threads = []
    for folder in folders:
        th = Thread(target=sort_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    end_time = time.time()
    finish = end_time-start_time
    print(finish)
    with open("з_потоками.txt", "w") as file:
        file.write(f"Час виконання скрипта: {finish} секунд")
