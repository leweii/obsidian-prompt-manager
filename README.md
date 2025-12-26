# Obsidian Prompt Manager

A Claude Code plugin for managing reusable prompts in your Obsidian vault.

## Features

- **Setup**: Configure your Obsidian vault path (persisted across sessions)
- **Save**: Save prompts with metadata (title, date, tags) in Obsidian-compatible markdown
- **List**: Browse and search your saved prompts
- **Use**: Load and execute saved prompts directly in Claude Code

All operations are handled natively by Claude Code - no external scripts required.

## Installation

```bash
/plugin install leweii/obsidian-prompt-manager
```

## Quick Start

### 1. Setup your vault

```
/obsidian setup ~/Documents/MyVault
```

This creates a `Claude-Prompts` folder in your vault.

### 2. Save a prompt

```
/obsidian save "Code Review Checklist" --tags review,quality
```

Claude will ask for the prompt content and save it as a markdown file.

### 3. List your prompts

```
/obsidian list
```

Or search:

```
/obsidian list --search review
```

### 4. Use a saved prompt

```
/obsidian use "Code Review Checklist"
```

Claude loads the prompt and executes it as if you typed it.

## Prompt Format

Prompts are saved as Obsidian-compatible markdown with frontmatter:

```markdown
---
title: "Code Review Checklist"
date: 2025-01-15
tags:
  - claude-prompt
  - review
  - quality
---

# Code Review Checklist

Review this code for:
1. Bugs and errors
2. Performance issues
3. Security vulnerabilities
```

## Configuration

Configuration is stored in the skill's `config.json`:

```json
{
  "vaultPath": "/path/to/your/vault",
  "promptsFolder": "Claude-Prompts"
}
```

## File Structure

```
obsidian-prompt-manager/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── obsidian/
│       ├── SKILL.md
│       ├── config.json
│       └── config.template.json
├── LICENSE
└── README.md
```

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
