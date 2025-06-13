def on_entry_change(dialogue_entry, send_btn, *args):
    if dialogue_entry.get().strip():
        send_btn.configure(state="normal")
    else:
        send_btn.configure(state="disabled")
