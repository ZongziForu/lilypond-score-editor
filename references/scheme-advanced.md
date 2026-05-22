# Scheme Advanced Guide

- LilyPond embeds Scheme (Guile).
- Use Scheme only when normal LilyPond syntax cannot express the task.
- Treat Scheme as executable code — do not run untrusted Scheme.

## Basic forms

- `#'symbol` — a Scheme symbol.
- `#(expression)` — evaluate a Scheme expression.
- Markup commands can call Scheme functions.

## Examples

```lilypond
\override NoteHead.color = #red
\set Staff.instrumentName = #"Violin"

#(define (my-function x) (+ x 1))

\markup \bold \italic "Hello"
```

## Music functions

```lilypond
myRepeat =
#(define-music-function (parser location music) (ly:music?)
   #{ \repeat unfold 2 $music #})
```

## Warnings

- Do not overuse Scheme for simple edits that LilyPond syntax handles directly.
- Avoid `#(system ...)` or other OS-interacting calls in shared files.
- Keep Scheme usage minimal and well-commented for maintainability.
