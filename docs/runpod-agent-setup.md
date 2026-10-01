# Runpod agent setup (modeOn)

Configured from [Runpod agent setup](https://docs.runpod.io/agent-setup.md).

## Done in this repo

- `.cursor/mcp.json` — **runpod** (manage Pods) + **runpod-docs** (documentation)

## Your steps (once)

### 1. Reload Cursor

Quit and reopen Cursor, or reload window, so MCP picks up `.cursor/mcp.json`.

### 2. Sign in to Runpod MCP

1. Open **Customize** (sidebar) → **MCP**
2. Find **runpod**
3. Turn it **on** if disabled
4. On first tool use → **Sign in with Runpod** (browser OAuth — no API key file)

### 3. Install Runpod skills (optional but recommended)

In **Mac Terminal** (one time):

```bash
npx -y skills add runpod/runpod-plugins-official --skill '*' --yes --global
```

Or use Runpod’s guided MCP installer (also adds MCP to other apps):

```bash
npx @runpod/mcp-server@latest add
```

Safe to re-run if already installed.

### 4. Verify

In Cursor chat, ask: **List all my Runpod Pods**

Empty list = connection OK.

## API key alternative (skip OAuth)

If OAuth fails, use a [Runpod API key](https://www.runpod.io/console/user/settings) in `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "runpod": {
      "command": "npx",
      "args": ["-y", "@runpod/mcp-server@latest"],
      "env": {
        "RUNPOD_API_KEY": "${env:RUNPOD_API_KEY}"
      }
    }
  }
}
```

Then `export RUNPOD_API_KEY=...` in your shell before starting Cursor.
