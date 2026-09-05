def minutes_to_time(minutes: int) -> str:
    """
    Convert minutes since midnight into HH:MM format.
    """

    hours = minutes // 60
    mins = minutes % 60

    return f"{hours:02}:{mins:02}"

def minutes_to_time(minutes: int) -> str:
    """
    Convierte minutos desde medianoche a HH:MM.
    """

    hours = minutes // 60
    mins = minutes % 60

    return f"{hours:02}:{mins:02}"


def time_to_minutes(time: str) -> int:
    """
    Convierte HH:MM a minutos.
    """

    hours, mins = map(int, time.split(":"))

    return hours * 60 + mins