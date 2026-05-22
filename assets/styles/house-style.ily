% House style include file
% Use with: \include "house-style.ily"

\paper {
  tagline = ##f
}

% Uncomment to adjust global staff size
% #(set-global-staff-size 18)

\layout {
  \context {
    \Score
    % Example: hide bar numbers
    % \remove "Bar_number_engraver"
  }
}
