# lilypond-score-editor

用于创建、编辑、调试和渲染 LilyPond 乐谱项目的 Claude Code 技能。

## 使用方法

在 Claude Code 中，当你处理 LilyPond 文件（`.ly`、`.ily`）时，该技能会自动触发。你也可以手动调用：

```
/lilypond-score-editor 创建一首钢琴曲
/lilypond-score-editor 修复 score.ly
/lilypond-score-editor 从 score.ly 中提取分谱
```

## 功能特性

- **乐谱创建** — 包含钢琴、吉他、贝斯、尤克里里、架子鼓、领谱、SATB 合唱、弦乐四重奏、管弦乐队等多种模板
- **辅助脚本** — 编译、批量渲染、分谱提取、日志解析、小节时值检查、自动生成分谱清单、格式化
- **参考文档** — 语法速查、项目结构指南、编辑工作流、排版微调、错误修复、乐器音域、制谱软件功能映射、Scheme 参考
- **分谱提取** — 基于清单的工作流，支持从现有乐谱自动检测变量
- **MIDI 输出** — 每个 `\score` 块集成 MIDI 生成

## 目录结构

```
├── SKILL.md                  # 技能入口
├── assets/
│   ├── styles/
│   └── templates/            # 可直接使用的 .ly 模板
├── references/               # 详细指南
├── scripts/                  # Python 工具脚本
└── evals/                    # 测试用例
```

## 依赖

- [LilyPond](https://lilypond.org) 2.24+ — 用于编译乐谱
- Python 3 — 用于运行工具脚本
- PyYAML（可选）— 用于 `extract_parts.py` 的 YAML 支持
