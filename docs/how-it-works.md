# How It Works

This page explains the internal mechanics of how `rolesnap` collects files and creates a snapshot.

## 1. File Collection

When you run a command like `rolesnap role <name>`, the process begins by collecting a list of files:

1.  **Resolve Roots**: The tool first identifies the root paths for each category (e.g., `Internal Logic`, `Collected Domain`) based on your `rolesnap.yaml`.
2.  **Recursive Scan**: It then performs a recursive scan (`rglob`) within these root paths to find all files.
3.  **Deduplication**: All collected file paths are resolved to their absolute paths, and any duplicates are removed.

## 2. File Exclusion

Once the initial list of files is gathered, a series of filters are applied to exclude irrelevant files:

- **Binary Extensions**: Files with common binary extensions are ignored. This is because they are not useful as text-based context for an LLM. The list includes (but is not limited to): `.png`, `.jpg`, `.gif`, `.pdf`, `.doc`, `.zip`, `.tar`, `.gz`, `.pyc`, `.ipynb`.

- **`exclude_dirs`**: The tool checks if any part of a file's absolute path contains a name from the `settings.exclude_dirs` list in your configuration. For example, if `exclude_dirs` contains `"node_modules"`, then any file path like `/path/to/project/node_modules/library/file.js` will be excluded.

- **Output File**: The snapshot output file itself (e.g., `rolesnap.json`) is always excluded to prevent it from including itself in the next run.

- **Gitignore**: In a Git repository, files and directories matching patterns in `.gitignore` may also be excluded.

## 3. Content Handling

For every file that passes the exclusion filters, its content is read and processed:

- **Default**: The file is read as a UTF-8 encoded text file.

- **`--max-bytes`**: If you provide this flag (e.g., `--max-bytes 50000`), the tool will read the file, but if the content exceeds the specified number of bytes, it will be truncated. This is a safety measure to prevent snapshots from becoming excessively large.

- **`--hide-files`**: If you use this flag, the tool does not read the file content at all. Instead, the value for the file in the final JSON will simply be the string `"<hidden>"`.

- **Unicode Errors**: If a file cannot be decoded as UTF-8, it is silently skipped.

Finally, all the collected file paths and their processed content are organized into the category map and written to the output JSON file.
