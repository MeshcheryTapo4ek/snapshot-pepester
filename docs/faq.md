# FAQ (Frequently Asked Questions)

### Why is a file missing from my snapshot?

There are several common reasons a file might not appear in your snapshot:

1.  **It's in `exclude_dirs`**: Check the `settings.exclude_dirs` list in your `rolesnap.yaml`. If any part of the file's path matches an entry in this list (e.g., `node_modules`), it will be skipped.

2.  **It has a binary extension**: `rolesnap` is designed for source code and ignores common binary file types by default (e.g., `.png`, `.jpg`, `.pdf`, `.zip`).

3.  **It's ignored by Git**: If your project is a Git repository, `rolesnap` may respect the patterns in your `.gitignore` file.

4.  **It's not part of the role**: Double-check the paths in your role definition. The file must be located under one of the directories specified in the role you are snapshotting.

### How can I make `rolesnap` faster on a large repository?

- **Be specific**: Instead of using `rolesnap full`, always prefer `rolesnap role <name>`. This limits the scan to only the files relevant to that role.

- **Tune `exclude_dirs`**: Make sure your `exclude_dirs` list is comprehensive. Including build output directories, caches (`.next`, `.mypy_cache`), and large asset folders can significantly speed up the file search.

- **Use `--hide-files`**: If you only need the file structure and not the content, using the `--hide-files` flag is much faster as it avoids reading the files from disk.

### How do I include shared utility code only when I need it?

This is a common pattern for keeping snapshots clean while allowing for deeper inspection when necessary.

1.  **Define `utils_dirs`**: Add your shared code paths to the `settings.utils_dirs` list in `rolesnap.yaml`.

    ```yaml
    settings:
      utils_dirs:
        - "packages/shared/utils/"
        - "common/helpers/"
    ```

2.  **Use the `--include-utils` flag**: When you run `rolesnap role`, add the `--include-utils` flag. The paths from `utils_dirs` will be added to the `Internal Logic` category for that snapshot only.

    ```bash
    # Snapshot without utils
    rolesnap role my_service

    # Snapshot WITH utils
    rolesnap role my_service --include-utils
    ```
