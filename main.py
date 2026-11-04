import random

import customtkinter as ctk

# ---------- COLORS ----------
BG_COLOR = "#111827"
PANEL_COLOR = "#1F2937"
INPUT_COLOR = "#111827"
TEXT_COLOR = "#F3F4F6"
MUTED_COLOR = "#9CA3AF"
ACCENT_COLOR = "#22C55E"
ACCENT_HOVER = "#16A34A"
ERROR_COLOR = "#F87171"
WARNING_COLOR = "#FACC15"


# ---------- MAIN WINDOW ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("PawDeploy")
root.geometry("1000x800")
root.minsize(1000, 800)
root.configure(fg_color=BG_COLOR)


# ---------- MAIN CONTAINER ----------
main_frame = ctk.CTkFrame(
    root,
    fg_color=BG_COLOR,
    corner_radius=0
)
main_frame.pack(
    fill="both",
    expand=True,
    padx=32,
    pady=30
)

content_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)
content_frame.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


# ---------- HEADER ----------
header_frame = ctk.CTkFrame(
    content_frame,
    fg_color=PANEL_COLOR,
    corner_radius=20
)
header_frame.pack(fill="x", pady=(0, 20))


welcome_label = ctk.CTkLabel(
    header_frame,
    text="🐾 PawDeploy",
    font=("Arial", 28, "bold"),
    text_color=TEXT_COLOR
)
welcome_label.pack(pady=(24, 0))

subtitle_label = ctk.CTkLabel(
    header_frame,
    text="Your friendly deployment companion",
    font=("Arial", 12),
    text_color=MUTED_COLOR
)
subtitle_label.pack(pady=(5, 24))


# ---------- APPLICATION CARD ----------
app_frame = ctk.CTkFrame(
    content_frame,
    fg_color=PANEL_COLOR,
    corner_radius=20
)
app_frame.pack(fill="x")

app_title = ctk.CTkLabel(
    app_frame,
    text="Application Setup",
    font=("Arial", 18, "bold"),
    text_color=TEXT_COLOR
)
app_title.pack(pady=(28, 5))

app_description = ctk.CTkLabel(
    app_frame,
    text="Enter the name of the application you want to deploy.",
    font=("Arial", 12),
    text_color=MUTED_COLOR
)
app_description.pack(pady=(0, 20))


# ---------- APPLICATION INPUT ----------
app_label = ctk.CTkLabel(
    app_frame,
    text="Application name",
    font=("Arial", 12, "bold"),
    text_color=TEXT_COLOR
)
app_label.pack(pady=(0, 8))

app_entry = ctk.CTkEntry(
    app_frame,
    width=400,
    height=40,
    font=("Arial", 14),
    fg_color=INPUT_COLOR,
    text_color=TEXT_COLOR,
    placeholder_text="e.g. PawDeploy",
    placeholder_text_color=MUTED_COLOR,
    border_color="#374151",
    border_width=1,
    corner_radius=10
)
app_entry.pack()
MAX_LENGTH = 30
app_entry.bind("<KeyRelease>", lambda event: app_entry.delete(MAX_LENGTH, "end"))

# ---------- OUTPUT ----------
app_output = ctk.CTkLabel(
    app_frame,
    text="",
    font=("Arial", 16, "bold"),
    text_color=TEXT_COLOR,
    width=400,
    height=30,
    wraplength=400
)
app_output.pack(pady=(16,0))


# ---------- APPLICATION CHECK ----------
def app_check():
    app_input = app_entry.get().strip()

    if not app_input:
        app_output.configure(
            text="Please enter an application name!",
            text_color=ERROR_COLOR
        )
    else:
        app_output.configure(
            text=f"Application: {app_input}",
            text_color=ACCENT_COLOR
        )

    app_output.pack(pady=(10, 10), before=app_check_app)


# ---------- CHECK BUTTON ----------
app_check_app = ctk.CTkButton(
    app_frame,
    text="Check Application",
    fg_color=ACCENT_COLOR,
    hover_color=ACCENT_HOVER,
    text_color="#052E16",
    font=("Arial", 13, "bold"),
    corner_radius=10,
    height=40,
    command=app_check
)
app_check_app.pack(pady=(10, 10))


# ---------- KEYBOARD BINDING ----------
app_entry.bind("<Return>", lambda event: app_check())

# ---------- DEPLAYMENT PIPELINE ----------
pipeline_frame = ctk.CTkFrame(
    content_frame,
    fg_color=PANEL_COLOR,
    corner_radius=20
)
pipeline_frame.pack(fill="x", pady=(20, 0))

pipeline_title = ctk.CTkLabel(
    pipeline_frame,
    text="Deployment Pipeline",
    font=("Arial", 16, "bold"),
    text_color=TEXT_COLOR
)
pipeline_title.pack(pady=20)

# ---------- DEPLOYMENT PIPELINE ----------
STAGES = ["Build", "Test", "Security Scan", "Deploy"]
stage_dots = []

for stage in STAGES:
    row = ctk.CTkFrame(pipeline_frame, fg_color=PANEL_COLOR)
    row.pack(fill="x", padx=40, pady=6)

    dot = ctk.CTkLabel(
        row,
        text="○",
        font=("Arial", 16),
        text_color=TEXT_COLOR
    )
    dot.pack(side="left")

    name = ctk.CTkLabel(
        row,
        text=stage,
        font=("Arial", 14),
        text_color=TEXT_COLOR
    )
    name.pack(side="left", padx=12)

    stage_dots.append(dot)

def finish(message, color):
    app_output.configure(text=message, text_color=color)
    run_button.configure(state="normal")

# ---------- RUN PIPELINE ----------

def run_pipeline():
    fail_at = random.randint(0, len(STAGES) + 2)   # 0 = Build, 1 = Test, 2 = Security Scan, 3 = Deploy


    app_name = app_entry.get().strip()
    if not app_name:
        app_output.configure(
            text="There is no app, please enter your application",
            text_color=ERROR_COLOR
        )
        return
    run_button.configure(state="disabled")
    for dot in stage_dots:
        dot.configure(text="○", text_color=TEXT_COLOR)
    app_output.configure(
        text=f"Deploying {app_name}...",
        text_color=ACCENT_COLOR
    )
    second = 1000
    for i, dot in enumerate(stage_dots):
        delay = (i + 1) * second
        start = i * second
        root.after(
            start,
            lambda d=dot: d.configure(text="●", text_color=WARNING_COLOR)
        )
        if i == fail_at:
            root.after(
                delay,
                lambda d=dot: d.configure(text="✕", text_color=ERROR_COLOR)
            )
            root.after(
                delay,
                lambda: finish(f"{app_name}, failed at {STAGES[fail_at]}", ERROR_COLOR)
            )
            return
        root.after(
            delay,
            lambda d=dot: d.configure(text="●", text_color=ACCENT_COLOR)
        )
    root.after(
        len(stage_dots) * second + second,
        lambda: finish(f"{app_name} deployed", ACCENT_COLOR)
    )
        

run_button = ctk.CTkButton(
    pipeline_frame,
    text = "Run Pipeline",
    fg_color=ACCENT_COLOR,
    hover_color=ACCENT_HOVER,
    text_color="#052E16",
    font=("Arial", 13, "bold"),
    corner_radius=10,
    height=40,
    command=run_pipeline
)
run_button.pack(pady=(10, 24))

def clear_error(event):
    if app_entry.get() and app_output.cget("text_color") == ERROR_COLOR:
        app_output.configure(text="")

app_entry.bind("<KeyRelease>", clear_error)



root.mainloop()
