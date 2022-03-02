import pulsectl
from models.sink import sink_serialize
from enum import Enum


class Change(Enum):
    UP = "UP"
    DOWN = "DOWN"
    TOGGLE = "MUTE"
    INFO = "INFO"


def volume(change: Change):

    sinks = []

    pulse = pulsectl.Pulse("volume-changer")
    for sink in pulse.sink_list():
        # Volume is usually in 0-1.0 range, with >1.0 being soft-boosted
        if change == Change.UP:
            pulse.volume_change_all_chans(sink, 0.1)
        elif change == Change.DOWN:
            pulse.volume_change_all_chans(sink, -0.1)
        elif change == Change.INFO:
            pulse.volume_change_all_chans(sink, 0) # possibly pulse.volume_get_all_chans() is better, if it returns same type.
        elif change == Change.TOGGLE:
            if sink.mute == 1:
                pulse.mute(sink, 0)
            else:
                pulse.mute(sink, 1)
        sinks.append(sink_serialize(sink))

    return sinks

def volume_down():
    return volume(Change.DOWN)

def volume_up():
    return volume(Change.UP)

def volume_toggle():
    return volume(Change.TOGGLE)

def volume_info():
    return volume(Change.INFO)
