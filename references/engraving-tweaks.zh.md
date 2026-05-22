# 排版微调

## 上下文（Contexts）

常用上下文：`Score`、`Staff`、`Voice`、`Lyrics`、`ChordNames`、`PianoStaff`、`StaffGroup`、`ChoirStaff`。

- `Voice` 是大多数音乐所在的位置。
- `Staff` 包含一个或多个声部，并决定谱号和乐器名称。
- `Score` 是顶层容器。

## Grobs 和 engravers

- **grob**（图形对象）是被绘制出来的元素：`NoteHead`、`Slur`、`TimeSignature`、`TextScript`。
- **engraver** 负责创建 grob。你可以从上下文中添加或移除 engraver。

## 设置属性

```lilypond
\set Staff.instrumentName = "Violin I"
\set Staff.midiInstrument = "violin"
```

## Override 和 revert

```lilypond
\once \override TextScript.extra-offset = #'(0 . 1)
c'4^\markup "solo"

\override Staff.TimeSignature.style = #'numbered
\revert Staff.TimeSignature.style
```

## 移除和添加 engraver

```lilypond
\layout {
  \context {
    \Staff
    \remove "Time_signature_engraver"
    \consists "Horizontal_bracket_engraver"
  }
}
```

## 微调的优先级

1. 语义化记谱（音乐本身）
2. 上下文属性（`\set`）
3. 布局设置（`\paper`、`\layout`）
4. 局部 override（`\once \override`）
5. Scheme / 自定义 engraver（最后手段）

## 常见错误

- 上下文错误：如果 grob 位于 `\Voice` 中，在 `\Staff` 层级执行 `\override NoteHead.color` 可能无效。
- 全局 override 会影响所有内容，除非使用 `\once` 限定范围或嵌套在特定上下文中。
- 过多的手动 `extra-offset` 微调会增加维护难度——将重复的微调收敛到共享的 `.ily` 样式文件中。
- 导入的乐谱通常包含冗余的 override；应合并它们，而不是在其上层层叠加。
