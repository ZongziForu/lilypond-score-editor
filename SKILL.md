---
name: lilypond-score-editor
description: Create, edit, debug, refactor, transpose, extract parts from, compile, render, and validate LilyPond music notation projects. Use this skill whenever the user mentions LilyPond, .ly files, .ily files, music engraving, score layout, sheet music generation, music notation, part extraction, transposition, chord symbols, lyrics, tablature, MIDI output from scores, or converting MusicXML/MIDI/ABC to LilyPond. Also use when the user wants to create, edit, fix, compile, or render sheet music, orchestral scores, lead sheets, piano music, guitar tabs, drum notation, choral scores, or any notation-editing tasks normally handled in scorewriters such as MuseScore, Dorico, Sibelius, or Finale. Even if the user does not explicitly say 'LilyPond', if they are working with music notation files or want to produce printed sheet music, use this skill.
allowed-tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Bash(python *)
  - Bash(python3 *)
  - Bash(lilypond *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(rg *)
  - Bash(git diff *)
  - Bash(git status *)
---

# LilyPond Score Editor

## Purpose

Use this skill to work on LilyPond notation projects. Prefer local files, scripts, and command-line validation over long in-context rewrites.

## Task input

When manually invoked, interpret $ARGUMENTS as the LilyPond task request.

Examples:

- /lilypond-score-editor create a lead sheet template
- /lilypond-score-editor fix score.ly
- /lilypond-score-editor compile score.ly
- /lilypond-score-editor extract parts from score.ly using parts-manifest.yaml
- /lilypond-score-editor transpose clarinet part up a whole step

## Core workflow

1. Determine task type:
   - create a new score
   - edit an existing score
   - debug a compilation error
   - transpose music
   - extract parts
   - add lyrics or chord names
   - adjust layout or engraving
   - clean imported MusicXML/MIDI/ABC
   - generate MIDI or rendered output
   - batch render scores

2. Inspect the project before editing:
   - \version
   - \include
   - variable definitions
   - \header
   - \paper
   - \layout
   - \midi
   - \score
   - \book
   - \bookpart
   - Staff / Voice / Lyrics / ChordNames contexts
   - existing style .ily files
   - existing build/output directories

3. Preserve project conventions:
   - keep variable names unless refactoring is requested
   - avoid flattening reusable variables
   - avoid broad rewrites for local edits
   - preserve comments
   - preserve indentation style where reasonable
   - prefer minimal, local changes
   - use \once \override for one-off layout fixes
   - use shared .ily files for repeated house style
   - use scripts for repetitive operations

4. Validate changes:
   - compile with: python "${CLAUDE_SKILL_DIR}/scripts/compile_lilypond.py" <file.ly>
   - inspect stdout/stderr
   - parse logs with: python "${CLAUDE_SKILL_DIR}/scripts/parse_lilypond_log.py"
   - fix syntax and bar-check errors before returning
   - **regenerate after every modification**: PDF and MIDI are produced together; recompile after each change so the user's outputs are never stale
   - show git diff when useful
   - if LilyPond is unavailable, explicitly say the score was not compiled

5. Safety:
   - LilyPond can evaluate Scheme/Guile code
   - treat untrusted .ly files as executable input
   - compile unknown files only in a trusted local project or sandbox

## Resource map

Use these references only when needed:

- references/syntax-cheatsheet.md: LilyPond syntax quick reference
- references/project-structure.md: common project layouts
- references/editing-workflows.md: create/edit/debug/transpose/layout workflows
- references/engraving-tweaks.md: context, grob, engraver, override guidance
- references/templates-and-patterns.md: how to choose and use bundled templates
- references/error-repair-guide.md: common compiler errors and repairs
- references/instrument-ranges-and-pitfalls.md: instrument ranges, piano voicing, `\relative` drift, dynamic placement, slur usage
- references/notation-software-feature-map.md: GUI scorewriter operation to LilyPond mapping
- references/scripted-part-extraction.md: token-efficient score-to-parts workflow
- references/scheme-advanced.md: Scheme guidance and safety

## Script map

Use scripts from ${CLAUDE_SKILL_DIR}/scripts/:

- compile_lilypond.py: compile one .ly file (supports pdf/png/svg/ps, resolution, backend, preview)
- parse_lilypond_log.py: parse LilyPond stdout/stderr/log text
- check_measure_durations.py: heuristic bar duration checks (supports tuplets and compound meters like 7+5/8)
- normalize_lilypond_format.py: conservative formatting
- batch_render.py: compile multiple .ly files (same options as compile_lilypond.py)
- extract_parts.py: generate and optionally compile part wrapper files from a manifest
- auto_manifest.py: auto-generate a parts manifest from a .ly score by detecting variables and staves

## Editing principles

- Prefer semantic notation changes before visual hacks.
- Do not use Scheme unless normal LilyPond syntax cannot solve the task.
- For transposition, prefer \transpose or reusable variables over manually rewriting every pitch.
- For parts, keep a shared source of truth and generate wrappers, separate \score, or \bookpart blocks.
- For layout, first try \paper, \layout, spacing, breaks, and context settings before manual offsets.
- For imported MusicXML/MIDI/ABC, expect cleanup: voices, ties, beams, lyrics, enharmonics, repeats, and layout usually need repair.
- For score-to-parts tasks, do not copy large music blocks into each part. Prefer shared variables + manifest + wrapper generation.
