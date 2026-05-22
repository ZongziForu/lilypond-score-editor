# Templates and Patterns

## Template selection

Use the template that matches the instrumentation:

| Need | Template |
|------|----------|
| Single melody | `single-staff.ly` |
| Piano | `piano.ly` |
| Guitar (standard notation + optional tab) | `guitar.ly` |
| Bass guitar | `bass.ly` |
| Ukulele | `ukulele.ly` |
| Drum kit / percussion | `drum-kit.ly` |
| Melody + lyrics + chords | `lead-sheet.ly` |
| Choir (SATB) | `satb.ly` |
| Chamber strings | `string-quartet.ly` |
| Full orchestra | `orchestra.ly` |
| Shared score + parts | `parts-project.ly` + `parts-manifest.yaml` |

## Copying a template

```bash
cp "${CLAUDE_SKILL_DIR}/assets/templates/lead-sheet.ly" ./song.ly
```

## Editing a template

1. Update `\header` title and composer.
2. Set `\key` and `\time` in `global`.
3. Fill music variables (e.g., `melody`, `rightHand`).
4. Add or adjust lyrics and chord names.
5. Compile:
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/compile_lilypond.py" song.ly
   ```

## Template details

- **single-staff.ly**: One staff, one voice, global block. Good for monophonic instruments.
- **piano.ly**: `PianoStaff` with `rightHand` and `leftHand` variables.
- **guitar.ly**: Treble staff with `treble_8` clef. Includes commented-out `TabStaff` example for simultaneous notation + tablature.
- **bass.ly**: Bass staff with `bass_8` clef for electric bass or bass guitar.
- **ukulele.ly**: Treble staff tuned for ukulele range.
- **drum-kit.ly**: `DrumStaff` with `\drummode` for standard drum notation (bd, sn, hh, etc.).
- **lead-sheet.ly**: `ChordNames`, melody staff, and `Lyrics`. Good for jazz/pop charts.
- **satb.ly**: `ChoirStaff` with soprano/alto/tenor/bass variables and lyrics.
- **string-quartet.ly**: `StaffGroup` with violin I/II, viola (alto clef), cello (bass clef).
- **orchestra.ly**: Full orchestral score with `StaffGroup` sections for Woodwinds, Brass, and Strings. Includes transpositions for Bb clarinet/trumpet and F horn.
- **parts-project.ly**: Shared variables plus a full score. Designed to work with `extract_parts.py` and a manifest.
- **parts-manifest.yaml**: Example manifest for a string quartet. Edit `variable` names to match your `.ly` source.
