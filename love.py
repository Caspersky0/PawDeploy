import hashlib

import customtkinter as ctk

# The password itself is never stored in this file, only its hash
# (a one-way fingerprint). To make a hash for a new password, use make_hash.py
# (or run: python3 -c "import hashlib; print(hashlib.sha256('newpassword'.encode()).hexdigest())")
# and paste it below. Use lowercase letters, because the check lowercases what you type.
PASSWORD_HASH = "d1c42e8f1f1fbebbbbb383c575eb6fba4863fd93fd3857e091c2b5f9e30e78fe"

MAX_TRIES = 3
FRAME_DELAY = 500          # milliseconds between pictures
MESSAGE = "Вежливый мишка любит тебя"

BG_COLOR = "#111827"
TEXT_COLOR = "#F3F4F6"
MUTED_COLOR = "#9CA3AF"
ACCENT_COLOR = "#F472B6"
ACCENT_HOVER = "#EC4899"
ERROR_COLOR = "#F87171"

CAT = r"""
            ♥
         /\_/\
        ( o.o )
         > ^ <
        /|   |\
       (_|   |_)
"""

FLOWERS = r"""
     _        _        _
   _(_)_    _(_)_    _(_)_
  (_)@(_)  (_)@(_)  (_)@(_)
    (_)      (_)      (_)
     |   \    |    /   |
     |    \   |   /    |
      \____\__|__/____/
"""

FRAMES = [CAT, FLOWERS]


def check_password(attempt):
    attempt_hash = hashlib.sha256(attempt.strip().lower().encode()).hexdigest()
    return attempt_hash == PASSWORD_HASH


def main():
    ctk.set_appearance_mode("dark")

    root = ctk.CTk()
    root.title("🐾 For you")
    root.geometry("560x520")
    root.resizable(False, False)
    root.configure(fg_color=BG_COLOR)

    state = {"tries": 0, "frame": 0}

    # ---------- LOCK SCREEN ----------
    lock_frame = ctk.CTkFrame(root, fg_color="transparent")
    lock_frame.place(relx=0.5, rely=0.5, anchor="center")

    lock_title = ctk.CTkLabel(
        lock_frame,
        text="🐾 Someone made this for you",
        font=("Arial", 22, "bold"),
        text_color=TEXT_COLOR
    )
    lock_title.pack(pady=(0, 6))

    lock_hint = ctk.CTkLabel(
        lock_frame,
        text="Enter the password to open it",
        font=("Arial", 13),
        text_color=MUTED_COLOR
    )
    lock_hint.pack(pady=(0, 20))

    password_entry = ctk.CTkEntry(
        lock_frame,
        width=280,
        height=40,
        show="•",
        font=("Arial", 14),
        placeholder_text="Password",
        corner_radius=10
    )
    password_entry.pack()

    lock_message = ctk.CTkLabel(
        lock_frame,
        text="",
        font=("Arial", 13, "bold"),
        text_color=ERROR_COLOR,
        width=280,
        height=30
    )
    lock_message.pack(pady=(10, 4))

    # ---------- ANIMATION SCREEN ----------
    animation_frame = ctk.CTkFrame(root, fg_color="transparent")

    animation_label = ctk.CTkLabel(
        animation_frame,
        text="",
        font=("Courier New", 20, "bold"),
        text_color=ACCENT_COLOR,
        justify="left",
        width=520,
        height=330
    )
    animation_label.pack(pady=(30, 0))

    message_label = ctk.CTkLabel(
        animation_frame,
        text=MESSAGE,
        font=("Arial", 18, "bold"),
        text_color=TEXT_COLOR
    )
    message_label.pack(pady=(10, 0))

    def animate():
        animation_label.configure(text=FRAMES[state["frame"]])
        state["frame"] = (state["frame"] + 1) % len(FRAMES)
        root.after(FRAME_DELAY, animate)

    def show_animation():
        lock_frame.place_forget()
        animation_frame.pack(expand=True)
        animate()

    # ---------- UNLOCK ----------
    def unlock():
        if check_password(password_entry.get()):
            show_animation()
            return

        state["tries"] += 1
        tries_left = MAX_TRIES - state["tries"]
        if tries_left > 0:
            lock_message.configure(text=f"Wrong password 🐾  ({tries_left} tries left)")
            password_entry.delete(0, "end")
        else:
            lock_message.configure(text="Too many tries. Come back later 🐾")
            password_entry.configure(state="disabled")
            unlock_button.configure(state="disabled")

    unlock_button = ctk.CTkButton(
        lock_frame,
        text="Open",
        fg_color=ACCENT_COLOR,
        hover_color=ACCENT_HOVER,
        text_color="#1F0A14",
        font=("Arial", 14, "bold"),
        corner_radius=10,
        height=40,
        width=280,
        command=unlock
    )
    unlock_button.pack()

    password_entry.bind("<Return>", lambda event: unlock())
    password_entry.focus()

    root.mainloop()


if __name__ == "__main__":
    main()