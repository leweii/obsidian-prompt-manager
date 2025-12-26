---
name: obsidian
description: Manage prompts in your Obsidian vault. Use for saving, listing, and loading reusable prompts. Triggers on /obsidian commands, Obsidian vault operations, or prompt management requests.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Obsidian Prompt Manager

Manage reusable prompts in your Obsidian vault from Claude Code.

## Commands

### `/obsidian setup`

Configure your Obsidian vault path.

**Usage:**
```
/obsidian setup /path/to/your/vault
```

**What it does:**
1. Validates the vault path exists
2. Creates a `Claude-Prompts` folder in your vault (if not exists)
3. Saves the configuration to `.claude/skills/obsidian/config.json`

**Example:**
```
/obsidian setup ~/Documents/MyVault
```

---

### `/obsidian save`

Save a prompt to your Obsidian vault.

**Usage:**
```
/obsidian save "Prompt Title" [--folder subfolder] [--tags tag1,tag2]
```

**What it does:**
1. Creates a markdown file with Obsidian-compatible frontmatter
2. Saves to `{vault}/Claude-Prompts/{title}.md`
3. Includes metadata: title, date, tags

**Example:**
```
/obsidian save "Code Review Checklist" --tags review,quality
```

**Prompt format saved:**
```markdown
---
title: Code Review Checklist
date: 2025-01-15
tags:
  - claude-prompt
  - review
  - quality
---

# Code Review Checklist

[Your prompt content here]
```

---

### `/obsidian list`

List all saved prompts from your vault.

**Usage:**
```
/obsidian list [--search keyword]
```

**What it does:**
1. Scans the `Claude-Prompts` folder in your vault
2. Displays prompts with title and preview
3. Optionally filters by search term

**Example:**
```
/obsidian list
/obsidian list --search review
```

---

### `/obsidian use`

Load and execute a saved prompt.

**Usage:**
```
/obsidian use "prompt-name"
```

**What it does:**
1. Reads the prompt file from your vault
2. Extracts the prompt content (excluding frontmatter)
3. Executes it as Claude Code input

**Example:**
```
/obsidian use "Code Review Checklist"
```

---

## Configuration

Configuration is stored in `.claude/skills/obsidian/config.json`:

```json
{
  "vaultPath": "/path/to/your/vault",
  "promptsFolder": "Claude-Prompts"
}
```

## Implementation Details

When executing commands, use the helper script:

```bash
python3 .claude/skills/obsidian/scripts/obsidian-manager.py <command> [args]
```

### Commands:

- `setup <vault-path>` - Configure vault path
- `save "<title>" "<content>" [--folder F] [--tags T]` - Save prompt
- `list [--search S]` - List prompts
- `get "<name>"` - Get prompt content for execution
