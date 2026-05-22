# 模板与模式

## 模板选择

根据乐器编制选择模板：

| 需求 | 模板 |
|------|------|
| 单旋律 | `single-staff.ly` |
| 钢琴 | `piano.ly` |
| 吉他（标准记谱 + 可选六线谱） | `guitar.ly` |
| 贝斯吉他 | `bass.ly` |
| 尤克里里 | `ukulele.ly` |
| 架子鼓 / 打击乐 | `drum-kit.ly` |
| 旋律 + 歌词 + 和弦 | `lead-sheet.ly` |
| 合唱（SATB） | `satb.ly` |
| 室内弦乐 | `string-quartet.ly` |
| 管弦乐队 | `orchestra.ly` |
| 总谱 + 分谱 | `parts-project.ly` + `parts-manifest.yaml` |

## 复制模板

```bash
cp "${CLAUDE_SKILL_DIR}/assets/templates/lead-sheet.ly" ./song.ly
```

## 编辑模板

1. 更新 `\header` 的标题和作曲家。
2. 在 `global` 中设置 `\key` 和 `\time`。
3. 填入音乐变量（如 `melody`、`rightHand`）。
4. 添加或调整歌词与和弦名称。
5. 编译：
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/compile_lilypond.py" song.ly
   ```

## 模板详情

- **single-staff.ly**：一行谱表、一个声部、global 块。适用于单音乐器。
- **piano.ly**： `PianoStaff`，包含 `rightHand` 和 `leftHand` 变量。
- **guitar.ly**：高音谱表，使用 `treble_8` 谱号。包含注释掉的 `TabStaff` 示例，可同时显示记谱和指法谱。
- **bass.ly**：低音谱表，使用 `bass_8` 谱号，适用于电贝斯或低音吉他。
- **ukulele.ly**：高音谱表，针对尤克里里音域调音。
- **drum-kit.ly**：`DrumStaff`，使用 `\drummode` 进行标准鼓记谱（bd、sn、hh 等）。
- **lead-sheet.ly**：包含 `ChordNames`、旋律谱表和 `Lyrics`。适用于爵士/流行乐谱。
- **satb.ly**：`ChoirStaff`，包含女高音/女低音/男高音/男低音变量和歌词。
- **string-quartet.ly**：`StaffGroup`，包含小提琴 I/II、中提琴（中音谱号）、大提琴（低音谱号）。
- **orchestra.ly**：完整管弦乐总谱，包含木管、铜管和弦乐三个 `StaffGroup` 段落。包括 Bb 单簧管/小号和 F 圆号的移调。
- **parts-project.ly**：共享变量加完整总谱。设计用于与 `extract_parts.py` 和清单配合使用。
- **parts-manifest.yaml**：弦乐四重奏的清单示例。编辑 `variable` 名称以匹配你的 `.ly` 源文件。
