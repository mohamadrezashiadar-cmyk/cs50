# ═══════════════════════════════════════════════
#         دِگْرِیز پرو - رابط گرافیکی
#         توسعه‌دهنده: شهداد
# ═══════════════════════════════════════════════

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import hashlib
import time
import random
import string
from datetime import datetime

import degrees
from degrees import load_data, shortest_path, neighbors_for_person


APP_NAME = "دِگْرِیز پرو"
APP_VERSION = "4.0.0"
APP_DEVELOPER = "شهداد"
FA_DEVELOPER = "توسعه‌دهنده: شهداد"
FA_COPYRIGHT = "© تمام حقوق برای شهداد محفوظ است"

CONFIG_FILE = "degrees_config.json"
USERS_FILE = "degrees_users.json"
HISTORY_FILE = "degrees_history.json"
FAVORITES_FILE = "degrees_favorites.json"
BADGES_FILE = "degrees_badges.json"
DATA_FILES = ["people.csv", "movies.csv", "stars.csv"]
FA_FONT = "Segoe UI"


COLORS_DARK = {
    "bg": "#1a1a2e",
    "bg2": "#16213e",
    "bg3": "#0f3460",
    "card": "#22224a",
    "accent": "#e94560",
    "accent2": "#533483",
    "accent3": "#0ea5e9",
    "text": "#ffffff",
    "text_dim": "#a0a0b8",
    "success": "#00b894",
    "warning": "#fdcb6e",
    "error": "#ff4757",
    "entry_bg": "#2a2a4a",
    "hover": "#ff5570",
    "border": "#3a3a6a"
}

COLORS_LIGHT = {
    "bg": "#f5f6fa",
    "bg2": "#e8eaf0",
    "bg3": "#487eb0",
    "card": "#ffffff",
    "accent": "#e94560",
    "accent2": "#6c5ce7",
    "accent3": "#0984e3",
    "text": "#2d3436",
    "text_dim": "#636e72",
    "success": "#00b894",
    "warning": "#e17055",
    "error": "#d63031",
    "entry_bg": "#ffffff",
    "hover": "#ff6b81",
    "border": "#b2bec3"
}


def hash_password(password, salt=None):
    if salt is None:
        salt = "".join(random.choices(string.ascii_letters + string.digits, k=32))
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt


def format_number(n):
    try:
        return f"{n:,}"
    except Exception:
        return str(n)


def to_persian_digits(text):
    persian = "۰۱۲۳۴۵۶۷۸۹"
    result = str(text)
    for i, d in enumerate("0123456789"):
        result = result.replace(d, persian[i])
    return result


def validate_email(email):
    if not email:
        return True
    if "@" not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    username, domain = parts
    if not username or not domain or "." not in domain:
        return False
    return True


class PersianText:
    LOGIN_SUBTITLE = "برای ادامه وارد شوید"
    USERNAME = "نام کاربری"
    PASSWORD = "رمز عبور"
    CONFIRM_PASSWORD = "تأیید رمز عبور"
    EMAIL = "ایمیل (اختیاری)"
    REMEMBER_ME = "مرا به خاطر بسپار"
    GUEST_MODE = "ورود به عنوان مهمان"
    SIGN_IN = "ورود"
    CREATE_ACCOUNT = "ساخت حساب جدید"
    BACK_TO_LOGIN = "← بازگشت به صفحه ورود"
    FILL_ALL_FIELDS = "لطفاً همه فیلدها را پر کنید"
    USERNAME_SHORT = "نام کاربری باید حداقل ۳ حرف باشد"
    PASSWORD_SHORT = "رمز عبور باید حداقل ۴ حرف باشد"
    USERNAME_EXISTS = "این نام کاربری قبلاً ثبت شده است"
    USER_NOT_FOUND = "کاربری با این نام پیدا نشد"
    INCORRECT_PASSWORD = "رمز عبور اشتباه است"
    PASSWORDS_NOT_MATCH = "رمزهای عبور یکسان نیستند"
    BAD_EMAIL = "فرمت ایمیل صحیح نیست"
    SEARCH_TAB = "🔍 جستجو"
    HISTORY_TAB = "📜 تاریخچه"
    FAVORITES_TAB = "⭐ علاقه‌مندی‌ها"
    STATS_TAB = "📊 آمار"
    BROWSE_TAB = "🌐 مرورگر"
    BADGES_TAB = "🏅 نشان‌ها"
    QUIZ_TAB = "🎯 آزمون"
    SETTINGS_TAB = "⚙ تنظیمات"
    ABOUT_TAB = "ℹ درباره"
    SOURCE_ACTOR = "بازیگر مبدأ"
    TARGET_ACTOR = "بازیگر مقصد"
    FIND_CONNECTION = "پیدا کردن ارتباط"
    SWAP = "جابجایی"
    RANDOM = "تصادفی"
    ENTER_BOTH_ACTORS = "لطفاً نام هر دو بازیگر را وارد کنید"
    NOT_FOUND = "پیدا نشد"
    DEGREES_APART = "درجه جدایی"
    MOVIES_IN_PATH = "فیلم‌ها در مسیر"
    PEOPLE_IN_PATH = "افراد در مسیر"
    EXPORT_TXT = "خروجی متنی"
    EXPORT_JSON = "خروجی JSON"
    SHOW_DETAILS = "نمایش جزئیات"
    ADD_FAVORITE = "افزودن به علاقه‌مندی"
    REMOVE_FAVORITE = "حذف از علاقه‌مندی"
    NO_HISTORY = "هنوز تاریخچه‌ای وجود ندارد"
    NO_FAVORITES = "هنوز علاقه‌مندی‌ای ندارید"
    CLEAR_HISTORY = "پاک کردن همه"
    TOTAL_SEARCHES = "کل جستجوها"
    CONNECTIONS_FOUND = "ارتباط پیدا شده"
    NOT_FOUND_COUNT = "پیدا نشده"
    AVG_DEGREES = "میانگین درجه‌ها"
    AVG_TIME = "میانگین زمان"
    MOST_CONNECTED = "پرکاربردترین بازیگران"
    THEME = "تم:"
    DARK_THEME = "تیره"
    LIGHT_THEME = "روشن"
    SPLASH = "نمایش صفحه بارگذاری"
    AUTOCOMPLETE = "پیشنهاد خودکار نام‌ها"
    SAVE_SETTINGS = "ذخیره تنظیمات"
    SETTINGS_SAVED = "تنظیمات ذخیره شد"
    CHANGE_PASSWORD = "تغییر رمز عبور"
    DELETE_ACCOUNT = "حذف حساب کاربری"
    CURRENT_PASSWORD = "رمز فعلی"
    NEW_PASSWORD = "رمز جدید"
    PASSWORD_CHANGED = "رمز عبور با موفقیت تغییر کرد"
    ACCOUNT_DELETED = "حساب شما حذف شد"
    LOGOUT = "خروج"
    LOGOUT_CONFIRM = "آیا می‌خواهید خارج شوید؟"
    READY = "آماده"
    MISSING_FILES = "فایل‌های زیر یافت نشد"
    SEARCH_HISTORY = "تاریخچه جستجو"
    FAVORITE_ACTORS = "بازیگران مورد علاقه"
    RECENT_SEARCHES = "جستجوهای اخیر"
    DOUBLE_CLICK_HINT = "برای تکرار جستجو روی هر ردیف دوبار کلیک کنید"
    CONNECTION_PATH = "مسیر ارتباط"
    SUMMARY = "خلاصه"
    QUICK_ACTIONS = "اقدامات سریع"
    STRENGTH_LABELS = ["خیلی ضعیف", "ضعیف", "متوسط", "خوب", "قوی"]


class AppConfig:
    def __init__(self):
        self.config = {
            "theme": "dark",
            "data_directory": "large",
            "last_user": "",
            "remember_me": False,
            "window_width": 1300,
            "window_height": 800,
            "max_history": 100,
            "show_splash": True,
            "auto_search_names": True
        }
        self.load()

    def load(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    for key, value in saved.items():
                        if key in self.config:
                            self.config[key] = value
        except Exception:
            pass

    def save(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save()


class UserDatabase:
    def __init__(self):
        self.users = {}
        self.load()

    def load(self):
        try:
            if os.path.exists(USERS_FILE):
                with open(USERS_FILE, "r", encoding="utf-8") as f:
                    self.users = json.load(f)
        except Exception:
            self.users = {}

    def save(self):
        try:
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def user_exists(self, username):
        return username.strip().lower() in self.users

    def register(self, username, password, email=""):
        username = username.strip().lower()
        if not username or len(username) < 3:
            return False, PersianText.USERNAME_SHORT
        if len(password) < 4:
            return False, PersianText.PASSWORD_SHORT
        if self.user_exists(username):
            return False, PersianText.USERNAME_EXISTS
        if email and not validate_email(email):
            return False, PersianText.BAD_EMAIL
        hashed, salt = hash_password(password)
        self.users[username] = {
            "password": hashed,
            "salt": salt,
            "email": email,
            "created": datetime.now().isoformat(),
            "last_login": ""
        }
        self.save()
        return True, "حساب شما با موفقیت ساخته شد!"

    def login(self, username, password):
        username = username.strip().lower()
        if not self.user_exists(username):
            return False, PersianText.USER_NOT_FOUND
        user = self.users[username]
        hashed, _ = hash_password(password, user["salt"])
        if hashed != user["password"]:
            return False, PersianText.INCORRECT_PASSWORD
        user["last_login"] = datetime.now().isoformat()
        self.save()
        return True, "ورود موفق"

    def change_password(self, username, old_password, new_password):
        username = username.strip().lower()
        if not self.user_exists(username):
            return False, PersianText.USER_NOT_FOUND
        user = self.users[username]
        hashed, _ = hash_password(old_password, user["salt"])
        if hashed != user["password"]:
            return False, "رمز فعلی اشتباه است"
        if len(new_password) < 4:
            return False, PersianText.PASSWORD_SHORT
        hashed_new, salt_new = hash_password(new_password)
        user["password"] = hashed_new
        user["salt"] = salt_new
        self.save()
        return True, PersianText.PASSWORD_CHANGED

    def delete_user(self, username, password):
        username = username.strip().lower()
        if not self.user_exists(username):
            return False, PersianText.USER_NOT_FOUND
        user = self.users[username]
        hashed, _ = hash_password(password, user["salt"])
        if hashed != user["password"]:
            return False, PersianText.INCORRECT_PASSWORD
        del self.users[username]
        self.save()
        return True, PersianText.ACCOUNT_DELETED


class HistoryManager:
    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        try:
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
        except Exception:
            self.data = {}

    def save(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def add_entry(self, username, person1, person2, found, deg, runtime):
        username = username.strip().lower()
        if username not in self.data:
            self.data[username] = []
        self.data[username].insert(0, {
            "person1": person1,
            "person2": person2,
            "found": found,
            "degrees": deg,
            "runtime": runtime,
            "timestamp": datetime.now().isoformat()
        })
        limit = APP_CONFIG.get("max_history", 100)
        if len(self.data[username]) > limit:
            self.data[username] = self.data[username][:limit]
        self.save()

    def get_history(self, username):
        return self.data.get(username.strip().lower(), [])

    def clear_history(self, username):
        self.data[username.strip().lower()] = []
        self.save()

    def get_stats(self, username):
        history = self.get_history(username)
        total = len(history)
        found = sum(1 for h in history if h["found"])
        if total == 0:
            return {"total": 0, "found": 0, "not_found": 0, "avg_degrees": 0, "avg_runtime": 0}
        found_entries = [h for h in history if h["found"]]
        degrees_list = [h["degrees"] for h in found_entries]
        return {
            "total": total,
            "found": found,
            "not_found": total - found,
            "avg_degrees": round(sum(degrees_list) / len(degrees_list), 2) if degrees_list else 0,
            "avg_runtime": round(sum(h["runtime"] for h in history) / total, 2)
        }


class FavoritesManager:
    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        try:
            if os.path.exists(FAVORITES_FILE):
                with open(FAVORITES_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
        except Exception:
            self.data = {}

    def save(self):
        try:
            with open(FAVORITES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def add(self, username, person_id, person_name):
        username = username.strip().lower()
        if username not in self.data:
            self.data[username] = []
        for fav in self.data[username]:
            if fav["id"] == person_id:
                return False
        self.data[username].append({
            "id": person_id,
            "name": person_name,
            "added": datetime.now().isoformat()
        })
        self.save()
        return True

    def remove(self, username, person_id):
        username = username.strip().lower()
        if username not in self.data:
            return False
        before = len(self.data[username])
        self.data[username] = [f for f in self.data[username] if f["id"] != person_id]
        if len(self.data[username]) < before:
            self.save()
            return True
        return False

    def get_favorites(self, username):
        return self.data.get(username.strip().lower(), [])

    def is_favorite(self, username, person_id):
        for fav in self.get_favorites(username):
            if fav["id"] == person_id:
                return True
        return False


class BadgeManager:
    BADGES = [
        {"id": "first_search", "name": "اولین جستجو", "icon": "🔍", "desc": "اولین جستجو را انجام بده"},
        {"id": "ten_searches", "name": "جستجوگر", "icon": "🔎", "desc": "۱۰ جستجو انجام بده"},
        {"id": "fifty_searches", "name": "کاوشگر", "icon": "🧭", "desc": "۵۰ جستجو انجام بده"},
        {"id": "first_connection", "name": "اولین ارتباط", "icon": "🔗", "desc": "اولین ارتباط را پیدا کن"},
        {"id": "ten_connections", "name": "متصل‌کننده", "icon": "🕸", "desc": "۱۰ ارتباط پیدا کن"},
        {"id": "one_degree", "name": "هم‌بازی", "icon": "1️⃣", "desc": "ارتباط ۱ درجه‌ای پیدا کن"},
        {"id": "two_degrees", "name": "نزدیک", "icon": "2️⃣", "desc": "ارتباط ۲ درجه‌ای پیدا کن"},
        {"id": "six_degrees", "name": "شش درجه", "icon": "6️⃣", "desc": "ارتباط ۶ درجه‌ای پیدا کن"},
        {"id": "five_favorites", "name": "کلکسیونر", "icon": "⭐", "desc": "۵ بازیگر ذخیره کن"},
        {"id": "quiz_player", "name": "آزمون‌دهنده", "icon": "🎯", "desc": "در آزمون شرکت کن"},
        {"id": "quiz_master", "name": "استاد آزمون", "icon": "🎓", "desc": "در آزمون ۵۰ امتیاز بگیر"},
    ]

    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        try:
            if os.path.exists(BADGES_FILE):
                with open(BADGES_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
        except Exception:
            self.data = {}

    def save(self):
        try:
            with open(BADGES_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def unlock(self, username, badge_id):
        username = username.strip().lower()
        if username not in self.data:
            self.data[username] = []
        if badge_id in self.data[username]:
            return False
        self.data[username].append(badge_id)
        self.save()
        return True

    def is_unlocked(self, username, badge_id):
        return badge_id in self.data.get(username.strip().lower(), [])

    def get_unlocked(self, username):
        return self.data.get(username.strip().lower(), [])

    def check_and_unlock(self, username, stats, favorites_count):
        new_badges = []
        checks = [
            ("first_search", stats["total"] >= 1),
            ("ten_searches", stats["total"] >= 10),
            ("fifty_searches", stats["total"] >= 50),
            ("first_connection", stats["found"] >= 1),
            ("ten_connections", stats["found"] >= 10),
            ("five_favorites", favorites_count >= 5),
        ]
        for badge_id, condition in checks:
            if condition and self.unlock(username, badge_id):
                new_badges.append(badge_id)
        return new_badges


class ThemeManager:
    theme_name = "dark"

    @classmethod
    def set_theme(cls, name):
        cls.theme_name = name

    @classmethod
    def current(cls):
        if cls.theme_name == "dark":
            return COLORS_DARK
        return COLORS_LIGHT


class ToolTip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tipwindow = None
        self.after_id = None
        self.widget.bind("<Enter>", self.schedule, add="+")
        self.widget.bind("<Leave>", self.hide, add="+")
        self.widget.bind("<Destroy>", self.hide, add="+")

    def schedule(self, event=None):
        self.hide()
        try:
            self.after_id = self.widget.after(self.delay, self.showtip)
        except Exception:
            pass

    def hide(self, event=None):
        if self.after_id:
            try:
                self.widget.after_cancel(self.after_id)
            except Exception:
                pass
            self.after_id = None
        if self.tipwindow:
            try:
                self.tipwindow.destroy()
            except Exception:
                pass
            self.tipwindow = None

    def showtip(self):
        self.after_id = None
        if self.tipwindow or not self.text:
            return
        try:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
            self.tipwindow = tw = tk.Toplevel(self.widget)
            tw.wm_overrideredirect(True)
            tw.wm_geometry(f"+{x}+{y}")
            theme = ThemeManager.current()
            tk.Label(
                tw, text=self.text, justify=tk.RIGHT,
                background=theme["bg3"], foreground=theme["text"],
                relief=tk.SOLID, borderwidth=1,
                font=(FA_FONT, 9), padx=8, pady=4
            ).pack(ipadx=1)
        except Exception:
            self.tipwindow = None


class ScrollableFrame(tk.Frame):
    def __init__(self, parent, bg_color, **kwargs):
        super().__init__(parent, bg=bg_color, **kwargs)
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg=bg_color)

        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.window_id, width=e.width))

        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self.on_wheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))
        self.bind("<Destroy>", self.on_destroy)

    def on_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_destroy(self, event):
        if event.widget is self:
            try:
                self.canvas.unbind_all("<MouseWheel>")
            except Exception:
                pass


class PasswordStrengthMeter(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.theme = ThemeManager.current()
        self.bar = tk.Canvas(self, height=6, bg=self.theme["entry_bg"], highlightthickness=0)
        self.bar.pack(fill=tk.X, pady=(4, 0))
        self.label = tk.Label(
            self, text="", font=(FA_FONT, 8),
            bg=self.theme["card"], fg=self.theme["text_dim"]
        )
        self.label.pack(anchor="e")

    @staticmethod
    def calculate_score(password):
        score = 0
        if len(password) >= 4:
            score += 15
        if len(password) >= 8:
            score += 15
        if len(password) >= 12:
            score += 10
        if any(c.isupper() for c in password):
            score += 15
        if any(c.isdigit() for c in password):
            score += 15
        if any(c in string.punctuation for c in password):
            score += 20
        return min(score, 100)

    def update_strength(self, password):
        self.theme = ThemeManager.current()
        score = self.calculate_score(password)
        self.bar.delete("all")
        width = self.bar.winfo_width() or 200
        segments = 4
        seg_width = width / segments - 4
        colors = [self.theme["error"], self.theme["warning"], "#9bde7e", self.theme["success"]]
        filled = 0
        if score >= 20:
            filled = 1
        if score >= 40:
            filled = 2
        if score >= 60:
            filled = 3
        if score >= 80:
            filled = 4
        for i in range(segments):
            x1 = i * (seg_width + 4)
            color = colors[filled - 1] if i < filled else self.theme["entry_bg"]
            self.bar.create_rectangle(x1, 0, x1 + seg_width, 6, fill=color, outline="")
        if password:
            text = PersianText.STRENGTH_LABELS[filled] if filled > 0 else PersianText.STRENGTH_LABELS[0]
            color = colors[filled - 1] if filled > 0 else self.theme["error"]
            self.label.config(text=f"قدرت رمز: {text}", fg=color)
        else:
            self.label.config(text="")


class SplashScreen(tk.Toplevel):
    def __init__(self, parent, duration=2200):
        super().__init__(parent)
        theme = ThemeManager.current()
        self.overrideredirect(True)
        self.configure(bg=theme["bg"])
        w, h = 500, 340
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

        frame = tk.Frame(self, bg=theme["bg"])
        frame.place(relx=0.5, rely=0.48, anchor="center")

        tk.Label(frame, text="🎬", font=("Segoe UI", 40), bg=theme["bg"]).pack()
        tk.Label(
            frame, text=APP_NAME, font=(FA_FONT, 26, "bold"),
            bg=theme["bg"], fg=theme["accent"]
        ).pack(pady=4)
        tk.Label(
            frame, text="شش درجه جدایی", font=(FA_FONT, 12),
            bg=theme["bg"], fg=theme["text_dim"]
        ).pack()
        tk.Label(
            frame, text=FA_DEVELOPER, font=(FA_FONT, 11, "bold"),
            bg=theme["bg"], fg=theme["accent2"]
        ).pack(pady=8)
        tk.Label(
            frame, text=f"نسخه {to_persian_digits(APP_VERSION)}", font=(FA_FONT, 9),
            bg=theme["bg"], fg=theme["text_dim"]
        ).pack()

        progress = ttk.Progressbar(self, mode="indeterminate", length=280)
        progress.place(relx=0.5, rely=0.88, anchor="center")
        progress.start(20)

        self.after(duration, self.destroy)


class ToastNotification(tk.Toplevel):
    def __init__(self, parent, message, msg_type="success", duration=2500):
        try:
            super().__init__(parent)
            theme = ThemeManager.current()
            self.overrideredirect(True)
            self.attributes("-topmost", True)
            colors = {
                "info": theme["accent3"],
                "success": theme["success"],
                "warning": theme["warning"],
                "error": theme["error"]
            }
            bg = colors.get(msg_type, theme["accent3"])
            frame = tk.Frame(self, bg=bg, padx=20, pady=12)
            frame.pack()
            tk.Label(frame, text=message, font=(FA_FONT, 11), bg=bg, fg="white").pack()
            self.update_idletasks()
            w = self.winfo_reqwidth()
            h = self.winfo_reqheight()
            x = parent.winfo_x() + (parent.winfo_width() - w) // 2
            y = parent.winfo_y() + 70
            self.geometry(f"{w}x{h}+{x}+{y}")
            self.after(duration, self.destroy)
        except Exception:
            pass


class BaseCenteredWindow(tk.Tk):
    def center_window(self, w, h):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def center_toplevel(self, win, w, h):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")


class LoginWindow(BaseCenteredWindow):
    def __init__(self):
        super().__init__()
        self.theme = ThemeManager.current()
        self.current_user = None
        self.title(f"{APP_NAME} - ورود")
        self.geometry("480x680")
        self.resizable(False, False)
        self.configure(bg=self.theme["bg"])
        self.center_window(480, 680)
        self.container = tk.Frame(self, bg=self.theme["bg"])
        self.container.pack(fill=tk.BOTH, expand=True)
        self.show_login_frame()

        if APP_CONFIG.get("show_splash", True):
            self.withdraw()
            SplashScreen(self)
            self.after(2300, self.deiconify)

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login_frame(self):
        self.clear_container()
        theme = self.theme
        frame = tk.Frame(self.container, bg=theme["bg"])
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.86)

        tk.Label(frame, text="🎬", font=("Segoe UI", 40), bg=theme["bg"]).pack(pady=(0, 4))
        tk.Label(
            frame, text=APP_NAME, font=(FA_FONT, 24, "bold"),
            bg=theme["bg"], fg=theme["accent"]
        ).pack()
        tk.Label(
            frame, text=PersianText.LOGIN_SUBTITLE, font=(FA_FONT, 10),
            bg=theme["bg"], fg=theme["text_dim"]
        ).pack(pady=(0, 20))

        card = tk.Frame(
            frame, bg=theme["card"], padx=28, pady=22,
            highlightbackground=theme["border"], highlightthickness=1
        )
        card.pack(fill=tk.X)

        tk.Label(
            card, text=PersianText.USERNAME, font=(FA_FONT, 10),
            bg=theme["card"], fg=theme["text"], anchor="e"
        ).pack(fill=tk.X)
        self.login_username = tk.Entry(
            card, font=(FA_FONT, 12), bg=theme["entry_bg"],
            fg=theme["text"], insertbackground=theme["text"],
            relief=tk.FLAT, highlightthickness=1,
            highlightcolor=theme["accent"], highlightbackground=theme["border"],
            justify=tk.RIGHT
        )
        self.login_username.pack(fill=tk.X, ipady=6, pady=(5, 12))

        tk.Label(
            card, text=PersianText.PASSWORD, font=(FA_FONT, 10),
            bg=theme["card"], fg=theme["text"], anchor="e"
        ).pack(fill=tk.X)
        pass_frame = tk.Frame(card, bg=theme["card"])
        pass_frame.pack(fill=tk.X, pady=(5, 4))
        self.login_password = tk.Entry(
            pass_frame, font=(FA_FONT, 12), show="•",
            bg=theme["entry_bg"], fg=theme["text"],
            insertbackground=theme["text"], relief=tk.FLAT,
            highlightthickness=1, highlightcolor=theme["accent"],
            highlightbackground=theme["border"], justify=tk.RIGHT
        )
        self.login_password.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)

        self.show_pass_btn = tk.Button(
            pass_frame, text="👁", font=("Segoe UI", 11),
            bg=theme["entry_bg"], fg=theme["text_dim"],
            relief=tk.FLAT, cursor="hand2", width=3,
            command=self.toggle_password
        )
        self.show_pass_btn.pack(side=tk.LEFT, padx=(5, 0))

        self.login_password.bind("<Return>", lambda e: self.do_login())
        self.login_username.bind("<Return>", lambda e: self.login_password.focus())

        options = tk.Frame(card, bg=theme["card"])
        options.pack(fill=tk.X, pady=8)
        self.remember_var = tk.BooleanVar(value=APP_CONFIG.get("remember_me", False))
        tk.Checkbutton(
            options, text=PersianText.REMEMBER_ME, variable=self.remember_var,
            font=(FA_FONT, 9), bg=theme["card"], fg=theme["text_dim"],
            activebackground=theme["card"], activeforeground=theme["text"],
            selectcolor=theme["entry_bg"]
        ).pack(side=tk.RIGHT)
        tk.Button(
            options, text=PersianText.GUEST_MODE, font=(FA_FONT, 9, "underline"),
            bg=theme["card"], fg=theme["accent"], relief=tk.FLAT,
            cursor="hand2", command=self.guest_login
        ).pack(side=tk.LEFT)

        self.login_status = tk.Label(
            frame, text="", font=(FA_FONT, 9),
            bg=theme["bg"], fg=theme["error"]
        )
        self.login_status.pack(pady=5)

        login_btn = tk.Button(
            frame, text=PersianText.SIGN_IN, font=(FA_FONT, 13, "bold"),
            bg=theme["accent"], fg="white", relief=tk.FLAT,
            cursor="hand2", command=self.do_login
        )
        login_btn.pack(fill=tk.X, ipady=8, pady=(8, 6))
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg=theme["hover"]))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg=theme["accent"]))

        tk.Button(
            frame, text=PersianText.CREATE_ACCOUNT, font=(FA_FONT, 10),
            bg=theme["bg"], fg=theme["accent2"], relief=tk.FLAT,
            cursor="hand2", command=self.show_register_frame
        ).pack(fill=tk.X, ipady=4)

        tk.Label(
            frame, text=FA_DEVELOPER, font=(FA_FONT, 9, "bold"),
            bg=theme["bg"], fg=theme["accent2"]
        ).pack(pady=(14, 0))

        if APP_CONFIG.get("last_user") and APP_CONFIG.get("remember_me"):
            self.login_username.insert(0, APP_CONFIG.get("last_user"))

    def show_register_frame(self):
        self.clear_container()
        theme = self.theme
        frame = tk.Frame(self.container, bg=theme["bg"])
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.86)

        tk.Label(
            frame, text="ساخت حساب کاربری", font=(FA_FONT, 20, "bold"),
            bg=theme["bg"], fg=theme["accent"]
        ).pack(pady=(0, 16))

        card = tk.Frame(
            frame, bg=theme["card"], padx=28, pady=22,
            highlightbackground=theme["border"], highlightthickness=1
        )
        card.pack(fill=tk.X)

        tk.Label(
            card, text=f"{PersianText.USERNAME} *", font=(FA_FONT, 10),
            bg=theme["card"], fg=theme["text"], anchor="e"
        ).pack(fill=tk.X)
        self.reg_username = tk.Entry(
            card, font=(FA_FONT, 12), bg=theme["entry_bg"],
            fg=theme["text"], insertbackground=theme["text"],
            relief=tk.FLAT, highlightthickness=1,
            highlightcolor=theme["accent"], highlightbackground=theme["border"],
            justify=tk.RIGHT
        )
        self.reg_username.pack(fill=tk.X, ipady=6, pady=(5, 10))

        tk.Label(
            card, text=PersianText.EMAIL, font=(FA_FONT, 10),
            bg=theme["card"], fg=theme["text"], anchor="e"
        ).pack(fill=tk.X)
        self.reg_email = tk.Entry(
            card, font=(FA_FONT, 12), bg=theme["entry_bg"],
            fg=theme["text"], insertbackground=theme["text"],
            relief=tk.FLAT, highlightthickness=1,
            highlightcolor=theme["accent"], highlightbackground=theme["border"],
            justify=tk.RIGHT
        )
        self.reg_email.pack(fill=tk.X, ipady=6, pady=(5, 10))

        tk.Label(
            card, text=f"{PersianText.PASSWORD} *", font=(FA_FONT, 10),
            bg=theme["card"], fg=theme["text"], anchor="e"
        ).pack(fill=tk.X)
        self.reg_password = tk.Entry(
            card, font=(FA_FONT, 12), show="•",
            bg=theme["entry_bg"], fg=theme["text"],
            insertbackground=theme["text"], relief=tk.FLAT,
            highlightthickness=1, highlightcolor=theme["accent"],
            highlightbackground=theme["border"], justify=tk.RIGHT
        )
        self.reg_password.pack(fill=tk.X, ipady=6, pady=(5, 2))

        self.strength_meter = PasswordStrengthMeter(card)
        self.strength_meter.pack(fill=tk.X, pady=(0, 10))
        self.reg_password.bind(
            "<KeyRelease>",
            lambda e: self.strength_meter.update_strength(self.reg_password.get())
        )

        tk.Label(
            card, text=f"{PersianText.CONFIRM_PASSWORD} *", font=(FA_FONT, 10),
            bg=theme["card"], fg=theme["text"], anchor="e"
        ).pack(fill=tk.X)
        self.reg_confirm = tk.Entry(
            card, font=(FA_FONT, 12), show="•",
            bg=theme["entry_bg"], fg=theme["text"],
            insertbackground=theme["text"], relief=tk.FLAT,
            highlightthickness=1, highlightcolor=theme["accent"],
            highlightbackground=theme["border"], justify=tk.RIGHT
        )
        self.reg_confirm.pack(fill=tk.X, ipady=6, pady=(5, 10))
        self.reg_confirm.bind("<Return>", lambda e: self.do_register())

        self.reg_status = tk.Label(
            frame, text="", font=(FA_FONT, 9),
            bg=theme["bg"], fg=theme["error"]
        )
        self.reg_status.pack(pady=3)

        register_btn = tk.Button(
            frame, text="ساخت حساب", font=(FA_FONT, 13, "bold"),
            bg=theme["accent"], fg="white", relief=tk.FLAT,
            cursor="hand2", command=self.do_register
        )
        register_btn.pack(fill=tk.X, ipady=8, pady=(6, 5))
        register_btn.bind("<Enter>", lambda e: register_btn.config(bg=theme["hover"]))
        register_btn.bind("<Leave>", lambda e: register_btn.config(bg=theme["accent"]))

        tk.Button(
            frame, text=PersianText.BACK_TO_LOGIN, font=(FA_FONT, 10),
            bg=theme["bg"], fg=theme["accent2"], relief=tk.FLAT,
            cursor="hand2", command=self.show_login_frame
        ).pack(fill=tk.X, ipady=4)

    def toggle_password(self):
        if self.login_password.cget("show") == "•":
            self.login_password.config(show="")
            self.show_pass_btn.config(fg=self.theme["accent"])
        else:
            self.login_password.config(show="•")
            self.show_pass_btn.config(fg=self.theme["text_dim"])

    def do_login(self):
        username = self.login_username.get().strip()
        password = self.login_password.get()
        if not username or not password:
            self.login_status.config(text=PersianText.FILL_ALL_FIELDS, fg=self.theme["error"])
            return
        success, message = USER_DATABASE.login(username, password)
        if success:
            APP_CONFIG.set("last_user", username.lower())
            APP_CONFIG.set("remember_me", self.remember_var.get())
            self.current_user = username.lower()
            self.open_main_app()
        else:
            self.login_status.config(text=message, fg=self.theme["error"])
            self.login_password.delete(0, tk.END)

    def guest_login(self):
        self.current_user = "مهمان"
        self.open_main_app()

    def do_register(self):
        username = self.reg_username.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get()
        confirm = self.reg_confirm.get()
        if not username or not password:
            self.reg_status.config(text=PersianText.FILL_ALL_FIELDS, fg=self.theme["error"])
            return
        if password != confirm:
            self.reg_status.config(text=PersianText.PASSWORDS_NOT_MATCH, fg=self.theme["error"])
            self.reg_confirm.delete(0, tk.END)
            return
        success, message = USER_DATABASE.register(username, password, email)
        if success:
            self.reg_status.config(text="حساب ساخته شد! در حال انتقال...", fg=self.theme["success"])
            self.after(1200, self.show_login_frame)
        else:
            self.reg_status.config(text=message, fg=self.theme["error"])

    def open_main_app(self):
        self.destroy()
        app = DataLoaderWindow(self.current_user)
        app.mainloop()


class DataLoaderWindow(BaseCenteredWindow):
    def __init__(self, username):
        super().__init__()
        self.theme = ThemeManager.current()
        self.username = username
        self.title(f"{APP_NAME} - بارگذاری داده‌ها")
        self.geometry("580x430")
        self.resizable(False, False)
        self.configure(bg=self.theme["bg"])
        self.center_window(580, 430)
        self.build_ui()
        self.after(400, self.auto_load)

    def build_ui(self):
        theme = self.theme
        header = tk.Frame(self, bg=theme["bg"])
        header.pack(pady=(28, 8))

        tk.Label(header, text="📂", font=("Segoe UI", 34), bg=theme["bg"]).pack()
        tk.Label(
            header, text="منبع داده‌ها", font=(FA_FONT, 17, "bold"),
            bg=theme["bg"], fg=theme["text"]
        ).pack(pady=4)
        tk.Label(
            header,
            text="پوشه حاوی فایل‌های people.csv و movies.csv و stars.csv را انتخاب کنید",
            font=(FA_FONT, 9), bg=theme["bg"], fg=theme["text_dim"], wraplength=460
        ).pack()

        dir_frame = tk.Frame(self, bg=theme["card"], padx=15, pady=15)
        dir_frame.pack(fill=tk.X, padx=30, pady=14)

        self.dir_var = tk.StringVar(value=APP_CONFIG.get("data_directory", "large"))
        tk.Entry(
            dir_frame, textvariable=self.dir_var, font=(FA_FONT, 10),
            bg=theme["entry_bg"], fg=theme["text"], relief=tk.FLAT,
            highlightthickness=1, highlightcolor=theme["accent"],
            highlightbackground=theme["border"]
        ).pack(side=tk.RIGHT, fill=tk.X, expand=True, ipady=5)

        tk.Button(
            dir_frame, text="انتخاب پوشه", font=(FA_FONT, 10),
            bg=theme["accent2"], fg="white", relief=tk.FLAT,
            cursor="hand2", padx=14, command=self.browse_folder
        ).pack(side=tk.LEFT, padx=(10, 0))

        self.status_label = tk.Label(
            self, text="در انتظار...", font=(FA_FONT, 10),
            bg=theme["bg"], fg=theme["text_dim"]
        )
        self.status_label.pack(pady=8)

        self.progress = ttk.Progressbar(self, mode="determinate", length=480)
        self.progress.pack(pady=4)

        self.load_btn = tk.Button(
            self, text="بارگذاری داده‌ها", font=(FA_FONT, 12, "bold"),
            bg=theme["accent"], fg="white", relief=tk.FLAT,
            cursor="hand2", command=self.manual_load
        )
        self.load_btn.pack(ipady=6, padx=30, fill=tk.X, pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory(title="انتخاب پوشه داده‌های IMDB")
        if folder:
            self.dir_var.set(folder)

    def manual_load(self):
        self.start_loading(self.dir_var.get())

    def auto_load(self):
        directory = self.dir_var.get().strip()
        if directory and os.path.isdir(directory):
            missing = [f for f in DATA_FILES if not os.path.exists(os.path.join(directory, f))]
            if not missing:
                self.start_loading(directory)

    def start_loading(self, directory):
        directory = directory.strip()
        if not directory:
            self.status_label.config(text="لطفاً ابتدا پوشه داده‌ها را انتخاب کنید", fg=self.theme["warning"])
            return
        if not os.path.isdir(directory):
            self.status_label.config(text="پوشه پیدا نشد", fg=self.theme["error"])
            return
        missing = [f for f in DATA_FILES if not os.path.exists(os.path.join(directory, f))]
        if missing:
            self.status_label.config(
                text=f"{PersianText.MISSING_FILES}: {', '.join(missing)}",
                fg=self.theme["error"]
            )
            return

        APP_CONFIG.set("data_directory", directory)
        self.load_btn.config(state=tk.DISABLED)
        self.status_label.config(text="در حال بارگذاری داده‌ها...", fg=self.theme["text"])
        self.progress.config(mode="indeterminate")
        self.progress.start(30)
        self.after(100, lambda: self.do_load(directory))

    def do_load(self, directory):
        try:
            start = time.time()
            load_data(directory)
            elapsed = time.time() - start
            self.progress.stop()
            self.progress.config(mode="determinate", value=100)
            self.status_label.config(
                text=f"داده‌ها بارگذاری شد ({elapsed:.1f} ثانیه)",
                fg=self.theme["success"]
            )
            self.after(700, self.open_main)
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text=f"خطا در بارگذاری: {e}", fg=self.theme["error"])
            self.load_btn.config(state=tk.NORMAL)

    def open_main(self):
        self.destroy()
        app = MainWindow(self.username)
        app.mainloop()


class MainWindow(BaseCenteredWindow):
    def __init__(self, username):
        super().__init__()
        self.theme = ThemeManager.current()
        self.username = username
        self.searching = False
        self.suggestion_listbox = None

        w = APP_CONFIG.get("window_width", 1300)
        h = APP_CONFIG.get("window_height", 800)
        self.geometry(f"{w}x{h}")
        self.minsize(1000, 700)
        self.configure(bg=self.theme["bg"])
        self.title(f"{APP_NAME} - {username}")

        self.build_statusbar()
        self.build_header()
        self.build_main()
        self.bind_shortcuts()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def build_statusbar(self):
        theme = self.theme
        self.statusbar = tk.Frame(self, bg=theme["bg2"], height=28)
        self.statusbar.pack(fill=tk.X, side=tk.BOTTOM)
        self.statusbar.pack_propagate(False)

        self.status_label = tk.Label(
            self.statusbar, text=PersianText.READY, font=(FA_FONT, 9),
            bg=theme["bg2"], fg=theme["text_dim"]
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)

        if degrees.people:
            tk.Label(
                self.statusbar,
                text=f"👥 {to_persian_digits(format_number(len(degrees.people)))} نفر  |  🎬 {to_persian_digits(format_number(len(degrees.movies)))} فیلم",
                font=(FA_FONT, 9), bg=theme["bg2"], fg=theme["text_dim"]
            ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            self.statusbar, text=FA_COPYRIGHT, font=(FA_FONT, 8),
            bg=theme["bg2"], fg=theme["accent2"]
        ).pack(side=tk.LEFT, padx=10)

    def build_header(self):
        theme = self.theme
        header = tk.Frame(self, bg=theme["bg2"], height=58)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        logo_frame = tk.Frame(header, bg=theme["bg2"])
        logo_frame.pack(side=tk.RIGHT, padx=20)
        tk.Label(logo_frame, text="🎬", font=("Segoe UI", 18), bg=theme["bg2"]).pack(side=tk.RIGHT)
        tk.Label(
            logo_frame, text=APP_NAME, font=(FA_FONT, 15, "bold"),
            bg=theme["bg2"], fg=theme["accent"]
        ).pack(side=tk.RIGHT, padx=8)

        self.connection_label = tk.Label(
            header, text="", font=(FA_FONT, 10),
            bg=theme["bg2"], fg=theme["text_dim"]
        )
        self.connection_label.pack(side=tk.RIGHT, padx=15)

        controls = tk.Frame(header, bg=theme["bg2"])
        controls.pack(side=tk.LEFT, padx=15)

        tk.Label(
            controls, text=f"👤 {self.username}", font=(FA_FONT, 10),
            bg=theme["bg2"], fg=theme["text"]
        ).pack(side=tk.RIGHT, padx=5)

        theme_btn = tk.Button(
            controls, text="🌓", font=("Segoe UI", 12),
            bg=theme["bg2"], fg=theme["text"],
            relief=tk.FLAT, cursor="hand2", command=self.toggle_theme
        )
        theme_btn.pack(side=tk.RIGHT, padx=5)
        ToolTip(theme_btn, "تغییر تم")

        tk.Button(
            controls, text=PersianText.LOGOUT, font=(FA_FONT, 9),
            bg=theme["bg2"], fg=theme["accent"], relief=tk.FLAT,
            cursor="hand2", command=self.logout
        ).pack(side=tk.RIGHT, padx=5)

    def build_main(self):
        theme = self.theme
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TNotebook", background=theme["bg"], borderwidth=0)
        self.style.configure(
            "TNotebook.Tab", background=theme["bg2"],
            foreground=theme["text"], padding=[16, 7],
            font=(FA_FONT, 10)
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", theme["accent"])],
            foreground=[("selected", "white")]
        )

        self.search_tab = ttk.Frame(self.notebook)
        self.history_tab = ttk.Frame(self.notebook)
        self.favorites_tab = ttk.Frame(self.notebook)
        self.stats_tab = ttk.Frame(self.notebook)
        self.browse_tab = ttk.Frame(self.notebook)
        self.badges_tab = ttk.Frame(self.notebook)
        self.quiz_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.about_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.search_tab, text=f"  {PersianText.SEARCH_TAB}  ")
        self.notebook.add(self.history_tab, text=f"  {PersianText.HISTORY_TAB}  ")
        self.notebook.add(self.favorites_tab, text=f"  {PersianText.FAVORITES_TAB}  ")
        self.notebook.add(self.stats_tab, text=f"  {PersianText.STATS_TAB}  ")
        self.notebook.add(self.browse_tab, text=f"  {PersianText.BROWSE_TAB}  ")
        self.notebook.add(self.badges_tab, text=f"  {PersianText.BADGES_TAB}  ")
        self.notebook.add(self.quiz_tab, text=f"  {PersianText.QUIZ_TAB}  ")
        self.notebook.add(self.settings_tab, text=f"  {PersianText.SETTINGS_TAB}  ")
        self.notebook.add(self.about_tab, text=f"  {PersianText.ABOUT_TAB}  ")

        self.build_search_tab()
        self.build_history_tab()
        self.build_favorites_tab()
        self.build_stats_tab()
        self.build_browse_tab()
        self.build_badges_tab()
        self.build_quiz_tab()
        self.build_settings_tab()
        self.build_about_tab()

    def build_search_tab(self):
        theme = self.theme
        container = tk.Frame(self.search_tab, bg=theme["bg"])
        container.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(
            container, bg=theme["card"], padx=20, pady=18,
            highlightbackground=theme["border"], highlightthickness=1
        )
        card.pack(fill=tk.X, padx=20, pady=(15, 10))

        inputs = tk.Frame(card, bg=theme["card"])
        inputs.pack(fill=tk.X)

        right_col = tk.Frame(inputs, bg=theme["card"])
        right_col.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(8, 0))

        tk.Label(
            right_col, text=PersianText.SOURCE_ACTOR, font=(FA_FONT, 10, "bold"),
            bg=theme["card"], fg=theme["text"], anchor="e"
        ).pack(fill=tk.X)
        self.source_var = tk.StringVar()
        self.source_entry = tk.Entry(
            right_col, textvariable=self.source_var, font=(FA_FONT, 12),
            bg=theme["entry_bg"], fg=theme["text"],
            insertbackground=theme["text"], relief=tk.FLAT,
            highlightthickness=1, highlightcolor=theme["accent"],
            highlightbackground=theme["border"], justify=tk.RIGHT
        )
        self.source_entry.pack(fill=tk.X, ipady=7, pady=(4, 0))
        self.source_entry.bind("<KeyRelease>", self.on_source_type)

        tk.Label(
            inputs, text="⬅", font=("Segoe UI", 16),
            bg=theme["card"], fg=theme["accent"]
        ).pack(side=tk.RIGHT, padx=8)

        left_col = tk.Frame(inputs, bg=theme["card"])
        left_col.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 8))

        tk.Label(
            left_col, text=PersianText.TARGET_ACTOR, font=(FA_FONT, 10, "bold"),
            bg=theme["card"], fg=theme["text"], anchor="e"
        ).pack(fill=tk.X)
        self.target_var = tk.StringVar()
        self.target_entry = tk.Entry(
            left_col, textvariable=self.target_var, font=(FA_FONT, 12),
            bg=theme["entry_bg"], fg=theme["text"],
            insertbackground=theme["text"], relief=tk.FLAT,
            highlightthickness=1, highlightcolor=theme["accent"],
            highlightbackground=theme["border"], justify=tk.RIGHT
        )
        self.target_entry.pack(fill=tk.X, ipady=7, pady=(4, 0))
        self.target_entry.bind("<KeyRelease>", self.on_target_type)

        btn_frame = tk.Frame(card, bg=theme["card"])
        btn_frame.pack(fill=tk.X, pady=(14, 0))

        self.search_btn = tk.Button(
            btn_frame, text=f"🔍 {PersianText.FIND_CONNECTION}",
            font=(FA_FONT, 12, "bold"),
            bg=theme["accent"], fg="white", relief=tk.FLAT,
            cursor="hand2", command=self.do_search
        )
        self.search_btn.pack(side=tk.RIGHT, ipady=7, padx=(10, 0), fill=tk.X, expand=True)
        self.search_btn.bind("<Enter>", lambda e: self.search_btn.config(bg=theme["hover"]))
        self.search_btn.bind("<Leave>", lambda e: self.search_btn.config(bg=theme["accent"]))

        swap_btn = tk.Button(
            btn_frame, text=f"🔄 {PersianText.SWAP}", font=(FA_FONT, 10),
            bg=theme["accent2"], fg="white", relief=tk.FLAT,
            cursor="hand2", padx=16, command=self.swap_actors
        )
        swap_btn.pack(side=tk.RIGHT, ipady=7)
        ToolTip(swap_btn, "جابجایی مبدأ و مقصد")

        random_btn = tk.Button(
            btn_frame, text=f"🎲 {PersianText.RANDOM}", font=(FA_FONT, 10),
            bg=theme["bg3"], fg="white", relief=tk.FLAT,
            cursor="hand2", padx=16, command=self.random_actors
        )
        random_btn.pack(side=tk.RIGHT, padx=(0, 10), ipady=7)
        ToolTip(random_btn, "انتخاب دو بازیگر تصادفی پرکاربرد")

        self.results_container = tk.Frame(container, bg=theme["bg"])
        self.results_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(8, 14))

        self.build_empty_result()

    def build_empty_result(self):
        for widget in self.results_container.winfo_children():
            widget.destroy()
        theme = self.theme

        empty = tk.Frame(
            self.results_container, bg=theme["card"],
            highlightbackground=theme["border"], highlightthickness=1
        )
        empty.pack(fill=tk.BOTH, expand=True)

        center = tk.Frame(empty, bg=theme["card"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="🔗", font=("Segoe UI", 46), bg=theme["card"]).pack()
        tk.Label(
            center, text="نام دو بازیگر را وارد کنید تا کوتاه‌ترین ارتباط پیدا شود",
            font=(FA_FONT, 12), bg=theme["card"], fg=theme["text_dim"]
        ).pack(pady=6)
        tk.Label(
            center, text="راهنما: Ctrl+Enter برای جستجو",
            font=(FA_FONT, 9), bg=theme["card"], fg=theme["text_dim"]
        ).pack()

    def build_result_view(self, source_name, target_name, path, num_explored, runtime):
        for widget in self.results_container.winfo_children():
            widget.destroy()
        theme = self.theme

        if path is None:
            not_found = tk.Frame(
                self.results_container, bg=theme["card"],
                highlightbackground=theme["border"], highlightthickness=1
            )
            not_found.pack(fill=tk.BOTH, expand=True)
            center = tk.Frame(not_found, bg=theme["card"])
            center.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(center, text="❌", font=("Segoe UI", 46), bg=theme["card"]).pack()
            tk.Label(
                center,
                text=f"هیچ ارتباطی بین\n{source_name} و {target_name} پیدا نشد",
                font=(FA_FONT, 13), bg=theme["card"],
                fg=theme["error"], justify=tk.CENTER
            ).pack(pady=8)
            tk.Label(
                center,
                text=f"{to_persian_digits(format_number(num_explored))} گره بررسی شد در {runtime:.2f} ثانیه",
                font=(FA_FONT, 9), bg=theme["card"], fg=theme["text_dim"]
            ).pack()
            return

        deg = len(path)
        header_frame = tk.Frame(self.results_container, bg=theme["success"], padx=14, pady=9)
        header_frame.pack(fill=tk.X)
        tk.Label(
            header_frame,
            text=f"✅ ارتباط پیدا شد! {source_name} و {target_name} — {to_persian_digits(deg)} درجه فاصله",
            font=(FA_FONT, 13, "bold"), bg=theme["success"], fg="white"
        ).pack()
        tk.Label(
            header_frame,
            text=f"{to_persian_digits(format_number(num_explored))} گره بررسی شد  •  زمان: {runtime:.2f} ثانیه",
            font=(FA_FONT, 9), bg=theme["success"], fg="#eafff7"
        ).pack()

        main_frame = tk.Frame(self.results_container, bg=theme["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True)

        path_panel = tk.Frame(
            main_frame, bg=theme["card"],
            highlightbackground=theme["border"], highlightthickness=1
        )
        path_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 8))

        scroll = ScrollableFrame(path_panel, theme["card"])
        scroll.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.render_path(scroll.inner, source_name, path)

        sidebar = tk.Frame(
            main_frame, bg=theme["card"], width=270,
            highlightbackground=theme["border"], highlightthickness=1
        )
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 0))
        sidebar.pack_propagate(False)
        self.build_result_sidebar(sidebar, source_name, target_name, path, deg)

    def render_path(self, parent, source_name, path):
        theme = self.theme
        tk.Label(
            parent, text=PersianText.CONNECTION_PATH,
            font=(FA_FONT, 11, "bold"),
            bg=theme["card"], fg=theme["accent"], anchor="e"
        ).pack(fill=tk.X, padx=14, pady=(12, 4))

        start_info = self.person_info_by_name(source_name)
        display_name = start_info["name"] if start_info else source_name

        start_card = tk.Frame(parent, bg=theme["bg3"], padx=12, pady=9)
        start_card.pack(fill=tk.X, padx=14, pady=4)
        tk.Label(start_card, text="🟢", font=("Segoe UI", 12), bg=theme["bg3"]).pack(side=tk.RIGHT, padx=(6, 0))
        tk.Label(
            start_card, text=display_name, font=(FA_FONT, 12, "bold"),
            bg=theme["bg3"], fg="white"
        ).pack(side=tk.RIGHT)
        if start_info and start_info["birth"]:
            tk.Label(
                start_card, text=f"({to_persian_digits(start_info['birth'])})",
                font=(FA_FONT, 9), bg=theme["bg3"], fg="#ccccdd"
            ).pack(side=tk.RIGHT, padx=(0, 5))

        full_path = [(None, self.person_id_by_name(source_name))] + list(path)

        for i in range(len(full_path) - 1):
            person1_id = full_path[i][1]
            movie_id = full_path[i + 1][0]
            person2_id = full_path[i + 1][1]

            connector = tk.Frame(parent, bg=theme["card"])
            connector.pack(fill=tk.X, padx=14)
            line_frame = tk.Frame(connector, bg=theme["card"])
            line_frame.pack(anchor="e", padx=18)
            tk.Frame(line_frame, bg=theme["accent"], width=2, height=16).pack(side=tk.RIGHT)
            tk.Label(
                line_frame, text="▼", font=("Segoe UI", 8),
                bg=theme["card"], fg=theme["accent"]
            ).pack(side=tk.RIGHT)

            movie = degrees.movies.get(movie_id)
            person1 = degrees.people.get(person1_id, {})
            person2 = degrees.people.get(person2_id, {})

            movie_card = tk.Frame(parent, bg=theme["entry_bg"], padx=12, pady=6)
            movie_card.pack(fill=tk.X, padx=28, pady=2)
            tk.Label(movie_card, text="🎥", font=("Segoe UI", 10), bg=theme["entry_bg"]).pack(side=tk.RIGHT, padx=(5, 0))
            if movie:
                movie_label = tk.Label(
                    movie_card,
                    text=f"{person1.get('name', '')} و {person2.get('name', '')} در «{movie['title']} ({to_persian_digits(movie['year'])})»",
                    font=(FA_FONT, 10), bg=theme["entry_bg"],
                    fg=theme["warning"], cursor="hand2", wraplength=520, justify=tk.RIGHT
                )
                movie_label.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                movie_label.bind("<Double-1>", lambda e, mid=movie_id: self.show_movie_details(mid))
                ToolTip(movie_label, "دوبار کلیک: جزئیات فیلم")

            person_card = tk.Frame(parent, bg=theme["bg3"], padx=12, pady=9)
            person_card.pack(fill=tk.X, padx=14, pady=3)
            tk.Label(person_card, text="🟣", font=("Segoe UI", 12), bg=theme["bg3"]).pack(side=tk.RIGHT, padx=(6, 0))
            name_label = tk.Label(
                person_card,
                text=person2.get("name", "ناشناس"),
                font=(FA_FONT, 12, "bold"), bg=theme["bg3"], fg="white", cursor="hand2"
            )
            name_label.pack(side=tk.RIGHT)
            name_label.bind("<Double-1>", lambda e, pid=person2_id: self.show_person_details(pid))
            ToolTip(name_label, "دوبار کلیک: اطلاعات بازیگر")
            if person2.get("birth"):
                tk.Label(
                    person_card, text=f"({to_persian_digits(person2['birth'])})",
                    font=(FA_FONT, 9), bg=theme["bg3"], fg="#ccccdd"
                ).pack(side=tk.RIGHT, padx=(0, 5))

            tk.Label(
                person_card, text=f"#{to_persian_digits(i + 1)}",
                font=(FA_FONT, 9, "bold"), bg=theme["bg3"], fg=theme["accent"]
            ).pack(side=tk.LEFT)

            fav_icon = "⭐" if FAVORITES_MANAGER.is_favorite(self.username, person2_id) else "☆"
            tk.Button(
                person_card, text=fav_icon, font=("Segoe UI", 10),
                bg=theme["bg3"], fg=theme["warning"], relief=tk.FLAT,
                cursor="hand2",
                command=lambda pid=person2_id, pinfo=person2: self.toggle_favorite(pid, pinfo)
            ).pack(side=tk.LEFT, padx=5)

    def build_result_sidebar(self, parent, source_name, target_name, path, deg):
        theme = self.theme
        tk.Label(
            parent, text=PersianText.SUMMARY, font=(FA_FONT, 11, "bold"),
            bg=theme["card"], fg=theme["accent"], anchor="e"
        ).pack(fill=tk.X, padx=14, pady=(14, 4))

        for label, value in [
            (PersianText.DEGREES_APART, to_persian_digits(deg)),
            (PersianText.MOVIES_IN_PATH, to_persian_digits(len(path))),
            (PersianText.PEOPLE_IN_PATH, to_persian_digits(len(path) + 1)),
        ]:
            row = tk.Frame(parent, bg=theme["card"])
            row.pack(fill=tk.X, padx=14, pady=2)
            tk.Label(
                row, text=label, font=(FA_FONT, 9),
                bg=theme["card"], fg=theme["text_dim"]
            ).pack(side=tk.RIGHT)
            tk.Label(
                row, text=value, font=(FA_FONT, 10, "bold"),
                bg=theme["card"], fg=theme["text"]
            ).pack(side=tk.LEFT)

        tk.Frame(parent, bg=theme["border"], height=1).pack(fill=tk.X, padx=14, pady=10)

        tk.Label(
            parent, text="خروجی گرفتن", font=(FA_FONT, 11, "bold"),
            bg=theme["card"], fg=theme["accent"], anchor="e"
        ).pack(fill=tk.X, padx=14, pady=(0, 4))

        tk.Button(
            parent, text=f"📄 {PersianText.EXPORT_TXT}", font=(FA_FONT, 10),
            bg=theme["bg3"], fg="white", relief=tk.FLAT, cursor="hand2",
            command=lambda: self.export_result(source_name, target_name, path, deg, "txt")
        ).pack(fill=tk.X, padx=14, pady=3, ipady=5)

        tk.Button(
            parent, text=f"📋 {PersianText.EXPORT_JSON}", font=(FA_FONT, 10),
            bg=theme["bg3"], fg="white", relief=tk.FLAT, cursor="hand2",
            command=lambda: self.export_result(source_name, target_name, path, deg, "json")
        ).pack(fill=tk.X, padx=14, pady=3, ipady=5)

        tk.Frame(parent, bg=theme["border"], height=1).pack(fill=tk.X, padx=14, pady=10)

        tk.Label(
            parent, text=PersianText.QUICK_ACTIONS, font=(FA_FONT, 11, "bold"),
            bg=theme["card"], fg=theme["accent"], anchor="e"
        ).pack(fill=tk.X, padx=14, pady=(0, 4))

        source_info = self.person_info_by_name(source_name)
        if source_info:
            fav_text = f"★ {PersianText.REMOVE_FAVORITE}" if FAVORITES_MANAGER.is_favorite(self.username, source_info["id"]) else f"☆ {PersianText.ADD_FAVORITE}"
            tk.Button(
                parent, text=fav_text, font=(FA_FONT, 10),
                bg=theme["entry_bg"], fg=theme["warning"], relief=tk.FLAT,
                cursor="hand2",
                command=lambda: self.toggle_favorite(source_info["id"], degrees.people.get(source_info["id"], {}))
            ).pack(fill=tk.X, padx=14, pady=3, ipady=5)

        tk.Button(
            parent, text=f"🔍 {PersianText.SHOW_DETAILS}", font=(FA_FONT, 10),
            bg=theme["entry_bg"], fg=theme["text"], relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.show_result_details(source_name, target_name, path, deg)
        ).pack(fill=tk.X, padx=14, pady=3, ipady=5)

    def person_id_by_name(self, name):
        ids = list(degrees.names.get(name.strip().lower(), set()))
        if not ids:
            return None
        return max(ids, key=lambda pid: len(degrees.people[pid]["movies"]) if pid in degrees.people else 0)

    def person_info_by_name(self, name):
        pid = self.person_id_by_name(name)
        if pid and pid in degrees.people:
            return {"id": pid, **degrees.people[pid]}
        return None

    def on_source_type(self, event=None):
        if event and event.keysym in ("Return", "Escape", "Tab", "Up", "Down"):
            return
        if APP_CONFIG.get("auto_search_names", True):
            self.show_suggestions(self.source_var, self.source_entry)

    def on_target_type(self, event=None):
        if event and event.keysym in ("Return", "Escape", "Tab", "Up", "Down"):
            return
        if APP_CONFIG.get("auto_search_names", True):
            self.show_suggestions(self.target_var, self.target_entry)

    def show_suggestions(self, text_var, entry_widget):
        self.hide_suggestions()
        query = text_var.get().strip().lower()
        if len(query) < 2:
            return

        exact = []
        starts = []
        contains = []
        for name_key in degrees.names:
            if name_key == query:
                exact.append(name_key)
            elif name_key.startswith(query):
                starts.append(name_key)
            elif query in name_key:
                contains.append(name_key)
        results = (exact + starts + contains)[:8]
        if not results:
            return

        theme = self.theme
        top = entry_widget.winfo_toplevel()
        self.suggestion_listbox = tk.Listbox(
            top, font=(FA_FONT, 10),
            bg=theme["entry_bg"], fg=theme["text"],
            relief=tk.FLAT, highlightthickness=1,
            highlightcolor=theme["accent"],
            selectbackground=theme["accent"], selectforeground="white"
        )
        for name_key in results:
            self.suggestion_listbox.insert(tk.END, name_key.title())

        x = entry_widget.winfo_rootx() - top.winfo_rootx()
        y = entry_widget.winfo_rooty() - top.winfo_rooty() + entry_widget.winfo_height()
        self.suggestion_listbox.place(x=x, y=y, width=entry_widget.winfo_width())

        def on_select(event=None):
            selection = self.suggestion_listbox.curselection()
            if selection:
                text_var.set(self.suggestion_listbox.get(selection[0]))
                self.hide_suggestions()
                entry_widget.focus_set()

        self.suggestion_listbox.bind("<ButtonRelease-1>", on_select)
        self.suggestion_listbox.bind("<Return>", on_select)
        self.suggestion_listbox.bind("<Double-Button-1>", on_select)
        self.suggestion_listbox.bind("<Escape>", lambda e: self.hide_suggestions())
        self.suggestion_listbox.bind("<FocusOut>", lambda e: self.after(150, self.hide_suggestions))

    def hide_suggestions(self):
        if self.suggestion_listbox:
            try:
                self.suggestion_listbox.destroy()
            except Exception:
                pass
            self.suggestion_listbox = None

    def swap_actors(self):
        s = self.source_var.get()
        t = self.target_var.get()
        self.source_var.set(t)
        self.target_var.set(s)

    def random_actors(self):
        popular = sorted(
            degrees.people.items(),
            key=lambda x: len(x[1]["movies"]),
            reverse=True
        )[:300]
        if len(popular) < 2:
            return
        (id1, p1), (id2, p2) = random.sample(popular, 2)
        self.source_var.set(p1["name"])
        self.target_var.set(p2["name"])
        self.set_status(f"تصادفی: {p1['name']} ← {p2['name']}")

    def do_search(self):
        if self.searching:
            return
        self.hide_suggestions()

        source_name = self.source_var.get().strip()
        target_name = self.target_var.get().strip()

        if not source_name or not target_name:
            messagebox.showwarning("هشدار", PersianText.ENTER_BOTH_ACTORS)
            return
        if source_name.lower() == target_name.lower():
            messagebox.showinfo(
                "اطلاعات",
                "لطفاً دو بازیگر متفاوت وارد کنید.\nهر فرد ۰ درجه از خودش فاصله دارد!"
            )
            return

        source_id = self.person_id_by_name(source_name)
        target_id = self.person_id_by_name(target_name)

        if source_id is None:
            messagebox.showerror(PersianText.NOT_FOUND, f"بازیگر '{source_name}' در پایگاه داده پیدا نشد.")
            return
        if target_id is None:
            messagebox.showerror(PersianText.NOT_FOUND, f"بازیگر '{target_name}' در پایگاه داده پیدا نشد.")
            return

        self.searching = True
        self.search_btn.config(state=tk.DISABLED, text="⏳ در حال جستجو...")
        self.set_status("در حال جستجوی کوتاه‌ترین مسیر...")
        self.after(50, lambda: self.run_search(source_id, target_id))

    def run_search(self, source_id, target_id):
        start = time.time()
        path = None
        try:
            path = shortest_path(source_id, target_id)
        except Exception as e:
            messagebox.showerror("خطا", f"جستجو ناموفق بود: {e}")

        runtime = time.time() - start
        source_display = degrees.people[source_id]["name"]
        target_display = degrees.people[target_id]["name"]

        self.build_result_view(source_display, target_display, path, 0, runtime)

        if path is not None:
            deg = len(path)
            self.connection_label.config(
                text=f"🔗 {to_persian_digits(deg)} درجه: {source_display} ← {target_display}",
                fg=self.theme["success"]
            )
            HISTORY_MANAGER.add_entry(self.username, source_display, target_display, True, deg, runtime)
            if deg == 1:
                BADGE_MANAGER.unlock(self.username, "one_degree")
            if deg == 2:
                BADGE_MANAGER.unlock(self.username, "two_degrees")
            if deg == 6:
                BADGE_MANAGER.unlock(self.username, "six_degrees")
            self.set_status(f"ارتباط در {runtime:.2f} ثانیه پیدا شد")
        else:
            self.connection_label.config(
                text=f"❌ بدون ارتباط: {source_display} ← {target_display}",
                fg=self.theme["error"]
            )
            HISTORY_MANAGER.add_entry(self.username, source_display, target_display, False, -1, runtime)
            self.set_status("هیچ ارتباطی وجود ندارد")

        stats = HISTORY_MANAGER.get_stats(self.username)
        new_badges = BADGE_MANAGER.check_and_unlock(
            self.username, stats, len(FAVORITES_MANAGER.get_favorites(self.username))
        )
        if new_badges:
            names = [b["name"] for b in BadgeManager.BADGES if b["id"] in new_badges]
            ToastNotification(self, f"🏅 نشان جدید: {'، '.join(names)}", "success")
        self.build_history_tab()
        self.build_badges_tab()

        self.searching = False
        self.search_btn.config(state=tk.NORMAL, text=f"🔍 {PersianText.FIND_CONNECTION}")

    def toggle_favorite(self, person_id, person_info):
        if not person_id or not person_info:
            return
        if FAVORITES_MANAGER.is_favorite(self.username, person_id):
            FAVORITES_MANAGER.remove(self.username, person_id)
            self.set_status(f"{person_info.get('name', '')} از علاقه‌مندی‌ها حذف شد")
        else:
            FAVORITES_MANAGER.add(self.username, person_id, person_info.get("name", ""))
            self.set_status(f"{person_info.get('name', '')} به علاقه‌مندی‌ها اضافه شد")
            BADGE_MANAGER.check_and_unlock(
                self.username,
                HISTORY_MANAGER.get_stats(self.username),
                len(FAVORITES_MANAGER.get_favorites(self.username))
            )
        self.build_favorites_tab()
        self.build_badges_tab()

    def export_result(self, source_name, target_name, path, deg, fmt):
        if path is None:
            messagebox.showwarning("هشدار", "نتیجه‌ای برای خروجی گرفتن وجود ندارد")
            return

        if fmt == "txt":
            filepath = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("فایل متنی", "*.txt")],
                title="ذخیره نتیجه"
            )
            if not filepath:
                return
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(f"{APP_NAME} - گزارش ارتباط\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"سازنده: {APP_DEVELOPER}\n")
                    f.write("-" * 50 + "\n\n")
                    f.write(f"مبدأ: {source_name}\n")
                    f.write(f"مقصد: {target_name}\n")
                    f.write(f"درجه جدایی: {deg}\n")
                    f.write(f"تاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("مسیر ارتباط:\n")
                    f.write("-" * 50 + "\n")
                    full_path = [(None, self.person_id_by_name(source_name))] + list(path)
                    for i in range(len(full_path) - 1):
                        person1 = degrees.people[full_path[i][1]]["name"]
                        person2 = degrees.people[full_path[i + 1][1]]["name"]
                        movie = degrees.movies[full_path[i + 1][0]]["title"]
                        f.write(f"{i + 1}: {person1} و {person2} در فیلم {movie}\n")
                    f.write("\n" + "=" * 50 + "\n")
                    f.write(f"ساخته شده توسط {APP_NAME} v{APP_VERSION}\n")
                    f.write(f"{FA_DEVELOPER}\n")
                messagebox.showinfo("موفق", f"نتیجه ذخیره شد در:\n{filepath}")
            except Exception as e:
                messagebox.showerror("خطا در ذخیره", str(e))
        else:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("فایل JSON", "*.json")],
                title="ذخیره نتیجه"
            )
            if not filepath:
                return
            try:
                data = {
                    "سازنده": APP_DEVELOPER,
                    "مبدأ": source_name,
                    "مقصد": target_name,
                    "درجه": deg,
                    "تاریخ": datetime.now().isoformat(),
                    "مسیر": []
                }
                full_path = [(None, self.person_id_by_name(source_name))] + list(path)
                for i in range(len(full_path) - 1):
                    movie = degrees.movies[full_path[i + 1][0]]
                    person2 = degrees.people[full_path[i + 1][1]]
                    data["مسیر"].append({
                        "فیلم": {"عنوان": movie["title"], "سال": movie["year"]},
                        "شخص": {"نام": person2["name"]}
                    })
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("موفق", f"نتیجه ذخیره شد در:\n{filepath}")
            except Exception as e:
                messagebox.showerror("خطا در ذخیره", str(e))

    def show_result_details(self, source_name, target_name, path, deg):
        theme = self.theme
        win = tk.Toplevel(self)
        win.title("جزئیات ارتباط")
        win.geometry("620x550")
        win.configure(bg=theme["bg"])
        win.transient(self)
        win.grab_set()
        self.center_toplevel(win, 620, 550)

        header = tk.Frame(win, bg=theme["accent"], padx=14, pady=10)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text=f"{source_name} ← {to_persian_digits(deg)} درجه ← {target_name}",
            font=(FA_FONT, 12, "bold"), bg=theme["accent"], fg="white"
        ).pack()

        text_area = tk.Text(
            win, font=("Consolas", 10), bg=theme["entry_bg"],
            fg=theme["text"], relief=tk.FLAT, padx=14, pady=14, wrap=tk.WORD
        )
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        content = f"سازنده: {APP_DEVELOPER}\n{'-' * 55}\n\n"
        content += f"مبدأ: {source_name}\n\n"
        full_path = [(None, self.person_id_by_name(source_name))] + list(path)
        for i in range(len(full_path) - 1):
            person1 = degrees.people[full_path[i][1]]["name"]
            person2 = degrees.people[full_path[i + 1][1]]
            movie = degrees.movies[full_path[i + 1][0]]
            content += f"{PersianText.STRENGTH_LABELS[0] and ''}مرحله {to_persian_digits(i + 1)}:\n"
            content += f"  فیلم: {movie['title']} ({movie['year']})\n"
            content += f"  {person1} و {person2['name']}\n"
            content += f"  فیلم‌های {person2['name']}: {len(person2['movies'])}\n"
            content += f"{'-' * 55}\n\n"
        content += f"مجموع: {to_persian_digits(deg)} درجه، {to_persian_digits(len(path))} فیلم\n"

        text_area.insert("1.0", content)
        text_area.config(state=tk.DISABLED)

        tk.Button(
            win, text="بستن", font=(FA_FONT, 10),
            bg=theme["accent"], fg="white", relief=tk.FLAT,
            cursor="hand2", command=win.destroy
        ).pack(pady=8, ipady=5, ipadx=20)

    def show_person_details(self, person_id):
        person = degrees.people.get(person_id)
        if not person:
            return
        theme = self.theme
        win = tk.Toplevel(self)
        win.title(f"اطلاعات: {person['name']}")
        win.geometry("540x620")
        win.configure(bg=theme["bg"])
        win.transient(self)
        self.center_toplevel(win, 540, 620)

        header = tk.Frame(win, bg=theme["accent2"], padx=14, pady=12)
        header.pack(fill=tk.X)
        tk.Label(header, text="👤", font=("Segoe UI", 26), bg=theme["accent2"]).pack()
        tk.Label(
            header, text=person["name"], font=(FA_FONT, 16, "bold"),
            bg=theme["accent2"], fg="white"
        ).pack()
        birth = person["birth"] if person["birth"] else "نامشخص"
        tk.Label(
            header, text=f"متولد: {to_persian_digits(birth)}",
            font=(FA_FONT, 10), bg=theme["accent2"], fg="#ddddff"
        ).pack()

        body = tk.Frame(win, bg=theme["bg"])
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=8)

        info_card = tk.Frame(
            body, bg=theme["card"], padx=14, pady=8,
            highlightbackground=theme["border"], highlightthickness=1
        )
        info_card.pack(fill=tk.X)
        for label, value in [
            ("تعداد فیلم‌ها", to_persian_digits(format_number(len(person["movies"])))),
            ("شناسه", person_id),
        ]:
            row = tk.Frame(info_card, bg=theme["card"])
            row.pack(fill=tk.X, pady=2)
            tk.Label(
                row, text=label, font=(FA_FONT, 9),
                bg=theme["card"], fg=theme["text_dim"]
            ).pack(side=tk.RIGHT)
            tk.Label(
                row, text=value, font=(FA_FONT, 9, "bold"),
                bg=theme["card"], fg=theme["text"]
            ).pack(side=tk.LEFT)

        tk.Label(
            body, text="فیلم‌ها", font=(FA_FONT, 12, "bold"),
            bg=theme["bg"], fg=theme["accent"]
        ).pack(anchor="e", pady=(8, 4))

        scroll = ScrollableFrame(body, theme["bg"])
        scroll.pack(fill=tk.BOTH, expand=True)

        movie_list = []
        for mid in list(person["movies"])[:60]:
            if mid in degrees.movies:
                movie_list.append((mid, degrees.movies[mid]))
        movie_list.sort(key=lambda x: x[1]["year"], reverse=True)

        for mid, movie in movie_list:
            m_frame = tk.Frame(
                scroll.inner, bg=theme["card"], padx=10, pady=5,
                highlightbackground=theme["border"], highlightthickness=1
            )
            m_frame.pack(fill=tk.X, pady=2, padx=4)
            title = tk.Label(
                m_frame, text=movie["title"], font=(FA_FONT, 10, "bold"),
                bg=theme["card"], fg=theme["text"], cursor="hand2"
            )
            title.pack(side=tk.RIGHT)
            title.bind("<Double-1>", lambda e, mid_=mid: self.show_movie_details(mid_))
            tk.Label(
                m_frame, text=to_persian_digits(movie["year"]),
                font=(FA_FONT, 9), bg=theme["card"], fg=theme["text_dim"]
            ).pack(side=tk.LEFT)

        btn_frame = tk.Frame(win, bg=theme["bg"])
        btn_frame.pack(pady=8)
        tk.Button(
            btn_frame, text="استفاده به عنوان مبدأ", font=(FA_FONT, 9),
            bg=theme["accent2"], fg="white", relief=tk.FLAT, cursor="hand2",
            command=lambda: self.use_person_in_search(person["name"], True, win)
        ).pack(side=tk.RIGHT, padx=4, ipady=5, ipadx=8)
        tk.Button(
            btn_frame, text="استفاده به عنوان مقصد", font=(FA_FONT, 9),
            bg=theme["bg3"], fg="white", relief=tk.FLAT, cursor="hand2",
            command=lambda: self.use_person_in_search(person["name"], False, win)
        ).pack(side=tk.RIGHT, padx=4, ipady=5, ipadx=8)
        tk.Button(
            btn_frame, text="بستن", font=(FA_FONT, 9),
            bg=theme["accent"], fg="white", relief=tk.FLAT, cursor="hand2",
            command=win.destroy
        ).pack(side=tk.RIGHT, padx=4, ipady=5, ipadx=8)

    def show_movie_details(self, movie_id):
        movie = degrees.movies.get(movie_id)
        if not movie:
            return
        theme = self.theme
        win = tk.Toplevel(self)
        win.title(f"فیلم: {movie['title']}")
        win.geometry("540x620")
        win.configure(bg=theme["bg"])
        win.transient(self)
        self.center_toplevel(win, 540, 620)

        header = tk.Frame(win, bg=theme["accent3"], padx=14, pady=12)
        header.pack(fill=tk.X)
        tk.Label(header, text="🎬", font=("Segoe UI", 26), bg=theme["accent3"]).pack()
        tk.Label(
            header, text=movie["title"], font=(FA_FONT, 15, "bold"),
            bg=theme["accent3"], fg="white", wraplength=480
        ).pack()
        tk.Label(
            header,
            text=f"سال: {to_persian_digits(movie['year'])}  |  بازیگران: {to_persian_digits(len(movie['stars']))}",
            font=(FA_FONT, 10), bg=theme["accent3"], fg="#ddddff"
        ).pack()

        body = tk.Frame(win, bg=theme["bg"])
        body.pack(fill=tk.BOTH, expand=True, padx=14, pady=8)

        tk.Label(
            body, text="بازیگران", font=(FA_FONT, 12, "bold"),
            bg=theme["bg"], fg=theme["accent"]
        ).pack(anchor="e", pady=(0, 4))

        scroll = ScrollableFrame(body, theme["bg"])
        scroll.pack(fill=tk.BOTH, expand=True)

        for actor_id in list(movie["stars"])[:80]:
            actor = degrees.people.get(actor_id)
            if not actor:
                continue
            a_frame = tk.Frame(
                scroll.inner, bg=theme["card"], padx=10, pady=5,
                highlightbackground=theme["border"], highlightthickness=1
            )
            a_frame.pack(fill=tk.X, pady=2, padx=4)
            name = tk.Label(
                a_frame, text=actor["name"], font=(FA_FONT, 10, "bold"),
                bg=theme["card"], fg=theme["text"], cursor="hand2"
            )
            name.pack(side=tk.RIGHT)
            name.bind("<Double-1>", lambda e, pid=actor_id: self.show_person_details(pid))
            if actor["birth"]:
                tk.Label(
                    a_frame, text=to_persian_digits(actor["birth"]),
                    font=(FA_FONT, 9), bg=theme["card"], fg=theme["text_dim"]
                ).pack(side=tk.LEFT)

        tk.Button(
            win, text="بستن", font=(FA_FONT, 10),
            bg=theme["accent"], fg="white", relief=tk.FLAT,
            cursor="hand2", command=win.destroy
        ).pack(pady=8, ipady=5, ipadx=20)

    def use_person_in_search(self, name, as_source, win=None):
        if win:
            win.destroy()
        self.notebook.select(self.search_tab)
        if as_source:
            self.source_var.set(name)
        else:
            self.target_var.set(name)

    def build_history_tab(self):
        for widget in self.history_tab.winfo_children():
            widget.destroy()
        theme = self.theme

        container = tk.Frame(self.history_tab, bg=theme["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        header = tk.Frame(container, bg=theme["bg"])
        header.pack(fill=tk.X, pady=(0, 8))
        tk.Label(
            header, text=f"📜 {PersianText.SEARCH_HISTORY}",
            font=(FA_FONT, 15, "bold"), bg=theme["bg"], fg=theme["text"]
        ).pack(side=tk.RIGHT)

        stats = HISTORY_MANAGER.get_stats(self.username)
        tk.Label(
            header, text=f"{to_persian_digits(stats['total'])} جستجو",
            font=(FA_FONT, 10), bg=theme["bg"], fg=theme["text_dim"]
        ).pack(side=tk.RIGHT, padx=12)

        tk.Button(
            header, text=f"🗑 {PersianText.CLEAR_HISTORY}", font=(FA_FONT, 9),
            bg=theme["error"], fg="white", relief=tk.FLAT,
            cursor="hand2", command=self.clear_history_confirm
        ).pack(side=tk.LEFT)

        history = HISTORY_MANAGER.get_history(self.username)
        if not history:
            empty = tk.Frame(container, bg=theme["card"])
            empty.pack(fill=tk.BOTH, expand=True)
            center = tk.Frame(empty, bg=theme["card"])
            center.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(center, text="📭", font=("Segoe UI", 40), bg=theme["card"]).pack()
            tk.Label(
                center, text=PersianText.NO_HISTORY,
                font=(FA_FONT, 12), bg=theme["card"], fg=theme["text_dim"]
            ).pack(pady=6)
            return

        frame = tk.Frame(container, bg=theme["card"])
        frame.pack(fill=tk.BOTH, expand=True)

        tree_frame = tk.Frame(frame, bg=theme["card"])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        columns = ("num", "source", "target", "degrees", "result", "time", "date")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=16)

        tree.heading("num", text="#")
        tree.heading("source", text="مبدأ")
        tree.heading("target", text="مقصد")
        tree.heading("degrees", text="درجه")
        tree.heading("result", text="نتیجه")
        tree.heading("time", text="زمان")
        tree.heading("date", text="تاریخ")

        tree.column("num", width=40, anchor="center")
        tree.column("source", width=170)
        tree.column("target", width=170)
        tree.column("degrees", width=60, anchor="center")
        tree.column("result", width=90, anchor="center")
        tree.column("time", width=80, anchor="center")
        tree.column("date", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        for i, entry in enumerate(history):
            try:
                dt = datetime.fromisoformat(entry["timestamp"])
                date_str = dt.strftime("%Y-%m-%d %H:%M")
            except Exception:
                date_str = ""
            result_text = "✅ پیدا شد" if entry["found"] else "❌ پیدا نشد"
            degrees_text = to_persian_digits(entry["degrees"]) if entry["found"] else "-"
            tree.insert("", tk.END, values=(
                to_persian_digits(i + 1), entry["person1"], entry["person2"],
                degrees_text, result_text,
                f"{entry['runtime']:.2f}s", date_str
            ))

        def on_double_click(event):
            selection = tree.selection()
            if not selection:
                return
            values = tree.item(selection[0])["values"]
            self.notebook.select(self.search_tab)
            self.source_var.set(values[1])
            self.target_var.set(values[2])
            self.set_status(f"از تاریخچه بارگذاری شد: {values[1]} ← {values[2]}")

        tree.bind("<Double-1>", on_double_click)

        tk.Label(
            container, text=PersianText.DOUBLE_CLICK_HINT,
            font=(FA_FONT, 9), bg=theme["bg"], fg=theme["text_dim"]
        ).pack(pady=4)

    def clear_history_confirm(self):
        answer = messagebox.askyesno(
            "پاک کردن تاریخچه",
            "آیا مطمئن هستید؟\nاین عمل قابل بازگشت نیست."
        )
        if answer:
            HISTORY_MANAGER.clear_history(self.username)
            self.build_history_tab()
            self.set_status("تاریخچه پاک شد")

    def build_favorites_tab(self):
        for widget in self.favorites_tab.winfo_children():
            widget.destroy()
        theme = self.theme

        container = tk.Frame(self.favorites_tab, bg=theme["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        header = tk.Frame(container, bg=theme["bg"])
        header.pack(fill=tk.X, pady=(0, 8))
        tk.Label(
            header, text=f"⭐ {PersianText.FAVORITE_ACTORS}",
            font=(FA_FONT, 15, "bold"), bg=theme["bg"], fg=theme["text"]
        ).pack(side=tk.RIGHT)

        favorites = FAVORITES_MANAGER.get_favorites(self.username)
        tk.Label(
            header, text=f"{to_persian_digits(len(favorites))} ذخیره‌شده",
            font=(FA_FONT, 10), bg=theme["bg"], fg=theme["text_dim"]
        ).pack(side=tk.RIGHT, padx=12)

        if not favorites:
            empty = tk.Frame(container, bg=theme["card"])
            empty.pack(fill=tk.BOTH, expand=True)
            center = tk.Frame(empty, bg=theme["card"])
            center.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(center, text="⭐", font=("Segoe UI", 40), bg=theme["card"]).pack()
            tk.Label(
                center, text=PersianText.NO_FAVORITES,
                font=(FA_FONT, 12), bg=theme["card"], fg=theme["text_dim"]
            ).pack(pady=4)
            tk.Label(
                center, text="در نتایج جستجو روی ستاره کلیک کنید",
                font=(FA_FONT, 9), bg=theme["card"], fg=theme["text_dim"]
            ).pack()
            return

        scroll = ScrollableFrame(container, theme["bg"])
        scroll.pack(fill=tk.BOTH, expand=True)

        columns = 3
        for idx, fav in enumerate(favorites):
            row = idx // columns
            col = idx % columns
            card = tk.Frame(
                scroll.inner, bg=theme["card"], padx=14, pady=10,
                highlightbackground=theme["border"], highlightthickness=1
            )
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            tk.Label(
                card, text=fav["name"], font=(FA_FONT, 11, "bold"),
                bg=theme["card"], fg=theme["text"], wraplength=180
            ).pack()

            info = degrees.people.get(fav["id"])
            if info:
                tk.Label(
                    card, text=f"🎬 {to_persian_digits(format_number(len(info['movies'])))} فیلم",
                    font=(FA_FONT, 9), bg=theme["card"], fg=theme["text_dim"]
                ).pack()

            btns = tk.Frame(card, bg=theme["card"])
            btns.pack(pady=(6, 0))
            tk.Button(
                btns, text="مبدأ", font=(FA_FONT, 8),
                bg=theme["accent2"], fg="white", relief=tk.FLAT, cursor="hand2",
                command=lambda n=fav["name"]: self.use_person_in_search(n, True)
            ).pack(side=tk.RIGHT, padx=2)
            tk.Button(
                btns, text="مقصد", font=(FA_FONT, 8),
                bg=theme["bg3"], fg="white", relief=tk.FLAT, cursor="hand2",
                command=lambda n=fav["name"]: self.use_person_in_search(n, False)
            ).pack(side=tk.RIGHT, padx=2)
            tk.Button(
                btns, text="👁", font=("Segoe UI", 8),
                bg=theme["accent3"], fg="white", relief=tk.FLAT, cursor="hand2",
                command=lambda pid=fav["id"]: self.show_person_details(pid)
            ).pack(side=tk.RIGHT, padx=2)
            tk.Button(
                btns, text="✕", font=("Segoe UI", 8),
                bg=theme["error"], fg="white", relief=tk.FLAT, cursor="hand2",
                command=lambda pid=fav["id"]: self.remove_favorite(pid)
            ).pack(side=tk.RIGHT, padx=2)

        for c in range(columns):
            scroll.inner.columnconfigure(c, weight=1)

    def remove_favorite(self, person_id):
        FAVORITES_MANAGER.remove(self.username, person_id)
        self.build_favorites_tab()
        self.set_status("از علاقه‌مندی‌ها حذف شد")

    def build_stats_tab(self):
        for widget in self.stats_tab.winfo_children():
            widget.destroy()
        theme = self.theme

        container = tk.Frame(self.stats_tab, bg=theme["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        tk.Label(
            container, text="📊 آمار و تحلیل",
            font=(FA_FONT, 15, "bold"), bg=theme["bg"], fg=theme["text"]
        ).pack(anchor="e", pady=(0, 10))

        notebook = ttk.Notebook(container)
        notebook.pack(fill=tk.BOTH, expand=True)

        user_frame = tk.Frame(notebook, bg=theme["card"])
        data_frame = tk.Frame(notebook, bg=theme["card"])
        notebook.add(user_frame, text="  فعالیت شما  ")
        notebook.add(data_frame, text="  پایگاه داده  ")

        self.build_user_stats(user_frame)
        self.build_data_stats(data_frame)

    def build_user_stats(self, parent):
        theme = self.theme
        stats = HISTORY_MANAGER.get_stats(self.username)

        cards_frame = tk.Frame(parent, bg=theme["card"])
        cards_frame.pack(fill=tk.X, padx=18, pady=18)

        cards = [
            (PersianText.TOTAL_SEARCHES, to_persian_digits(stats["total"]), "🔍", theme["accent"]),
            (PersianText.CONNECTIONS_FOUND, to_persian_digits(stats["found"]), "✅", theme["success"]),
            (PersianText.NOT_FOUND_COUNT, to_persian_digits(stats["not_found"]), "❌", theme["error"]),
            (PersianText.AVG_DEGREES, to_persian_digits(stats["avg_degrees"]), "🔗", theme["accent2"]),
            (PersianText.AVG_TIME, f"{stats['avg_runtime']:.2f}s", "⏱", theme["warning"]),
        ]

        for i, (label, value, icon, color) in enumerate(cards):
            card = tk.Frame(
                cards_frame, bg=theme["entry_bg"], padx=12, pady=12,
                highlightbackground=theme["border"], highlightthickness=1
            )
            card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
            cards_frame.columnconfigure(i, weight=1)
            tk.Label(card, text=icon, font=("Segoe UI", 18), bg=theme["entry_bg"]).pack()
            tk.Label(
                card, text=value, font=(FA_FONT, 16, "bold"),
                bg=theme["entry_bg"], fg=color
            ).pack()
            tk.Label(
                card, text=label, font=(FA_FONT, 9),
                bg=theme["entry_bg"], fg=theme["text_dim"]
            ).pack()

        history = HISTORY_MANAGER.get_history(self.username)
        if history:
            tk.Label(
                parent, text=PersianText.RECENT_SEARCHES,
                font=(FA_FONT, 11, "bold"), bg=theme["card"],
                fg=theme["text"], anchor="e"
            ).pack(fill=tk.X, padx=18, pady=(12, 4))

            for entry in history[:8]:
                row = tk.Frame(parent, bg=theme["entry_bg"])
                row.pack(fill=tk.X, padx=18, pady=2)
                icon = "✅" if entry["found"] else "❌"
                color = theme["success"] if entry["found"] else theme["error"]
                tk.Label(
                    row, text=icon, font=("Segoe UI", 10), bg=theme["entry_bg"]
                ).pack(side=tk.RIGHT, padx=5)
                tk.Label(
                    row, text=f"{entry['person1']} ← {entry['person2']}",
                    font=(FA_FONT, 10), bg=theme["entry_bg"], fg=theme["text"]
                ).pack(side=tk.RIGHT, padx=5)
                degrees_text = f"{to_persian_digits(entry['degrees'])}°" if entry["found"] else "-"
                tk.Label(
                    row, text=degrees_text, font=(FA_FONT, 10, "bold"),
                    bg=theme["entry_bg"], fg=color
                ).pack(side=tk.LEFT, padx=8)

    def build_data_stats(self, parent):
        theme = self.theme
        if not degrees.people:
            tk.Label(
                parent, text="داده‌ای بارگذاری نشده",
                font=(FA_FONT, 12), bg=theme["card"], fg=theme["text_dim"]
            ).pack(expand=True)
            return

        info_frame = tk.Frame(parent, bg=theme["card"])
        info_frame.pack(fill=tk.X, padx=18, pady=18)

        rows = [
            ("کل افراد", to_persian_digits(format_number(len(degrees.people)))),
            ("کل فیلم‌ها", to_persian_digits(format_number(len(degrees.movies)))),
            ("نام‌های یکتا", to_persian_digits(format_number(len(degrees.names)))),
            ("پوشه داده‌ها", APP_CONFIG.get("data_directory", "نامشخص")),
        ]

        for label, value in rows:
            row = tk.Frame(info_frame, bg=theme["entry_bg"])
            row.pack(fill=tk.X, pady=3, ipady=6, padx=5)
            tk.Label(
                row, text=label, font=(FA_FONT, 10),
                bg=theme["entry_bg"], fg=theme["text_dim"]
            ).pack(side=tk.RIGHT, padx=10)
            tk.Label(
                row, text=str(value), font=(FA_FONT, 10, "bold"),
                bg=theme["entry_bg"], fg=theme["text"]
            ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            parent, text=PersianText.MOST_CONNECTED,
            font=(FA_FONT, 12, "bold"), bg=theme["card"],
            fg=theme["accent"], anchor="e"
        ).pack(fill=tk.X, padx=22, pady=(8, 4))

        most_connected = sorted(
            degrees.people.items(),
            key=lambda x: len(x[1]["movies"]),
            reverse=True
        )[:5]

        for i, (pid, person) in enumerate(most_connected):
            row = tk.Frame(parent, bg=theme["entry_bg"])
            row.pack(fill=tk.X, padx=18, pady=2, ipady=5)
            tk.Label(
                row, text=f"#{to_persian_digits(i + 1)}",
                font=(FA_FONT, 10, "bold"), bg=theme["entry_bg"],
                fg=theme["accent"], width=4
            ).pack(side=tk.RIGHT)
            name = tk.Label(
                row, text=person["name"], font=(FA_FONT, 10),
                bg=theme["entry_bg"], fg=theme["text"], cursor="hand2"
            )
            name.pack(side=tk.RIGHT, padx=10)
            name.bind("<Double-1>", lambda e, pid_=pid: self.show_person_details(pid_))
            tk.Label(
                row, text=f"{to_persian_digits(len(person['movies']))} فیلم",
                font=(FA_FONT, 9), bg=theme["entry_bg"], fg=theme["text_dim"]
            ).pack(side=tk.LEFT, padx=10)

    def build_browse_tab(self):
        for widget in self.browse_tab.winfo_children():
            widget.destroy()
        theme = self.theme

        container = tk.Frame(self.browse_tab, bg=theme["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        tk.Label(
            container, text="🌐 مرورگر داده‌ها",
            font=(FA_FONT, 15, "bold"), bg=theme["bg"], fg=theme["text"]
        ).pack(anchor="e", pady=(0, 8))

        search_row = tk.Frame(container, bg=theme["bg"])
        search_row.pack(fill=tk.X, pady=(0, 6))

        tk.Label(
            search_row, text="جستجو:", font=(FA_FONT, 10),
            bg=theme["bg"], fg=theme["text"]
        ).pack(side=tk.RIGHT, padx=(0, 6))

        self.browse_search_var = tk.StringVar()
        browse_entry = tk.Entry(
            search_row, textvariable=self.browse_search_var,
            font=(FA_FONT, 11), bg=theme["entry_bg"], fg=theme["text"],
            relief=tk.FLAT, highlightthickness=1,
            highlightcolor=theme["accent"], highlightbackground=theme["border"]
        )
        browse_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, ipady=6)
        browse_entry.bind("<Return>", lambda e: self.do_browse_search())

        tk.Button(
            search_row, text="🔍", font=("Segoe UI", 11),
            bg=theme["accent"], fg="white", relief=tk.FLAT,
            cursor="hand2", command=self.do_browse_search
        ).pack(side=tk.LEFT, padx=(6, 0), ipady=4)

        type_row = tk.Frame(container, bg=theme["bg"])
        type_row.pack(fill=tk.X, pady=(0, 6))
        self.browse_type = tk.StringVar(value="people")
        tk.Radiobutton(
            type_row, text="افراد", variable=self.browse_type, value="people",
            font=(FA_FONT, 10), bg=theme["bg"], fg=theme["text"],
            selectcolor=theme["entry_bg"], activebackground=theme["bg"],
            command=self.load_browse_initial
        ).pack(side=tk.RIGHT, padx=8)
        tk.Radiobutton(
            type_row, text="فیلم‌ها", variable=self.browse_type, value="movies",
            font=(FA_FONT, 10), bg=theme["bg"], fg=theme["text"],
            selectcolor=theme["entry_bg"], activebackground=theme["bg"],
            command=self.load_browse_initial
        ).pack(side=tk.RIGHT, padx=8)

        result_frame = tk.Frame(container, bg=theme["card"])
        result_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("name", "d1", "d2")
        self.browse_tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=18)
        self.browse_tree.heading("name", text="نام")
        self.browse_tree.heading("d1", text="اطلاعات ۱")
        self.browse_tree.heading("d2", text="اطلاعات ۲")
        self.browse_tree.column("name", width=320)
        self.browse_tree.column("d1", width=140, anchor="center")
        self.browse_tree.column("d2", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.browse_tree.yview)
        self.browse_tree.configure(yscrollcommand=scrollbar.set)
        self.browse_tree.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 8), pady=8)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, pady=8, padx=(8, 4))

        self.browse_tree.bind("<Double-1>", self.on_browse_double_click)
        self.load_browse_initial()

    def load_browse_initial(self):
        self.browse_tree.delete(*self.browse_tree.get_children())
        if not degrees.people:
            return
        if self.browse_type.get() == "people":
            top = sorted(
                degrees.people.items(),
                key=lambda x: len(x[1]["movies"]),
                reverse=True
            )[:60]
            for pid, p in top:
                self.browse_tree.insert("", tk.END, values=(
                    p["name"],
                    to_persian_digits(p["birth"]) if p["birth"] else "",
                    f"{to_persian_digits(len(p['movies']))} فیلم"
                ), tags=(pid, "people"))
        else:
            top = sorted(
                degrees.movies.items(),
                key=lambda x: len(x[1]["stars"]),
                reverse=True
            )[:60]
            for mid, m in top:
                self.browse_tree.insert("", tk.END, values=(
                    m["title"], to_persian_digits(m["year"]),
                    f"{to_persian_digits(len(m['stars']))} بازیگر"
                ), tags=(mid, "movies"))

    def do_browse_search(self):
        query = self.browse_search_var.get().strip().lower()
        if not query:
            self.load_browse_initial()
            return
        self.browse_tree.delete(*self.browse_tree.get_children())
        count = 0

        if self.browse_type.get() == "people":
            for name_key, ids in degrees.names.items():
                if query in name_key and count < 100:
                    for pid in list(ids)[:2]:
                        if pid in degrees.people:
                            p = degrees.people[pid]
                            self.browse_tree.insert("", tk.END, values=(
                                p["name"],
                                to_persian_digits(p["birth"]) if p["birth"] else "",
                                f"{to_persian_digits(len(p['movies']))} فیلم"
                            ), tags=(pid, "people"))
                            count += 1
        else:
            for mid, m in degrees.movies.items():
                if query in m["title"].lower() and count < 100:
                    self.browse_tree.insert("", tk.END, values=(
                        m["title"], to_persian_digits(m["year"]),
                        f"{to_persian_digits(len(m['stars']))} بازیگر"
                    ), tags=(mid, "movies"))
                    count += 1

    def on_browse_double_click(self, event):
        selection = self.browse_tree.selection()
        if not selection:
            return
        tags = self.browse_tree.item(selection[0]).get("tags", ())
        if not tags:
            return
        if tags[1] == "people":
            self.show_person_details(tags[0])
        else:
            self.show_movie_details(tags[0])

    def build_badges_tab(self):
        for widget in self.badges_tab.winfo_children():
            widget.destroy()
        theme = self.theme

        container = tk.Frame(self.badges_tab, bg=theme["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        unlocked = BADGE_MANAGER.get_unlocked(self.username)
        tk.Label(
            container, text="🏅 نشان‌ها و دستاوردها",
            font=(FA_FONT, 15, "bold"), bg=theme["bg"], fg=theme["text"]
        ).pack(anchor="e", pady=(0, 4))
        tk.Label(
            container,
            text=f"دستاورد: {to_persian_digits(len(unlocked))} از {to_persian_digits(len(BadgeManager.BADGES))}",
            font=(FA_FONT, 10), bg=theme["bg"], fg=theme["text_dim"]
        ).pack(anchor="e", pady=(0, 8))

        ttk.Progressbar(
            container, mode="determinate",
            maximum=len(BadgeManager.BADGES),
            value=len(unlocked), length=420
        ).pack(anchor="e", pady=(0, 12))

        scroll = ScrollableFrame(container, theme["bg"])
        scroll.pack(fill=tk.BOTH, expand=True)

        columns = 4
        for idx, badge in enumerate(BadgeManager.BADGES):
            row = idx // columns
            col = idx % columns
            is_unlocked = BADGE_MANAGER.is_unlocked(self.username, badge["id"])
            bg = theme["card"] if is_unlocked else theme["entry_bg"]
            fg = theme["text"] if is_unlocked else theme["text_dim"]

            card = tk.Frame(
                scroll.inner, bg=bg, padx=12, pady=12,
                highlightbackground=theme["border"], highlightthickness=1
            )
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            tk.Label(
                card, text=badge["icon"] if is_unlocked else "🔒",
                font=("Segoe UI", 22), bg=bg
            ).pack()
            tk.Label(card, text=badge["name"], font=(FA_FONT, 10, "bold"), bg=bg, fg=fg).pack()
            tk.Label(
                card, text=badge["desc"], font=(FA_FONT, 8),
                bg=bg, fg=theme["text_dim"], wraplength=140, justify=tk.CENTER
            ).pack(pady=2)
            tk.Label(card, text="✅" if is_unlocked else "⬜", font=("Segoe UI", 10), bg=bg).pack()

        for c in range(columns):
            scroll.inner.columnconfigure(c, weight=1)

    def build_quiz_tab(self):
        for widget in self.quiz_tab.winfo_children():
            widget.destroy()
        theme = self.theme

        container = tk.Frame(self.quiz_tab, bg=theme["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        tk.Label(
            container, text="🎯 آزمون و چالش",
            font=(FA_FONT, 15, "bold"), bg=theme["bg"], fg=theme["text"]
        ).pack(anchor="e", pady=(0, 10))

        card = tk.Frame(
            container, bg=theme["card"], padx=24, pady=24,
            highlightbackground=theme["border"], highlightthickness=1
        )
        card.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            card,
            text="حدس بزن دو بازیگر پرکاربرد چند درجه از هم فاصله دارند!\n"
                 "برنامه دو بازیگر معروف انتخاب می‌کند و شما حدس می‌زنید.",
            font=(FA_FONT, 11), bg=theme["card"], fg=theme["text"], justify=tk.CENTER
        ).pack(pady=18)

        tk.Button(
            card, text="🚀 شروع آزمون", font=(FA_FONT, 13, "bold"),
            bg=theme["accent"], fg="white", relief=tk.FLAT,
            cursor="hand2", command=self.start_quiz
        ).pack(ipady=9, ipadx=30)

        tk.Label(
            card, text="هر پاسخ درست: ۱۰ امتیاز",
            font=(FA_FONT, 10), bg=theme["card"], fg=theme["text_dim"]
        ).pack(pady=12)

        BADGE_MANAGER.unlock(self.username, "quiz_player")

    def start_quiz(self):
        if not degrees.people:
            messagebox.showwarning("هشدار", "ابتدا داده‌ها را بارگذاری کنید")
            return

        popular = sorted(
            degrees.people.items(),
            key=lambda x: len(x[1]["movies"]),
            reverse=True
        )[:200]

        theme = self.theme
        quiz_win = tk.Toplevel(self)
        quiz_win.title("آزمون درجات جدایی")
        quiz_win.geometry("500x430")
        quiz_win.configure(bg=theme["bg"])
        quiz_win.transient(self)
        quiz_win.grab_set()
        self.center_toplevel(quiz_win, 500, 430)

        score = [0]
        question_num = [0]
        total_questions = 5

        def show_results():
            for widget in quiz_win.winfo_children():
                widget.destroy()
            center = tk.Frame(quiz_win, bg=theme["bg"])
            center.place(relx=0.5, rely=0.5, anchor="center")
            emoji = "🏆" if score[0] >= 40 else "👍" if score[0] >= 20 else "💪"
            tk.Label(center, text=emoji, font=("Segoe UI", 40), bg=theme["bg"]).pack()
            tk.Label(
                center, text=f"امتیاز نهایی: {to_persian_digits(score[0])}",
                font=(FA_FONT, 17, "bold"), bg=theme["bg"], fg=theme["accent"]
            ).pack(pady=8)
            if score[0] >= 50:
                BADGE_MANAGER.unlock(self.username, "quiz_master")
                tk.Label(
                    center, text="🏅 نشان «استاد آزمون» باز شد!",
                    font=(FA_FONT, 10, "bold"), bg=theme["bg"], fg=theme["success"]
                ).pack()
            tk.Button(
                center, text="بستن", font=(FA_FONT, 10),
                bg=theme["accent"], fg="white", relief=tk.FLAT,
                cursor="hand2", command=quiz_win.destroy
            ).pack(pady=12, ipady=5, ipadx=18)

        def check_answer(selected, actual, options_frame, result_label):
            for btn in options_frame.winfo_children():
                btn.config(state=tk.DISABLED)
            if selected == actual:
                score[0] += 10
                correct_text = to_persian_digits(actual) if actual != -1 else "ارتباط نداشت"
                result_label.config(text=f"✅ درست! جواب {correct_text}", fg=theme["success"])
            else:
                correct_text = to_persian_digits(actual) if actual != -1 else "ارتباطی وجود نداشت"
                result_label.config(text=f"❌ اشتباه! جواب: {correct_text}", fg=theme["error"])
            tk.Button(
                quiz_win, text="سؤال بعدی ←", font=(FA_FONT, 11, "bold"),
                bg=theme["accent"], fg="white", relief=tk.FLAT,
                cursor="hand2", command=next_question
            ).pack(pady=8, ipady=5, ipadx=16)

        def next_question():
            for widget in quiz_win.winfo_children():
                widget.destroy()

            question_num[0] += 1
            if question_num[0] > total_questions:
                show_results()
                return

            (id1, p1), (id2, p2) = random.sample(popular, 2)
            try:
                path = shortest_path(id1, id2)
                actual = len(path) if path else -1
            except Exception:
                actual = -1

            header = tk.Frame(quiz_win, bg=theme["accent2"], padx=14, pady=8)
            header.pack(fill=tk.X)
            tk.Label(
                header,
                text=f"سؤال {to_persian_digits(question_num[0])} از {to_persian_digits(total_questions)}",
                font=(FA_FONT, 12, "bold"), bg=theme["accent2"], fg="white"
            ).pack()
            tk.Label(
                header, text=f"امتیاز: {to_persian_digits(score[0])}",
                font=(FA_FONT, 10), bg=theme["accent2"], fg="#ddddff"
            ).pack()

            body = tk.Frame(quiz_win, bg=theme["bg"])
            body.pack(fill=tk.BOTH, expand=True, padx=18, pady=14)

            tk.Label(
                body,
                text=f"{p1['name']}\nو\n{p2['name']}\nچند درجه از هم فاصله دارند؟",
                font=(FA_FONT, 13, "bold"), bg=theme["bg"],
                fg=theme["text"], justify=tk.CENTER
            ).pack(pady=12)

            options = [1, 2, 3, 4, 5]
            if actual not in options:
                options.append(actual)
            random.shuffle(options)

            options_frame = tk.Frame(body, bg=theme["bg"])
            options_frame.pack(pady=8)

            result_label = tk.Label(
                body, text="", font=(FA_FONT, 11), bg=theme["bg"]
            )
            result_label.pack(pady=8)

            for opt in options:
                text = "ارتباط ندارد" if opt == -1 else to_persian_digits(opt)
                btn = tk.Button(
                    options_frame, text=text, font=(FA_FONT, 11, "bold"), width=12,
                    bg=theme["card"], fg=theme["text"], relief=tk.FLAT,
                    cursor="hand2",
                    command=lambda o=opt: check_answer(o, actual, options_frame, result_label)
                )
                btn.pack(side=tk.RIGHT, padx=4, ipady=5)

        next_question()

    def build_settings_tab(self):
        for widget in self.settings_tab.winfo_children():
            widget.destroy()
        theme = self.theme

        container = tk.Frame(self.settings_tab, bg=theme["bg"])
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        tk.Label(
            container, text="⚙ تنظیمات",
            font=(FA_FONT, 15, "bold"), bg=theme["bg"], fg=theme["text"]
        ).pack(anchor="e", pady=(0, 10))

        scroll = ScrollableFrame(container, theme["bg"])
        scroll.pack(fill=tk.BOTH, expand=True)

        card = tk.Frame(
            scroll.inner, bg=theme["card"], padx=22, pady=18,
            highlightbackground=theme["border"], highlightthickness=1
        )
        card.pack(fill=tk.X, padx=8, pady=6)

        tk.Label(
            card, text="ظاهر", font=(FA_FONT, 12, "bold"),
            bg=theme["card"], fg=theme["accent"], anchor="e"
        ).pack(fill=tk.X, pady=(0, 8))

        theme_row = tk.Frame(card, bg=theme["card"])
        theme_row.pack(fill=tk.X, pady=4)
        tk.Label(
            theme_row, text=PersianText.THEME, font=(FA_FONT, 10),
            bg=theme["card"], fg=theme["text"]
        ).pack(side=tk.RIGHT)
        self.theme_var = tk.StringVar(value=APP_CONFIG.get("theme", "dark"))
        tk.Radiobutton(
            theme_row, text=PersianText.DARK_THEME, variable=self.theme_var, value="dark",
            font=(FA_FONT, 10), bg=theme["card"], fg=theme["text"],
            selectcolor=theme["entry_bg"], activebackground=theme["card"],
            command=self.apply_theme_setting
        ).pack(side=tk.LEFT, padx=12)
        tk.Radiobutton(
            theme_row, text=PersianText.LIGHT_THEME, variable=self.theme_var, value="light",
            font=(FA_FONT, 10), bg=theme["card"], fg=theme["text"],
            selectcolor=theme["entry_bg"], activebackground=theme["card"],
            command=self.apply_theme_setting
        ).pack(side=tk.LEFT)

        self.splash_var = tk.BooleanVar(value=APP_CONFIG.get("show_splash", True))
        tk.Checkbutton(
            card, text=PersianText.SPLASH, variable=self.splash_var,
            font=(FA_FONT, 10), bg=theme["card"], fg=theme["text"],
            selectcolor=theme["entry_bg"], activebackground=theme["card"],
            command=self.save_settings
        ).pack(anchor="e", pady=3)

        self.autocomplete_var = tk.BooleanVar(value=APP_CONFIG.get("auto_search_names", True))
        tk.Checkbutton(
            card, text=PersianText.AUTOCOMPLETE, variable=self.autocomplete_var,
            font=(FA_FONT, 10), bg=theme["card"], fg=theme["text"],
            selectcolor=theme["entry_bg"], activebackground=theme["card"],
            command=self.save_settings
        ).pack(anchor="e", pady=3)

        tk.Frame(card, bg=theme["border"], height=1).pack(fill=tk.X, pady=12)

        tk.Label(
            card, text="داده‌ها", font=(FA_FONT, 12, "bold"),
            bg=theme["card"], fg=theme["accent"], anchor="e"
        ).pack(fill=tk.X, pady=(0, 8))

        history_row = tk.Frame(card, bg=theme["card"])
        history_row.pack(fill=tk.X, pady=4)
        tk.Label(
            history_row, text="حداکثر تعداد تاریخچه", font=(FA_FONT, 10),
            bg=theme["card"], fg=theme["text"]
        ).pack(side=tk.RIGHT)
        self.history_limit_var = tk.StringVar(value=str(APP_CONFIG.get("max_history", 100)))
        tk.Spinbox(
            history_row, from_=10, to=1000, increment=10,
            textvariable=self.history_limit_var, width=8,
            font=(FA_FONT, 10), bg=theme["entry_bg"], fg=theme["text"],
            relief=tk.FLAT, buttonbackground=theme["entry_bg"],
            command=self.save_settings
        ).pack(side=tk.LEFT)

        dir_row = tk.Frame(card, bg=theme["card"])
        dir_row.pack(fill=tk.X, pady=6)
        tk.Label(
            dir_row, text=APP_CONFIG.get("data_directory", "تنظیم نشده"),
            font=(FA_FONT, 9), bg=theme["entry_bg"], fg=theme["text_dim"],
            padx=8, pady=5
        ).pack(side=tk.RIGHT, fill=tk.X, expand=True)
        tk.Button(
            dir_row, text="تغییر پوشه داده‌ها", font=(FA_FONT, 9),
            bg=theme["accent2"], fg="white", relief=tk.FLAT,
            cursor="hand2", padx=12, command=self.change_data_dir
        ).pack(side=tk.LEFT, padx=(6, 0))

        tk.Frame(card, bg=theme["border"], height=1).pack(fill=tk.X, pady=12)

        tk.Label(
            card, text="حساب کاربری", font=(FA_FONT, 12, "bold"),
            bg=theme["card"], fg=theme["accent"], anchor="e"
        ).pack(fill=tk.X, pady=(0, 8))

        if self.username != "مهمان":
            tk.Button(
                card, text=f"🔑 {PersianText.CHANGE_PASSWORD}", font=(FA_FONT, 10),
                bg=theme["bg3"], fg="white", relief=tk.FLAT,
                cursor="hand2", ipady=5, command=self.open_change_password
            ).pack(fill=tk.X, pady=3)
            tk.Button(
                card, text=f"🗑 {PersianText.DELETE_ACCOUNT}", font=(FA_FONT, 10),
                bg=theme["error"], fg="white", relief=tk.FLAT,
                cursor="hand2", ipady=5, command=self.open_delete_account
            ).pack(fill=tk.X, pady=3)
        else:
            tk.Label(
                card, text="شما در حالت مهمان هستید.\nبرای مدیریت حساب، با حساب کاربری وارد شوید.",
                font=(FA_FONT, 9), bg=theme["card"], fg=theme["text_dim"], justify=tk.RIGHT
            ).pack(fill=tk.X)

        tk.Button(
            card, text=f"💾 {PersianText.SAVE_SETTINGS}", font=(FA_FONT, 11, "bold"),
            bg=theme["accent"], fg="white", relief=tk.FLAT,
            cursor="hand2", command=self.save_settings_manual
        ).pack(pady=14, ipady=6, ipadx=26)

    def apply_theme_setting(self):
        APP_CONFIG.set("theme", self.theme_var.get())
        ThemeManager.set_theme(self.theme_var.get())
        messagebox.showinfo(
            "تغییر تم",
            "تم اعمال شد. اگر رنگ‌ها به‌روز نشدند، برنامه را مجدداً باز کنید."
        )

    def save_settings(self):
        try:
            limit = int(self.history_limit_var.get())
        except (ValueError, tk.TclError):
            limit = 100
        APP_CONFIG.set("show_splash", self.splash_var.get())
        APP_CONFIG.set("auto_search_names", self.autocomplete_var.get())
        APP_CONFIG.set("max_history", limit)
        self.set_status(PersianText.SETTINGS_SAVED)

    def save_settings_manual(self):
        self.save_settings()
        messagebox.showinfo("تنظیمات", PersianText.SETTINGS_SAVED)

    def change_data_dir(self):
        folder = filedialog.askdirectory(title="انتخاب پوشه داده‌های IMDB")
        if folder:
            missing = [f for f in DATA_FILES if not os.path.exists(os.path.join(folder, f))]
            if missing:
                messagebox.showerror(
                    "پوشه نامعتبر",
                    f"{PersianText.MISSING_FILES}: {', '.join(missing)}"
                )
                return
            APP_CONFIG.set("data_directory", folder)
            messagebox.showinfo(
                "پوشه داده‌ها",
                "پوشه ذخیره شد. برای اعمال، برنامه را مجدداً باز کنید."
            )
            self.build_settings_tab()

    def open_change_password(self):
        theme = self.theme
        win = tk.Toplevel(self)
        win.title(PersianText.CHANGE_PASSWORD)
        win.geometry("390x340")
        win.configure(bg=theme["bg"])
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()
        self.center_toplevel(win, 390, 340)

        tk.Label(
            win, text=PersianText.CHANGE_PASSWORD,
            font=(FA_FONT, 15, "bold"), bg=theme["bg"], fg=theme["accent"]
        ).pack(pady=14)

        card = tk.Frame(win, bg=theme["card"], padx=22, pady=18)
        card.pack(fill=tk.X, padx=18)

        entries = {}
        for label_text in [PersianText.CURRENT_PASSWORD, PersianText.NEW_PASSWORD, PersianText.CONFIRM_PASSWORD]:
            tk.Label(
                card, text=label_text, font=(FA_FONT, 10),
                bg=theme["card"], fg=theme["text"], anchor="e"
            ).pack(fill=tk.X)
            entry = tk.Entry(
                card, show="•", font=(FA_FONT, 11),
                bg=theme["entry_bg"], fg=theme["text"],
                insertbackground=theme["text"], relief=tk.FLAT, justify=tk.RIGHT
            )
            entry.pack(fill=tk.X, ipady=6, pady=(4, 10))
            entries[label_text] = entry

        status_label = tk.Label(
            win, text="", font=(FA_FONT, 9),
            bg=theme["bg"], fg=theme["error"]
        )
        status_label.pack(pady=4)

        def do_change():
            old = entries[PersianText.CURRENT_PASSWORD].get()
            new = entries[PersianText.NEW_PASSWORD].get()
            confirm = entries[PersianText.CONFIRM_PASSWORD].get()
            if new != confirm:
                status_label.config(text=PersianText.PASSWORDS_NOT_MATCH)
                return
            success, message = USER_DATABASE.change_password(self.username, old, new)
            if success:
                messagebox.showinfo("موفق", message)
                win.destroy()
            else:
                status_label.config(text=message)

        tk.Button(
            win, text="تغییر رمز", font=(FA_FONT, 11, "bold"),
            bg=theme["accent"], fg="white", relief=tk.FLAT,
            cursor="hand2", command=do_change
        ).pack(pady=8, ipady=6, ipadx=18)

    def open_delete_account(self):
        theme = self.theme
        win = tk.Toplevel(self)
        win.title(PersianText.DELETE_ACCOUNT)
        win.geometry("380x250")
        win.configure(bg=theme["bg"])
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()
        self.center_toplevel(win, 380, 250)

        tk.Label(win, text="⚠️", font=("Segoe UI", 30), bg=theme["bg"]).pack(pady=(12, 4))
        tk.Label(
            win,
            text="این عمل حساب شما و تمام داده‌هایتان را\nبرای همیشه حذف می‌کند.",
            font=(FA_FONT, 10), bg=theme["bg"], fg=theme["error"], justify=tk.CENTER
        ).pack(pady=4)

        tk.Label(
            win, text="رمز عبور خود را وارد کنید:",
            font=(FA_FONT, 10), bg=theme["bg"], fg=theme["text"]
        ).pack(pady=(8, 3))

        pass_entry = tk.Entry(
            win, show="•", font=(FA_FONT, 11), width=24,
            bg=theme["entry_bg"], fg=theme["text"],
            insertbackground=theme["text"], relief=tk.FLAT, justify=tk.CENTER
        )
        pass_entry.pack(ipady=6)

        btn_frame = tk.Frame(win, bg=theme["bg"])
        btn_frame.pack(pady=12)

        def do_delete():
            success, message = USER_DATABASE.delete_user(self.username, pass_entry.get())
            if success:
                messagebox.showinfo("حذف شد", PersianText.ACCOUNT_DELETED)
                win.destroy()
                self.logout()
            else:
                messagebox.showerror("خطا", message)

        tk.Button(
            btn_frame, text="حذف برای همیشه", font=(FA_FONT, 10, "bold"),
            bg=theme["error"], fg="white", relief=tk.FLAT,
            cursor="hand2", padx=12, command=do_delete
        ).pack(side=tk.RIGHT, padx=4, ipady=5)
        tk.Button(
            btn_frame, text="انصراف", font=(FA_FONT, 10),
            bg=theme["bg3"], fg="white", relief=tk.FLAT,
            cursor="hand2", padx=12, command=win.destroy
        ).pack(side=tk.RIGHT, padx=4, ipady=5)

    def build_about_tab(self):
        for widget in self.about_tab.winfo_children():
            widget.destroy()
        theme = self.theme

        container = tk.Frame(self.about_tab, bg=theme["bg"])
        container.pack(fill=tk.BOTH, expand=True)

        center = tk.Frame(container, bg=theme["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="🎬", font=("Segoe UI", 46), bg=theme["bg"]).pack()
        tk.Label(
            center, text=APP_NAME, font=(FA_FONT, 26, "bold"),
            bg=theme["bg"], fg=theme["accent"]
        ).pack()
        tk.Label(
            center, text=f"نسخه {to_persian_digits(APP_VERSION)}",
            font=(FA_FONT, 10), bg=theme["bg"], fg=theme["text_dim"]
        ).pack(pady=2)

        dev_card = tk.Frame(
            center, bg=theme["card"], padx=28, pady=14,
            highlightbackground=theme["accent"], highlightthickness=2
        )
        dev_card.pack(pady=12)
        tk.Label(dev_card, text="👨‍💻", font=("Segoe UI", 24), bg=theme["card"]).pack()
        tk.Label(
            dev_card, text="طراح و توسعه‌دهنده",
            font=(FA_FONT, 9), bg=theme["card"], fg=theme["text_dim"]
        ).pack()
        tk.Label(
            dev_card, text=APP_DEVELOPER, font=(FA_FONT, 20, "bold"),
            bg=theme["card"], fg=theme["accent"]
        ).pack()

        tk.Label(
            center,
            text="تحلیل‌گر شش درجه جدایی\nکوتاه‌ترین ارتباط بین دو بازیگر را\nاز طریق فیلم‌های مشترک پیدا کنید",
            font=(FA_FONT, 10), bg=theme["bg"], fg=theme["text"], justify=tk.CENTER
        ).pack(pady=10)

        features_card = tk.Frame(
            center, bg=theme["card"], padx=22, pady=12,
            highlightbackground=theme["border"], highlightthickness=1
        )
        features_card.pack(pady=8)

        features = [
            "🧠 الگوریتم BFS از degrees.py",
            "👥 پایگاه داده کامل IMDB",
            "🔐 حساب کاربری امن با رمز هش‌شده",
            "📜 تاریخچه جستجو و علاقه‌مندی‌ها",
            "🏅 نشان‌ها و دستاوردها",
            "🎯 حالت آزمون و چالش",
            "📄 خروجی TXT و JSON",
            "🌓 تم تیره و روشن",
        ]
        for feature in features:
            tk.Label(
                features_card, text=feature, font=(FA_FONT, 10),
                bg=theme["card"], fg=theme["text"], anchor="e"
            ).pack(fill=tk.X, pady=1)

        tk.Label(
            center,
            text="بر اساس پروژه Degrees دوره CS50 هاروارد",
            font=(FA_FONT, 9), bg=theme["bg"], fg=theme["text_dim"]
        ).pack(pady=8)

        tk.Label(
            center, text=FA_COPYRIGHT,
            font=(FA_FONT, 9, "bold"), bg=theme["bg"], fg=theme["accent2"]
        ).pack()

    def set_status(self, text):
        if hasattr(self, "status_label"):
            try:
                if self.status_label.winfo_exists():
                    self.status_label.config(text=text)
            except Exception:
                pass

    def toggle_theme(self):
        new_theme = "light" if APP_CONFIG.get("theme", "dark") == "dark" else "dark"
        APP_CONFIG.set("theme", new_theme)
        ThemeManager.set_theme(new_theme)
        self.rebuild_ui()

    def rebuild_ui(self):
        self.hide_suggestions()
        for widget in self.winfo_children():
            widget.destroy()
        self.theme = ThemeManager.current()
        self.configure(bg=self.theme["bg"])
        self.build_statusbar()
        self.build_header()
        self.build_main()
        self.bind_shortcuts()

    def bind_shortcuts(self):
        self.bind("<Control-Return>", lambda e: self.do_search())
        self.bind("<Control-r>", lambda e: self.random_actors())
        self.bind("<Control-s>", lambda e: self.swap_actors())
        self.bind("<Escape>", lambda e: self.hide_suggestions())

    def on_close(self):
        APP_CONFIG.set("window_width", self.winfo_width())
        APP_CONFIG.set("window_height", self.winfo_height())
        self.hide_suggestions()
        self.destroy()

    def logout(self):
        if messagebox.askyesno(PersianText.LOGOUT, PersianText.LOGOUT_CONFIRM):
            self.destroy()
            login = LoginWindow()
            login.mainloop()


APP_CONFIG = AppConfig()
USER_DATABASE = UserDatabase()
HISTORY_MANAGER = HistoryManager()
FAVORITES_MANAGER = FavoritesManager()
BADGE_MANAGER = BadgeManager()


def main():
    ThemeManager.set_theme(APP_CONFIG.get("theme", "dark"))
    app = LoginWindow()
    app.mainloop()


if __name__ == "__main__":
    main()