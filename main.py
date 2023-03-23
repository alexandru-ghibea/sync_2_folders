"""Implement a program that synchronizes two folders: source and replica.
The program should maintain a full, identical copy of source folder at replica folder"""

# TODO 1: Synchronization must be one-way: after the synchronization content of the replica folder should be modified to
# exactly match content of the source folder;
# TODO 2: Synchronization should be performed periodically.
# TODO 3: File creation/copying/removal operations should be logged to a file and to the console output;
# TODO 4(Done): Folder paths, synchronization interval and log file path should be provided using the command line arguments;
# TODO 5: It is undesirable to use third-party libraries that implement folder synchronization;
# TODO 6: It is allowed (and recommended) to use external libraries implementing other well-known algorithms.
# For example, there is no point in implementing yet another function that calculates MD5 if you need it for the task –
# it is perfectly acceptable to use a third-party (or built-in) library.


import os
import shutil
import argparse
import time
import logging

"""create logger file"""
logging.basicConfig(filename='sync.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

"""Parse command line arguments"""
# TODO 4
parser = argparse.ArgumentParser(description='Synchronize two folders')
parser.add_argument('source', type=str,
                    help='Source folder path')
parser.add_argument('replica', type=str,
                    help='Replica folder path')
parser.add_argument('-i', type=int, default=60,
                    help='Synchronization interval in seconds (default: 60)')
args = parser.parse_args()


"""Check if source and replica folders exist"""
if not os.path.isdir(args.source):
    print(f'Error: {args.source} is not a valid folder path')
    logging.error(f'Source folder - {args.source} - does not exist')
    exit(1)
if not os.path.isdir(args.replica):
    print(f'Error: {args.replica} is not a valid folder path')
    logging.error(f'Source folder - {args.replica} - does not exist')
    exit(1)


def sync_folder(source_path, replica_path):
    ''' Synchronize source folder with replica folder '''
    files_modified = []
    for root, dirs, files in os.walk(source_path):
        replica_root = os.path.join(
            replica_path, os.path.relpath(root, source_path))
        if not os.path.isdir(replica_root):
            os.makedirs(replica_root)
        for file in files:
            source_file_path = os.path.join(root, file)
            replica_file_path = os.path.join(replica_root, file)
            source_stat = os.stat(source_file_path)
            replica_stat = os.stat(replica_file_path) if os.path.exists(
                replica_path) else None
            if replica_stat is None or source_stat.st_mtime > replica_stat.st_mtime:
                shutil.copy2(source_file_path, replica_file_path)
                files_modified.append(file)
                log_operation(
                    'create' if replica_stat is None else 'modify', replica_file_path)
            for replica_file in os.listdir(replica_root):
                pass
    return files_modified


def log_operation(operation, path):
    message = logging.info(f'{operation} - {path}')
    print(message)


while True:
    sync_folder(args.source, args.replica)
    time.sleep(args.i)
