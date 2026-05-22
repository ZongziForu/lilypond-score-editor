# 编辑工作流

## 创建乐谱工作流

1. 确定乐器编制、调性、节拍、弱起、歌词、和弦、MIDI 需求。
2. **检查乐器音域**（参见 `references/instrument-ranges-and-pitfalls.md`）—— LilyPond 不会阻止你写出不可演奏的音符。
3. 从 `${CLAUDE_SKILL_DIR}/assets/templates` 选择模板。
4. 将模板复制到项目中。
5. 编辑 `\header`、调号、节拍和 global 块。
6. 填入音乐变量。
7. 编译并修复错误。

## 编辑现有乐谱工作流

1. 检查结构：`\version`、变量、上下文、include。
2. 定位目标声部、谱表或小节。
3. 做最小、精准的修改。
4. 编译。
5. 解析日志并修复问题。
6. 显示相关的 git diff。

## 调试工作流

1. 运行编译。
2. 使用 `parse_lilypond_log.py` 解析日志。
3. 记录行号/列号。
4. 检查周围的括号和音乐表达式。
5. 逐步修复（一次解决一个问题）。
6. 重新编译并确认。
7. **每次修改后重新生成 PDF + MIDI**——不要让输出文件过时。

## 转调工作流

1. 区分音乐会音高和移调音高。
2. 优先使用 `\transpose` 而不是手动重写每个音。
3. 尽可能将源变量保持在音乐会音高。
4. 注意等音替换的风险。
5. 示例：
   ```lilypond
   \transpose c d { \clarinetMusic }
   ```

## 分谱提取工作流

1. 识别谱表及其音乐变量。
2. 优先使用清单 + 包装文件生成。
3. 运行 `extract_parts.py`。
4. 每个分谱生成一个输出文件。
5. 保留共享的全局设置。
6. 如果源文件没有独立的变量，请先重构出变量。

## 歌词工作流

1. 使用 `\lyricmode` 定义歌词文本。
2. 使用 `\lyricsto` 绑定到指定的命名声部。
3. 用 `__` 处理同音延音（melisma）。
4. 用 `--` 处理音节连接。
5. 检查编译器中关于歌词对齐的警告。

## 和弦标记工作流

1. 使用 `\chordmode` 定义和声内容。
2. 放在 `\new ChordNames` 上下文中。
3. 与旋律和歌词结合制成领谱。

## 排版工作流

1. 使用 `\paper` 设置页面级属性（尺寸、边距、分页）。
2. 使用 `\layout` 设置排版和上下文设置。
3. 节制使用分行/分页符。
4. 使用 `\once \override` 做局部微调。
5. 除非明确要求，避免全局 override。

## 导入清理工作流

`musicxml2ly`、`midi2ly`、`abc2ly` 生成的文件通常需要清理：

- 声部和多声部
- 节奏拼写和冗余连音
- 等音
- 反复和房子
- 连线和符杠
- 歌词对齐
- 排版和间距
- 变量名
- 冗余的样板代码

## 批量转调工作流

适用于转调多个乐器或将整个乐谱移至新调：

1. 保持源变量为音乐会音高。
2. 在每个谱表或分谱包装中使用 `\transpose`。
3. 对于全乐谱调性变换，在 `\score` 级别应用 `\transpose` 或重新生成包装文件。
4. 示例：从音乐会音高生成 Bb 单簧管分谱：
   ```lilypond
   \new Staff \with { instrumentName = "Clarinet in Bb" }
   \transpose bes c' { \melody }
   ```
5. 使用 `extract_parts.py` 的 per-part `transposition` 字段批量生成移调分谱。

## MIDI 工作流

在 `\score` 块内使用 `\midi { }` 以启用编译时的 MIDI 输出。

```lilypond
\score {
  \new Staff \melody
  \layout { }
  \midi { }
}
```

- 在 `global` 块或 `\midi { \tempo 4 = 120 }` 中设置 `\tempo`。
- 使用 `\set Staff.midiInstrument = "violin"` 为各谱表指定正确的乐器音色。
- 编译后检查是否存在 `.midi` 文件来验证 MIDI 是否已生成。
- 如果不需要 MIDI，省略 `\midi { }` 块以减少编译时间。
