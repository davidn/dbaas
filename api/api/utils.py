from time import sleep
from logging import getLogger

logger = getLogger(__name__)

def retry(func, initialDelay=50, maxRetries=12):
    delay = initialDelay
    for retry in range(maxRetries-1):
        try:
            result = func()
            if result:
                break
        except:
            #Logging for this can be captured from Boto
            pass
        sleep(delay / 1000.0)
        delay *= 2
    else:
        # Final attempt, don't catch exception
        result = func()
    return result
