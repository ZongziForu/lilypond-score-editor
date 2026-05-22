\version "2.24.4"

\header {
  title = "Ukulele Piece"
  composer = "Composer"
}

global = {
  \key c \major
  \time 4/4
}

ukuleleMusic = \relative c'' {
  \global
  \clef treble
  c4 d e f |
  g2 g |
}

\score {
  \new Staff \with { instrumentName = "Ukulele" } \ukuleleMusic
  \layout { }
  \midi { }
}
