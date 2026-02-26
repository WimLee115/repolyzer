<div align="center">

<img src="https://capsule-render.vercel.app/api?type=venom&color=3776AB&height=300&section=header&text=Repolyzer&fontSize=90&fontColor=ffffff&animation=twinkling&fontAlignY=35&desc=Instant%20beautiful%20insights%20about%20any%20codebase&descSize=18&descAlignY=55&descColor=58a6ff" width="100%" />

<br/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=28&duration=3000&pause=1000&color=4CAF50&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=100&lines=Like+neofetch%2C+but+for+your+repos;Analyze+any+codebase+in+seconds;Languages+%E2%80%A2+Structure+%E2%80%A2+Health+Scores" alt="Typing SVG" />

<br/>

[![PyPI Version](https://img.shields.io/pypi/v/repolyzer?style=for-the-badge&logo=pypi&logoColor=white&color=3776AB)](https://pypi.org/project/repolyzer/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-4CAF50?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/repolyzer?style=for-the-badge&logo=pypi&logoColor=white&color=3776AB)](https://pypi.org/project/repolyzer/)
[![Stars](https://img.shields.io/github/stars/WimLee115/repolyzer?style=for-the-badge&logo=github&logoColor=white&color=4CAF50)](https://github.com/WimLee115/repolyzer)

<br/>

```
                            ╭─────────────────────────────────╮
  ┌─┐┌─┐┌─┐┌─┐┬  ┬ ┬┌─┐┌─┐│  Instant beautiful insights     │
  ├┬┘├┤ ├─┘│ ││  └┬┘┌─┘├┤ │  about any codebase.            │
  ┴└─└─┘┴  └─┘┴─┘ ┴ └─┘└─┘│  Like neofetch, but for repos.  │
                            ╰─────────────────────────────────╯
```

<img src="https://skillicons.dev/icons?i=python,bash,git&perline=8" />

</div>

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

## What is Repolyzer?

**Repolyzer** is a Python CLI tool that gives you a gorgeous, instant snapshot of any codebase — right in your terminal. Think of it as **neofetch for your repositories**. Point it at any directory and get a beautiful breakdown of languages, project structure, git history, dependencies, health scores, and code markers.

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

## Features

<div align="center">

<table>
<tr>
<td align="center" width="33%">

### Language Detection

Scans your entire codebase and displays a **color-coded language breakdown** with percentages, file counts, and line counts.

</td>
<td align="center" width="33%">

### Project Structure

Visualizes your **directory tree** with smart depth limits, file grouping, and highlights for important files like configs and entry points.

</td>
<td align="center" width="33%">

### Git History

Analyzes your **commit history** showing contributors, commit frequency, branch info, and recent activity at a glance.

</td>
</tr>
<tr>
<td align="center" width="33%">

### Dependency Analysis

Detects and parses **dependency files** (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, etc.) across all major ecosystems.

</td>
<td align="center" width="33%">

### Health Scores

Calculates a **repo health score** based on documentation, testing, CI/CD presence, license, code quality markers, and more.

</td>
<td align="center" width="33%">

### Code Markers

Finds and counts `TODO`, `FIXME`, `HACK`, `BUG`, and other **code markers** scattered across your codebase with file locations.

</td>
</tr>
</table>

</div>

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

## Installation

```bash
pip install repolyzer
```

That's it. No configuration needed. Works on **Linux**, **macOS**, and **Windows**.

<details>
<summary><b>Alternative installation methods</b></summary>

<br/>

**With pipx (isolated environment):**

```bash
pipx install repolyzer
```

**From source:**

```bash
git clone https://github.com/WimLee115/repolyzer.git
cd repolyzer
pip install -e .
```

</details>

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

## Usage

### Basic Analysis

```bash
# Analyze the current directory
repolyzer

# Analyze a specific path
repolyzer /path/to/your/project

# Analyze a remote repository (clones temporarily)
repolyzer https://github.com/user/repo
```

### Output Options

```bash
# JSON output for scripting and pipelines
repolyzer --json

# Save results to a file
repolyzer --output report.txt

# JSON output to file
repolyzer --json --output report.json

# Quiet mode (only show summary)
repolyzer --quiet
```

### Customization

```bash
# Set maximum directory depth for structure view
repolyzer --depth 4

# Exclude specific directories
repolyzer --exclude node_modules,.git,dist

# Show only specific sections
repolyzer --sections languages,health,markers

# Disable color output
repolyzer --no-color
```

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

## Example Output

<div align="center">

```
╭──────────────────────────────────────────────────────────────╮
│                     repolyzer v1.0.0                         │
│              Analyzing: my-awesome-project                   │
╰──────────────────────────────────────────────────────────────╯

 Languages
├── Python          ████████████████████░░░░░  78.3%  (142 files, 18,420 lines)
├── JavaScript      ████░░░░░░░░░░░░░░░░░░░░  12.1%  ( 28 files,  3,105 lines)
├── Shell           ██░░░░░░░░░░░░░░░░░░░░░░   5.6%  ( 12 files,    892 lines)
├── Dockerfile      █░░░░░░░░░░░░░░░░░░░░░░░   2.4%  (  3 files,    310 lines)
└── YAML            █░░░░░░░░░░░░░░░░░░░░░░░   1.6%  (  8 files,    204 lines)

 Git History
├── Commits:        1,247
├── Contributors:   3
├── First commit:   2024-01-15
├── Last commit:    2025-06-02
├── Branches:       5
└── Most active:    WimLee115 (1,089 commits)

 Health Score       ████████████████████████░  92/100
├── [+] README.md found
├── [+] LICENSE found (MIT)
├── [+] CI/CD configured (.github/workflows)
├── [+] Tests directory found
├── [+] .gitignore present
├── [-] No CONTRIBUTING.md
└── [-] No CHANGELOG.md

 Code Markers
├── TODO:           14
├── FIXME:          3
├── HACK:           1
└── Total:          18

 Dependencies
├── requirements.txt     (12 packages)
├── pyproject.toml       (8 packages)
└── package.json         (5 packages)
```

</div>

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

## JSON Output

<details>
<summary><b>View full JSON output structure</b></summary>

<br/>

When using `--json`, Repolyzer outputs structured data perfect for CI/CD pipelines, dashboards, or further processing:

```json
{
  "project": {
    "name": "my-awesome-project",
    "path": "/home/user/my-awesome-project",
    "analyzed_at": "2025-06-02T14:30:00Z"
  },
  "languages": {
    "Python": {
      "percentage": 78.3,
      "files": 142,
      "lines": 18420
    },
    "JavaScript": {
      "percentage": 12.1,
      "files": 28,
      "lines": 3105
    }
  },
  "git": {
    "total_commits": 1247,
    "contributors": 3,
    "first_commit": "2024-01-15",
    "last_commit": "2025-06-02",
    "branches": 5
  },
  "health": {
    "score": 92,
    "checks": {
      "readme": true,
      "license": "MIT",
      "ci_cd": true,
      "tests": true,
      "gitignore": true,
      "contributing": false,
      "changelog": false
    }
  },
  "markers": {
    "TODO": 14,
    "FIXME": 3,
    "HACK": 1,
    "total": 18
  },
  "dependencies": {
    "requirements.txt": 12,
    "pyproject.toml": 8,
    "package.json": 5
  }
}
```

</details>

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

## Supported Dependency Files

<div align="center">

<table>
<tr>
<th>Ecosystem</th>
<th>File</th>
<th>Detected</th>
</tr>
<tr><td><b>Python</b></td><td><code>requirements.txt</code>, <code>pyproject.toml</code>, <code>setup.py</code>, <code>Pipfile</code></td><td>Packages + versions</td></tr>
<tr><td><b>JavaScript / Node</b></td><td><code>package.json</code>, <code>yarn.lock</code>, <code>pnpm-lock.yaml</code></td><td>deps + devDeps</td></tr>
<tr><td><b>Rust</b></td><td><code>Cargo.toml</code></td><td>Dependencies + features</td></tr>
<tr><td><b>Go</b></td><td><code>go.mod</code></td><td>Modules + versions</td></tr>
<tr><td><b>Java / Kotlin</b></td><td><code>pom.xml</code>, <code>build.gradle</code>, <code>build.gradle.kts</code></td><td>Dependencies</td></tr>
<tr><td><b>Ruby</b></td><td><code>Gemfile</code></td><td>Gems</td></tr>
<tr><td><b>PHP</b></td><td><code>composer.json</code></td><td>Packages</td></tr>
<tr><td><b>.NET / C#</b></td><td><code>*.csproj</code>, <code>*.fsproj</code></td><td>NuGet packages</td></tr>
<tr><td><b>Swift</b></td><td><code>Package.swift</code></td><td>Dependencies</td></tr>
<tr><td><b>Dart / Flutter</b></td><td><code>pubspec.yaml</code></td><td>Packages</td></tr>
</table>

</div>

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

## Health Score Breakdown

<details>
<summary><b>How is the health score calculated?</b></summary>

<br/>

The health score (0-100) is computed from the following checks:

| Check | Points | Description |
|-------|--------|-------------|
| **README** | +15 | Has a `README.md` or `README` file |
| **License** | +15 | Has a `LICENSE` or `COPYING` file |
| **CI/CD** | +15 | Has `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, etc. |
| **Tests** | +15 | Has a `tests/`, `test/`, `spec/`, or `__tests__/` directory |
| **.gitignore** | +10 | Has a `.gitignore` file |
| **CONTRIBUTING** | +5 | Has a `CONTRIBUTING.md` file |
| **CHANGELOG** | +5 | Has a `CHANGELOG.md` or `HISTORY.md` file |
| **Code of Conduct** | +5 | Has a `CODE_OF_CONDUCT.md` file |
| **Issue Templates** | +5 | Has `.github/ISSUE_TEMPLATE/` directory |
| **Security Policy** | +5 | Has a `SECURITY.md` file |
| **Docs Directory** | +5 | Has a `docs/` directory |

</details>

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

## Supported Languages

<details>
<summary><b>View all 50+ detected languages</b></summary>

<br/>

Repolyzer detects languages by file extension and applies color coding in the terminal output:

> Python, JavaScript, TypeScript, Rust, Go, Java, Kotlin, C, C++, C#, Ruby, PHP, Swift, Dart, Shell/Bash, PowerShell, Perl, Lua, R, Julia, Elixir, Erlang, Haskell, Scala, Clojure, F#, OCaml, Zig, Nim, Crystal, V, SQL, HTML, CSS, SCSS/SASS, Less, Svelte, Vue, JSX/TSX, Markdown, YAML, TOML, JSON, XML, Dockerfile, Makefile, CMake, Nix, Terraform (HCL), Protobuf, GraphQL, and more.

</details>

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

## Use Cases

<div align="center">

<table>
<tr>
<td width="50%">

**For Developers**
- Get a quick overview of an unfamiliar codebase
- Find scattered `TODO`s and `FIXME`s before a release
- Check repo health before open-sourcing
- Compare language distributions across projects

</td>
<td width="50%">

**For Teams & CI/CD**
- Add `repolyzer --json` to your pipeline for automated reports
- Track health score regressions over time
- Generate dependency summaries for security audits
- Onboard new team members with instant project overviews

</td>
</tr>
</table>

</div>

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

```bash
# Clone the repo
git clone https://github.com/WimLee115/repolyzer.git
cd repolyzer

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
```

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

<div align="center">

## Support

If you find Repolyzer useful, consider supporting the project:

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black)](https://buymeacoffee.com/wimlee115)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-EA4AAA?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/WimLee115)

<img src="https://i.imgur.com/dBaSKWF.gif" height="20" width="100%" >

<br/>

[![Built By](https://img.shields.io/badge/Built%20by-WimLee115-3776AB?style=for-the-badge&logo=github&logoColor=white)](https://github.com/WimLee115)
[![Solo Engineer](https://img.shields.io/badge/Solo-Engineer-4CAF50?style=for-the-badge&logo=openbadges&logoColor=white)](#)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MIT License](https://img.shields.io/badge/License-MIT-4CAF50?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)

<br/>

Contact: [ai-idle@outlook.com](mailto:ai-idle@outlook.com)

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=3776AB&height=120&section=footer" width="100%" />

</div>
