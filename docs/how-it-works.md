# How It Works

This page explains the internal mechanics of how `rolesnap` collects files and creates a snapshot.

## 1. File Collection

When you run a command like `rolesnap role <name>`, the process begins by collecting a list of files:

1.  **Resolve Roots**: The tool first identifies the root paths for each category (e.g., `Internal Logic`, `Collected Domain`) based on your `rolesnap.yaml`.
2.  **Efficient Traversal**: It then performs an efficient, top-down directory walk (`os.walk`) starting from these roots. This allows the tool to prune (i.e., not descend into) entire directory trees that match an exclusion pattern, significantly speeding up the scan on large projects.
3.  **Deduplication**: All collected file paths are resolved to their absolute paths, and any duplicates are removed.

## 2. File Exclusion

During the directory traversal, a series of filters are applied to exclude irrelevant files and directories:

- **`exclude_dirs` Patterns**: The tool checks if a directory or file matches any of the **glob patterns** in `settings.exclude_dirs`. The matching is performed against both the full relative path (e.g., `**/__pycache__/**`) and against individual path segments (e.g., `.venv`, `*.log`). This check is done without resolving symlinks, ensuring that directories like a symlinked `.venv` are correctly excluded.

- **Default Exclusions**: `rolesnap` comes with a comprehensive default list of exclusions for common caches (`__pycache__`, `.mypy_cache`), build artifacts (`*.egg-info`), logs, and various media file types (`.png`, `.jpg`, `.mp4`, etc.).

- **Output File**: The snapshot output file itself (e.g., `rolesnap.json`) is always excluded to prevent it from including itself in the next run.

## 3. Content Handling

For every file that passes the exclusion filters, its content is read and processed:

- **`--max-file-size`**: The tool first checks the file's size on disk. If it's larger than the value of this flag (default 2 MiB), the file is not read at all. Instead, its content is replaced with the marker `"<skipped_large_file>"`.

- **`--hide-files`**: If you use this flag, the tool does not read the file content. The value for the file in the final JSON will simply be the string `"<hidden>"`.

- **Default Read**: If the file is not skipped or hidden, it is read as a UTF-8 encoded text file.

- **Unicode Errors**: If a file cannot be decoded as UTF-8, it is silently skipped.

- **Empty Directories**: If a path specified in a role is a directory that turns out to be empty (or only contains excluded files), it will be represented by an entry with the marker `"<empty_dir>"`.

Finally, all the collected file paths and their processed content are organized into the category map and written to the output JSON file.
