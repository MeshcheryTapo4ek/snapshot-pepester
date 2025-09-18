# CLI Reference

```bash
rolesnap --help
rolesnap full [--config FILE] [--hide-files] [--output PATH] [--max-bytes N] [--quiet]
rolesnap role <name> [--include-utils] [--config FILE] ...
rolesnap selfscan [--config FILE] ...
rolesnap validate [--config FILE]
```

Useful flags:

* `--hide-files` — only paths without content
* `--max-bytes N` — truncate large files
* `--quiet` — minimal output
* `--no-color` — no colors