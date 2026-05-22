# Notation Software Feature Map

Mapping common GUI scorewriter features to LilyPond / Claude Code equivalents.

| GUI Feature | LilyPond / Claude Code Approach |
|-------------|---------------------------------|
| New score wizard | Choose a template from `assets/templates/` |
| Note entry | Edit voice variables in `.ly` files |
| Copy/paste bars | Reuse variables or use `\repeat unfold` |
| Transpose dialog | `\transpose from to { ... }` |
| Extract parts | Manifest + wrapper generation / `\bookpart` / tags |
| Layout panel | `\paper`, `\layout` |
| Drag symbol to staff | `\once \override` for local tweaks |
| Lyrics tool | `\lyricmode`, `\lyricsto` |
| Chord symbols tool | `\chordmode`, `\new ChordNames` |
| Playback | `\midi { }` block |
| Export PDF/PNG/SVG | LilyPond command flags (`-fpdf`, `-fpng`, `-fsvg`) |
| Style library | Shared `.ily` file included across projects |
| Plugins / macros | Scheme functions or external Python scripts |
| MusicXML import | `musicxml2ly` followed by cleanup workflow |

## Claude Code advantages

- Read and write local `.ly` files directly.
- Run `lilypond` and Python scripts for validation.
- Use `git diff` to review minimal, safe changes.
- Script repetitive operations (batch render, part extraction) to save tokens.
- Refactor large scores into variables and manifests efficiently.
