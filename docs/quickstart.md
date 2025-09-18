# Quickstart (60 seconds)

```bash
rolesnap init
export ROLESNAP_CONFIG=./rolesnap.yaml
rolesnap selfscan --output rolesnap.json --max-bytes 2000000
rolesnap role rolesnap --output rolesnap.json
```

What happened:

* `init` generated a config template.
* `selfscan` — a snapshot of the tool itself.
* `role <name>` — collection by a specific role.