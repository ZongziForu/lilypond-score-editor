# Instrument Ranges and Notation Pitfalls

Know the playable range of instruments before writing music. LilyPond will happily engrave
notes outside a real instrument's range — the output looks correct but is unplayable.

## Common instrument ranges

| Instrument | Written range | Notes |
|------------|---------------|-------|
| Violin | G3 – E7 (practical: G3 – D7) | Avoid sustained notes below G3 (open G string); highest positions are possible but avoid prolonged C7+ |
| Viola | C3 – E6 | Alto clef; open C string is lowest note |
| Cello | C2 – C6 | Bass clef (tenor/treble for high passages) |
| Double bass | E1 – G4 | Sounds an octave lower than written |
| Flute | C4 – C7 | Low register (C4–C5) is soft; middle (C5–C6) projecting; high (C6+) can be shrill |
| Clarinet | E3 – C7 | Written pitch (sounds lower depending on transposition) |
| Trumpet | F#3 – C6 | Written pitch (sounds a major 2nd lower for Bb trumpet) |
| French horn | F2 – C6 | Written pitch (sounds a 5th lower for F horn) |
| Trombone | E2 – F5 | Bass clef |
| Piano | A0 – C8 | Full 88-key range; block chords in the middle two octaves (C3–C5) are warmest |

## Piano writing pitfalls

### 1. Right hand register (most common mistake)

Do not write piano right-hand block chords in the same octave as a solo violin melody.
The chord tones mask the melody. Place piano chords **1–2 octaves below** the solo line.

```
Violin:  g''4 b'' d'''   (G4–D5)
Piano:   <g b d'>        (G3–D4) ← one octave below, warm and supporting
         NOT <g' b' d''> (G4–D5) ← clashes with melody
```

### 2. `\relative` mode and chords

`\relative` mode tracks the **last note of the previous chord** as a reference.
This causes gradual octave drift upward or downward when consecutive chords
are written without explicit octave marks.

```lilypond
% BAD — register drifts:
\relative c' {
  <g b d>2. |  % G3 B3 D4  (ok)
  <g b d>2. |  % G4 B4 D5  (drifted up!)
}
```

**Fix 1 — Absolute pitch** (recommended for all chordal parts):
```lilypond
{
  <g b d'>2. |  % G3 B3 D4 — always exact
  <g b d'>2. |  % G3 B3 D4 — same
}
```

**Fix 2 — Octave marks** (if you must use `\relative`):
```lilypond
\relative c' {
  <g b d>2. |   % G3 B3 D4
  <g, b d>2. |  % G3 B3 D4 — forced down with ,
}
```

### 3. Chord voicing

Block chords (`<c e g>`) in the piano's middle register (C3–C5) sound warmest.
- Below C3: block chords become muddy (close voicing in low register)
- Above C5: block chords become thin for sustained accompaniment

Prefer **close voicing** (notes packed within an octave) for block chords in the
middle register, and **open voicing** (spread across >1 octave) for low-register chords.

## Dynamic placement

Dynamics (`\p`, `\mf`, `\dim`, etc.) must be attached directly to a note or
preceded by an invisible note. Placing them standalone between notes causes
"missing attached object" warnings.

```lilypond
c4\p d e f |            % OK — attached to c4
\p c4 d e f |            % WRONG — warning
c4 d e f |
\dim c4 d e f |          % WRONG — warning
```

## Time signature in final measures

The final measure must respect the time signature. A `1` (whole note, 4 beats)
in a `3/4` measure triggers a bar check warning even if followed by `\fermata`.

```lilypond
% BAD in 3/4:
g2. | b1\fermata \bar "|."  % b1 = 4 beats in 3/4 bar — warning

% GOOD in 3/4:
g2. | b2.\fermata \bar "|."  % b2. = 3 beats — correct
```

If you want a held final note, either:
- Use the correct duration for the meter (`2.` for 3/4, `1` for 4/4)
- Change time signature before the final measure: `\time 4/4 b1\fermata`

## Slur usage

Two types exist in LilyPond. Do not mix them in the same voice:

| Slur type | Syntax | Use |
|-----------|--------|-----|
| Regular slur | `c( d e)` | Phrasing within a voice, ≤1 active per voice |
| Phrasing slur | `c\( d e\)` | Long-range phrasing, useful across `\bar` but limited nesting |

Nesting a regular slur inside a phrasing slur (or vice versa) works, but
**two active phrasing slurs** (`\(` inside `\(`) in the same voice causes
warnings and incorrect output. Use only one type per musical line.
