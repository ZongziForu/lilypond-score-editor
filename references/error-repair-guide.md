# Error Repair Guide

## General rule

Do not rewrite the entire file because of one error. Look at the error line and the surrounding ~20 lines. Many errors are caused by unmatched braces, missing durations, or typos earlier in the file.

## Syntax error / unexpected token

- **Cause**: missing brace, unexpected symbol, misplaced keyword.
- **Inspection**: check line number and the line before it for unclosed `{`, `<<`, `(`, or `[`.
- **Repair**: add the missing delimiter or remove the stray token.

## Unknown escaped string / not a note name

- **Cause**: typo like `\abc` or `h` instead of `b` in English nomenclature.
- **Inspection**: verify note names and command spellings.
- **Repair**: correct the typo.

## Bar check failed

- **Cause**: note durations inside a measure do not add up to the time signature.
- **Inspection**: count durations in the flagged measure.
- **Repair**: add missing rests, fix durations, or correct the time signature.

## Cannot find file

- **Cause**: `\include` path is wrong or file is missing.
- **Inspection**: check path relative to the compiled file.
- **Repair**: fix path or create the missing file.

## Wrong type for argument

- **Cause**: passing music to a function expecting a string, or vice versa.
- **Inspection**: check the function signature.
- **Repair**: wrap or unwrap the argument correctly.

## Guile/Scheme error

- **Cause**: invalid Scheme expression inside `#(...)`.
- **Inspection**: look at the Scheme expression near the error line.
- **Repair**: fix quoting, parentheses, or function names.

## Unmatched braces / `<< >>`

- **Cause**: missing closing `}`, `>>`, `)`, or `]`.
- **Inspection**: use the compiler hint; if none, bisect the file or use a brace-matching editor.
- **Repair**: add the missing closer.

## Lyrics do not align

- **Cause**: syllable count does not match available notes (often due to tied or slurred notes).
- **Inspection**: compare lyric syllables to note events.
- **Repair**: add `__` for melismas or adjust lyrics.

## Warning vs fatal error

- Warnings usually produce output but indicate engraving problems.
- Fatal errors stop compilation. Fix fatals first; then review warnings.

## Example repair

Given:
```lilypond
\relative c' { c4 d e f | g2 g }
```

Error: `syntax error, unexpected '}'`
Cause: missing bar check or `|` before the final `}` is not the issue — likely a missing `|` is fine, but here the real issue is often an earlier unmatched brace. In this tiny example it compiles; scale up and watch nesting carefully.
