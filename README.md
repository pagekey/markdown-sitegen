# markdown-sitegen

This repo is a command-line tool to generate static sites from Markdown, especially Obsidian vaults.

## Video Series

This package has been developed on video on the PageKey Tech YouTube channel. You can check the series out [here](https://www.youtube.com/watch?v=rB1uyE7tJKw&list=PL3Kz_hCNpKSQ5gDVSWvrQ-9COk0CLLrTs).

## Discord

[Join the Discord](https://discord.gg/5m5yFgDPF5) to discuss this project and connect with others!

## Installation

General use:

```
pip install markdown-sitegen
```

Development:

```
git clone git@github.com:pagekeytech/markdown-sitegen
cd markdown-sitegen
pip install -e .
```

## Development One-Liner

This is a quick and easy way to test things out once you've cloned the repo and installed:

```bash
markdown-sitegen example/ && python3 -m http.server --directory build
```
