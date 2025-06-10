from dataclasses import dataclass
from typing import List
import os
import shutil
from datetime import datetime
import time


@dataclass
class FileObject:
    """
    Represents a file object with its path, name, and size.
    """
    path: str
    name: str
    size: int


def move_files_from_filesystem(camera_folder, drafts_folder, progress_callback=None):
    """
    Move files from the camera folder to a drafts folder, preserving the folder structure.
    """

    # check if camera folder exists
    if not os.path.exists(camera_folder):
        raise FileNotFoundError(
            f"Camera folder does not exist: {camera_folder}")

    # create unique timestamp to handle multiple transfers per day
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    target_folder = os.path.join(drafts_folder, timestamp)

    os.makedirs(target_folder, exist_ok=False)

    total_files = sum(len(files) for _, _, files in os.walk(camera_folder))
    copied_files = 0

    # copy all files from target to dest
    for root, dirs, files in os.walk(camera_folder):
        # preserve subfolder structure
        rel_path = os.path.relpath(root, camera_folder)
        dest_path = os.path.join(target_folder, rel_path)
        os.makedirs(dest_path, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_path, file)
            shutil.copy2(src_file, dst_file)
            # test sleep
            time.sleep(3)

            copied_files += 1
            if progress_callback:
                percent_complete = int((copied_files / total_files) * 100)
                progress_callback(percent_complete)

    return target_folder


def delete_files_from_filesystem(camera_folder, progress_callback=None):
    """
    Delete all files from the camera folder.
    """
    # check if camera folder exists
    if not os.path.exists(camera_folder):
        raise FileNotFoundError(
            f"Camera folder does not exist: {camera_folder}")

    # delete all files in the camera folder
    total_files = sum(len(files) for _, _, files in os.walk(camera_folder))
    deleted_files = 0
    for root, dirs, files in os.walk(camera_folder):
        for file in files:
            src_file = os.path.join(root, file)
            os.remove(src_file)
            deleted_files += 1
            if progress_callback:
                percent_complete = int((deleted_files / total_files) * 100)
                progress_callback(percent_complete)

    return camera_folder


def read_files_from_filesystem(camera_folder) -> List[FileObject]:
    """
    Read all files from the camera folder.
    """
    # check if camera folder exists
    if not os.path.exists(camera_folder):
        raise FileNotFoundError(
            f"Camera folder does not exist: {camera_folder}")

    files_list = []
    for root, dirs, files in os.walk(camera_folder):
        for file in files:
            path = os.path.join(root, file)
            name = os.path.basename(path)
            file_size = os.path.getsize(path)

            files_list.append(FileObject(
                path=path,
                name=name,
                size=format_size(file_size)
            ))

    return files_list


def format_size(size_in_bytes: int) -> str:
    """
    Format size in bytes to a human-readable string.
    """
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 ** 2:
        return f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024 ** 3:
        return f"{size_in_bytes / (1024 ** 2):.2f} MB"
    else:
        return f"{size_in_bytes / (1024 ** 3):.2f} GB"
