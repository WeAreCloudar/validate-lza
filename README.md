# GitHub action template repository

This is a template repository for a custom GitHub action.

## Implementing changes

This repository uses [release-please](https://github.com/googleapis/release-please) to create new releases upon merging to `main` branch.

You can implement changes by:
  - Creating a feature branch
  - Implementing your changes and using [Conventional Commits](https://www.conventionalcommits.org/)
  - Push your changes to GitHub
  - Create a Pull Request and merge into main
  - Release-please will open a release PR that, when merged, creates a new tag vX.Y.Z and moves the major (vX) and minor (vX.Y) tags to this latest version.
