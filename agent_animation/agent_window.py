"""
Agent Animation Window
======================
An always-on-top Tkinter window that shows a pixel-art sprite of the currently
active workflow agent.  The character sits behind a pixel-art desk with a
keyboard; in typing states the arms animate down to the keys.

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

WIN_W       = 260                   # content width
CANVAS_H    = SPRITE_H + 20        # enough for sprite + desk/keyboard overlap
LABEL_H     = 36                   # agent name row
BUBBLE_H    = 74                   # speech bubble
WIN_H       = CANVAS_H + LABEL_H + BUBBLE_H + 10

BG          = '#1E1E2E'
FONT_LABEL  = ('Courier', 14, 'bold')
FONT_STATUS = ('Courier', 11)
FONT_HEADER = ('Courier', 9)

POLL_MS     = 800
BOB_PERIOD  = 1.4

# Desk row — row 11 of the sprite (hips level); desk covers legs/feet below
DESK_ROW    = 11


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
    # Window construction  (native OS decorations — min/max/close work out-of-box)
    # -----------------------------------------------------------------------
    def _build_window(self):
        r = self.root
        r.title('⬡ SoftwareTeam Agents')
        r.geometry(f'{WIN_W}x{WIN_H}+80+80')
        r.resizable(True, True)
        r.configure(bg=BG)
        r.attributes('-topmost', True)
        # NOTE: overrideredirect is intentionally NOT set so that the OS
        # provides native minimize / maximize / close buttons.

        try:
            r.attributes('-alpha', 0.97)
        except tk.TclError:
            pass

        # Coloured border frame (changes with agent state)
        self._border_frame = tk.Frame(r, bg='#888888', padx=2, pady=2)
        self._border_frame.pack(fill='both', expand=True)

        inner = tk.Frame(self._border_frame, bg=BG)
        inner.pack(fill='both', expand=True)

        # Small header strip (purely decorative — drag is via OS title bar)
        header = tk.Frame(inner, bg='#252540', height=18)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text='● active agent', bg='#252540', fg='#7777AA',
                 font=FONT_HEADER, anchor='w').pack(side='left', padx=8)

        # Canvas — sprite + desk + keyboard + arms/hands
        self._canvas = tk.Canvas(inner, width=WIN_W - 8, height=CANVAS_H,
                                 bg=BG, highlightthickness=0)
        self._canvas.pack(pady=(4, 0))

        # Agent name label — large, bright
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
        canvas_w = WIN_W - 8
        cx       = canvas_w // 2
        ox       = cx - SPRITE_W // 2
        oy       = 4 + bob_y

        c.delete('all')

        # Desk position — at DESK_ROW in the sprite grid (covers hips/legs/feet)
        desk_top = oy + DESK_ROW * CELL   # ~99 px from sprite top + oy

        # ------ 1. Draw sprite (rows 0..DESK_ROW) ------
        # We only need to render visible rows (0 to DESK_ROW-1); lower rows are
        # covered by the desk.  Rendering all rows is fine — the desk paints
        # over them afterward.
        for row_i, row in enumerate(frame):
            for col_i, ch in enumerate(row):
                color = PALETTE.get(ch)
                if color is None:
                    continue
                x1 = ox + col_i * CELL
                y1 = oy + row_i * CELL
                c.create_rectangle(x1, y1, x1 + CELL - 1, y1 + CELL - 1,
                                   fill=color, outline='')

        # State icon (top-right of sprite)
        icon = state_cfg['icon']
        c.create_text(ox + SPRITE_W - 2, oy + 4, text=icon,
                      anchor='ne', font=('Courier', 14))

        # ------ 2. Desk (covers lower sprite) ------
        desk_w = SPRITE_W + 40
        dkx    = cx - desk_w // 2

        # Desk front panel drop-shadow
        c.create_rectangle(dkx + 3, desk_top + 3,
                           dkx + desk_w + 3, desk_top + 34,
                           fill='#111122', outline='')
        # Desk front panel
        c.create_rectangle(dkx, desk_top, dkx + desk_w, desk_top + 32,
                           fill='#2A2A50', outline='#5555AA', width=1)
        # Desk top surface (lighter strip)
        c.create_rectangle(dkx, desk_top - 5, dkx + desk_w, desk_top,
                           fill='#3E3E70', outline='')
        # Desk top highlight edge
        c.create_line(dkx, desk_top - 5, dkx + desk_w, desk_top - 5,
                      fill='#8888CC', width=1)

        # ------ 3. Keyboard (sits on top of desk surface) ------
        kbd_y = desk_top - 28   # keyboard sits above the desk front panel, on the surface
        self._draw_keyboard(c, cx, kbd_y)

        # ------ 4. Arms and hands ------
        self._draw_arms_and_hands(c, ox, oy, cx, kbd_y, state_cfg)

        # ------ 5. Update UI elements ------
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
    # Keyboard
    # -----------------------------------------------------------------------
    def _draw_keyboard(self, c, cx, ky):
        kw, kh = 160, 34
        kx = cx - kw // 2

        # Drop shadow
        c.create_rectangle(kx + 3, ky + 3, kx + kw + 3, ky + kh + 3,
                           fill='#111122', outline='')
        # Body
        c.create_rectangle(kx, ky, kx + kw, ky + kh,
                           fill='#252545', outline='#5555AA', width=1)
        # Inner bevel
        c.create_line(kx + 1, ky + 1, kx + kw - 1, ky + 1, fill='#4444AA')
        c.create_line(kx + 1, ky + 1, kx + 1,      ky + kh - 1, fill='#4444AA')

        kh_key, gap = 6, 2
        self._draw_key_row(c, kx + 4,  ky + 4,                   kw - 8,  10, kh_key, gap)
        self._draw_key_row(c, kx + 8,  ky + 4 + kh_key + gap,    kw - 12,  9, kh_key, gap)
        self._draw_key_row(c, kx + 12, ky + 4 + 2*(kh_key+gap),  kw - 18,  7, kh_key, gap)

        # Space bar
        sp_x = kx + kw // 4
        sp_y = ky + kh - 9
        c.create_rectangle(sp_x, sp_y, sp_x + kw // 2, sp_y + 6,
                           fill='#3A3A72', outline='#7777BB', width=1)
        c.create_line(sp_x + 1, sp_y + 1, sp_x + kw // 2 - 1, sp_y + 1,
                      fill='#9999CC')

    def _draw_key_row(self, c, rx, ry, row_w, n, kh, gap):
        kw = max(4, (row_w - gap * (n - 1)) // n)
        for i in range(n):
            x1 = rx + i * (kw + gap)
            c.create_rectangle(x1, ry, x1 + kw, ry + kh,
                               fill='#3A3A72', outline='#6666AA', width=1)
            c.create_line(x1 + 1, ry + 1, x1 + kw - 1, ry + 1, fill='#8888CC')

    # -----------------------------------------------------------------------
    # Arms and hands
    # -----------------------------------------------------------------------
    def _draw_arms_and_hands(self, c, ox, oy, cx, kbd_y, state_cfg):
        """
        Draw arms from the sprite shoulders down to the keyboard.
        Shoulders are at sprite row 8, cols 3 and 10 (left/right).
        In typing states: arms extend diagonally to keyboard, hands animate.
        In idle states: arms hang (already visible in sprite), hands rest on desk.
        """
        skin   = '#FFCC99'
        shadow = '#CC9966'

        # Shoulder anchor points in canvas coords
        l_sh_x = ox + 3 * CELL + CELL // 2   # left shoulder  ~ ox + 31
        r_sh_x = ox + 10 * CELL + CELL // 2  # right shoulder ~ ox + 94
        sh_y   = oy + 8 * CELL + CELL // 2   # row 8 centre   ~ oy + 76

        is_typing = state_cfg['frames_key'] == 'typing'

        if is_typing:
            # Hand target positions on/above keyboard
            l_hx = cx - 38
            r_hx = cx + 16
            left_down  = self._frame_idx % 2 == 0
            l_hy = kbd_y + 2 + (4 if left_down else 0)
            r_hy = kbd_y + 2 + (4 if not left_down else 0)

            # Arms as smooth thick lines from shoulder to hand centre
            c.create_line(l_sh_x, sh_y, l_hx + 10, l_hy + 6,
                          fill=skin, width=8, capstyle='round', smooth=True)
            c.create_line(r_sh_x, sh_y, r_hx + 10, r_hy + 6,
                          fill=skin, width=8, capstyle='round', smooth=True)

            # Hands
            self._draw_hand(c, l_hx, l_hy, skin, shadow, fingers_up=True)
            self._draw_hand(c, r_hx, r_hy, skin, shadow, fingers_up=True)

        else:
            # Idle/thinking: straight arms along the body sides, hands resting
            # on the desk surface
            l_hx = cx - 52
            r_hx = cx + 30
            hand_y = kbd_y + 6

            # Short arm lines down the sides
            c.create_line(l_sh_x, sh_y, l_hx + 9, hand_y,
                          fill=skin, width=7, capstyle='round', smooth=True)
            c.create_line(r_sh_x, sh_y, r_hx + 9, hand_y,
                          fill=skin, width=7, capstyle='round', smooth=True)

            self._draw_hand(c, l_hx, hand_y, skin, shadow, fingers_up=False)
            self._draw_hand(c, r_hx, hand_y, skin, shadow, fingers_up=False)

    def _draw_hand(self, c, hx, hy, skin, shadow, fingers_up=True):
        # Palm
        c.create_oval(hx, hy, hx + 20, hy + 12,
                      fill=skin, outline=shadow, width=1)
        if fingers_up:
            # Four fingers above palm
            for fi in range(4):
                fx = hx + 2 + fi * 5
                finger_h = 8 - fi % 2  # slight variation in length
                c.create_rectangle(fx, hy - finger_h, fx + 4, hy + 3,
                                   fill=skin, outline=shadow, width=1)
        # Thumb
        c.create_oval(hx - 5, hy + 3, hx + 4, hy + 11,
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
