import tkinter as tk

#colors of project
BG_COLOR = "#111827"
PANEL_COLOR = "#1F2937"
TEXT_COLOR = "#F3F4F6"
MUTED_COLOR = "9#CA3AF"
ACCENT_COLOR = "#22C55E"



#Does whatever it needs to do
root = tk.Tk()
root.configure(bg=BG_COLOR)
root.title("PawDeploy")
root.geometry("640x480")
root.minsize(320, 240)


# A welcome label on top
welcome_label = tk.Label(
    root,
    text="PawDeploy",
    font=("Arial", 20, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
welcome_label.pack(pady=20)

#Label for application name ig
app_label = tk.Label(
    root,
    text="Application name:",
    bg=BG_COLOR,
    fg=TEXT_COLOR
    )
app_label.pack()

#Space where we enter the application
app_entry = tk.Entry(
    root,
    bg=PANEL_COLOR,
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR
    )
app_entry.pack(pady=5)

# our little weird app check
def app_check(event=None):
    app_input = app_entry.get().strip()
    if not app_input:
        app_output.config(text="Please enter an application name!")
    else:
        #Updates the existing label
        app_output.config(text=f"Application: {app_input}")

app_entry.bind("<Return>", app_check)

#Button for checking app
app_check_app = tk.Label(
    root,
    text="Check Application", 
    bg=ACCENT_COLOR,
    fg="#052E16",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=10,
    cursor="hand2",
    )
app_check_app.pack(pady=10)
app_check_app.bind("<Button-1>", lambda event: app_check())
app_check_app.bind("<Enter>", lambda e: app_check_app.config(bg="#16A34A"))
app_check_app.bind("<Leave>", lambda e: app_check_app.config(bg=ACCENT_COLOR))



#Label that outputs our inputed application
app_output = tk.Label(root, text="", font=("Arial", 12, "bold"), bg=BG_COLOR, fg=TEXT_COLOR)
app_output.pack(pady=10)

root.mainloop()