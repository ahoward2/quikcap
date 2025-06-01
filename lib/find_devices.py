import os

def list_volume_contents(volume_path):
    if os.path.exists(volume_path):
        print(f"Contents of {volume_path}:")
        for item in os.listdir(volume_path):
            item_path = os.path.join(volume_path, item)
            if os.path.isfile(item_path):
                print(f"- {item} (file, {os.path.getsize(item_path)} bytes)")
            elif os.path.isdir(item_path):
                print(f"- {item} (directory)")
    else:
        print(f"Error: Volume path '{volume_path}' does not exist.")

# Example Usage
# volume_path = "/Volumes/Macintosh HD" # Example for macOS, adjust accordingly
# list_volume_contents(volume_path)