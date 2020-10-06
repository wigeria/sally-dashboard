# <p align=center style="margin-bottom: 0">Sally Dashboard</p>
###### <p align=center>1.0.0 - 9/28/2020</p>
--------------------------------------------

Sally Dashboard is a UI for creating, managing and running [SeleniumYAML](https://wigeria.github.io/selenium-yaml-core/) bots. This documentation aims to make it's structure and deployment process as clear as possible.

## Commands

- `flask db history --directory=backend/migrations` - Get migrations history
- `flask run` - Run flask app
- `pytest tests` - Run flask tests
- `mkdocs serve` - Serve the documentation

## Contents

1. [Outline](structure/outline.md)

## Roadmap

1. POC Deployment

2. Implement support for custom plugins during deployment

3. Implement support for chained bots (modularized bots with sub-bot calls)
