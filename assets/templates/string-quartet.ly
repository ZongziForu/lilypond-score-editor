\version "2.24.4"

\header {
  title = "String Quartet"
  composer = "Composer"
}

global = {
  \key c \major
  \time 4/4
}

violinI = \relative c'' {
  \global
  c4 d e f |
  g2 g |
}

violinII = \relative c'' {
  \global
  g4 a b c |
  d2 d |
}

viola = \relative c' {
  \global
  \clef alto
  e4 f g a |
  b2 b |
}

cello = \relative c {
  \global
  \clef bass
  c4 e g c |
  g2 g |
}

\score {
  \new StaffGroup <<
    \new Staff \with { instrumentName = "Violin I" } \violinI
    \new Staff \with { instrumentName = "Violin II" } \violinII
    \new Staff \with { instrumentName = "Viola" } \viola
    \new Staff \with { instrumentName = "Cello" } \cello
  >>
  \layout { }
  \midi { }
}
