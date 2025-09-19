# Rolesnap: Create Perfect LLM Context from Your Codebase

**Rolesnap is a command-line tool that creates structured, role-based snapshots of your codebase.**

Instead of manually copying files or dumping an entire directory, you define the "roles" of your architecture (like `backend-api`, `frontend-app`, or `shared-library`) in a simple YAML file. `rolesnap` then generates a clean, focused JSON file containing only the code relevant to that role and its dependencies. This is perfect for providing high-quality context to Large Language Models (LLMs).

## Key Features

- **Role-Based Snapshots**: Generate context for a specific feature, microservice, or architectural layer. Stop feeding the LLM irrelevant code.

- **Dependency-Aware**: When you snapshot a role, `rolesnap` automatically includes the public APIs of its declared `imports`, giving the LLM the necessary context without the clutter of implementation details.

- **Highly Configurable**: Use a simple `rolesnap.yaml` file to define roles, exclude boilerplate, and fine-tune your snapshots to perfectly match your project's structure.

- **Simple & Fast CLI**: A clean, modern command-line interface makes it easy to integrate `rolesnap` into your development workflow.

## Get Started

Ready to try it? Head over to our **[Quickstart Guide](./quickstart.md)** to create your first snapshot in under a minute.

## What's Next?

Curious about upcoming features? Check out our **[Roadmap](./roadmap.md)** to see what we're planning.
