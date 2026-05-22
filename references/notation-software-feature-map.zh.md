# 制谱软件功能映射

将常见的 GUI 制谱软件功能映射到 LilyPond / Claude Code 的对应实现方式。

| GUI 功能 | LilyPond / Claude Code 实现方式 |
|---------|--------------------------------|
| 新建乐谱向导 | 从 `assets/templates/` 选择模板 |
| 音符输入 | 编辑 `.ly` 文件中的声部变量 |
| 复制/粘贴小节 | 复用变量或使用 `\repeat unfold` |
| 移调对话框 | `\transpose from to { ... }` |
| 提取分谱 | 清单 + 包装文件生成 / `\bookpart` / tags |
| 布局面板 | `\paper`、`\layout` |
| 将符号拖到谱表上 | `\once \override` 进行局部微调 |
| 歌词工具 | `\lyricmode`、`\lyricsto` |
| 和弦符号工具 | `\chordmode`、`\new ChordNames` |
| 播放 | `\midi { }` 块 |
| 导出 PDF/PNG/SVG | LilyPond 命令参数（`-fpdf`、`-fpng`、`-fsvg`） |
| 样式库 | 跨项目引用的共享 `.ily` 文件 |
| 插件/宏 | Scheme 函数或外部 Python 脚本 |
| MusicXML 导入 | `musicxml2ly` 后接清理工作流 |

## Claude Code 的优势

- 直接读写本地的 `.ly` 文件。
- 运行 `lilypond` 和 Python 脚本进行验证。
- 使用 `git diff` 审查最小、安全的变更。
- 对重复操作（批量渲染、分谱提取）编写脚本以节省 token。
- 高效地将大型乐谱重构为变量和清单。
