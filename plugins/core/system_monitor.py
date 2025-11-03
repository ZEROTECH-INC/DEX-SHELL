# core/system_monitor.py
import psutil

def register():
    """Registers the system monitor plugin."""
    def system_monitor(args, cwd, input_text=None):
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory().percent
        net = psutil.net_io_counters().bytes_sent / (1024 * 1024)
        return f"CPU: {cpu}% | MEM: {mem}% | NET OUT: {net:.2f} MB"
    return system_monitor
