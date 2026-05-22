---
name: lilypond-score-editor
description: Create, edit, debug, refactor, transpose, extract parts from, compile, render, and validate LilyPond music notation projects. Use this skill whenever the user mentions LilyPond, .ly files, .ily files, music engraving, score layout, sheet music generation, music notation, part extraction, transposition, chord symbols, lyrics, tablature, MIDI output from scores, or converting MusicXML/MIDI/ABC to LilyPond. Also use when the user wants to create, edit, fix, compile, or render sheet music, orchestral scores, lead sheets, piano music, guitar tabs, drum notation, choral scores, or any notation-editing tasks normally handled in scorewriters such as MuseScore, Dorico, Sibelius, or Finale. Even if the user does not explicitly say 'LilyPond', if they are working with music notation files or want to produce printed sheet music, use this skill.
allowed-tools:
  - Read
  - Write
  - Edit
  - MultiEdit
  - Bash(python *)
  - Bash(python3 *)
  - Bash(lilypond *)
  - Bash(find *)
  - Bash(grep *)
  - Bash(rg *)
  - Bash(git diff *)
  - Bash(git status *)
---

# LilyPond Score Editor

## Purpose

Use this skill to work on LilyPond notation projects. Prefer local files, scripts, and command-line validation over long in-context rewrites.

## Task input

When manually invoked, interpret $ARGUMENTS as the LilyPond task request.

Examples:

- /lilypond-score-editor create a lead sheet template
- /lilypond-score-editor fix score.ly
- /lilypond-score-editor compile score.ly
- /lilypond-score-editor extract parts from score.ly using parts-manifest.yaml
- /lilypond-score-editor transpose clarinet part up a whole step

## Core workflow

1. Determine task type:
   - create a new score
   - edit an existing score
   - debug a compilation error
   - transpose music
   - extract parts
   - add lyrics or chord names
   - adjust layout or engraving
   - clean imported MusicXML/MIDI/ABC
   - generate MIDI or rendered output
   - batch render scores

2. Inspect the project before editing:
   - \version
   - \include
   - variable definitions
   - \header
   - \paper
   - \layout
   - \midi
   - \score
   - \book
   - \bookpart
   - Staff / Voice / Lyrics / ChordNames contexts
   - existing style .ily files
   - existing build/output directories

3. Preserve project conventions:
   - keep variable names unless refactoring is requested
   - avoid flattening reusable variables
   - avoid broad rewrites for local edits
   - preserve comments
   - preserve indentation style where reasonable
   - prefer minimal, local changes
   - use \once \override for one-off layout fixes
   - use shared .ily files for repeated house style
   - use scripts for repetitive operations

4. Validate changes:
   - compile with: python "${CLAUDE_SKILL_DIR}/scripts/compile_lilypond.py" <file.ly>
   - inspect stdout/stderr
   - parse logs with: python "${CLAUDE_SKILL_DIR}/scripts/parse_lilypond_log.py"
   - fix syntax and bar-check errors before returning
   - **regenerate after every modification**: PDF and MIDI are produced together; recompile after each change so the user's outputs are never stale
   - show git diff when useful
   - if LilyPond is unavailable, explicitly say the score was not compiled

5. Safety:
   - LilyPond can evaluate Scheme/Guile code
   - treat untrusted .ly files as executable input
   - compile unknown files only in a trusted local project or sandbox

## Resource map

Use these references only when needed:

- references/syntax-cheatsheet.md: LilyPond syntax quick reference
- references/project-structure.md: common project layouts
- references/editing-workflows.md: create/edit/debug/transpose/layout workflows
- references/engraving-tweaks.md: context, grob, engraver, override guidance
- references/templates-and-patterns.md: how to choose and use bundled templates
- references/error-repair-guide.md: common compiler errors and repairs
- references/instrument-ranges-and-pitfalls.md: instrument ranges, piano voicing, `\relative` drift, dynamic placement, slur usage
- references/notation-software-feature-map.md: GUI scorewriter operation to LilyPond mapping
- references/scripted-part-extraction.md: token-efficient score-to-parts workflow
- references/scheme-advanced.md: Scheme guidance and safety

## Script map

Use scripts from ${CLAUDE_SKILL_DIR}/scripts/:

- compile_lilypond.py: compile one .ly file (supports pdf/png/svg/ps, resolution, backend, preview)
- parse_lilypond_log.py: parse LilyPond stdout/stderr/log text
- check_measure_durations.py: heuristic bar duration checks (supports tuplets and compound meters like 7+5/8)
- normalize_lilypond_format.py: conservative formatting
- batch_render.py: compile multiple .ly files (same options as compile_lilypond.py)
- extract_parts.py: generate and optionally compile part wrapper files from a manifest
- auto_manifest.py: auto-generate a parts manifest from a .ly score by detecting variables and staves

## Editing principles

- Prefer semantic notation changes before visual hacks.
- Do not use Scheme unless normal LilyPond syntax cannot solve the task.
- For transposition, prefer \transpose or reusable variables over manually rewriting every pitch.
- For parts, keep a shared source of truth and generate wrappers, separate \score, or \bookpart blocks.
- For layout, first try \paper, \layout, spacing, breaks, and context settings before manual offsets.
- For imported MusicXML/MIDI/ABC, expect cleanup: voices, ties, beams, lyrics, enharmonics, repeats, and layout usually need repair.
- For score-to-parts tasks, do not copy large music blocks into each part. Prefer shared variables + manifest + wrapper generation.

---

# LilyPond 乐谱编辑器 — 中文说明

## 用途

使用此技能处理 LilyPond 记谱项目。优先使用本地文件、脚本和命令行验证，而非在对话上下文中进行长篇幅重写。

## 任务输入

手动调用时，将 $ARGUMENTS 解释为 LilyPond 任务请求。

示例：

- /lilypond-score-editor 新建一个领谱模板
- /lilypond-score-editor 修复 score.ly
- /lilypond-score-editor 编译 score.ly
- /lilypond-score-editor 从 score.ly 提取分谱
- /lilypond-score-editor 将单簧管分谱移高大二度

## 核心工作流

1. 确定任务类型：创建新乐谱、编辑现有乐谱、调试编译错误、移调、提取分谱、添加歌词或和弦、调整布局或排版、清理导入的 MusicXML/MIDI/ABC、生成 MIDI 或渲染输出、批量渲染乐谱。

2. 编辑前检查项目结构：\version、\include、变量定义、\header、\paper、\layout、\midi、\score、\book、\bookpart、Staff/Voice/Lyrics/ChordNames 上下文、现有 .ily 样式文件、现有 build/output 目录。

3. 保持项目惯例：除非要求重构，保留变量名；避免展平可复用变量；避免对局部编辑进行大规模重写；保留注释；合理保留缩进风格；优先最小局部修改；使用 \once \override 进行一次性布局修复；使用共享 .ily 文件管理重复样式；使用脚本处理重复操作。

4. 验证更改：编译、检查输出、解析日志、修复语法和小节检查错误、每次修改后重新生成 PDF 和 MIDI、必要时显示 git diff。如果 LilyPond 不可用，明确说明乐谱未编译。

5. 安全：LilyPond 可执行 Scheme/Guile 代码。将不可信的 .ly 文件视为可执行输入。仅在受信任的本地项目或沙箱中编译未知文件。

## 资源索引

按需查阅以下参考文件：

- references/syntax-cheatsheet.zh.md：语法速查
- references/project-structure.zh.md：项目结构指南
- references/editing-workflows.zh.md：编辑工作流
- references/engraving-tweaks.zh.md：排版微调
- references/templates-and-patterns.zh.md：模板选择
- references/error-repair-guide.zh.md：错误修复
- references/instrument-ranges-and-pitfalls.zh.md：乐器音域
- references/notation-software-feature-map.zh.md：功能映射
- references/scripted-part-extraction.zh.md：分谱提取
- references/scheme-advanced.zh.md：Scheme 参考

## 脚本索引

使用 ${CLAUDE_SKILL_DIR}/scripts/ 中的脚本：

- compile_lilypond.py：编译单个 .ly 文件（支持 pdf/png/svg/ps、分辨率、后端、预览）
- parse_lilypond_log.py：解析 LilyPond 标准输出/错误/日志
- check_measure_durations.py：小节时值检查（支持连音和复合拍号如 7+5/8）
- normalize_lilypond_format.py：保守格式化
- batch_render.py：批量编译多个 .ly 文件
- extract_parts.py：从清单生成并可选编译分谱包装文件
- auto_manifest.py：通过检测变量和谱表自动生成分谱清单

## 编辑原则

- 优先语义化记谱调整，再考虑视觉 hack。
- 除非普通 LilyPond 语法无法解决任务，不要使用 Scheme。
- 移调优先使用 \transpose 或可复用变量，而不是手动重写每个音。
- 分谱保持共享源头，生成包装文件、独立的 \score 或 \bookpart 块。
- 布局优先尝试 \paper、\layout、间距、换行和上下文设置，再考虑手动偏移。
- 导入的 MusicXML/MIDI/ABC 需要清理：声部、连音线、符杠、歌词、等音、反复和布局通常需要修复。
- 分谱提取任务不要将大型音乐块复制到每个分谱文件中。优先使用共享变量 + 清单 + 包装文件生成。
