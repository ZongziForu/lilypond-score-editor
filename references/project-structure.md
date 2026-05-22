# LilyPond Project Structure

## Minimal file

```lilypond
\version "2.24.4"

\header {
  title = "Title"
  composer = "Composer"
}

\score {
  \new Staff {
    \clef treble
    \key c \major
    \time 4/4
    c'4 d' e' f' |
    g'2 g' |
  }
  \layout { }
  \midi { }
}
```

## Reusable variables and global

```lilypond
\version "2.24.4"

global = {
  \key c \major
  \time 4/4
}

melody = \relative c' {
  \global
  c4 d e f |
  g2 g |
}

\score {
  \new Staff <<
    \global
    \melody
  >>
  \layout { }
  \midi { }
}
```

## Multiple staves

```lilypond
\new StaffGroup <<
  \new Staff { \clef treble \violinMusic }
  \new Staff { \clef bass \celloMusic }
>>
```

## Piano staff

```lilypond
\new PianoStaff <<
  \new Staff = "right" \rightHand
  \new Staff = "left" \leftHand
>>
```

## Lyrics attachment

```lilypond
\new Staff \with { instrumentName = "Soprano" } \soprano
\new Lyrics \lyricsto "soprano" \sopranoLyrics
```

## Chord names

```lilypond
\new ChordNames \chordNames
\new Staff \melody
\new Lyrics \lyricsto "melody" \verseLyrics
```

## Score / book / bookpart

- `\score` = one engraved score block.
- `\book` = collection of scores; can set output name.
- `\bookpart` = section within a book, useful for separate titling or page breaks.

```lilypond
\book {
  \bookOutputName "full-score"
  \score { ... \layout { } }
}
```

## Include files and shared style

```lilypond
\include "layout.ily"
\include "music.ily"
```

Keep house style in a shared `.ily` so all scores and parts inherit the same settings.

## Part extraction pattern

The preferred pattern for large projects:

```
project/
├── score.ly           % full score assembly
├── music.ily          % all shared music variables
├── layout.ily         % shared paper/layout/style
├── parts-manifest.yaml
├── parts/
│   ├── violin-i.ly    % generated wrapper
│   └── cello.ly       % generated wrapper
└── build/             % output PDFs/MIDI
```

Part wrappers `\include` the shared source and reference variables. Do not copy music blocks into each part file.
