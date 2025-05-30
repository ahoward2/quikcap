import os
import shutil
from datetime import datetime

def move_files(camera_folder, drafts_folder):
  # create unique timestamp for folder name
  timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
  target_folder = os.path.join(drafts_folder, timestamp)

  # make the folder
  os.makedirs(target_folder, exist_ok=False)

  #copy all files from target to dest
  for root, dirs, files in os.walk(camera_folder):
    #preserve subfolder structure
    rel_path = os.path.relpath(root, camera_folder)
    dest_path = os.path.join(target_folder, rel_path)
    os.makedirs(dest_path, exist_ok=True)

    for file in files:
        src_file = os.path.join(root, file)
        dst_file = os.path.join(dest_path, file)
        shutil.copy2(src_file, dst_file)

  return target_folder

def delete_files(camera_folder):
  # remove files from camera

  for root, dirs, files in os.walk(camera_folder):
      for file in files:
         src_file = os.path.join(root, file)
         os.remove(src_file) 

  return camera_folder