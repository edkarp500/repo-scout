# Repo Scout
Repo Scout is a small command-line tool that checks whether a project has the basic pieces of a healthy open-source repository.
It looks for common maintainer signals like a README, license, contributing guide, tests, issue templates, release notes, and continuous integration. The goal is not to shame projects with a score. The goal is to give maintainers a fast checklist they can improve over time.
## Why This Exists
New maintainers often ask: "What should my repo include before I share it?"
Repo Scout answers that with a plain-language report:
- what is already present
- what is missing
- why each item matters
- suggested next steps
## Install
Clone this repository, then run:
```bash
python -m pip install -e .
```
## Usage
Check the current directory:
```bash
repo-scout
```
Check another repository:
```bash
repo-scout /path/to/project
```
Print JSON output:
```bash
repo-scout --json
```
## Example
```text
Repo Scout report for .
Score: 7/10
[pass] README: Found README.md
[pass] License: Found LICENSE
[warn] Contributing guide: Missing CONTRIBUTING.md
[pass] Tests: Found tests/
```
## Checks
Repo Scout currently checks for:
- README
- license
- contributing guide
- code of conduct
- changelog or release notes
- tests
- continuous integration workflow
- issue templates
- pull request template
- security policy
## Roadmap
- Add language-specific checks for Python, JavaScript, and Rust projects
- Support configurable checks through a `.repo-scout.toml` file
- Add markdown suggestions for missing files
- Add GitHub Actions output annotations
## Contributing
Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup steps and contribution guidelines.
## License
MIT