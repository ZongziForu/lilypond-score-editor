# Scripted Part Extraction

## Recommended structure

Keep shared music variables in a single source file. Use a manifest to describe parts. Generate wrapper `.ly` files. Compile in batch.

### Example source

```lilypond
\version "2.24.4"

global = {
  \key c \major
  \time 4/4
}

violinIMusic = \relative c'' {
  \global
  c4 d e f
}

celloMusic = \relative c {
  \clef bass
  \global
  c4 d e f
}
```

### Example manifest

```yaml
source: score.ly
parts:
  - id: violin-i
    name: Violin I
    variable: violinIMusic
    clef: treble
  - id: cello
    name: Cello
    variable: celloMusic
    clef: bass
```

### Run extraction

```bash
python "${CLAUDE_SKILL_DIR}/scripts/extract_parts.py" score.ly parts-manifest.yaml --compile
```

## Alternative structure: multiple books

One `.ly` file with multiple `\book` blocks:

```lilypond
\book {
  \bookOutputName "full-score"
  \score { ... }
}

\book {
  \bookOutputName "violin-i"
  \score { \new Staff \violinIMusic }
}
```

## Advanced: tags

Use `\tag`, `\keepWithTag`, and `\removeWithTag` for:

- Cue notes
- Score-only markings
- Part-only breaks
- Different rehearsal marks
- Ossia
- Cuts or variants

## Anti-patterns

Avoid:

- Hard-splitting a huge `StaffGroup` with regex.
- Copying full music blocks into each part file.
- Maintaining separate divergent sources for score and parts.
- Handwriting large amounts of repetitive wrapper code.

## Token-saving rule

Never rely on Claude Code to copy large music blocks for part generation. Prefer:

1. Shared variables
2. Manifest file
3. Generated wrappers
4. Batch compilation
