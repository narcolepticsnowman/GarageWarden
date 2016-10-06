from GarageWarden import status, control, notify, settingHelper
from threading import Timer

timer = None


def state_change():
    if not settingHelper.value("autoclose.enabled"):
        return
    global timer
    # always stop any existing timer before proceeding. This means that we will technically start counting when this is
    # triggered by the full open switch in the normal case, but we also want to catch the scenario where the garage is
    # only partially opened and never activates the open switch.
    # This also makes sure that any timers running when the door gets closed will stop running
    stop_timer()
    if not status.garage_is_full_close():
        print("starting autoclose countdown")
        timer = Timer((settingHelper.value("autoclose.minutes") * 60) - 30, notify_before_close)
        timer.start()


def notify_before_close():
    global timer
    if not status.garage_is_full_close():
        if settingHelper.value("autoclose.notification enabled"):
            notify.send_mail("Closing garage in 30 seconds", "The garage door will automatically close in 30 seconds")
        # make sure to stop the timer before re-assigning it so we don't leave any threads running
        stop_timer()
        timer = Timer(30, do_close)
        timer.start()


def do_close():
    if not status.garage_is_full_close():
        stop_timer()
        if settingHelper.value("autoclose.notification enabled"):
            notify.send_mail("Closing garage door", "The garage is automatically closing now.")
        control.trigger_door()


def stop_timer():
    print("stopping autoclose")
    global timer
    if timer:
        timer.cancel()
    timer = None
