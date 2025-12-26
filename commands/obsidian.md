---
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Obsidian Prompt Manager

You are managing prompts in the user's Obsidian vault.

## Configuration

Config file location: `~/.claude/plugins/obsidian-prompt-manager/skills/obsidian/config.json`

If config doesn't exist or vaultPath is empty, ask user to provide their vault path first.

## Parse the user's command

The user ran: `/obsidian $ARGUMENTS`

Parse the arguments to determine which action to take:

### If `setup <path>` or just a path:
1. Validate path exists: `ls -la <path>`
2. Create prompts folder: `mkdir -p <path>/Claude-Prompts`
3. Save config using Write tool to `~/.claude/plugins/obsidian-prompt-manager/skills/obsidian/config.json`:
   ```json
   {
     "vaultPath": "<absolute-path>",
     "promptsFolder": "Claude-Prompts"
   }
   ```
4. Confirm: "Vault configured: <path>"

### If `save "<title>"` or `save "<title>" --tags <tags>`:
1. Read config.json to get vaultPath
2. Ask user: "What content should I save for this prompt?"
3. Create file at `<vaultPath>/Claude-Prompts/<title>.md` with:
   ```markdown
   ---
   title: "<title>"
   date: <today YYYY-MM-DD>
   tags:
     - claude-prompt
     - <any additional tags>
   ---

   # <title>

   <user's content>
   ```
4. Confirm: "Saved: <filepath>"

### If `list` or `list --search <keyword>`:
1. Read config.json to get vaultPath
2. Use Glob: `<vaultPath>/Claude-Prompts/**/*.md`
3. If --search provided, use Grep to filter
4. Read each file, extract title and first content line
5. Display formatted list

### If `use "<name>"`:
1. Read config.json to get vaultPath
2. Find matching file in Claude-Prompts folder
3. Read file content
4. Remove frontmatter (between --- markers) and title header
5. Execute the remaining content as if user typed it

### If no arguments or `help`:
Show available commands:
- `/obsidian setup <vault-path>` - Configure vault
- `/obsidian save "<title>" [--tags t1,t2]` - Save prompt
- `/obsidian list [--search keyword]` - List prompts
- `/obsidian use "<name>"` - Load and execute prompt
