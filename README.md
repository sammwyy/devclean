# DevClean 🚀

**DevClean** is a Python tool designed to clean up artifact directories in your development projects. It scans your project folders for build artifacts and lists them for removal, helping you reclaim disk space and keep your projects tidy! ✨

---

## Features 🌟

- **Detects Multiple Project Types**:
  - Node.js projects (`node_modules`)
  - Java (Gradle/Maven) projects (`build`, `target`)
  - Rust projects (`target`)
- **Custom Recursive Search**: Efficiently scans directories while excluding ignored folders.
- **Disk Space Calculation**: Calculates and displays the total space occupied by artifacts.
- **User-Friendly Output**: Includes animations and progress indicators. 📊

---

## Usage 💻

1. Clone the repository and navigate to the project directory:

   ```bash
   git clone https://github.com/sammwyy/devclean.git
   cd devclean
   ```

2. Run the tool:

   ```bash
   python devclean.py /path/to/your/projects
   ```

3. Example output:

   ```text
   Scanning directories...
   Searching: 28791 dirs [00:08, 3504.47 dirs/s]

   Deleting 104 artifact directories...
   Deleting /projects/hello_world/target (7.14 MB)
   Deleting /projects/foobar/node_modules (23.94 MB)
   ... (omitted for brevity)

   Successfully deleted 104 directories with a total size of 51461.42 MB
   ```

---

## How It Works ⚙️

1. **Identify Project Types**: DevClean checks for marker files like `package.json`, `build.gradle`, `pom.xml`, and `Cargo.toml` to determine the project type.
2. **Locate Artifact Directories**: Each project type has predefined directories (e.g., `node_modules`, `build`, `target`) that are marked for cleaning.
3. **Exclude Irrelevant Folders**: Custom directory traversal ensures ignored directories are not scanned internally, saving time and resources.
4. **Deletion**: Artifacts are identified and deleted, freeing up disk space.

---

## Future Features 🛠️

- **Analysis**: Provide insights into the artifacts that are being deleted, such as file counts and sizes.
- **Logging**: Option to save logs to a file for further analysis.
- **Configuration File**: Allow users to define custom project types and artifact directories.

---

## Contributing 🤝

Contributions are welcome! If you'd like to add features or improve the code, feel free to open a pull request.

---

## License 📜

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments 🙌

Thanks to the open-source community for inspiration and tools like `tqdm` for progress visualization. ❤️
