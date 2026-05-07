import hashlib
import math
import os
import queue
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox

from deepfaceresult import DeepFaceResults


APP_BG = "#090b16"
PANEL = "#171e31"
PANEL_2 = "#1c2539"
BORDER = "#2b3655"
TEXT = "#f7f8fc"
MUTED = "#9aa3bb"
DIM = "#69738b"
BLUE = "#3e73ff"
PURPLE = "#7c4dff"
GREEN = "#10b981"
CYAN = "#24d1a0"
YELLOW = "#ffd60a"
MAGENTA = "#ff2bd6"


class RoundedCanvas(tk.Canvas):
    def rounded_rect(self, x1, y1, x2, y2, radius=18, **kwargs):
        points = [
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)


class DeepFaceVideoAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DeepFace AI Analiz")
        self.root.geometry("1000x650")
        self.root.minsize(900, 580)
        self.root.configure(bg=APP_BG)

        self.video_path = None
        self.is_analyzing = False
        self.progress = 0
        self.history = []
        self.result_queue = queue.Queue()
        self.stop_flag = False

        self.canvas = RoundedCanvas(root, bg=APP_BG, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.render)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_motion)

        self.click_zones = {}
        self.poll_queue()

    def render(self, event=None):
        self.canvas.delete("all")
        self.click_zones = {}

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        margin = 22
        card_x1 = margin
        card_y1 = 8
        card_x2 = width - margin
        card_y2 = height - 14

        self.canvas.rounded_rect(
            card_x1,
            card_y1,
            card_x2,
            card_y2,
            radius=26,
            fill="#0c1222",
            outline="",
        )

        self.draw_header(card_x1, card_y1, card_x2)
        self.canvas.create_rectangle(card_x1, 92, card_x2, 96, fill=MAGENTA, outline="")

        content_top = 120
        left_x = card_x1 + 24
        right_w = max(320, int((card_x2 - card_x1) * 0.37))
        gap = 24
        right_x = card_x2 - right_w - 22
        left_w = max(420, right_x - left_x - gap)

        self.draw_upload_panel(left_x, content_top, left_x + left_w, content_top + 324)
        self.draw_action_panel(left_x, content_top + 344, left_x + left_w, content_top + 484)
        self.draw_history_panel(right_x, content_top, right_x + right_w, card_y2 - 24)

        if self.is_analyzing:
            self.draw_progress_overlay(left_x, content_top + 344, left_x + left_w, content_top + 484)

    def draw_header(self, x1, y1, x2):
        icon_x = x1 + 24
        icon_y = y1 + 17
        self.canvas.rounded_rect(icon_x, icon_y, icon_x + 54, icon_y + 54, radius=14, fill=BLUE, outline="")
        self.canvas.rounded_rect(icon_x + 8, icon_y + 8, icon_x + 54, icon_y + 54, radius=14, fill=PURPLE, outline="")
        self.canvas.create_text(icon_x + 27, icon_y + 28, text="AI", fill=TEXT, font=("Segoe UI", 17, "bold"))

        self.canvas.create_text(
            icon_x + 66,
            icon_y + 18,
            text="DeepFace AI Analiz",
            fill=TEXT,
            anchor="w",
            font=("Segoe UI", 21, "bold"),
        )
        self.canvas.create_text(
            icon_x + 66,
            icon_y + 45,
            text="Yapay zeka destekli yuz tanima ve deepfake tespit sistemi",
            fill=MUTED,
            anchor="w",
            font=("Segoe UI", 9, "bold"),
        )



    def draw_upload_panel(self, x1, y1, x2, y2):
        self.canvas.rounded_rect(x1, y1, x2, y2, radius=11, fill=PANEL, outline=BORDER, width=1)
        self.draw_small_icon(x1 + 24, y1 + 26, "⇧", BLUE)
        self.canvas.create_text(x1 + 70, y1 + 43, text="Video Yukle", fill=TEXT, anchor="w", font=("Segoe UI", 17, "bold"))

        dz_x1, dz_y1 = x1 + 24, y1 + 80
        dz_x2, dz_y2 = x2 - 24, y2 - 24
        self.canvas.rounded_rect(
            dz_x1,
            dz_y1,
            dz_x2,
            dz_y2,
            radius=12,
            fill="#1a2435",
            outline="#2563eb",
            width=2,
            dash=(5, 4),
        )
        self.register_zone("choose_video", dz_x1, dz_y1, dz_x2, dz_y2)

        cx = (dz_x1 + dz_x2) / 2
        cy = dz_y1 + 78
        self.canvas.rounded_rect(cx - 42, cy - 42, cx + 42, cy + 42, radius=14, fill=BLUE, outline="")
        self.canvas.create_text(cx, cy - 2, text="📁", fill=TEXT, font=("Segoe UI", 30))

        if self.video_path:
            title = os.path.basename(self.video_path)
            subtitle = self.video_path
        else:
            title = "Video secmek icin tiklayin"
            subtitle = "MP4, AVI, MOV formatlari desteklenir"

        self.canvas.create_text(cx, cy + 76, text=title, fill=TEXT, font=("Segoe UI", 12, "bold"))
        self.canvas.create_text(cx, cy + 103, text=subtitle, fill=MUTED, font=("Segoe UI", 8, "bold"), width=430)
        self.canvas.create_text(dz_x2 - 43, dz_y1 + 47, text="✦", fill=YELLOW, font=("Segoe UI", 21, "bold"))

    def draw_action_panel(self, x1, y1, x2, y2):
        self.canvas.rounded_rect(x1, y1, x2, y2, radius=11, fill=PANEL, outline=BORDER, width=1)
        
        btn1_x1, btn1_y1 = x1 + 24, y1 + 20
        btn1_x2, btn1_y2 = x2 - 24, y1 + 65
        
        disabled = not self.video_path or self.is_analyzing
        fill = "#145f50" if disabled else "#059669"
        glow = "#163f43" if disabled else "#0dbb83"
        self.canvas.rounded_rect(btn1_x1 - 1, btn1_y1 + 8, btn1_x2 + 1, btn1_y2 + 8, radius=9, fill=glow, outline="")
        self.canvas.rounded_rect(btn1_x1, btn1_y1, btn1_x2, btn1_y2, radius=9, fill=fill, outline="")
        self.register_zone("start_analysis", btn1_x1, btn1_y1, btn1_x2, btn1_y2)

        label = "Analiz yapiliyor..." if self.is_analyzing else "Analizi Baslat"
        self.canvas.create_text(
            (btn1_x1 + btn1_x2) / 2,
            (btn1_y1 + btn1_y2) / 2,
            text=label,
            fill=TEXT,
            font=("Segoe UI", 11, "bold"),
        )
        
        btn2_x1, btn2_y1 = x1 + 24, y1 + 75
        btn2_x2, btn2_y2 = x2 - 24, y1 + 120
        
        stop_disabled = not self.is_analyzing
        stop_fill = "#731821" if stop_disabled else "#e11d48"
        stop_glow = "#4d1016" if stop_disabled else "#be123c"
        self.canvas.rounded_rect(btn2_x1 - 1, btn2_y1 + 8, btn2_x2 + 1, btn2_y2 + 8, radius=9, fill=stop_glow, outline="")
        self.canvas.rounded_rect(btn2_x1, btn2_y1, btn2_x2, btn2_y2, radius=9, fill=stop_fill, outline="")
        self.register_zone("stop_analysis", btn2_x1, btn2_y1, btn2_x2, btn2_y2)

        self.canvas.create_text(
            (btn2_x1 + btn2_x2) / 2,
            (btn2_y1 + btn2_y2) / 2,
            text="Islemi Durdur",
            fill=TEXT,
            font=("Segoe UI", 11, "bold"),
        )

    def draw_history_panel(self, x1, y1, x2, y2):
        self.canvas.rounded_rect(x1, y1, x2, y2, radius=11, fill=PANEL, outline=BORDER, width=1)
        self.draw_small_icon(x1 + 24, y1 + 26, "◷", PURPLE)
        self.canvas.create_text(x1 + 70, y1 + 39, text="Analiz Gecmisi", fill=TEXT, anchor="w", font=("Segoe UI", 16, "bold"))
        self.canvas.create_text(
            x1 + 70,
            y1 + 61,
            text=f"Son {len(self.history)} tarama" if self.history else "Son 20 tarama",
            fill=MUTED,
            anchor="w",
            font=("Segoe UI", 8, "bold"),
        )

        if not self.history:
            box_x1, box_y1 = x1 + 25, y1 + 82
            box_x2, box_y2 = x2 - 30, y1 + 292
            self.canvas.rounded_rect(box_x1, box_y1, box_x2, box_y2, radius=10, fill="#1a2433", outline=BORDER, width=1)
            cx = (box_x1 + box_x2) / 2
            cy = box_y1 + 78
            self.canvas.create_oval(cx - 26, cy - 26, cx + 26, cy + 26, outline="#536075", width=5)
            self.canvas.create_line(cx, cy, cx, cy - 17, fill="#536075", width=5)
            self.canvas.create_line(cx, cy, cx + 13, cy + 8, fill="#536075", width=5)
            self.canvas.create_text(cx + 30, cy - 21, text="✦", fill=YELLOW, font=("Segoe UI", 19, "bold"))
            self.canvas.create_text(cx, cy + 59, text="Henuz analiz yapilmadi", fill=TEXT, font=("Segoe UI", 9, "bold"))
            self.canvas.create_text(cx, cy + 82, text="Ilk videonuzu yukleyin", fill=DIM, font=("Segoe UI", 8))
            return

        item_top = y1 + 92
        for index, item in enumerate(self.history[:5]):
            top = item_top + index * 82
            if top + 68 > y2 - 18:
                break
            risk_color = GREEN if item["score"] < 45 else YELLOW if item["score"] < 70 else "#ff5a6a"
            self.canvas.rounded_rect(x1 + 24, top, x2 - 24, top + 68, radius=10, fill="#1a2433", outline=BORDER, width=1)
            self.canvas.create_text(x1 + 42, top + 19, text=item["name"], fill=TEXT, anchor="w", font=("Segoe UI", 9, "bold"), width=x2 - x1 - 130)
            self.canvas.create_text(x1 + 42, top + 43, text=item["summary"], fill=MUTED, anchor="w", font=("Segoe UI", 8), width=x2 - x1 - 125)
            self.canvas.create_text(x2 - 50, top + 24, text=f"%{item['score']}", fill=risk_color, font=("Segoe UI", 16, "bold"))
            self.canvas.create_text(x2 - 50, top + 48, text="risk", fill=DIM, font=("Segoe UI", 8, "bold"))

    def draw_progress_overlay(self, x1, y1, x2, y2):
        bar_x1, bar_y1 = x1 + 44, y2 - 30
        bar_x2, bar_y2 = x2 - 44, y2 - 20
        self.canvas.rounded_rect(bar_x1, bar_y1, bar_x2, bar_y2, radius=5, fill="#26304d", outline="")
        fill_w = (bar_x2 - bar_x1) * (self.progress / 100)
        self.canvas.rounded_rect(bar_x1, bar_y1, bar_x1 + fill_w, bar_y2, radius=5, fill=CYAN, outline="")
        self.canvas.create_text(bar_x2, bar_y1 - 12, text=f"%{self.progress}", fill=MUTED, anchor="e", font=("Segoe UI", 8, "bold"))

    def draw_small_icon(self, x, y, text, color):
        self.canvas.rounded_rect(x, y, x + 36, y + 36, radius=10, fill=color, outline="")
        self.canvas.create_text(x + 18, y + 18, text=text, fill=TEXT, font=("Segoe UI", 17, "bold"))

    def register_zone(self, name, x1, y1, x2, y2):
        self.click_zones[name] = (x1, y1, x2, y2)

    def zone_at(self, x, y):
        for name, (x1, y1, x2, y2) in self.click_zones.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                return name
        return None

    def handle_motion(self, event):
        zone = self.zone_at(event.x, event.y)
        self.canvas.configure(cursor="hand2" if zone in {"choose_video", "start_analysis", "stop_analysis"} else "")

    def handle_click(self, event):
        zone = self.zone_at(event.x, event.y)
        if zone == "choose_video":
            self.choose_video()
        elif zone == "start_analysis":
            self.start_analysis()
        elif zone == "stop_analysis":
            self.stop_analysis()

    def choose_video(self):
        path = filedialog.askopenfilename(
            title="Video sec",
            filetypes=[
                ("Video dosyalari", "*.mp4 *.avi *.mov *.mkv *.webm"),
                ("Tum dosyalar", "*.*"),
            ],
        )
        if path:
            self.video_path = path
            self.render()

    def start_analysis(self):
        if self.is_analyzing:
            return
        if not self.video_path:
            messagebox.showinfo("Video gerekli", "Once analiz edilecek bir video secin.")
            return

        self.is_analyzing = True
        self.progress = 1
        self.stop_flag = False
        self.render()

        worker = threading.Thread(target=self.analyze_worker, args=(self.video_path,), daemon=True)
        worker.start()

    def stop_analysis(self):
        if not self.is_analyzing:
            return
        self.stop_flag = True
        self.render()

    def analyze_worker(self, path):
        def progress_callback(p):
            self.progress = p
            self.root.after(0, self.render)
            return not self.stop_flag
            
        try:
            analyzer = DeepFaceResults(path)
            res = analyzer.start(progress_callback=progress_callback)
            
            name = os.path.basename(path)
            if "Fake" in res:
                score = 85
                verdict = "Yuksek risk"
                summary = "Deepfake tespit edildi!"
            elif "Stopped" in res:
                score = 0
                verdict = "Durduruldu"
                summary = "Islem iptal edildi"
            elif "Real" in res:
                score = 15
                verdict = "Dusuk risk"
                summary = "Gercek video"
            else:
                score = 50
                verdict = "Bilinmeyen"
                summary = "Analiz tamamlanamadi"
                
        except Exception as e:
            name = os.path.basename(path)
            score = 50
            summary = f"Hata: {str(e)}"
            verdict = "Hata"

        result = {
            "name": name,
            "score": score,
            "summary": f"{verdict} • {summary}",
        }
        self.result_queue.put(result)

    def poll_queue(self):
        try:
            result = self.result_queue.get_nowait()
        except queue.Empty:
            self.root.after(100, self.poll_queue)
            return

        self.progress = 100
        self.is_analyzing = False
        self.history.insert(0, result)
        self.history = self.history[:20]
        self.render()

        self.root.after(100, self.poll_queue)

def main():
    root = tk.Tk()
    try:
        root.iconbitmap(default="")
    except tk.TclError:
        pass
    DeepFaceVideoAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()