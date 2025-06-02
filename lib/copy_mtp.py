from win32com.client import Dispatch
from datetime import datetime
import os


def move_files_from_mtp(camera_shell_path, drafts_folder, log_fn=print):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    target_folder = os.path.join(drafts_folder, timestamp)
    os.makedirs(target_folder, exist_ok=False)

    shell = Dispatch("Shell.Application")
    root_folder = shell.Namespace(camera_shell_path)
    if root_folder is None:
        raise Exception(f"Cannot access camera path: {camera_shell_path}")

    def recurse_and_copy(folder, dest_base, rel_path=""):
        items = folder.Items()
        for item in items:
            name = item.Name
            full_rel = os.path.join(rel_path, name)

            if item.IsFolder:
                # Only descend into folders if they are DCIM or inside DCIM
                # This means skipping all other root-level folders except DCIM
                if "DCIM" in full_rel or name == "DCIM":
                    subfolder = item.GetFolder
                    if subfolder is None:
                        log_fn(f"Warning: Could not access folder {full_rel}")
                        continue
                    recurse_and_copy(subfolder, dest_base, full_rel)
                else:
                    # Skip folders outside DCIM
                    continue
            else:
                # Only copy files inside DCIM or subfolders of DCIM
                if "DCIM" in rel_path:
                    dest_dir = os.path.join(dest_base, rel_path)
                    os.makedirs(dest_dir, exist_ok=True)
                    log_fn(f"Copying {name} to {dest_dir}")
                    dest_shell_folder = shell.NameSpace(
                        os.path.abspath(dest_dir))
                    if dest_shell_folder is None:
                        raise Exception(
                            f"Could not access destination shell folder: {dest_dir}")
                    # 16 = Do not display progress dialog, and overwrite existing files
                    dest_shell_folder.CopyHere(item, 16)

    recurse_and_copy(root_folder, target_folder)
    return target_folder
