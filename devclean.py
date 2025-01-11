import os
import argparse
import time
import shutil

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

def get_dir_size(path):
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                continue
    return total

def format_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}"
        bytes /= 1024
    return f"{bytes:.2f}TB"

def is_project_directory(path):
    for project, config in PROJECT_TYPES.items():
        if any(os.path.isfile(os.path.join(path, marker)) for marker in config["marker_files"]):
            return project
    return None

def cleanup_artifacts(root_dir, dry_run=False):
    cleaned = 0
    total_size = 0
    
    print(f"\nScanning {root_dir}...")
    for current_dir, _, _ in os.walk(root_dir):
        project_type = is_project_directory(current_dir)
        if not project_type:
            continue
            
        for artifact_dir in PROJECT_TYPES[project_type]["artifact_dirs"]:
            artifact_path = os.path.join(current_dir, artifact_dir)
            if not os.path.exists(artifact_path):
                continue
                
            size = get_dir_size(artifact_path)
            total_size += size
            cleaned += 1
            
            action = "Would remove" if dry_run else "Removing"
            print(f"{action} {artifact_path} ({format_size(size)})")
            
            if not dry_run:
                shutil.rmtree(artifact_path)
    
    return cleaned, total_size

def main():
    parser = argparse.ArgumentParser(description='Clean build artifacts from projects')
    parser.add_argument('directory', help='Root directory to clean')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be deleted without actually deleting')
    args = parser.parse_args()
    
    start_time = time.time()
    cleaned, total_size = cleanup_artifacts(args.directory, args.dry_run)
    duration = time.time() - start_time
    
    print(f"\nSummary:")
    print(f"Cleaned {cleaned} directories")
    print(f"Freed up {format_size(total_size)}")
    print(f"Time taken: {duration:.2f} seconds")

if __name__ == "__main__":
    main()