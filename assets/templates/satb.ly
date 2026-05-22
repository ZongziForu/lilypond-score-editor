\version "2.24.4"

\header {
  title = "SATB Choir Piece"
  composer = "Composer"
}

global = {
  \key c \major
  \time 4/4
}

soprano = \relative c'' {
  \global
  c4 d e f |
  g2 g |
}

alto = \relative c' {
  \global
  c4 c c c |
  e2 e |
}

tenor = \relative c' {
  \global
  \clef "treble_8"
  g4 g g g |
  c2 c |
}

bass = \relative c {
  \global
  \clef bass
  c4 e g c |
  c,2 c |
}

verse = \lyricmode {
  Hap -- py birth -- day to you
}

\score {
  \new ChoirStaff <<
    \new Staff = "soprano" \with { instrumentName = "Soprano" } <<
      \new Voice = "soprano" { \soprano }
      \new Lyrics \lyricsto "soprano" \verse
    >>
    \new Staff = "alto" \with { instrumentName = "Alto" } \alto
    \new Staff = "tenor" \with { instrumentName = "Tenor" } \tenor
    \new Staff = "bass" \with { instrumentName = "Bass" } \bass
  >>
  \layout { }
  \midi { }
}
