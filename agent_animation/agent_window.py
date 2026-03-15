"""
Agent Animation Window
======================
An always-on-top floating Tkinter window that shows a pixel-art sprite of
the currently active workflow agent, with idle bob animation, state-based
border color, speech bubble, and an animated keyboard.

Usage:
    python -m agent_animation.agent_window          # reads /tmp/agent-state.json
    python -m agent_animation.agent_window --demo   # cycles through all agents/states

Drag the window by clicking and dragging anywhere on it.
Close with ✕, minimise with −, toggle compact mode with □, or press Escape.
"""

import tkinter as tk
import math
import time
import random
import argparse

from .sprites import PALETTE, CELL, get_agent, get_state_config, AGENTS, STATE_CONFIG
from .state import read as read_state

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
SPRITE_COLS  = 14
SPRITE_ROWS  = 16
SPRITE_W     = SPRITE_COLS * CELL      # 126 px
SPRITE_H     = SPRITE_ROWS * CELL      # 144 px

KEYBOARD_H   = 46                      # pixel-art keyboard + desk area
WIN_W        = 240                     # wider window
CANVAS_H     = SPRITE_H + KEYBOARD_H + 14
TITLE_H      = 28                      # title bar
LABEL_H      = 32                      # agent name row
BUBBLE_H     = 72                      # speech bubble
WIN_H        = TITLE_H + CANVAS_H + LABEL_H + BUBBLE_H + 12

BG           = '#1E1E2E'               # dark background
TITLE_BG     = '#252540'               # title bar background
FG           = '#E8E8FF'               # bright white-ish text
FONT_LABEL   = ('Courier', 14, 'bold') # large agent name
FONT_STATUS  = ('Courier', 11)         # status bubble text
FONT_BTN     = ('Courier', 11, 'bold') # window buttons
FONT_TITLE   = ('Courier', 9)          # title bar label

POLL_MS      = 800
BOB_PERIOD   = 1.4


class AgentWindow:
    def __init__(self, root: tk.Tk, demo: bool = False):
        self.root   = root
        self.demo   = demo
        self._compact = False

        # --- display state ---
        self._agent_name = 'developer'
        self._state_name = 'idle'
        self._message    = ''
        self._frame_idx  = 0
        self._start_time = time.time()
        self._drag_x = self._drag_y = 0

        # --- demo cycling ---
        self._demo_agents = list(AGENTS.keys())
        self._demo_states = list(STATE_CONFIG.keys())
        self._demo_ai = self._demo_si = 0
        self._demo_ts = time.time()

        self._build_window()
        self._schedule_poll()
        self._schedule_frame()

    # -----------------------------------------------------------------------
    # Window construction
    # -----------------------------------------------------------------------
    def _build_window(self):
        r = self.root
        r.title('SoftwareTeam')
        r.geometry(f'{WIN_W}x{WIN_H}+80+80')
        r.resizable(False, False)
        r.configure(bg=BG)
        r.attributes('-topmost', True)
        r.overrideredirect(True)

        try:
            r.attributes('-alpha', 0.96)
        except tk.TclError:
            pass

        # Outer frame — border changes color with agent state
        self._border_frame = tk.Frame(r, bg='#888888', padx=2, pady=2)
        self._border_frame.pack(fill='both', expand=True)

        self._inner = tk.Frame(self._border_frame, bg=BG)
        self._inner.pack(fill='both', expand=True)

        # ---- Title bar ----
        title_bar = tk.Frame(self._inner, bg=TITLE_BG, height=TITLE_H)
        title_bar.pack(fill='x')
        title_bar.pack_propagate(False)

        self._title_lbl = tk.Label(
            title_bar, text='⬡ SoftwareTeam',
            bg=TITLE_BG, fg='#BBBBFF', font=FONT_TITLE, anchor='w')
        self._title_lbl.pack(side='left', padx=8)

        # Buttons: close / minimize / compact — right side
        for text, fg_col, handler in [
            ('✕', '#FF6677', lambda e: self.root.destroy()),
            ('−', '#FFDD55', lambda e: self._minimize()),
            ('□', '#55DDFF', lambda e: self._toggle_compact()),
        ]:
            btn = tk.Label(title_bar, text=text, bg=TITLE_BG, fg=fg_col,
                           font=FONT_BTN, cursor='hand2', padx=5)
            btn.pack(side='right', padx=1)
            btn.bind('<Button-1>', handler)

        for w in (title_bar, self._title_lbl):
            w.bind('<ButtonPress-1>', self._on_drag_start)
            w.bind('<B1-Motion>',     self._on_drag_motion)

        # ---- Sprite + keyboard canvas ----
        self._canvas = tk.Canvas(
            self._inner, width=WIN_W - 8, height=CANVAS_H,
            bg=BG, highlightthickness=0)
        self._canvas.pack(pady=(4, 0))
        self._canvas.bind('<ButtonPress-1>', self._on_drag_start)
        self._canvas.bind('<B1-Motion>',     self._on_drag_motion)

        # ---- Agent name label (large, bright) ----
        self._name_lbl = tk.Label(
            self._inner, text='Developer',
            bg=BG, fg='#66EE88', font=FONT_LABEL, anchor='center')
        self._name_lbl.pack(fill='x', padx=4)

        # ---- Speech bubble ----
        self._bubble_frame = tk.Frame(self._inner, bg='#EEEEFF', padx=6, pady=5)
        self._bubble_frame.pack(fill='x', padx=6, pady=(2, 6))

        self._bubble_icon = tk.Label(
            self._bubble_frame, text='💤',
            bg='#EEEEFF', font=('Courier', 16))
        self._bubble_icon.pack(side='left')

        self._bubble_lbl = tk.Label(
            self._bubble_frame, text='Idle',
            bg='#EEEEFF', fg='#111133', font=FONT_STATUS,
            anchor='w', wraplength=WIN_W - 72, justify='left')
        self._bubble_lbl.pack(side='left', fill='x', expand=True)

        r.bind('<Escape>', lambda e: r.destroy())

    # -----------------------------------------------------------------------
    # Window controls
    # -----------------------------------------------------------------------
    def _minimize(self):
        self.root.iconify()

    def _toggle_compact(self):
        """Toggle between full and compact (sprite-only) mode."""
        self._compact = not self._compact
        if self._compact:
            self._name_lbl.pack_forget()
            self._bubble_frame.pack_forget()
            self.root.geometry(f'{WIN_W}x{TITLE_H + CANVAS_H + 8}')
        else:
            self._name_lbl.pack(fill='x', padx=4)
            self._bubble_frame.pack(fill='x', padx=6, pady=(2, 6))
            self.root.geometry(f'{WIN_W}x{WIN_H}')

    # -----------------------------------------------------------------------
    # Drag
    # -----------------------------------------------------------------------
    def _on_drag_start(self, event):
        self._drag_x = event.x_root - self.root.winfo_x()
        self._drag_y = event.y_root - self.root.winfo_y()

    def _on_drag_motion(self, event):
        self.root.geometry(
            f'+{event.x_root - self._drag_x}+{event.y_root - self._drag_y}')

    # -----------------------------------------------------------------------
    # State polling
    # -----------------------------------------------------------------------
    def _schedule_poll(self):
        self._poll()
        self.root.after(POLL_MS, self._schedule_poll)

    def _poll(self):
        self.root.attributes('-topmost', True)
        self.root.lift()
        if self.demo:
            self._advance_demo()
            return
        s = read_state()
        if s['agent'] != self._agent_name or s['state'] != self._state_name:
            self._frame_idx = 0
        self._agent_name = s['agent']
        self._state_name = s['state']
        self._message    = s['message']

    def _advance_demo(self):
        now = time.time()
        if now - self._demo_ts < 2.5:
            return
        self._demo_ts = now
        self._demo_si += 1
        if self._demo_si >= len(self._demo_states):
            self._demo_si = 0
            self._demo_ai = (self._demo_ai + 1) % len(self._demo_agents)
        self._agent_name = self._demo_agents[self._demo_ai]
        self._state_name = self._demo_states[self._demo_si]
        self._message    = f'Demo: {self._agent_name} / {self._state_name}'
        self._frame_idx  = 0

    # -----------------------------------------------------------------------
    # Animation render loop
    # -----------------------------------------------------------------------
    def _schedule_frame(self):
        self._render_frame()
        sc       = get_state_config(self._state_name)
        interval = max(80, int(1000 / sc['fps']))
        self.root.after(interval, self._schedule_frame)

    def _render_frame(self):
        agent_cfg = get_agent(self._agent_name)
        state_cfg = get_state_config(self._state_name)

        frames = agent_cfg[state_cfg['frames_key']]
        frame  = frames[self._frame_idx % len(frames)]
        self._frame_idx += 1

        # Sinusoidal bob
        bob_y = 0
        if state_cfg['bob']:
            elapsed = time.time() - self._start_time
            bob_y   = int(math.sin(elapsed * 2 * math.pi / BOB_PERIOD) * 2)

        c        = self._canvas
        canvas_w = WIN_W - 8
        cx       = canvas_w // 2
        ox       = cx - SPRITE_W // 2
        oy       = 4 + bob_y

        c.delete('all')

        # ---- Draw sprite ----
        for row_i, row in enumerate(frame):
            for col_i, ch in enumerate(row):
                color = PALETTE.get(ch)
                if color is None:
                    continue
                x1 = ox + col_i * CELL
                y1 = oy + row_i * CELL
                c.create_rectangle(x1, y1, x1 + CELL - 1, y1 + CELL - 1,
                                   fill=color, outline='')

        # State icon top-right of sprite
        icon = state_cfg['icon']
        c.create_text(ox + SPRITE_W - 2, oy + 4, text=icon,
                      anchor='ne', font=('Courier', 14))

        # ---- Desk surface ----
        desk_y = oy + SPRITE_H + 4
        c.create_rectangle(cx - 95, desk_y, cx + 95, desk_y + 4,
                           fill='#35355A', outline='')
        # Desk highlight edge
        c.create_line(cx - 95, desk_y, cx + 95, desk_y,
                      fill='#6666AA', width=1)

        # ---- Keyboard ----
        kbd_y = desk_y + 7
        self._draw_keyboard(c, cx, kbd_y)

        # ---- Hands ----
        self._draw_hands(c, cx, kbd_y, state_cfg)

        # ---- Border color ----
        border_color = state_cfg['border_color']
        if self._state_name == 'celebrating':
            border_color = random.choice(
                ['#FF5566', '#55FF88', '#5566FF', '#FFEE44', '#FF55FF'])
        self._border_frame.configure(bg=border_color)

        # ---- Speech bubble ----
        bubble_bg = state_cfg['bubble_color']
        message   = self._message or _default_message(self._state_name)
        self._bubble_frame.configure(bg=bubble_bg)
        self._bubble_icon.configure(bg=bubble_bg, text=icon)
        self._bubble_lbl.configure(bg=bubble_bg, fg='#111133', text=message)

        # ---- Agent name label ----
        self._name_lbl.configure(
            text=agent_cfg['label'], fg=agent_cfg['color'])

    # -----------------------------------------------------------------------
    # Keyboard drawing
    # -----------------------------------------------------------------------
    def _draw_keyboard(self, c, cx, ky):
        """Draw a pixel-art keyboard centered at cx, top edge at ky."""
        kw, kh = 172, 36
        kx = cx - kw // 2

        # Drop shadow
        c.create_rectangle(kx + 3, ky + 3, kx + kw + 3, ky + kh + 3,
                           fill='#111122', outline='')
        # Keyboard body
        c.create_rectangle(kx, ky, kx + kw, ky + kh,
                           fill='#252545', outline='#5555AA', width=1)
        # Inner bevel highlight
        c.create_line(kx + 1, ky + 1, kx + kw - 1, ky + 1, fill='#4444AA')
        c.create_line(kx + 1, ky + 1, kx + 1, ky + kh - 1, fill='#4444AA')

        key_h, gap = 7, 2

        # Row 1 — 10 keys
        self._draw_key_row(c, kx + 5,  ky + 4,                  kw - 10, 10, key_h, gap)
        # Row 2 — 9 keys
        self._draw_key_row(c, kx + 9,  ky + 4 + key_h + gap,    kw - 14,  9, key_h, gap)
        # Row 3 — 7 keys
        self._draw_key_row(c, kx + 14, ky + 4 + 2*(key_h+gap),  kw - 20,  7, key_h, gap)
        # Space bar
        sp_x = kx + kw // 4
        sp_y = ky + kh - 10
        c.create_rectangle(sp_x, sp_y, sp_x + kw // 2, sp_y + 6,
                           fill='#3A3A72', outline='#7777BB', width=1)
        c.create_line(sp_x + 1, sp_y + 1, sp_x + kw // 2 - 1, sp_y + 1,
                      fill='#9999CC')

    def _draw_key_row(self, c, rx, ry, row_w, n, key_h, gap):
        key_w = max(4, (row_w - gap * (n - 1)) // n)
        for i in range(n):
            x1 = rx + i * (key_w + gap)
            c.create_rectangle(x1, ry, x1 + key_w, ry + key_h,
                               fill='#3A3A72', outline='#6666AA', width=1)
            # Key top highlight
            c.create_line(x1 + 1, ry + 1, x1 + key_w - 1, ry + 1,
                          fill='#8888CC')

    # -----------------------------------------------------------------------
    # Hands drawing
    # -----------------------------------------------------------------------
    def _draw_hands(self, c, cx, kbd_y, state_cfg):
        """Draw animated hands above/on the keyboard."""
        skin   = '#FFCC99'
        shadow = '#CC9966'
        is_typing = state_cfg['frames_key'] == 'typing'

        if is_typing:
            # Alternating left/right key-press animation
            left_down  = self._frame_idx % 2 == 0
            right_down = not left_down

            lx = cx - 46
            rx = cx + 22
            base_y = kbd_y - 6

            ly = base_y + (3 if left_down  else 0)
            ry = base_y + (3 if right_down else 0)

            # Left hand palm
            c.create_oval(lx, ly, lx + 20, ly + 13,
                         fill=skin, outline=shadow, width=1)
            # Left fingers (4 small rectangles above palm)
            for fi in range(4):
                fx = lx + 2 + fi * 5
                c.create_rectangle(fx, ly - 6, fx + 4, ly + 3,
                                  fill=skin, outline=shadow, width=1)

            # Right hand palm
            c.create_oval(rx, ry, rx + 20, ry + 13,
                         fill=skin, outline=shadow, width=1)
            # Right fingers
            for fi in range(4):
                fx = rx + 2 + fi * 5
                c.create_rectangle(fx, ry - 6, fx + 4, ry + 3,
                                  fill=skin, outline=shadow, width=1)

            # Arms connecting hands to sprite body
            arm_top_y = kbd_y - 30
            c.create_line(lx + 10, arm_top_y, lx + 10, ly + 6,
                         fill=skin, width=5, capstyle='round')
            c.create_line(rx + 10, arm_top_y, rx + 10, ry + 6,
                         fill=skin, width=5, capstyle='round')
        else:
            # Hands resting at sides of keyboard
            lx = cx - 96
            rx = cx + 74
            hy = kbd_y + 14

            c.create_oval(lx, hy, lx + 17, hy + 11,
                         fill=skin, outline=shadow, width=1)
            c.create_oval(rx, hy, rx + 17, hy + 11,
                         fill=skin, outline=shadow, width=1)


def _default_message(state: str) -> str:
    return {
        'idle':              'Idle…',
        'thinking':          'Thinking…',
        'reviewing':         'Reviewing code…',
        'typing':            'Writing…',
        'reworking':         'Addressing feedback…',
        'approved':          'All good! ✅',
        'changes_requested': 'Changes needed 🔴',
        'handingoff':        'Handing off…',
        'celebrating':       'Merged! 🎉',
        'waiting':           'Waiting for you…',
    }.get(state, '')


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='Agent animation floating window')
    parser.add_argument('--demo', action='store_true',
                        help='Cycle through all agents and states automatically')
    args = parser.parse_args()

    root = tk.Tk()
    AgentWindow(root, demo=args.demo)
    root.mainloop()


if __name__ == '__main__':
    main()
