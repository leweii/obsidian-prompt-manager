---
name: obsidian
description: Manage prompts in your Obsidian vault. Use for saving, listing, and loading reusable prompts. Triggers on /obsidian commands, Obsidian vault operations, or prompt management requests.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Obsidian Prompt Manager

Manage reusable prompts in your Obsidian vault from Claude Code using native tools.

## Configuration

Configuration is stored in the skill's `config.json`:

```json
{
  "vaultPath": "/path/to/your/vault",
  "promptsFolder": "Claude-Prompts"
}
```

**Config location:** `~/.claude/skills/obsidian/config.json` (personal) or `.claude/skills/obsidian/config.json` (project)

---

## Commands

### `/obsidian setup <vault-path>`

Configure your Obsidian vault path.

**Steps to execute:**

1. **Validate path exists:**
   ```
   Use Bash: ls -la <vault-path>
   ```
   If path doesn't exist, inform user and stop.

2. **Create prompts folder:**
   ```
   Use Bash: mkdir -p <vault-path>/Claude-Prompts
   ```

3. **Save configuration:**
   Use Write tool to update config.json:
   ```json
   {
     "vaultPath": "<vault-path>",
     "promptsFolder": "Claude-Prompts"
   }
   ```

4. **Confirm to user:**
   "Vault configured: <vault-path>
   Prompts folder: <vault-path>/Claude-Prompts"

---

### `/obsidian save "<title>" [--tags tag1,tag2]`

Save a prompt to your Obsidian vault.

**Steps to execute:**

1. **Read config:**
   Use Read tool on config.json to get vaultPath.
   If vaultPath is empty, ask user to run `/obsidian setup` first.

2. **Get prompt content:**
   Ask user: "What content should I save for this prompt?"

3. **Create markdown file:**
   Use Write tool to create `<vaultPath>/Claude-Prompts/<title>.md`:

   ```markdown
   ---
   title: "<title>"
   date: <YYYY-MM-DD>
   tags:
     - claude-prompt
     - <additional tags if provided>
   ---

   # <title>

   <prompt content>
   ```

4. **Confirm to user:**
   "Saved: <vaultPath>/Claude-Prompts/<title>.md"

---

### `/obsidian list [--search <keyword>]`

List all saved prompts from your vault.

**Steps to execute:**

1. **Read config:**
   Use Read tool on config.json to get vaultPath.
   If vaultPath is empty, ask user to run `/obsidian setup` first.

2. **Find prompts:**
   Use Glob tool: `<vaultPath>/Claude-Prompts/**/*.md`

3. **If --search provided:**
   Use Grep tool to filter files containing the keyword.

4. **For each file found:**
   Use Read tool to extract:
   - Title (from frontmatter or filename)
   - Preview (first line of content after frontmatter)

5. **Display formatted list:**
   ```
   Found X prompt(s):

     <Title 1>
       Path: <relative-path>
       Preview: <first 60 chars>...

     <Title 2>
       ...
   ```

---

### `/obsidian use "<prompt-name>"`

Load and execute a saved prompt.

**Steps to execute:**

1. **Read config:**
   Use Read tool on config.json to get vaultPath.
   If vaultPath is empty, ask user to run `/obsidian setup` first.

2. **Find the prompt:**
   Use Glob tool: `<vaultPath>/Claude-Prompts/**/*.md`
   Match filename or title (case-insensitive) to <prompt-name>.

3. **If not found:**
   List available prompts and ask user to choose.

4. **Read prompt file:**
   Use Read tool to get file contents.

5. **Extract content:**
   Remove YAML frontmatter (everything between `---` markers).
   Remove the title header line (starts with `# `).

6. **Execute the prompt:**
   Treat the extracted content as if the user typed it.
   Respond to it as a new instruction.

---

## Examples

### Setup Example
```
User: /obsidian setup ~/Documents/MyVault

Claude: Let me configure your Obsidian vault...
[Uses Bash to verify path exists]
[Uses Bash to create Claude-Prompts folder]
[Uses Write to save config.json]

Vault configured: /Users/you/Documents/MyVault
Prompts folder: /Users/you/Documents/MyVault/Claude-Prompts
```

### Save Example
```
User: /obsidian save "Code Review Checklist" --tags review,quality

Claude: What content should I save for this prompt?

User: Review this code for: 1) bugs 2) performance 3) security

Claude: [Uses Write to create the markdown file]

Saved: /Users/you/Documents/MyVault/Claude-Prompts/Code Review Checklist.md
```

### List Example
```
User: /obsidian list

Claude: [Uses Glob to find .md files]
[Uses Read to extract titles and previews]

Found 3 prompt(s):

  Code Review Checklist
    Path: Code Review Checklist.md
    Preview: Review this code for: 1) bugs 2) performance...

  Debug Helper
    Path: Debug Helper.md
    Preview: Help me debug this issue by...
```

### Use Example
```
User: /obsidian use "Code Review Checklist"

Claude: [Uses Glob to find the file]
[Uses Read to get contents]
[Extracts content, removing frontmatter]

Now executing prompt: "Review this code for: 1) bugs 2) performance 3) security"

[Claude then responds as if user typed that prompt]
```
