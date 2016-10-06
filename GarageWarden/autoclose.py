from GarageWarden import status, control, notify, settingHelper
from threading import Timer
import time

timer = None


def state_change():
    if not settingHelper.value("autoclose.enabled"):
        return
    global timer
    if not status.garage_is_full_close():
        if not timer:
            print("starting autoclose countdown")
            timer = Timer((settingHelper.value("autoclose.minutes") * 60) - 30, notify_before_close)
            timer.start()
    else:
        # it's closed now, so we can stop waiting
        stop_timer()


def notify_before_close():
    global timer
    if not status.garage_is_full_close():
        if settingHelper.value("autoclose.notification enabled"):
            notify.send_mail("Auto-Closing garage in 30 seconds", "The garage door will close in 30 seconds")
        # just sleep since we're on an async thread anyway
        time.sleep(30)
        do_close()


def do_close():
    if not status.garage_is_full_close():
        stop_timer()
        if settingHelper.value("autoclose.notification enabled"):
            notify.send_mail("Auto-Closing garage door", "The garage was closed")
        control.trigger_door()


def stop_timer():
    print("stopping autoclose")
    global timer
    if timer:
        timer.cancel()
    timer = None
