import os
import constants as C
import requests
import logging
import sys


log = logging.getLogger()
log.setLevel(logging.DEBUG)

if __name__ == "__main__":
    TG_API_TOKEN = os.environ["TG_API_TOKEN"]
    proxy = getattr(C, "PROXY", None)

    try:
        requests.get(C.ENDPOINT, timeout=1)
        endpoint_is_reachable = True
    except requests.exceptions.ConnectTimeout:
        log.warning(f"ConnectTimeout to {C.ENDPOINT}. Probably Telegram is blocked in your country.")
        endpoint_is_reachable = False

    if not endpoint_is_reachable and proxy:
        log.warning(f"Trying to use proxy: {proxy}")
        response = requests.get(C.ENDPOINT, timeout=10, proxies={"https": proxy})
        if response.ok:
            endpoint_is_reachable = True

    if endpoint_is_reachable:
        response = requests.get(
            f"https://api.telegram.org/bot{TG_API_TOKEN}/setWebhook", timeout=10, proxies={"https": proxy}
        )
        if response.ok:
            log.warning("200 OK")

    else:
        log.error("Not OK")
        sys.exit(1)
