<div align="center">
<h1>GitHub Organisation Summary</h1>

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/GeekMasher/gh-org-summary)
[![GitHub Issues](https://img.shields.io/github/issues/geekmasher/gh-org-summary?style=for-the-badge)](https://github.com/GeekMasher/gh-org-summary/issues)
[![GitHub Stars](https://img.shields.io/github/stars/geekmasher/gh-org-summary?style=for-the-badge)](https://github.com/GeekMasher/gh-org-summary)
[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

</div>

## ⚡️ Requirements

- [Python][python] `>= 3.10`
- [pip][python-pip] `>= 23.x`
  - `pip install ghastoolkit` (`>= 0.10.0`)
- [gh-cli][gh-cli] (optional)
- GitHub Personal Access Token (PAT)
  - Requires access to `org:read`, `repo:read`, and `repo:security_events` scopes

## 📦 Installing

**Using [gh-cli][gh-cli]:**

To install and setup the CLI tool, you can use the following commands:

```bash
# install extension
gh extension install GeekMasher/gh-org-summary
# install deps (ghastoolkit)
gh gh-org-summary install
# run
gh gh-org-summary --help
```

**Install Manually:**

```bash
# clone and cd into repo
clone https://github.com/GeekMasher/gh-org-summary.git
cd gh-org-summary
# install deps (ghastoolkit)
pip install ghastoolkit
# run
python ./summary.py --help
```

## 📝 Usage

To generate a summary of your GitHub organisation, you can use the following command:

```bash
gh gh-org-summary \
    --github-instance "https://github.example.com" \
    --output "./output.csv"
```

**Access Token:**

The script automatically looks for the `GITHUB_TOKEN` environment variable but you can also supply the token via the `-t` or `--github-token` argument or it will prompt you.

```bash
gh gh-org-summary \
    --github-instance "https://github.example.com" \
    --output "./output.csv" \
    --github-token "ghp_1234567890"
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

<!-- Resources -->

[python]: https://www.python.org/
[python-pip]: https://pip.pypa.io/en/stable
[gh-cli]: https://cli.github.com/
