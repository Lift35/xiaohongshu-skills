# 小红书封面生成 Skill

机器名称：`xiaohongshu-cover`

这个 Skill 根据笔记主题、内容、目标人群、核心价值和可信证据，生成 4 套差异化的小红书封面方案，并在环境支持时继续生成最终封面。

## 文件结构

```text
xiaohongshu-cover/
├── SKILL.md
├── README.md
├── references/
│   ├── cover-design-sop.md
│   └── output-template.md
└── tests/
    └── test-cases.md
```

## 最简单的调用方式

```text
请使用 xiaohongshu-cover Skill，为这期“手把手制作小红书封面 Skill”的视频生成封面。
```

也可以直接描述需求：

```text
为这篇小红书笔记设计封面，先给我 4 套不同方向的方案。
```

## 安装位置

### Claude Code：个人级

把整个文件夹复制到：

```text
~/.claude/skills/xiaohongshu-cover/
```

### Claude Code：项目级

把整个文件夹复制到项目中的：

```text
.claude/skills/xiaohongshu-cover/
```

安装后可直接输入：

```text
/xiaohongshu-cover
```

或用自然语言描述需要制作、优化小红书封面的任务，让模型自动匹配。

## 版本 1.0 的设计重点

- 输入、输出、执行步骤和验收标准完整。
- 默认生成 4 套真正不同的方向。
- 不伪造官方背书或数据。
- 强制保持一个视觉中心。
- 支持把真实使用中的反馈抽象成新规则。
