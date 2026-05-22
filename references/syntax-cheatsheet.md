# LilyPond Syntax Cheatsheet

Quick reference for Claude Code when reading or writing `.ly` files.

## Version

```lilypond
\version "2.24.4"
```

## Notes and rests

```lilypond
c4 d e f    % notes
g'2 a,4     % octave up/down from middle C
r4 r2       % rests
```

## Durations

```lilypond
c1 c2 c4 c8 c16 c32   % whole, half, quarter, eighth...
c4. c4..              % dotted values
```

- Omitting a duration repeats the previous duration.

## Octave marks

```lilypond
c'   % one octave above middle C
c,   % one octave below middle C
c''  % two octaves above
c,,  % two octaves below
```

## Accidentals

```lilypond
cis4 des ees fisis   % sharp/flat/double-sharp
```

## Relative mode

```lilypond
\relative c' { c d e f }   % first note is c'
\relative { c d e f }      % defaults to f as reference
```

- Octaves are inferred from the *previous* note. A jump of a fourth or more does not change octave unless marked.

## Absolute pitch

```lilypond
\absolute { c'4 d' e' f' }
```

## Key, time, clef, tempo

```lilypond
\key g \major
\time 3/4
\clef treble
\tempo "Allegro" 4 = 120
```

## Bar checks

```lilypond
c4 d e f | g2 g |
```

- `|` is a bar check (sanity check), not a required printed bar line.

## Ties, slurs, phrasing

```lilypond
c2~ c2       % tie (same pitch)
c4( d e f)   % slur
c4\( d e f\) % phrasing slur
```

## Beams

```lilypond
c8[ d e f]   % manual beam
```

## Articulations

```lilypond
c4-. c-> c-. c-^
c4\staccato c\accent
```

## Dynamics and hairpins

```lilypond
c4\p d\f e2\ff
c2\< d2\> c2\!
```

## Chords

```lilypond
<c e g>2 <c f a>4   % simultaneous sounding
```

## Polyphony

```lilypond
<<
  \relative { c'4 d e f }
  \\
  \relative { c'2 c }
>>
```

## Tuplets

```lilypond
\tuplet 3/2 { c4 d e }
\tuplet 5/4 { c8 d e f g }
```

## Grace notes

```lilypond
\grace c8 d4
\appoggiatura c8 d4
```

## Repeats and alternatives

```lilypond
\repeat volta 2 { c4 d e f }
\alternative {
  { g2 g }
  { a2 a }
}
```

## Lyrics

```lilypond
verse = \lyricmode {
  Hap -- py birth -- day to __ you
}
\new Lyrics \lyricsto "voice" \verse
```

- `--` = syllable hyphen
- `__` = melisma extender

## Chord names

```lilypond
chords = \chordmode { c2 g:sus4 f:m7 }
\new ChordNames \chords
```

## Markup

```lilypond
c4^\markup \italic "solo"
\header { title = "My Piece" composer = "Me" }
```

## Comments and includes

```lilypond
% line comment
\include "layout.ily"
```

## Common pitfalls

- `\relative` octave inference surprises: large leaps keep the octave unless explicitly marked with `'` or `,`.
- Missing durations inherit the previous one — easy to accidentally write all quarter notes.
- `|` is a bar check; it does not insert a printed bar line by itself (but usually coincides with one).
- `~` is a tie and only works between identical pitches; slurs use `(` and `)`.
- `<c e g>` is a chord sounding together; `<< ... \\ ... >>` is polyphony on one staff.
- LilyPond files can contain executable Scheme/Guile code. Do not compile untrusted `.ly` files blindly.
