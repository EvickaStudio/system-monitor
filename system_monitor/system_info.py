import psutil


def format_bytes(bytes):
    """
    Convert bytes to a human-readable format (KB, MB, GB).

    Args:
        bytes (int): Number of bytes.

    Returns:
        str: Human-readable string representation of the byte size.
    """
    if bytes < 1024:
        return f"{bytes} B"
    elif bytes < 1048576:
        return f"{bytes / 1024:.2f} KB"
    elif bytes < 1073741824:
        return f"{bytes / 1048576:.2f} MB"
    else:
        return f"{bytes / 1073741824:.2f} GB"


def get_system_info():
    """
    Retrieve current system information including CPU, RAM, Disk, and Network usage.

    Returns:
        tuple: CPU usage (%), RAM usage (%), Disk usage (%), Network sent (bytes), Network received (bytes).
    """
    cpu_usage = psutil.cpu_percent(interval=0)  # Non-blocking call
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    disk_usage = psutil.disk_usage("/").percent
    net_info = psutil.net_io_counters()
    net_sent = net_info.bytes_sent
    net_recv = net_info.bytes_recv
    return cpu_usage, memory_usage, disk_usage, net_sent, net_recv
