# lilypond-score-editor

A Claude Code skill for creating, editing, debugging, and rendering LilyPond music notation projects.

## Usage

In Claude Code, this skill triggers automatically when you work with LilyPond files (`.ly`, `.ily`). You can also invoke it manually:

```
/lilypond-score-editor create a piano piece
/lilypond-score-editor fix score.ly
/lilypond-score-editor extract parts from score.ly
```

## Features

- **Score creation** — templates for piano, guitar, bass, ukulele, drum kit, lead sheet, SATB choir, string quartet, full orchestra, and more
- **Scripts** — compile, batch render, part extraction, log parsing, bar duration checking, auto manifest generation, formatting
- **Documentation** — syntax cheatsheet, project structure guides, editing workflows, engraving tweaks, error repair, instrument ranges, notation software feature map, Scheme reference
- **Part extraction** — manifest-based workflow with auto-detection of variables from existing scores
- **MIDI output** — integrated with every `\score` block

## Structure

```
├── SKILL.md                  # Skill entry point
├── assets/
│   ├── styles/
│   └── templates/            # Ready-to-use .ly templates
├── references/               # Detailed guides
├── scripts/                  # Python utility scripts
└── evals/                    # Test cases
```

## Requirements

- [LilyPond](https://lilypond.org) 2.24+ for compilation
- Python 3 for utility scripts
- PyYAML (optional, for YAML manifest support in `extract_parts.py`)
