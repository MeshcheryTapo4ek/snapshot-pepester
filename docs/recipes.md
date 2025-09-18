# Recipes

## Monorepos
- Specify `project_root` to the top `src` or service; use `exclude_dirs`.

## Hexagonal / Ports & Adapters
- `external_ports` and `external_domain` — public contract; `internal_logic` — implementation.

## Microservices
- Split roles by services, add `imports` to a common `shared_kernel`.

## Libraries
- A separate role for the public API, without `internal_logic`.