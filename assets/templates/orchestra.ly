\version "2.24.4"

\header {
  title = "Orchestral Score"
  composer = "Composer"
}

global = {
  \key c \major
  \time 4/4
  \tempo "Allegro" 4 = 120
}

fluteMusic = \relative c'' {
  \global
  c4 d e f |
  g2 g |
}

oboeMusic = \relative c'' {
  \global
  e4 f g a |
  b2 b |
}

clarinetMusic = \relative c'' {
  \global
  \transposition bes
  d4 e fis g |
  a2 a |
}

bassoonMusic = \relative c {
  \global
  \clef bass
  c4 e g c |
  g2 g |
}

hornMusic = \relative c'' {
  \global
  \transposition f
  g4 a b c |
  d2 d |
}

trumpetMusic = \relative c'' {
  \global
  \transposition bes
  c4 d e f |
  g2 g |
}

tromboneMusic = \relative c' {
  \global
  \clef bass
  c4 d e f |
  g2 g |
}

violinIMusic = \relative c'' {
  \global
  c4 d e f |
  g2 g |
}

violinIIMusic = \relative c'' {
  \global
  g4 a b c |
  d2 d |
}

violaMusic = \relative c' {
  \global
  \clef alto
  e4 f g a |
  b2 b |
}

celloMusic = \relative c {
  \global
  \clef bass
  c4 e g c |
  g2 g |
}

doubleBassMusic = \relative c, {
  \global
  \clef "bass_8"
  c4 e g c |
  g2 g |
}

\score {
  <<
    \new StaffGroup = "Woodwinds" <<
      \new Staff \with { instrumentName = "Flute" } \fluteMusic
      \new Staff \with { instrumentName = "Oboe" } \oboeMusic
      \new Staff \with { instrumentName = "Clarinet in Bb" } \clarinetMusic
      \new Staff \with { instrumentName = "Bassoon" } \bassoonMusic
    >>
    \new StaffGroup = "Brass" <<
      \new Staff \with { instrumentName = "Horn in F" } \hornMusic
      \new Staff \with { instrumentName = "Trumpet in Bb" } \trumpetMusic
      \new Staff \with { instrumentName = "Trombone" } \tromboneMusic
    >>
    \new StaffGroup = "Strings" <<
      \new Staff \with { instrumentName = "Violin I" } \violinIMusic
      \new Staff \with { instrumentName = "Violin II" } \violinIIMusic
      \new Staff \with { instrumentName = "Viola" } \violaMusic
      \new Staff \with { instrumentName = "Cello" } \celloMusic
      \new Staff \with { instrumentName = "Double Bass" } \doubleBassMusic
    >>
  >>
  \layout { }
  \midi { }
}
