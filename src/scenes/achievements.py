from __future__ import annotations
import pygame as pg

from .base import BaseScene
from ..ui import Button, draw_panel, draw_text, hover_state
from ..achievements import ACHIEVEMENTS, get_unlocked_count, get_total_count, get_achievement_progress, claim_achievement
from ..core import change_scene


class AchievementsScene(BaseScene):
    def enter(self, **kwargs):
        self.btns = []
        self.scroll = 0.0
        self.scroll_target = 0.0
        self.scroll_max = 0
        self._layout()

    def _layout(self):
        w, h = self.app.screen.get_size()
        self.panel = pg.Rect(w // 2 - 560, h // 2 - 330, 1120, 660)

    def handle_event(self, ev):
        if ev.type == pg.VIDEORESIZE:
            self._layout()

        # Mouse wheel scrolling
        if ev.type == pg.MOUSEWHEEL:
            mx, my = pg.mouse.get_pos()
            if self.panel.collidepoint(mx, my):
                self.scroll_target -= ev.y * 50
                self.scroll_target = max(0.0, min(self.scroll_target, self.scroll_max))

        for b in self.btns:
            b.handle(ev)

    def update(self, dt):
        # Smooth scrolling
        self.scroll += (self.scroll_target - self.scroll) * min(1.0, dt * 12.0)
        if abs(self.scroll - self.scroll_target) < 0.5:
            self.scroll = self.scroll_target

    def draw(self, surf):
        app = self.app
        sd = app.save
        lang = sd.settings.lang
        colors, fonts = app.colors, app.fonts
        self.draw_background(surf, colors)

        title = "Achievements" if lang == "en" else "Достигнувања"
        draw_panel(surf, self.panel, colors, title=title, title_font=fonts.ui_bold)

        self.btns = []

        # ── Progress header ──────────────────────────────────────────────
        unlocked = get_unlocked_count(sd)
        total = get_total_count()
        progress_pct = int((unlocked / total) * 100) if total > 0 else 0

        header_y = self.panel.y + 48
        progress_label = (
            f"{unlocked}/{total} Unlocked ({progress_pct}%)"
            if lang == "en"
            else f"{unlocked}/{total} Отклучени ({progress_pct}%)"
        )
        draw_text(surf, progress_label, fonts.ui_bold, colors["accent"],
                  (self.panel.x + 40, header_y), max_w=self.panel.w - 80)

        # Overall progress bar
        bar_x = self.panel.x + 40
        bar_y = header_y + 26
        bar_w = self.panel.w - 80
        bar_h = 12
        pg.draw.rect(surf, colors["line"], (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        if total > 0:
            fill_w = int((unlocked / total) * bar_w)
            if fill_w > 0:
                pg.draw.rect(surf, colors["accent"], (bar_x, bar_y, fill_w, bar_h), border_radius=6)

        # ── Scrollable card area ─────────────────────────────────────────
        # Leave 20px above and 70px below for back button
        content_top = bar_y + bar_h + 16
        content_bot = self.panel.bottom - 70
        view = pg.Rect(self.panel.x + 20, content_top, self.panel.w - 40, content_bot - content_top)

        # Grid layout — 4 columns, fixed sizes for 1280x720
        cols = 4
        gap_x = 12
        gap_y = 12
        card_w = (view.w - gap_x * (cols - 1) - 14) // cols   # 14 = scrollbar clearance
        pad = 12
        card_h = 155

        # Total content height for scrolling
        rows = (len(ACHIEVEMENTS) + cols - 1) // cols
        content_height = rows * (card_h + gap_y) - gap_y
        self.scroll_max = max(0, content_height - view.h)

        # Clip to viewport
        old_clip = surf.get_clip()
        surf.set_clip(view)

        start_x = view.x
        start_y = view.y - int(self.scroll)

        # Draw achievement cards
        for i, achievement in enumerate(ACHIEVEMENTS.values()):
            row = i // cols
            col = i % cols

            x = start_x + col * (card_w + gap_x)
            y = start_y + row * (card_h + gap_y)

            card_rect = pg.Rect(x, y, card_w, card_h)

            # Visibility cull
            if card_rect.bottom < view.y - 10 or card_rect.top > view.bottom + 10:
                continue

            is_unlocked = achievement.id in sd.unlocked_achievements
            is_claimed  = achievement.id in sd.claimed_achievements
            mx, my = pg.mouse.get_pos()
            is_hovered = card_rect.collidepoint(mx, my)

            # Card colours
            if is_unlocked:
                bg_color     = colors["panel2"] if is_hovered else colors["panel"]
                border_color = colors["accent"]
                text_color   = colors["text"]
            else:
                p = colors["panel"]
                bg_color     = (p[0] // 2, p[1] // 2, p[2] // 2)
                border_color = colors["line"]
                text_color   = colors["muted"]

            pg.draw.rect(surf, bg_color, card_rect, border_radius=12)
            pg.draw.rect(surf, border_color, card_rect, width=2, border_radius=12)

            inner_w = card_w - pad * 2

            # ── Achievement name ────────────────────────────────────────
            name = achievement.name_en if lang == "en" else achievement.name_mk
            draw_text(surf, name, fonts.ui_bold, text_color,
                      (card_rect.x + pad, card_rect.y + pad), max_w=inner_w)

            # ── Description (clean — no newlines, no emoji) ─────────────
            desc = achievement.desc_en if lang == "en" else achievement.desc_mk
            # Strip any stray newlines/emoji-like chars
            desc = desc.replace("\n", " ").replace("\r", " ").strip()
            desc_y = card_rect.y + pad + fonts.ui_bold.get_height() + 6
            desc_end_y = draw_text(surf, desc, fonts.ui, text_color,
                                   (card_rect.x + pad, desc_y), max_w=inner_w)

            # ── Reward line (separate, muted yellow) ─────────────────────
            if achievement.reward_coins > 0:
                reward_label = (
                    f"Reward: {achievement.reward_coins} coins"
                    if lang == "en"
                    else f"Награда: {achievement.reward_coins} coins"
                )
                reward_y = desc_end_y + 2
                draw_text(surf, reward_label, fonts.ui, colors["yellow"],
                          (card_rect.x + pad, reward_y), max_w=inner_w)

            # ── Bottom section (only draw when card bottom is in view) ──
            bottom_area_y = card_rect.bottom - 36
            # Only hide bottom elements if the card bottom is outside the view
            # (avoids claim button / progress bar floating over the header or off-screen)
            card_fully_visible = (card_rect.bottom - 40) >= view.y and card_rect.bottom <= view.bottom

            if not is_unlocked:
                # Progress bar for incremental achievements
                if achievement.requirement > 1 and card_fully_visible:
                    current, required = get_achievement_progress(sd, achievement.id)
                    prog_text = f"{current}/{required}"
                    draw_text(surf, prog_text, fonts.ui, text_color,
                              (card_rect.x + pad, bottom_area_y - 2), max_w=inner_w)

                    bx = card_rect.x + pad
                    by = card_rect.bottom - 18
                    bw = card_w - pad * 2
                    bh = 8
                    pg.draw.rect(surf, colors["line"], (bx, by, bw, bh), border_radius=4)
                    if required > 0 and current > 0:
                        fw = int((min(current, required) / required) * bw)
                        pg.draw.rect(surf, colors["accent"], (bx, by, fw, bh), border_radius=4)

            elif not is_claimed:
                # Claim button — only register when card is fully visible
                if card_fully_visible:
                    claim_rect = pg.Rect(card_rect.x + pad, bottom_area_y - 4, card_w - pad * 2, 30)
                    claim_text = (
                        f"CLAIM +{achievement.reward_coins}"
                        if lang == "en"
                        else f"ЗЕМИ +{achievement.reward_coins}"
                    )

                    def make_claim(ach_id):
                        def _cb():
                            coins = claim_achievement(sd, ach_id)
                            if coins > 0:
                                from ..save_system import save
                                save(sd)
                        return _cb

                    self.btns.append(Button(claim_rect, claim_text, make_claim(achievement.id)))

            else:
                # Already claimed
                if card_fully_visible:
                    status = "CLAIMED" if lang == "en" else "ЗЕМЕНО"
                    draw_text(surf, status, fonts.ui_bold, colors["good"],
                              (card_rect.x + pad, bottom_area_y), max_w=inner_w)

        # Restore clip
        surf.set_clip(old_clip)

        # ── Scrollbar ────────────────────────────────────────────────────
        if self.scroll_max > 0:
            track_x = view.right - 8
            track = pg.Rect(track_x, view.y, 6, view.h)
            pg.draw.rect(surf, colors["line"], track, border_radius=3)
            knob_h = max(30, int(view.h * (view.h / (view.h + self.scroll_max))))
            knob_y = int(view.y + (view.h - knob_h) * (self.scroll / self.scroll_max))
            knob = pg.Rect(track_x, knob_y, 6, knob_h)
            pg.draw.rect(surf, colors["accent"], knob, border_radius=3)

        # ── Back button ──────────────────────────────────────────────────
        back_rect = pg.Rect(self.panel.x + 40, self.panel.bottom - 62, 180, 46)
        back_text  = "Back" if lang == "en" else "Назад"
        menu_mod   = __import__('src.scenes.menu', fromlist=['MenuScene'])
        self.btns.append(Button(back_rect, back_text,
                                lambda: change_scene(app, menu_mod.MenuScene(app))))

        # Draw all buttons
        for b in self.btns:
            b.draw(surf, fonts.ui_bold, colors, hover_state(b.rect))
