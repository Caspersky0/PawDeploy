import random  # noqa: I001
import sys

from datetime import datetime
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk

import pipeline
import security_scan



# ---------- COLORS ----------
BG_COLOR = "#111827"
PANEL_COLOR = "#1F2937"
TEXT_COLOR = "#F3F4F6"
MUTED_COLOR = "#9CA3AF"
ACCENT_COLOR = "#22C55E"
ACCENT_HOVER = "#16A34A"
ERROR_COLOR = "#F87171"
WARNING_COLOR = "#FACC15"
TERMINAL_BG = "#0B0F14"


# ---------- MAIN WINDOW ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title("PawDeploy")
root.geometry("1100x800")
root.minsize(1100, 800)
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
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)

content_frame.grid(row=0, column=0, padx=(0, 20), sticky="e")


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
    text="Choose the Python file you want to deploy.",
    font=("Arial", 12),
    text_color=MUTED_COLOR
)
app_description.pack(pady=(0, 20))


# ---------- FILE PICKER ----------
selected_file = ""


def choose_file():
    global selected_file
    path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    if path:
        selected_file = path
        name = Path(path).name
        app_output.configure(
            text=f"Application: {name}",
            text_color=ACCENT_COLOR
        )
        add_log(f"INFO: Selected application {name}")


file_button = ctk.CTkButton(
    app_frame,
    text="Choose .py file",
    fg_color=ACCENT_COLOR,
    hover_color=ACCENT_HOVER,
    text_color="#052E16",
    font=("Arial", 13, "bold"),
    corner_radius=10,
    height=40,
    command=choose_file
)
file_button.pack()


# ---------- OUTPUT ----------
app_output = ctk.CTkLabel(
    app_frame,
    text="No file selected",
    font=("Arial", 16, "bold"),
    text_color=MUTED_COLOR,
    width=440,
    height=30,
    wraplength=420
)
app_output.pack(pady=(16, 28))


# ---------- DEPLOYMENT PIPELINE ----------
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
    add_log(message)
    app_output.configure(text=message, text_color=color)
    run_button.configure(state="normal")


# ---------- RUN PIPELINE ----------
def run_pipeline():
    if not selected_file:
        app_output.configure(
            text="Please choose a .py file first",
            text_color=ERROR_COLOR
        )
        add_log("ERROR: No application selected. Choose a .py file first")
        return

    app_name = Path(selected_file).name

    # 0-3 = that stage crashes, anything bigger = no crash (rare crash for a real feel)
    fail_at = random.randint(0, len(STAGES) * 5)

    # real Build check: a broken file always fails at Build
    build_error = pipeline.check_build(selected_file)
    security_error = security_scan.check_security(selected_file)
    reason = build_error or security_error or "unexpected crash"
    if build_error or security_error:
        fail_at = 0

    run_button.configure(state="disabled")

    def finish(message, color):
        add_log(message)
        app_output.configure(text=message, text_color=color)
        run_button.configure(state="normal")
        file_button.configure(state="normal")

    for dot in stage_dots:
        dot.configure(text="○", text_color=TEXT_COLOR)
    app_output.configure(
        text=f"Deploying {app_name}...",
        text_color=ACCENT_COLOR
    )

    second = 1000

    add_log(f"INFO: Pipeline started for {app_name}")

    for i, dot in enumerate(stage_dots):
        delay = (i + 1) * second
        start = i * second

        # stage starts: yellow dot + log line
        root.after(
            start,
            lambda d=dot: d.configure(text="●", text_color=WARNING_COLOR)
        )
        root.after(
            start,
            lambda n=STAGES[i]: add_log(f"INFO: {n} started")
        )

        if i == fail_at:
            # stage fails: red dot + log line + final message
            root.after(
                delay,
                lambda d=dot: d.configure(text="✕", text_color=ERROR_COLOR)
            )
            root.after(
                delay,
                lambda n=STAGES[i]: add_log(f"ERROR: {n} failed ({reason})")
            )
            root.after(
                delay,
                lambda: finish(f"{app_name} failed at {STAGES[fail_at]}", ERROR_COLOR)
            )
            return

        # stage passes: green dot + log line
        root.after(
            delay,
            lambda d=dot: d.configure(text="●", text_color=ACCENT_COLOR)
        )
        root.after(
            delay,
            lambda n=STAGES[i]: add_log(f"INFO: {n} passed")
        )

        # all stages passed
    def deploy_now():
            target = pipeline.deploy(selected_file)
            add_log(f"INFO: Copied to {target}")
            add_log("INFO: Building the app, this can take a minute...")
            app_output.configure(text=f"Building {app_name}...", text_color=WARNING_COLOR)
            process = pipeline.build_app(selected_file)

            def wait_for_build():
                if process.poll() is None:
                    root.after(500, wait_for_build)
                elif process.returncode == 0:
                    finish(f"{app_name} deployed successfully", ACCENT_COLOR)
                    add_log(f"INFO: App ready in {pipeline.DEPLOY_FOLDER}")
                else:
                    finish(f"{app_name} build failed", ERROR_COLOR)
                    add_log("ERROR: See build_tmp/build.log for details")

            wait_for_build()

    root.after(len(stage_dots) * second + second, deploy_now)

run_button = ctk.CTkButton(
    pipeline_frame,
    text="Run Pipeline",
    fg_color=ACCENT_COLOR,
    hover_color=ACCENT_HOVER,
    text_color="#052E16",
    font=("Arial", 13, "bold"),
    corner_radius=10,
    height=40,
    command=run_pipeline
)
run_button.pack(pady=(10, 24))


# ---------- LOG TERMINAL ----------
log_frame = ctk.CTkFrame(
    main_frame,
    fg_color=TERMINAL_BG,
    corner_radius=12,
    border_width=1,
    border_color="#374151"
)
log_frame.grid(row=0, column=1, padx=(10, 0), sticky="w")

log_title = ctk.CTkLabel(
    log_frame,
    text="● ● ●   pawdeploy.log",
    font=("Menlo", 11),
    text_color=MUTED_COLOR
)
log_title.pack(anchor="w", padx=14, pady=(10, 6))

log_box = ctk.CTkTextbox(
    log_frame,
    width=320,
    height=420,
    fg_color=TERMINAL_BG,
    text_color=ACCENT_COLOR,
    font=("Menlo", 12),
    wrap="word",
    state="disabled"
)
log_box.pack(padx=12, pady=(0, 12))


def add_log(text):
    stamp = datetime.now().strftime("%H:%M:%S")
    log_box.configure(state="normal")
    log_box.insert("end", f"[{stamp}] {text}\n")
    log_box.see("end")
    log_box.configure(state="disabled")


add_log("INFO: PawDeploy ready. Choose a .py file to begin.")

root.mainloop()

