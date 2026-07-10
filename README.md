# validate-lza

Pre-commit hooks that validate AWS Landing Zone Accelerator (LZA) config YAML
files against the upstream `@aws-accelerator/config` JSON Schema for a
specific LZA release. The schema is fetched directly from the
[`awslabs/landing-zone-accelerator-on-aws`](https://github.com/awslabs/landing-zone-accelerator-on-aws)
repo at the matching git tag — nothing is vendored here. `check-jsonschema`
downloads and caches the remote schema at hook run time.

## Why

LZA's own deploy-time config parser silently discards "additional properties"
schema errors, so stale/renamed/removed config keys are never caught at
deploy time — they just linger in the repo unnoticed. These hooks run a
standard JSON Schema validator (which does *not* discard those errors)
against your config files, so drift gets caught in pre-commit/CI instead.

## Usage

Add one hook per LZA config file present in your repo, passing your deployed
LZA version via `--lza-version`:

```yaml
repos:
  - repo: https://github.com/WeAreCloudar/validate-lza
    rev: v1.0.0 # see Releases for the latest tag
    hooks:
      - id: validate-lza-global-config
        args: [--lza-version, v1.15.5]
      - id: validate-lza-accounts-config
        args: [--lza-version, v1.15.5]
      - id: validate-lza-customizations-config
        args: [--lza-version, v1.15.5]
      - id: validate-lza-iam-config
        args: [--lza-version, v1.15.5]
      - id: validate-lza-network-config
        args: [--lza-version, v1.15.5]
      - id: validate-lza-organization-config
        args: [--lza-version, v1.15.5]
      - id: validate-lza-security-config
        args: [--lza-version, v1.15.5]
      - id: validate-lza-replacements-config
        args: [--lza-version, v1.15.5]
```

Only include the hooks for config files that actually exist in your repo.

### Available hooks

| Hook id                              | Validates                     |
| ------------------------------------- | ------------------------------ |
| `validate-lza-global-config`          | `global-config.yaml`           |
| `validate-lza-accounts-config`        | `accounts-config.yaml`          |
| `validate-lza-customizations-config`  | `customizations-config.yaml`   |
| `validate-lza-iam-config`             | `iam-config.yaml`              |
| `validate-lza-network-config`         | `network-config.yaml`          |
| `validate-lza-organization-config`    | `organization-config.yaml`     |
| `validate-lza-security-config`        | `security-config.yaml`         |
| `validate-lza-replacements-config`    | `replacements-config.yaml`     |

### Bumping the LZA version

Update `--lza-version` to the new release tag (e.g. `v1.16.0`) on each hook in
the consuming repo's `.pre-commit-config.yaml`. Nothing needs to change in
this repo unless the upstream schema *filenames* change.

## Development

```bash
pip install -e '.[test]'
pytest
```

`validate-lza --lza-version <tag> --config-type <type> <files...>` builds the
schema URL for `<tag>`/`<type>` and delegates to `check-jsonschema
--schemafile <url> <files...>`.

## Implementing changes

This repository uses [release-please](https://github.com/googleapis/release-please)
to create new releases upon merging to `main`. Implement changes by:

- Creating a feature branch
- Implementing your changes using [Conventional Commits](https://www.conventionalcommits.org/)
- Pushing your changes to GitHub
- Creating a Pull Request and merging into `main`
- Release-please will open a release PR that, when merged, creates a new tag
  `vX.Y.Z` and moves the major (`vX`) and minor (`vX.Y`) tags to that latest
  version.
