import os
import argparse
import time
import shutil
from tqdm import tqdm

# Define project types and their artifact directories
PROJECT_TYPES = {
    "node": {
        "marker_files": ["package.json"],
        "artifact_dirs": ["node_modules"],
    },
    "java_gradle": {
        "marker_files": ["build.gradle"],
        "artifact_dirs": ["build", "target"],
    },
    "java_maven": {
        "marker_files": ["pom.xml"],
        "artifact_dirs": ["target"],
    },
    "rust": {
        "marker_files": ["Cargo.toml"],
        "artifact_dirs": ["target"],
    },
}

# Check if a directory contains any marker files of a project type
def is_project_directory(path):
    for project, config in PROJECT_TYPES.items():
        if any(os.path.isfile(os.path.join(path, marker)) for marker in config["marker_files"]):
            return project
    return None

# Get size of a directory
def get_directory_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total_size += os.path.getsize(fp)
    return total_size

# Recursively find directories to clean
def find_directories_to_clean(base_path):
    directories_to_clean = []

    print("\nScanning directories...")
    time.sleep(1)

    for root, dirs, _ in tqdm(os.walk(base_path), desc="Searching", unit=" dirs"):
        # Identify and mark artifact directories for cleaning
        artifact_dirs = sum((config["artifact_dirs"] for config in PROJECT_TYPES.values()), [])
        for d in list(dirs):
            if d in artifact_dirs:
                directories_to_clean.append(os.path.join(root, d))
                dirs.remove(d)  # Exclude artifact directories from further traversal

        project_type = is_project_directory(root)
        if project_type:
            # Add artifact directories to the list
            for artifact_dir in PROJECT_TYPES[project_type]["artifact_dirs"]:
                artifact_path = os.path.join(root, artifact_dir)
                if os.path.exists(artifact_path):
                    if artifact_path not in directories_to_clean:
                        directories_to_clean.append(artifact_path)

    return directories_to_clean

# Main function
def main():
    parser = argparse.ArgumentParser(description="DevClean: Clean artifact directories in project folders.")
    parser.add_argument("path", help="Base path to scan for project folders.")
    args = parser.parse_args()

    base_path = args.path

    if not os.path.isdir(base_path):
        print(f"Error: Path '{base_path}' is not a valid directory.")
        return

    directories_to_clean = find_directories_to_clean(base_path)

    total_size = 0
    print(f"\nDeleting {len(directories_to_clean)} artifact directories...")
    for directory in directories_to_clean:
        size = get_directory_size(directory)
        total_size += size
        shutil.rmtree(directory)
        print(f"Deleting {directory} ({size / (1024 * 1024):.2f} MB)")

    print(f"\nSuccessfully deleted {len(directories_to_clean)} directories with a total size of {total_size / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    main()
