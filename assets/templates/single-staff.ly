\version "2.24.4"

\header {
  title = "Single Staff Piece"
  composer = "Composer"
}

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
  \new Staff \melody
  \layout { }
  \midi { }
}
