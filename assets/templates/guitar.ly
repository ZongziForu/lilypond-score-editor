\version "2.24.4"

\header {
  title = "Guitar Piece"
  composer = "Composer"
}

global = {
  \key c \major
  \time 4/4
}

% Standard notation staff
guitarMusic = \relative c' {
  \global
  \clef "treble_8"
  c4 d e f |
  g2 g |
}

% Optional: tablature staff (uncomment to use)
% guitarTab = \relative c' {
%   \global
%   c4 d e f |
%   g2 g |
% }

\score {
  <<
    \new Staff \with { instrumentName = "Guitar" } \guitarMusic
    % \new TabStaff \with { instrumentName = "Tab" } \guitarTab
  >>
  \layout { }
  \midi { }
}
