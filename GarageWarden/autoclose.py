from GarageWarden import status, control, notify, settingHelper
from threading import Timer, Lock
import time

timer = None
timer_lock = Lock()


def state_change():
    global timer
    got_lock = timer_lock.acquire()
    if not got_lock:
        print("already starting timer on another thread")
        return
    try:
        if should_close():
            if not timer:
                print("starting autoclose countdown")
                timer = Timer((settingHelper.value("autoclose.minutes") * 60) - 30, close)
                timer.start()
        else:
            # it's closed now, so we can stop waiting
            stop_timer()
    finally:
        if got_lock:
            timer_lock.release()


def close():
    global timer
    if should_close():
        if should_notify():
            notify.send_mail("Auto-Closing garage in 30 seconds", "The garage door will close in 30 seconds")
        # just sleep since we're on an async thread anyway
        time.sleep(15)
        count = 0
        while count < 15:
            if not should_close():
                # if we closed or autoclose was disabled just bail
                return
            count += 1
            notify.start_beep()
            time.sleep(.75)
            notify.stop_beep()
            time.sleep(.25)
        if should_close():
            control.trigger_door()
            if should_notify():
                notify.send_mail("Auto-Closing garage door", "The garage was closed")
    # cleanup after we're done whether we closed it or it was already closed
    stop_timer()

    # There's an edge case where the garage gets stuck operating, so we'll execute the state change manually after two
    # minutes to make sure it's not open still. This way we can just keep executing this until the door is really closed
    Timer(120, state_change)


def stop_timer():
    print("stopping autoclose")
    global timer
    if timer:
        timer.cancel()
    timer = None


def should_notify():
    return settingHelper.value("autoclose.notification enabled")


def should_close():
    return not status.garage_is_full_close() and settingHelper.value("autoclose.enabled")
