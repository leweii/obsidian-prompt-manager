# Obsidian Prompt Manager

A Claude Code plugin for managing reusable prompts in your Obsidian vault.

## Features

- **Setup**: Configure your Obsidian vault path (persisted across sessions)
- **Save**: Save prompts with metadata (title, date, tags) in Obsidian-compatible markdown
- **List**: Browse and search your saved prompts
- **Use**: Load and execute saved prompts directly in Claude Code

## Installation

```bash
/plugin install JakobHe/obsidian-prompt-manager
```

## Setup

After installation, configure your Obsidian vault path:

```bash
python3 ~/.claude/plugins/obsidian-prompt-manager/skills/obsidian/scripts/obsidian-manager.py setup ~/path/to/your/vault
```

This creates a `Claude-Prompts` folder in your vault.

## Commands

### Setup Vault

```bash
python3 <plugin-path>/scripts/obsidian-manager.py setup /path/to/vault
```

### Save a Prompt

```bash
python3 <plugin-path>/scripts/obsidian-manager.py save "Prompt Title" "Prompt content here" --tags tag1,tag2
```

Prompts are saved with Obsidian-compatible frontmatter:

```markdown
---
title: "Prompt Title"
date: 2025-01-15
tags:
  - claude-prompt
  - tag1
  - tag2
---

# Prompt Title

Prompt content here
```

### List Prompts

```bash
# List all prompts
python3 <plugin-path>/scripts/obsidian-manager.py list

# Search prompts
python3 <plugin-path>/scripts/obsidian-manager.py list --search keyword
```

### Use a Prompt

```bash
python3 <plugin-path>/scripts/obsidian-manager.py get "Prompt Title"
```

## Configuration

Configuration is stored in the plugin's `config.json`:

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
│       └── scripts/
│           └── obsidian-manager.py
└── README.md
```

## License

MIT

## Contributing

Contributions welcome! Please open an issue or submit a pull request.
