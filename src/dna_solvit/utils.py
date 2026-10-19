def format_elapsed_time(elapsed_seconds: float) -> str:
    if elapsed_seconds < 1e-3:
        return f"{elapsed_seconds * 1e6:.1f}µs"
    if elapsed_seconds < 1:
        return f"{elapsed_seconds * 1e3:.1f}ms"
    return f"{elapsed_seconds:.2f}s"
