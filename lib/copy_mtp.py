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

    def recurse_until_dcim(folder, rel_path=""):
        items = folder.Items()
        for item in items:
            name = item.Name
            full_rel = os.path.join(rel_path, name)

            if item.IsFolder:
                if name.upper() == "DCIM":
                    dcim_folder = shell.Namespace(
                        os.path.join(camera_shell_path, full_rel))
                    if dcim_folder is not None:
                        return dcim_folder, full_rel
                    else:
                        log_fn(f"Failed to access DCIM path: {full_rel}")
                        return None, None
                else:
                    subfolder = shell.Namespace(
                        os.path.join(camera_shell_path, full_rel))
                    if subfolder is not None:
                        found, path = recurse_until_dcim(subfolder, full_rel)
                        if found:
                            return found, path
                    else:
                        log_fn(f"Skipping inaccessible folder: {full_rel}")
        return None, None

    def recurse_and_copy(folder, dest_base, rel_path=""):
        items = folder.Items()
        for item in items:
            name = item.Name
            full_rel = os.path.join(rel_path, name)

            if item.IsFolder:
                try:
                    subfolder_path = os.path.join(camera_shell_path, full_rel)
                    subfolder = shell.Namespace(subfolder_path)
                    if subfolder is None:
                        log_fn(f"Warning: Could not access folder {full_rel}")
                        continue
                    recurse_and_copy(subfolder, dest_base, full_rel)
                except Exception as e:
                    log_fn(f"Error accessing subfolder {full_rel}: {e}")
            else:
                dest_dir = os.path.join(dest_base, rel_path)
                os.makedirs(dest_dir, exist_ok=True)
                log_fn(f"Copying {name} to {dest_dir}")
                dest_shell_folder = shell.NameSpace(dest_dir)
                if dest_shell_folder is None:
                    raise Exception(
                        f"Could not access destination shell folder: {dest_dir}")
                dest_shell_folder.CopyHere(item, 16)  # 16 = No UI, overwrite
                log_fn(f"Copied {name} to {dest_dir}")

    dcim_folder, rel_path = recurse_until_dcim(root_folder)
    if dcim_folder is None:
        raise Exception("No DCIM folder found on the device.")
    log_fn(f"Found DCIM folder: {rel_path}")
    recurse_and_copy(dcim_folder, target_folder, rel_path)

    return target_folder
