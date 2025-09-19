# Quickstart: Your First Snapshot in 60 Seconds

This guide will walk you through installing `rolesnap`, configuring it for your project, and generating your first code snapshot for an LLM.

## 1. Installation

We recommend installing `rolesnap` into a dedicated virtual environment using `uv`.

```bash
# Install the tool
uv tool install rolesnap

# Verify the installation
uv run rolesnap --version
```

## 2. Initialize Configuration

Navigate to your project's root directory and run the `init` command:

```bash
cd /path/to/your/project
rolesnap init
```

This creates a configuration file at `docs/roles/rolesnap.yaml`. This is where you will describe the architecture of your project.

## 3. Configure Your Project

Open the newly created `docs/roles/rolesnap.yaml`. You'll see two main sections: `settings` and `roles`.

### `settings`
The most important setting is `project_root`. **You must update this** to the absolute path of your project. The tool uses this path to find all your source files.

```yaml
settings:
  # Replace this with the actual absolute path to your project's root
  project_root: "/path/to/your/project"
  ...
```

### `roles`
A "role" is a logical part of your application (e.g., a backend service, a frontend app, a shared library).

Let's imagine your project has a simple structure:
```
/path/to/your/project/
├── services/
│   ├── api/          # Python backend
│   └── webapp/       # TypeScript frontend
└── shared/
    └── dtos.py       # Shared data models
```

You would define two roles, `api` and `webapp`. The `api` role exposes the `dtos.py` as its public contract (`external_domain`) and depends on nothing. The `webapp` role depends on the `api` role by `imports`.

Here’s how you would configure `rolesnap.yaml`:

```yaml
roles:
  api:
    help: "The Python backend service."
    # The public contract: what other roles can import.
    external_domain:
      - "shared/dtos.py"
    # The implementation details.
    internal_logic:
      - "services/api/"
    imports: [] # No dependencies

  webapp:
    help: "The TypeScript frontend application."
    internal_logic:
      - "services/webapp/"
    # This role depends on the 'api' role's public contract.
    imports:
      - "api"
```

## 4. Create a Snapshot

Now, let's create a snapshot of the `webapp` role. This will include the source code for `webapp` **and** the public contract of its dependency, `api`.

```bash
# Set the config path for your shell session
export ROLESNAP_CONFIG=./docs/roles/rolesnap.yaml

# Generate the snapshot
rolesnap role webapp 
```

This creates a file named `rolesnap.json` in your project root.

## 5. Use the Snapshot

The `rolesnap.json` file contains the categorized source code, ready to be used as context for an LLM.

```json
{
  "Collected Domain": {
    "shared/dtos.py": "class UserDTO:\n..."
  },
  "Internal Logic": {
    "services/webapp/src/App.tsx": "import React from 'react';\n...",
    "services/webapp/src/api.ts": "..."
  },
  ...
}
```

**To use it, simply copy the entire content of `rolesnap.json` and paste it into your chat with an LLM, followed by your question.**

For example:
> "Based on the following code context, how would I add a new field to the user profile page?"
> 
> *[...paste content of rolesnap.json here...]*

You have now successfully created and used your first snapshot!
