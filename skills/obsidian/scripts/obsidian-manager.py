#!/usr/bin/env python3
"""
Obsidian Prompt Manager - Helper script for Claude Code skill
Manages prompts in an Obsidian vault.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def get_config_path():
    """Get the path to config.json relative to this script."""
    script_dir = Path(__file__).parent.parent
    return script_dir / "config.json"


def load_config():
    """Load configuration from config.json."""
    config_path = get_config_path()
    if not config_path.exists():
        return {"vaultPath": "", "promptsFolder": "Claude-Prompts"}
    with open(config_path) as f:
        return json.load(f)


def save_config(config):
    """Save configuration to config.json."""
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")


def get_prompts_path(config):
    """Get the full path to the prompts folder."""
    if not config.get("vaultPath"):
        return None
    return Path(config["vaultPath"]) / config.get("promptsFolder", "Claude-Prompts")


def cmd_setup(args):
    """Setup the Obsidian vault path."""
    vault_path = Path(args.vault_path).expanduser().resolve()

    if not vault_path.exists():
        print(f"Error: Vault path does not exist: {vault_path}", file=sys.stderr)
        sys.exit(1)

    if not vault_path.is_dir():
        print(f"Error: Path is not a directory: {vault_path}", file=sys.stderr)
        sys.exit(1)

    config = load_config()
    config["vaultPath"] = str(vault_path)
    save_config(config)

    # Create prompts folder if it doesn't exist
    prompts_path = get_prompts_path(config)
    prompts_path.mkdir(parents=True, exist_ok=True)

    print(f"Vault configured: {vault_path}")
    print(f"Prompts folder: {prompts_path}")


def cmd_save(args):
    """Save a prompt to the vault."""
    config = load_config()
    prompts_path = get_prompts_path(config)

    if not prompts_path:
        print("Error: Vault not configured. Run 'setup' first.", file=sys.stderr)
        sys.exit(1)

    # Determine target folder
    if args.folder:
        target_folder = prompts_path / args.folder
    else:
        target_folder = prompts_path

    target_folder.mkdir(parents=True, exist_ok=True)

    # Sanitize filename
    safe_title = re.sub(r'[<>:"/\\|?*]', '-', args.title)
    filename = f"{safe_title}.md"
    filepath = target_folder / filename

    # Parse tags
    tags = ["claude-prompt"]
    if args.tags:
        tags.extend([t.strip() for t in args.tags.split(",")])

    # Build frontmatter
    frontmatter = {
        "title": args.title,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "tags": tags
    }

    # Format as YAML frontmatter
    yaml_lines = ["---"]
    yaml_lines.append(f"title: \"{frontmatter['title']}\"")
    yaml_lines.append(f"date: {frontmatter['date']}")
    yaml_lines.append("tags:")
    for tag in frontmatter["tags"]:
        yaml_lines.append(f"  - {tag}")
    yaml_lines.append("---")
    yaml_lines.append("")
    yaml_lines.append(f"# {args.title}")
    yaml_lines.append("")
    yaml_lines.append(args.content)
    yaml_lines.append("")

    content = "\n".join(yaml_lines)

    with open(filepath, "w") as f:
        f.write(content)

    print(f"Saved: {filepath}")


def cmd_list(args):
    """List prompts from the vault."""
    config = load_config()
    prompts_path = get_prompts_path(config)

    if not prompts_path:
        print("Error: Vault not configured. Run 'setup' first.", file=sys.stderr)
        sys.exit(1)

    if not prompts_path.exists():
        print(f"No prompts folder found at: {prompts_path}")
        return

    # Find all markdown files
    prompts = list(prompts_path.rglob("*.md"))

    if not prompts:
        print("No prompts found.")
        return

    # Filter by search term if provided
    if args.search:
        search_lower = args.search.lower()
        filtered = []
        for p in prompts:
            with open(p) as f:
                content = f.read()
            if search_lower in content.lower() or search_lower in p.stem.lower():
                filtered.append(p)
        prompts = filtered

    if not prompts:
        print(f"No prompts matching '{args.search}'")
        return

    # Display prompts
    print(f"Found {len(prompts)} prompt(s):\n")

    for prompt_path in sorted(prompts):
        rel_path = prompt_path.relative_to(prompts_path)

        # Extract title from frontmatter or filename
        with open(prompt_path) as f:
            content = f.read()

        title = prompt_path.stem
        # Try to extract title from frontmatter
        if content.startswith("---"):
            match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
            if match:
                title = match.group(1)

        # Get preview (first non-frontmatter, non-header line)
        preview = ""
        in_frontmatter = False
        for line in content.split("\n"):
            if line.strip() == "---":
                in_frontmatter = not in_frontmatter
                continue
            if in_frontmatter:
                continue
            if line.startswith("#"):
                continue
            if line.strip():
                preview = line.strip()[:60]
                if len(line.strip()) > 60:
                    preview += "..."
                break

        print(f"  {title}")
        print(f"    Path: {rel_path}")
        if preview:
            print(f"    Preview: {preview}")
        print()


def cmd_get(args):
    """Get prompt content for execution."""
    config = load_config()
    prompts_path = get_prompts_path(config)

    if not prompts_path:
        print("Error: Vault not configured. Run 'setup' first.", file=sys.stderr)
        sys.exit(1)

    # Search for the prompt file
    name_lower = args.name.lower()
    found = None

    for prompt_path in prompts_path.rglob("*.md"):
        if prompt_path.stem.lower() == name_lower:
            found = prompt_path
            break
        # Also check title in frontmatter
        with open(prompt_path) as f:
            content = f.read()
        if content.startswith("---"):
            match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
            if match and match.group(1).lower() == name_lower:
                found = prompt_path
                break

    if not found:
        print(f"Error: Prompt not found: {args.name}", file=sys.stderr)
        print("\nAvailable prompts:", file=sys.stderr)
        for p in prompts_path.rglob("*.md"):
            print(f"  - {p.stem}", file=sys.stderr)
        sys.exit(1)

    # Read and extract content (without frontmatter)
    with open(found) as f:
        content = f.read()

    # Remove frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2].strip()

    # Remove the title header if it matches
    lines = content.split("\n")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]

    content = "\n".join(lines).strip()
    print(content)


def main():
    parser = argparse.ArgumentParser(description="Obsidian Prompt Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # setup command
    setup_parser = subparsers.add_parser("setup", help="Configure vault path")
    setup_parser.add_argument("vault_path", help="Path to Obsidian vault")

    # save command
    save_parser = subparsers.add_parser("save", help="Save a prompt")
    save_parser.add_argument("title", help="Prompt title")
    save_parser.add_argument("content", help="Prompt content")
    save_parser.add_argument("--folder", "-f", help="Subfolder within prompts folder")
    save_parser.add_argument("--tags", "-t", help="Comma-separated tags")

    # list command
    list_parser = subparsers.add_parser("list", help="List prompts")
    list_parser.add_argument("--search", "-s", help="Filter by search term")

    # get command
    get_parser = subparsers.add_parser("get", help="Get prompt content")
    get_parser.add_argument("name", help="Prompt name or title")

    args = parser.parse_args()

    commands = {
        "setup": cmd_setup,
        "save": cmd_save,
        "list": cmd_list,
        "get": cmd_get,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
