\version "2.24.4"

\header {
  title = "Piano Piece"
  composer = "Composer"
}

global = {
  \key c \major
  \time 4/4
}

rightHand = \relative c' {
  \global
  c4 d e f |
  g2 g |
}

leftHand = \relative c {
  \global
  \clef bass
  c4 e g c |
  g2 g |
}

\score {
  \new PianoStaff \with { instrumentName = "Piano" } <<
    \new Staff = "right" \rightHand
    \new Staff = "left" \leftHand
  >>
  \layout { }
  \midi { }
}
