from datetime import datetime, timedelta
from GarageWarden import settings

last_un_close = datetime.now() - timedelta(minutes=settings.DEFAULT_AUTO_CLOSE_TIME)


def state_change():
    print("un-close detected")
    # any time this method is executed, async wait 10 seconds (to let the switches settle from bouncing)
    # then check if the door is still not closed
    # if door is still not closed, set up an async timer to countdown and eventually close the garage
    #   notify the user that the garage will be closing in 30 seconds before closing
    #   before closing the door, check to make sure it's actually not closed
    # if the door has returned to close cancel the async timer if it's running
