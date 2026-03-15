#!/usr/bin/env python3
"""
Claude Code PreToolUse hook — sets animation to 'waiting for permission'
when a Bash tool call is about to show a permission dialog.

Animation script calls are excluded (they're auto-approved and harmless).
Reads tool input JSON from stdin; exits 0 to allow the tool to proceed.
"""
import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Commands that are auto-approved — don't show waiting for these
# Covers both bash (Mac/Linux) and PowerShell (Windows) variants
_AUTO_APPROVED_PREFIXES = (
    # Mac / Linux
    'bash scripts/set-agent-state.sh',
    'bash scripts/start-animation.sh',
    # Windows PowerShell
    'powershell', 'pwsh',
    '.\\scripts\\Set-AgentState.ps1',
    '.\\scripts\\Start-Animation.ps1',
    'scripts\\Set-AgentState.ps1',
    'scripts\\Start-Animation.ps1',
    # Python animation module (all platforms)
    'python -m agent_animation.',
    'python -c "from agent_animation',
    "python -c 'from agent_animation",
    'python3 -m agent_animation.',
    'python3 -c "from agent_animation',
    "python3 -c 'from agent_animation",
)

def main():
    try:
        payload = json.load(sys.stdin)
        tool_name = payload.get('tool_name', '')
        tool_input = payload.get('tool_input', {})

        if tool_name != 'Bash':
            sys.exit(0)

        command = tool_input.get('command', '').strip()

        # Skip animation scripts — they're auto-approved and set state themselves
        for prefix in _AUTO_APPROVED_PREFIXES:
            if command.startswith(prefix):
                sys.exit(0)

        # Any other Bash call that may need permission — show waiting state
        from agent_animation.state import read, write
        s = read()
        if s['state'] not in ('idle', 'waiting', 'celebrating'):
            write(s['agent'], 'waiting', 'Waiting for permission to run command...')

    except Exception:
        pass  # never block the tool on hook errors

    sys.exit(0)

if __name__ == '__main__':
    main()
