from GarageWarden import status, control, notify, settingHelper
from threading import Timer, Lock
import time

timer = None
timer_lock = Lock()


def state_change():
    if not settingHelper.value("autoclose.enabled"):
        return
    global timer
    got_lock = timer_lock.acquire()
    if not got_lock:
        return
    if not status.garage_is_full_close():
        if not timer:
            print("starting autoclose countdown")
            timer = Timer((settingHelper.value("autoclose.minutes") * 60) - 30, close)
            timer.start()
    else:
        # it's closed now, so we can stop waiting
        stop_timer()
    if got_lock:
        timer_lock.release()


def close():
    global timer
    if not status.garage_is_full_close():
        if settingHelper.value("autoclose.notification enabled"):
            notify.send_mail("Auto-Closing garage in 30 seconds", "The garage door will close in 30 seconds")
        # just sleep since we're on an async thread anyway
        time.sleep(15)
        count = 0
        while count < 15:
            count += 1
            notify.start_beep()
            time.sleep(.75)
            notify.stop_beep()
            time.sleep(.25)
        control.trigger_door()
        if settingHelper.value("autoclose.notification enabled"):
            notify.send_mail("Auto-Closing garage door", "The garage was closed")
    # cleanup after we're done whether we closed it or it was already closed
    stop_timer()


def stop_timer():
    print("stopping autoclose")
    global timer
    if timer:
        timer.cancel()
    timer = None
