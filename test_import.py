# test_import.py
from lib.import_files import move_files 
import os

# Setup test paths
camera_folder = "test_data/fake_camera"
drafts_folder = "test_data/drafts"

# Create test camera folder with dummy files
os.makedirs(camera_folder, exist_ok=True)
os.makedirs(drafts_folder, exist_ok=True)

# Add fake files
for i in range(3):
    with open(os.path.join(camera_folder, f"video{i}.mp4"), "w") as f:
        f.write("fake content")

# Run import
result = move_files(camera_folder, drafts_folder)
print(result)

# Clean up after test (optional)
# shutil.rmtree("test_data")
