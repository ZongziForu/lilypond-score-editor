# Scheme 高级指南

- LilyPond 内嵌了 Scheme（Guile）。
- 仅当普通 LilyPond 语法无法表达任务时才使用 Scheme。
- 将 Scheme 视为可执行代码——不要运行不受信任的 Scheme。

## 基本形式

- `#'symbol` — Scheme 符号。
- `#(expression)` — 计算 Scheme 表达式。
- Markup 命令可以调用 Scheme 函数。

## 示例

```lilypond
\override NoteHead.color = #red
\set Staff.instrumentName = #"Violin"

#(define (my-function x) (+ x 1))

\markup \bold \italic "Hello"
```

## 音乐函数

```lilypond
myRepeat =
#(define-music-function (parser location music) (ly:music?)
   #{ \repeat unfold 2 $music #})
```

## 警告

- 不要对 LilyPond 语法能直接处理的简单编辑过度使用 Scheme。
- 避免在共享文件中使用 `#(system ...)` 或其他与操作系统交互的调用。
- 保持 Scheme 用法最小化并添加清晰注释，以便维护。
