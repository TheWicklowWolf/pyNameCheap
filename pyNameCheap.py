import os
import time
import logging
import ipaddress
import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger()

api_endpoints = ["https://api.ipify.org", "http://wtfismyip.com/text"]
domain = os.environ.get("domain", "domainA")
hosts = os.environ.get("hosts", "a,b,c")
ddns_password = os.environ.get("ddns_password ", "password")
refresh_interval = float(os.environ.get("refresh_interval", 600))


def get_public_ip(api_endpoint):
    try:
        ip = requests.get(api_endpoint, timeout=5).text.replace("\n", "")
        ipaddress.ip_address(ip)
        logger.info(f"Found IP Address: {ip} from {api_endpoint}")
        return ip.strip()
    except Exception as e:
        logger.error(f"Error getting public IP from {api_endpoint}, Error: {e}")
        return None


def update_dynamic_dns(ip):
    for host in hosts.split(","):
        try:
            url_template = "https://dynamicdns.park-your-domain.com/update?host={}&domain={}&password={}&ip={}"
            url = url_template.format(host, domain, ddns_password, ip or "")
            req = requests.get(url, timeout=5)

            if req.status_code == 200:
                logger.info(f"Dynamic Address update successful for {host}.{domain}")
            else:
                logger.error(f"Failed to update Dynamic Address for {host}.{domain}, HTTP Status Code: {req.status_code}")
                logger.error("Response content:")
                logger.error(req.text)

        except Exception as e:
            logger.error(f"Error updating Dynamic Address for {host}.{domain}: {e}")


while True:
    logger.info("Getting IP Address")
    ip = next((ip for api in api_endpoints if (ip := get_public_ip(api)) is not None), None)
    if not ip:
        logger.warning("No valid IP Address Found, letting it be obtained automatically")

    ret = update_dynamic_dns(ip)
    logger.info(f"Sleeping for {refresh_interval} seconds")
    time.sleep(refresh_interval)
