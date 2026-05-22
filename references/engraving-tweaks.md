# Engraving Tweaks

## Contexts

Common contexts: `Score`, `Staff`, `Voice`, `Lyrics`, `ChordNames`, `PianoStaff`, `StaffGroup`, `ChoirStaff`.

- `Voice` is where most music lives.
- `Staff` holds one or more voices and determines clef/instrument name.
- `Score` is the top-level container.

## Grobs and engravers

- A **grob** (graphical object) is something drawn: `NoteHead`, `Slur`, `TimeSignature`, `TextScript`.
- An **engraver** creates grobs. You can add or remove engravers from a context.

## Setting properties

```lilypond
\set Staff.instrumentName = "Violin I"
\set Staff.midiInstrument = "violin"
```

## Overrides and reverts

```lilypond
\once \override TextScript.extra-offset = #'(0 . 1)
c'4^\markup "solo"

\override Staff.TimeSignature.style = #'numbered
\revert Staff.TimeSignature.style
```

## Removing and adding engravers

```lilypond
\layout {
  \context {
    \Staff
    \remove "Time_signature_engraver"
    \consists "Horizontal_bracket_engraver"
  }
}
```

## Priority of tweaks

1. Semantic notation (the music itself)
2. Context property (`\set`)
3. Layout setting (`\paper`, `\layout`)
4. Local override (`\once \override`)
5. Scheme / custom engraver (last resort)

## Common mistakes

- Wrong context: `\override NoteHead.color` in `\Staff` may not apply if the grob lives in `\Voice`.
- Global overrides affect everything unless scoped with `\once` or nested in a specific context.
- Too many manual `extra-offset` tweaks make maintenance hard — converge repeated tweaks into a shared `.ily` style file.
- Imported scores often contain redundant overrides; consolidate them rather than layering more on top.
