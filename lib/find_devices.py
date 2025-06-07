import win32file
import win32com.client
import win32api


def get_connected_devices():
    shell = win32com.client.Dispatch("Shell.Application")
    namespace = shell.NameSpace(17)  # This PC

    devices = []

    # First get shell devices (MTP, etc)
    for i in range(namespace.Items().Count):
        item = namespace.Items().Item(i)
        name = item.Name
        path = item.Path

        if item.IsFolder:
            # Check if MTP device: path is shell id (starts with ::)
            if path.startswith("::{"):
                connection_type = "MTP"
            else:
                # Could be USB mass storage or network share, we'll check later
                connection_type = "Unknown"

            devices.append((name, path, connection_type))

    # Also check mounted drives for USB mass storage
    drives = win32api.GetLogicalDriveStrings().split('\000')
    drives = [d for d in drives if d]

    for d in drives:
        # Skip system drives
        if d.startswith("C:"):
            continue

        # Check drive type
        drive_type = win32file.GetDriveType(d)
        # DRIVE_REMOVABLE = 2, DRIVE_FIXED = 3, DRIVE_REMOTE = 4, DRIVE_CDROM = 5, DRIVE_RAMDISK = 6
        if drive_type == 2 or drive_type == 3:
            # Check if drive has a volume label that suggests camera
            try:
                vol_name = win32api.GetVolumeInformation(d)[0]
            except:
                vol_name = ""

            # Simple heuristic to detect Sony or other camera
            if "SONY" in vol_name.upper():
                devices.append((f"{vol_name} ({d})", d, "USB Mass Storage"))

    return devices
