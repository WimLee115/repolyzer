<p align="center">
  <img src="https://img.shields.io/badge/python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/pypi/v/repolyzer?style=for-the-badge&color=brightgreen" alt="PyPI">
  <img src="https://img.shields.io/github/license/repolyzer/repolyzer?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/stars/repolyzer/repolyzer?style=for-the-badge&color=yellow" alt="Stars">
</p>

<h1 align="center">
<pre>
                      .__
_______   ____ ______ |  |  ___.__._________ _____
\_  __ \_/ __ \\____ \|  | <   |  |\___   // __ \_ __ \
 |  | \/\  ___/|  |_> >  |__\___  | /    /\  ___/|  | \/
 |__|    \___  >   __/|____// ____|/_____ \\___  >__|
             \/|__|         \/           \/    \/
</pre>
</h1>

<p align="center">
  <strong>Instant beautiful insights about any codebase.</strong><br>
  <em>Like <code>neofetch</code>, but for your repositories.</em>
</p>

---

## Why?

Ever jump into a new codebase and wonder: *"What's going on here?"*

**repolyzer** gives you a complete overview of any project in seconds — languages, structure, git history, dependencies, health, and code markers — all in a gorgeous terminal display.

```
$ repolyzer

╔══════════════════════════════════════════════════════════════╗
║                        repolyzer                            ║
║              analyzing my-awesome-project                   ║
╚══════════════════════════════════════════════════════════════╝

╭─ Languages ──────────────────────────────────────────────────╮
│  Python       █████████████████████████░░░░░  78.2%   12,847 lines │
│  JavaScript   ████████░░░░░░░░░░░░░░░░░░░░░  15.3%    2,341 lines │
│  CSS          ███░░░░░░░░░░░░░░░░░░░░░░░░░░   4.1%      687 lines │
│  Shell        █░░░░░░░░░░░░░░░░░░░░░░░░░░░░   2.4%      402 lines │
╰──────────────────────────────────────────────────────────────╯

╭─ Structure ──────────────────────────────────────────────────╮
│  Files      142          Dirs       23                       │
│  Size       1.2 MB       Max depth  6                        │
╰──────────────────────────────────────────────────────────────╯

╭─ Git ────────────────────────────────────────────────────────╮
│  Branch     main         Commits    847                      │
│  Branches   3            Tags       12                       │
│  Authors    5            Changes    2                        │
│                                                              │
│  🥇 Alice Johnson          423 commits                       │
│  🥈 Bob Smith               312 commits                      │
│  🥉 Charlie Dev             112 commits                      │
╰──────────────────────────────────────────────────────────────╯

╭─ Dependencies ───────────────────────────────────────────────╮
│  requirements.txt                          23 deps           │
│  package.json                     15 deps  8 dev             │
│                                                              │
│  Total: 38 dependencies, 8 dev                               │
╰──────────────────────────────────────────────────────────────╯

╭─ Health ─────────────────────────────────────────────────────╮
│  ✓ README           ✓ License          ✓ .gitignore         │
│  ✓ CI/CD            ✓ Tests            ✗ Docker             │
│  ✗ Contributing     ✗ Changelog        ✗ Security policy    │
│                                                              │
│  Health score: 60%  ████████████░░░░░░░░                     │
╰──────────────────────────────────────────────────────────────╯

╭─ Code Markers ───────────────────────────────────────────────╮
│  TODO 23    FIXME 5    HACK 2                                │
│  Total: 30 markers found                                     │
╰──────────────────────────────────────────────────────────────╯

  Scanned in 0.34s
```

## Installation

```bash
pip install repolyzer
```

Or with [pipx](https://pipx.pypa.io/) (recommended):

```bash
pipx install repolyzer
```

## Usage

```bash
# Analyze current directory
repolyzer

# Analyze a specific path
repolyzer /path/to/project

# Output as JSON (for scripting)
repolyzer --json

# Skip specific analyses
repolyzer --no-git --no-todos
```

## What it analyzes

| Category | Details |
|---|---|
| **Languages** | 60+ languages detected with line counts, file counts, and visual breakdown |
| **Structure** | File/directory counts, total size, nesting depth |
| **Git** | Commits, branches, tags, contributors, last commit, repo age |
| **Dependencies** | Supports package.json, requirements.txt, Cargo.toml, go.mod, Gemfile, pyproject.toml, and more |
| **Health** | README, license, CI/CD, tests, Docker, linting, contributing guide, changelog, security policy |
| **Code Markers** | TODO, FIXME, HACK, BUG, XXX, OPTIMIZE, DEPRECATED |

## JSON output

Perfect for CI/CD pipelines, dashboards, or scripting:

```bash
repolyzer --json | jq '.health.score'
```

## Supported dependency files

- `package.json` (Node.js)
- `requirements.txt` / `Pipfile` / `pyproject.toml` (Python)
- `Cargo.toml` (Rust)
- `go.mod` (Go)
- `Gemfile` (Ruby)
- `composer.json` (PHP)
- `pom.xml` / `build.gradle` (Java)
- `pubspec.yaml` (Dart/Flutter)
- `mix.exs` (Elixir)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

```bash
# Clone the repo
git clone https://github.com/repolyzer/repolyzer.git
cd repolyzer

# Install in development mode
pip install -e ".[dev]"

# Run on itself
repolyzer .
```

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <sub>Built with <a href="https://github.com/Textualize/rich">Rich</a> and <a href="https://click.palletsprojects.com/">Click</a></sub>
</p>
