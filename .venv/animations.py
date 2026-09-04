# animations.py

def animate_number(widget, label, start_val, target_val, prefix="", suffix="", step=0, total_steps=18):
    """Плавный пересчет числа с частотой 60 кадров в секунду"""
    diff = (target_val - start_val) * (step / total_steps)
    current = start_val + diff
    label.configure(text=f"{prefix}{current:,.2f}{suffix}")

    if step < total_steps:
        widget.after(16, animate_number, widget, label, start_val, target_val, prefix, suffix, step + 1, total_steps)
    else:
        label.configure(text=f"{prefix}{target_val:,.2f}{suffix}")
