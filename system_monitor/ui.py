import tkinter as tk
from ctypes import windll

from customtkinter import CTk, CTkCanvas, CTkLabel

from .config import *
from .system_info import format_bytes, get_system_info

cpu_usage_history = []
ram_usage_history = []


def round_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    """
    Draw a rounded rectangle on a canvas.

    Args:
        canvas (tk.Canvas): The canvas to draw on.
        x1, y1, x2, y2 (int): Coordinates of the rectangle.
        radius (int, optional): Radius of the corners. Defaults to 20.
        **kwargs: Additional keyword arguments for canvas.create_polygon.

    Returns:
        int: The ID of the created polygon.
    """
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
    return canvas.create_polygon(points, **kwargs, smooth=True)


def draw_usage_graph(canvas, usage_history, color):
    """
    Draw a usage graph on a canvas.

    Args:
        canvas (tk.Canvas): The canvas to draw on.
        usage_history (list): List of usage values.
        color (str): Color of the graph lines.
    """
    canvas.delete("usage_graph")
    if len(usage_history) > 1:
        max_usage = max(usage_history)
        for i in range(1, len(usage_history)):
            x1 = (i - 1) * 5
            y1 = 30 - (usage_history[i - 1] / max_usage) * 20
            x2 = i * 5
            y2 = 30 - (usage_history[i] / max_usage) * 20
            canvas.create_line(x1, y1, x2, y2, fill=color, tags="usage_graph")


def create_overlay():
    """
    Create an overlay window displaying system information.
    """
    global root, cpu_label, ram_label, disk_label, net_label, cpu_value, ram_value, disk_value, net_value, cpu_canvas, ram_canvas

    root = CTk()
    root.overrideredirect(True)
    root.geometry(f"{WIDTH}x{HEIGHT}")  # Adjusted size for more information
    root.attributes("-topmost", True)
    root.wm_attributes(
        "-transparentcolor", TRANSPARENT_COLOR
    )  # Use a unique color for transparency
    root.wm_attributes("-alpha", ALPHA)  # Set transparency level (0.0 to 1.0)
    root.wm_attributes("-toolwindow", True)  # Make the window a tool window

    # Make the window click-through
    hwnd = windll.user32.GetParent(root.winfo_id())
    styles = windll.user32.GetWindowLongPtrW(hwnd, -20)
    windll.user32.SetWindowLongPtrW(hwnd, -20, styles | 0x80000 | 0x20)
    # windll.user32.SetLayeredWindowAttributes(hwnd, 0, 255, 0x2)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (WIDTH // 2)
    y = 10
    root.geometry(f"+{x}+{y}")

    canvas = CTkCanvas(
        root, width=WIDTH, height=HEIGHT, bg=TRANSPARENT_COLOR, highlightthickness=0
    )  # Match the transparent color
    canvas.pack()

    round_rectangle(
        canvas, 10, 10, WIDTH - 10, 40, radius=20, fill=BACKGROUND_COLOR
    )  # No outline

    cpu_usage, ram_usage, disk_usage, net_sent, net_recv = get_system_info()

    cpu_label = CTkLabel(
        root,
        text="CPU:",
        bg_color=BACKGROUND_COLOR,
        text_color=CPU_GRAPH_COLOR,
        font=("Helvetica", 12),
        width=10,
    )
    cpu_label.place(x=20, y=12)
    cpu_value = CTkLabel(
        root,
        text=f"{cpu_usage:>5}%",
        bg_color=BACKGROUND_COLOR,
        text_color="white",
        font=("Helvetica", 12),
        width=10,
    )
    cpu_value.place(x=60, y=12)

    cpu_canvas = CTkCanvas(
        root, width=60, height=30, bg=BACKGROUND_COLOR, highlightthickness=0
    )
    cpu_canvas.place(x=100, y=10)

    ram_label = CTkLabel(
        root,
        text="RAM:",
        bg_color=BACKGROUND_COLOR,
        text_color=RAM_GRAPH_COLOR,
        font=("Helvetica", 12),
        width=10,
    )
    ram_label.place(x=170, y=12)
    ram_value = CTkLabel(
        root,
        text=f"{ram_usage:>5}%",
        bg_color=BACKGROUND_COLOR,
        text_color="white",
        font=("Helvetica", 12),
        width=10,
    )
    ram_value.place(x=210, y=12)

    ram_canvas = CTkCanvas(
        root, width=60, height=30, bg=BACKGROUND_COLOR, highlightthickness=0
    )
    ram_canvas.place(x=250, y=10)

    disk_label = CTkLabel(
        root,
        text="Disk:",
        bg_color=BACKGROUND_COLOR,
        text_color=DISK_GRAPH_COLOR,
        font=("Helvetica", 12),
        width=10,
    )
    disk_label.place(x=320, y=12)
    disk_value = CTkLabel(
        root,
        text=f"{disk_usage:>5}%",
        bg_color=BACKGROUND_COLOR,
        text_color="white",
        font=("Helvetica", 12),
        width=10,
    )
    disk_value.place(x=360, y=12)

    net_label = CTkLabel(
        root,
        text="Net (Sent/Recv):",
        bg_color=BACKGROUND_COLOR,
        text_color=NET_GRAPH_COLOR,
        font=("Helvetica", 12),
        width=15,
    )
    net_label.place(x=430, y=12)
    net_value = CTkLabel(
        root,
        text=f"{format_bytes(net_sent):>10}/{format_bytes(net_recv):>10}",
        bg_color=BACKGROUND_COLOR,
        text_color="white",
        font=("Helvetica", 12),
        width=20,
    )
    net_value.place(x=540, y=12)

    def update_info():
        """
        Update the system information displayed in the overlay.
        """
        cpu_usage, ram_usage, disk_usage, net_sent, net_recv = get_system_info()
        cpu_value.configure(text=f"{cpu_usage:>5}%")
        ram_value.configure(text=f"{ram_usage:>5}%")
        disk_value.configure(text=f"{disk_usage:>5}%")
        net_value.configure(
            text=f"{format_bytes(net_sent):>10}/{format_bytes(net_recv):>10}"
        )

        cpu_usage_history.append(cpu_usage)
        if len(cpu_usage_history) > GRAPH_HISTORY_LENGTH:
            cpu_usage_history.pop(0)
        draw_usage_graph(cpu_canvas, cpu_usage_history, CPU_GRAPH_COLOR)

        ram_usage_history.append(ram_usage)
        if len(ram_usage_history) > GRAPH_HISTORY_LENGTH:
            ram_usage_history.pop(0)
        draw_usage_graph(ram_canvas, ram_usage_history, RAM_GRAPH_COLOR)

        root.after(
            UPDATE_INTERVAL, update_info
        )  # Update every UPDATE_INTERVAL milliseconds

    root.after(
        UPDATE_INTERVAL, update_info
    )  # Update every UPDATE_INTERVAL milliseconds
    root.mainloop()
