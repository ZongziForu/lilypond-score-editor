\version "2.24.4"

\header {
  title = "Lead Sheet"
  composer = "Composer"
}

global = {
  \key c \major
  \time 4/4
}

chordNames = \chordmode {
  c2 g:7 f c
}

melody = \relative c' {
  \global
  c4 d e f |
  g2 g |
}

verseOne = \lyricmode {
  Hap -- py birth -- day to you
}

\score {
  <<
    \new ChordNames \chordNames
    \new Staff \with { instrumentName = "Melody" } <<
      \new Voice = "melody" { \melody }
      \new Lyrics \lyricsto "melody" \verseOne
    >>
  >>
  \layout { }
  \midi { }
}
