# LilyPond 语法速查

Claude Code 在读写 `.ly` 文件时的快速参考。

## 版本声明

```lilypond
\version "2.24.4"
```

## 音符和休止符

```lilypond
c4 d e f    % 音名
g'2 a,4     % 高/低八度（相对于中央C）
r4 r2       % 休止符
```

## 时值

```lilypond
c1 c2 c4 c8 c16 c32   % 全音符、二分、四分、八分、十六分、三十二分
c4. c4..              % 附点音符
```

- 省略时值会沿用前一个音符的时值。

## 八度标记

```lilypond
c'   % 比中央C高一八度
c,   % 比中央C低一八度
c''  % 高两个八度
c,,  % 低两个八度
```

## 变音记号

```lilypond
cis4 des ees fisis   % 升号/降号/重升
```

## 相对模式

```lilypond
\relative c' { c d e f }   % 第一个音是 c'
\relative { c d e f }      % 默认以 f 为参照
```

- 八度基于**前一个音符**推断。四度及以上的跳进不会自动变八度，除非手动标记。

## 绝对模式

```lilypond
\absolute { c'4 d' e' f' }
```

## 调号、拍号、谱号、速度

```lilypond
\key g \major
\time 3/4
\clef treble
\tempo "Allegro" 4 = 120
```

## 小节检查

```lilypond
c4 d e f | g2 g |
```

- `|` 是小节检查（验证时值正确性），不是打印的终止线。

## 连音线、圆滑线、分句线

```lilypond
c2~ c2       % 同音连线
c4( d e f)   % 圆滑线
c4\( d e f\) % 分句线
```

## 连谱号

```lilypond
c8[ d e f]   % 手动控制符杠
```

## 演奏法记号

```lilypond
c4-. c-> c-. c-^
c4\staccato c\accent
```

## 力度和渐强/渐弱

```lilypond
c4\p d\f e2\ff
c2\< d2\> c2\!
```

## 和弦

```lilypond
<c e g>2 <c f a>4   % 同时发声
```

## 多声部

```lilypond
<<
  \relative { c'4 d e f }
  \\
  \relative { c'2 c }
>>
```
