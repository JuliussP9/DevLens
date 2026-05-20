# DevLens 🔍

An AI-powered GitHub profile analyzer that fetches a developer's public GitHub data and generates an intelligent summary of their strengths, top projects, and language patterns using the Claude API.

---

## Demo

```
$ python analyzer.py JuliussP9

Analyzing @JuliussP9...

╭─────────────────── 👤 GitHub Profile ───────────────────╮
│ Julius Parkin                                            │
│ CS student @ TMU | Building things that matter          │
│ 📦 12 repos   👥 8 followers   📍 Ajax, Ontario         │
╰──────────────────────────────────────────────────────────╯

💻 Top Languages
  Python          ████████████░░░░░░░░  45%
  JavaScript      █████████░░░░░░░░░░░  30%
  TypeScript      ██████░░░░░░░░░░░░░░  20%

🚀 Top Repositories
  ⭐ 3  PRism — Automated code review tool using Claude API
  ⭐ 2  CommuteU — Smart commute assistant for TMU students
  ⭐ 1  DevLens — AI-powered GitHub profile analyzer

╭─────────────────── 🧠 AI Analysis ──────────────────────╮
│ Julius is a full stack developer with a strong focus on  │
│ AI-powered tooling and automation. His repositories show │
│ a consistent pattern of building practical developer     │
│ tools that integrate external APIs.                      │
│                                                          │
│ Top Strengths:                                           │
│ • AI/API integration (Claude, GitHub APIs)               │
│ • Full stack web development (Next.js, Firebase)         │
│ • Automation and developer tooling                       │
│                                                          │
│ Best suited for: Full stack, backend, or AI engineering  │
│ roles focused on developer tools and automation.         │
╰──────────────────────────────────────────────────────────╯
```

---

## Features

- **Profile overview** — name, bio, location, followers, and repo count
- **Language breakdown** — visual bar chart of top programming languages across all public repos
- **Top repositories** — sorted by stars with descriptions
- **AI-generated summary** — developer profile, top strengths, and role recommendations powered by Claude
- **Works on any public GitHub profile** — just pass in a username

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core language |
| GitHub REST API | Fetching public profile and repo data |
| Anthropic Claude API | AI-generated developer analysis |
| Rich | Terminal formatting and visual output |

---

## Getting Started

### Prerequisites
- Python 3.8+
- An Anthropic API key — get one at [console.anthropic.com](https://console.anthropic.com)

### Installation

```bash
# Clone the repo
git clone https://github.com/JuliussP9/DevLens.git
cd DevLens

# Install dependencies
pip install anthropic requests rich
```

### Setup

Create a `.env` file in the root of the project:

```
ANTHROPIC_API_KEY=your_api_key_here
```

Never commit this file — it's already in `.gitignore`.

### Usage

```bash
python analyzer.py <github_username>
```

**Examples:**
```bash
python analyzer.py JuliussP9
python analyzer.py torvalds
python analyzer.py gvanrossum
```

---

## Project Structure

```
DevLens/
├── analyzer.py       # Main script
├── .env              # Your API keys (never committed)
├── .gitignore        # Ignores .env and pycache
└── README.md
```

---

## License

MIT
