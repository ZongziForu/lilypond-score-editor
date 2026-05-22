# 脚本化分谱提取

## 推荐结构

将共享的音乐变量保存在一个源文件中。使用清单描述分谱。生成包装 `.ly` 文件。批量编译。

### 源文件示例

```lilypond
\version "2.24.4"

global = {
  \key c \major
  \time 4/4
}

violinIMusic = \relative c'' {
  \global
  c4 d e f
}

celloMusic = \relative c {
  \clef bass
  \global
  c4 d e f
}
```

### 清单示例

```yaml
source: score.ly
parts:
  - id: violin-i
    name: Violin I
    variable: violinIMusic
    clef: treble
  - id: cello
    name: Cello
    variable: celloMusic
    clef: bass
```

### 运行提取

```bash
python "${CLAUDE_SKILL_DIR}/scripts/extract_parts.py" score.ly parts-manifest.yaml --compile
```

## 替代结构：多 book 方式

一个包含多个 `\book` 块的 `.ly` 文件：

```lilypond
\book {
  \bookOutputName "full-score"
  \score { ... }
}

\book {
  \bookOutputName "violin-i"
  \score { \new Staff \violinIMusic }
}
```

## 进阶：tags 标签

使用 `\tag`、`\keepWithTag` 和 `\removeWithTag` 实现：

- 提示音（cue notes）
- 仅总谱标记
- 仅分谱换行
- 不同的排练标记
- Ossia（另谱）
- 删减或变体

## 反模式

应避免：

- 用正则表达式硬切割大型 `StaffGroup`。
- 将完整音乐块复制到每个分谱文件中。
- 为总谱和分谱维护各自独立且不同的源文件。
- 手写大量重复的包装代码。

## 节省 Token 的原则

绝不要依赖 Claude Code 来复制大型音乐块以生成分谱。推荐：

1. 共享变量
2. 清单文件
3. 自动生成的包装文件
4. 批量编译
