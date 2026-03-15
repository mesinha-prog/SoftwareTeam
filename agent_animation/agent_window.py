"""
Agent Animation Window
======================
An always-on-top Tkinter window that shows a pixel-art sprite of the currently
active workflow agent.  The character stands in front of a pixel-art desk with
a keyboard; in typing states the hands animate pressing keys.

Layout (top → bottom in canvas):
  4px gap
  sprite (144px tall, 16 rows × 9px)   [full character visible]
  keyboard (16px tall, overlaps sprite feet — looks like desk in front)
  desk surface strip (5px)
  desk front panel (22px)
  4px margin

Usage:
    python -m agent_animation.agent_window          # reads /tmp/agent-state.json
    python -m agent_animation.agent_window --demo   # cycles through all agents/states

Native OS window decorations provide minimize / maximize / close.
Press Escape to close.
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
SPRITE_COLS = 14
SPRITE_ROWS = 16
SPRITE_W    = SPRITE_COLS * CELL    # 126 px
SPRITE_H    = SPRITE_ROWS * CELL    # 144 px

KBD_W       = 150
KBD_H       = 16                    # keyboard body height
DESK_SURF   = 5                     # desk surface strip height
DESK_PANEL  = 22                    # desk front panel height

WIN_W       = 290
# Canvas: sprite + keyboard (overlaps last 12px of sprite) + desk surf + desk panel + margin
CANVAS_H    = SPRITE_H + KBD_H + DESK_SURF + DESK_PANEL + 8  # ~211
LABEL_H     = 46                    # agent name row
BUBBLE_H    = 82                    # speech bubble
WIN_H       = CANVAS_H + LABEL_H + BUBBLE_H + 10

BG          = '#1E1E2E'
FONT_LABEL  = ('Courier', 18, 'bold')
FONT_STATUS = ('Courier', 13)
FONT_HEADER = ('Courier', 9)

POLL_MS     = 800
BOB_PERIOD  = 1.4

# How far the keyboard overlaps the sprite bottom (covers feet row)
KBD_OVERLAP = 12


class AgentWindow:
    def __init__(self, root: tk.Tk, demo: bool = False):
        self.root  = root
        self.demo  = demo

        self._agent_name = 'developer'
        self._state_name = 'idle'
        self._message    = ''
        self._frame_idx  = 0
        self._start_time = time.time()

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
        r.title('⬡ SoftwareTeam Agents')
        r.geometry(f'{WIN_W}x{WIN_H}+80+80')
        r.resizable(True, True)
        r.configure(bg=BG)
        r.attributes('-topmost', True)

        try:
            r.attributes('-alpha', 0.97)
        except tk.TclError:
            pass

        # Coloured border frame (changes with agent state)
        self._border_frame = tk.Frame(r, bg='#888888', padx=2, pady=2)
        self._border_frame.pack(fill='both', expand=True)

        inner = tk.Frame(self._border_frame, bg=BG)
        inner.pack(fill='both', expand=True)

        # Small decorative header strip
        header = tk.Frame(inner, bg='#252540', height=18)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text='● active agent', bg='#252540', fg='#7777AA',
                 font=FONT_HEADER, anchor='w').pack(side='left', padx=8)

        # Canvas — sprite + keyboard + desk
        self._canvas = tk.Canvas(inner, width=WIN_W - 8, height=CANVAS_H,
                                 bg=BG, highlightthickness=0)
        self._canvas.pack(pady=(4, 0))

        # Agent name label
        self._name_lbl = tk.Label(inner, text='Developer',
                                  bg=BG, fg='#66EE88',
                                  font=FONT_LABEL, anchor='center')
        self._name_lbl.pack(fill='x', padx=4)

        # Speech bubble
        self._bubble_frame = tk.Frame(inner, bg='#EEEEFF', padx=6, pady=5)
        self._bubble_frame.pack(fill='x', padx=6, pady=(2, 6))

        self._bubble_icon = tk.Label(self._bubble_frame, text='💤',
                                     bg='#EEEEFF', font=('Courier', 16))
        self._bubble_icon.pack(side='left')

        self._bubble_lbl = tk.Label(self._bubble_frame, text='Idle',
                                    bg='#EEEEFF', fg='#111133',
                                    font=FONT_STATUS, anchor='w',
                                    wraplength=WIN_W - 76, justify='left')
        self._bubble_lbl.pack(side='left', fill='x', expand=True)

        r.bind('<Escape>', lambda e: r.destroy())

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
    # Render loop
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

        bob_y = 0
        if state_cfg['bob']:
            elapsed = time.time() - self._start_time
            bob_y   = int(math.sin(elapsed * 2 * math.pi / BOB_PERIOD) * 2)

        c        = self._canvas
        canvas_w = WIN_W - 8          # 282
        cx       = canvas_w // 2      # 141
        ox       = cx - SPRITE_W // 2 # 141 - 63 = 78
        oy       = 4 + bob_y

        c.delete('all')

        # ------ 1. Draw full sprite ------
        for row_i, row in enumerate(frame):
            for col_i, ch in enumerate(row):
                color = PALETTE.get(ch)
                if color is None:
                    continue
                x1 = ox + col_i * CELL
                y1 = oy + row_i * CELL
                c.create_rectangle(x1, y1, x1 + CELL - 1, y1 + CELL - 1,
                                   fill=color, outline='')

        # State icon (top-right corner)
        icon = state_cfg['icon']
        c.create_text(ox + SPRITE_W - 2, oy + 4, text=icon,
                      anchor='ne', font=('Courier', 14))

        # Bright outline around the shoulder/body area to make arms pop
        body_x1 = ox + 2 * CELL
        body_x2 = ox + 12 * CELL
        body_y1 = oy + 8 * CELL
        body_y2 = oy + 12 * CELL
        agent_color = agent_cfg['color']
        c.create_rectangle(body_x1, body_y1, body_x2, body_y2,
                           outline=agent_color, fill='', width=1)

        # ------ 2. Arm lines: drawn BEFORE keyboard so keyboard covers their ends ------
        sprite_bottom = oy + SPRITE_H          # ~152
        kbd_y         = sprite_bottom - KBD_OVERLAP   # ~140
        kx            = cx - KBD_W // 2       # 141 - 75 = 66
        self._draw_arm_connections(c, ox, oy, kx, kbd_y, agent_cfg)

        # ------ 3. Keyboard (painted over sprite feet — appears as foreground desk) ------
        self._draw_keyboard(c, kx, kbd_y, KBD_W, KBD_H)

        # ------ 4. Desk surface + panel (below keyboard) ------
        desk_top = kbd_y + KBD_H              # ~156
        desk_w   = KBD_W + 40                 # 190
        dkx      = cx - desk_w // 2           # 141 - 95 = 46

        # Desk surface (lighter strip visible above panel)
        c.create_rectangle(dkx, desk_top,
                           dkx + desk_w, desk_top + DESK_SURF,
                           fill='#3E3E70', outline='')
        c.create_line(dkx, desk_top, dkx + desk_w, desk_top,
                      fill='#8888CC', width=1)

        # Desk front panel drop-shadow
        c.create_rectangle(dkx + 3, desk_top + DESK_SURF + 3,
                           dkx + desk_w + 3, desk_top + DESK_SURF + DESK_PANEL + 3,
                           fill='#111122', outline='')
        # Desk front panel
        c.create_rectangle(dkx, desk_top + DESK_SURF,
                           dkx + desk_w, desk_top + DESK_SURF + DESK_PANEL,
                           fill='#2A2A50', outline='#5555AA', width=1)

        # ------ 5. Hands on keyboard ------
        self._draw_hands(c, cx, kx, kbd_y, state_cfg)

        # ------ 6. Update UI labels ------
        border_color = state_cfg['border_color']
        if self._state_name == 'celebrating':
            border_color = random.choice(
                ['#FF5566', '#55FF88', '#5566FF', '#FFEE44', '#FF55FF'])
        self._border_frame.configure(bg=border_color)

        bubble_bg = state_cfg['bubble_color']
        message   = self._message or _default_message(self._state_name)
        self._bubble_frame.configure(bg=bubble_bg)
        self._bubble_icon.configure(bg=bubble_bg, text=icon)
        self._bubble_lbl.configure(bg=bubble_bg, fg='#111133', text=message)

        self._name_lbl.configure(
            text=agent_cfg['label'], fg=agent_cfg['color'])

    # -----------------------------------------------------------------------
    # Arm connections (sleeve lines bridging sprite body → keyboard)
    # -----------------------------------------------------------------------
    def _draw_arm_connections(self, c, ox, oy, kx, kbd_y, agent_cfg):
        """
        Draw two sleeve-colored lines from the sprite shoulders down to the
        keyboard surface.  Positioned at the outer edges of the body sprite
        (cols 2 and 12) so they clear the leg pixels in the middle.
        The keyboard is drawn on top afterward, hiding the line ends.
        """
        color = agent_cfg['color']

        # Shoulders: row 8 top, outer body edge columns 2 (left) and 12 (right)
        sh_y   = oy + 8 * CELL
        l_x_sh = ox + 2 * CELL + 2     # left  outer edge of body (col 2 + inset)
        r_x_sh = ox + 12 * CELL - 2    # right outer edge of body (col 12 - inset)

        # Target: centre of each hand on the keyboard
        # Hand positions must match those in _draw_hands
        l_x_kd = kx + 22 + 11          # left  hand centre x
        r_x_kd = kx + KBD_W - 42 + 11  # right hand centre x
        tgt_y  = kbd_y + KBD_H         # just below keyboard surface (hidden by keyboard)

        # Elbow control points — bow outward from the body for a natural curve
        elbow_y    = sh_y + (tgt_y - sh_y) // 2   # vertically halfway down
        l_elbow_x  = l_x_sh - 18                   # left arm bows to the left
        r_elbow_x  = r_x_sh + 18                   # right arm bows to the right

        w = CELL - 2    # 7 px — thick enough to see, not blocky
        c.create_line(l_x_sh, sh_y, l_elbow_x, elbow_y, l_x_kd, tgt_y,
                      fill=color, width=w, capstyle='round', smooth=True)
        c.create_line(r_x_sh, sh_y, r_elbow_x, elbow_y, r_x_kd, tgt_y,
                      fill=color, width=w, capstyle='round', smooth=True)

    # -----------------------------------------------------------------------
    # Keyboard
    # -----------------------------------------------------------------------
    def _draw_keyboard(self, c, kx, ky, kw, kh):
        # Drop shadow
        c.create_rectangle(kx + 3, ky + 3, kx + kw + 3, ky + kh + 3,
                           fill='#111122', outline='')
        # Body
        c.create_rectangle(kx, ky, kx + kw, ky + kh,
                           fill='#252545', outline='#5555AA', width=1)
        # Inner bevel
        c.create_line(kx + 1, ky + 1, kx + kw - 1, ky + 1, fill='#4444AA')
        c.create_line(kx + 1, ky + 1, kx + 1,      ky + kh - 1, fill='#4444AA')

        # Three rows of keys
        kh_key, gap = 4, 2
        row_y0 = ky + 2
        self._draw_key_row(c, kx + 4,  row_y0,                    kw - 8,  11, kh_key, gap)
        self._draw_key_row(c, kx + 7,  row_y0 + kh_key + gap,     kw - 12, 10, kh_key, gap)
        self._draw_key_row(c, kx + 10, row_y0 + 2*(kh_key + gap), kw - 16,  8, kh_key, gap)

    def _draw_key_row(self, c, rx, ry, row_w, n, kh, gap):
        kw = max(3, (row_w - gap * (n - 1)) // n)
        for i in range(n):
            x1 = rx + i * (kw + gap)
            c.create_rectangle(x1, ry, x1 + kw, ry + kh,
                               fill='#3A3A72', outline='#6666AA', width=1)
            c.create_line(x1 + 1, ry + 1, x1 + kw - 1, ry + 1, fill='#8888CC')

    # -----------------------------------------------------------------------
    # Hands
    # -----------------------------------------------------------------------
    def _draw_hands(self, c, cx, kx, kbd_y, state_cfg):
        """
        Draw two hands resting on / pressing the keyboard.
        Hand positions are aligned with the sprite arm-end pixels:
          left hand  ~ 1/4 from left edge of keyboard
          right hand ~ 1/4 from right edge of keyboard
        In typing states hands alternate pressing down (+4px) and lifting up (+0px).
        """
        skin   = '#FFCC99'
        shadow = '#CC9966'

        # Hand x centres — left third and right third of keyboard
        l_hx = kx + 22          # left hand left edge
        r_hx = kx + KBD_W - 42  # right hand left edge

        is_typing = state_cfg['frames_key'] == 'typing'

        if is_typing:
            # Alternate left/right key press each animation frame
            press_left = self._frame_idx % 2 == 0
            l_hy = kbd_y + (4 if press_left else 0)
            r_hy = kbd_y + (4 if not press_left else 0)
        else:
            # Idle: both hands resting flat on desk surface
            l_hy = kbd_y + 1
            r_hy = kbd_y + 1

        self._draw_hand(c, l_hx, l_hy, skin, shadow)
        self._draw_hand(c, r_hx, r_hy, skin, shadow)

    def _draw_hand(self, c, hx, hy, skin, shadow):
        """Draw a simple top-down hand: palm oval + 4 finger stubs above."""
        # Palm
        c.create_oval(hx, hy, hx + 22, hy + 10,
                      fill=skin, outline=shadow, width=1)
        # Four finger stubs above palm
        for fi in range(4):
            fx = hx + 2 + fi * 5
            fh = 7 if fi in (1, 2) else 5   # middle fingers slightly longer
            c.create_rectangle(fx, hy - fh, fx + 4, hy + 2,
                               fill=skin, outline=shadow, width=1)
        # Thumb (small oval on the side)
        c.create_oval(hx - 5, hy + 2, hx + 4, hy + 9,
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
