# LilyPond 项目结构

## 最小文件

```lilypond
\version "2.24.4"

\header {
  title = "标题"
  composer = "作曲者"
}

\score {
  \new Staff {
    \clef treble
    \key c \major
    \time 4/4
    c'4 d' e' f' |
    g'2 g' |
  }
  \layout { }
  \midi { }
}
```

## 可复用变量和全局块

```lilypond
\version "2.24.4"

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
  \new Staff <<
    \global
    \melody
  >>
  \layout { }
  \midi { }
}
```

## 多行谱表

```lilypond
\new StaffGroup <<
  \new Staff { \clef treble \violinMusic }
  \new Staff { \clef bass \celloMusic }
>>
```

## 钢琴谱

```lilypond
\new PianoStaff <<
  \new Staff = "right" \rightHand
  \new Staff = "left" \leftHand
>>
```

## 歌词绑定

```lilypond
\new Staff \with { instrumentName = "Soprano" } \soprano
\new Lyrics \lyricsto "soprano" \sopranoLyrics
```

## 和弦标记

```lilypond
\new ChordNames \chordNames
\new Staff \melody
\new Lyrics \lyricsto "melody" \verseLyrics
```

## Score / Book / Bookpart

- `\score` = 一个乐谱块
- `\book` = 乐谱集合，可设置输出文件名
- `\bookpart` = book 内的章节，适合独立标题或分页

```lilypond
\book {
  \bookOutputName "full-score"
  \score { ... \layout { } }
}
```

## 包含文件和共享样式

```lilypond
\include "layout.ily"
\include "music.ily"
```

将 house style 放在共享的 `.ily` 文件中，所有乐谱和分谱统一继承。

## 分谱提取结构

大项目推荐的结构：

```
project/
├── score.ly           % 总谱
├── music.ily          % 所有共享音乐变量
├── layout.ily         % 共享的 paper/layout/style
├── parts-manifest.yaml
├── parts/
│   ├── violin-i.ly    % 自动生成的分谱包装
│   └── cello.ly       % 自动生成的分谱包装
└── build/             % 输出的 PDF/MIDI
```

分谱包装文件 `\include` 共享源文件，引用变量，而不是将音乐块复制到每个分谱文件中。
