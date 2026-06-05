import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# 1. Manuscript and Monitoring Configuration
# ==========================================
# ACC_CODE = "LH19466"
ACC_CODE = "CP10848"
LAST_NAME = "hu"  # Author's Last Name
CHECK_INTERVAL = 600  # Check interval in seconds (600s = 10 minutes)

# ==========================================
# 2. Email Configuration (You must modify this section)
# ==========================================
SMTP_SERVER = "smtp.qq.com"  # e.g., smtp.qq.com, smtp.163.com, or your institutional SMTP
SMTP_PORT = 465  # SSL port is usually 465

SENDER_EMAIL = "rongzhehu@qq.com"  # [MODIFY] The email address used to send notifications
SENDER_PASSWORD = "pcmhajdddxehbfdh"  # [MODIFY] The SMTP authorization code (NOT your login password)

RECEIVER_EMAIL = "rongzhe_hu@pku.edu.cn"  # The email address that receives notifications
# ==========================================


def send_email(subject, content):
    """Function to send an email notification."""
    print(f"\nPreparing to send email to {RECEIVER_EMAIL} ...")
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject

    # Using 'plain' for plain text email format
    msg.attach(MIMEText(content, "plain", "utf-8"))

    try:
        # Connect to SMTP server and send
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


def get_latest_status():
    """Function to fetch and parse the latest manuscript status."""
    url = f"https://authors.aps.org/Submissions/status?accode={ACC_CODE}&author={LAST_NAME}&commit=Submit"

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract general status
        general_status = "Unknown"
        status_label = soup.find(lambda tag: tag.name in ["b", "strong"] and "Status:" in tag.get_text())
        if status_label:
            general_status = status_label.find_next_sibling(string=True)
            if not general_status or general_status.strip() == "":
                general_status = status_label.parent.get_text(strip=True).replace("Status:", "")

        latest_date = "Unknown"
        latest_detail = "Unknown"

        # Extract the latest record from the History table
        tables = soup.find_all("table")
        for table in tables:
            if "Description" in table.get_text() and "Open" in table.get_text():
                rows = table.find_all("tr")
                if len(rows) > 1:
                    cols = rows[1].find_all(["td", "th"])
                    if len(cols) >= 3:
                        latest_date = cols[0].get_text(strip=True)
                        latest_detail = cols[2].get_text(strip=True)
                break

        return general_status.strip(), latest_date, latest_detail
    except Exception as e:
        print(f"Request failed: {e}")
        return None, None, None


def monitor():
    """Main loop to monitor the status continuously."""
    print("🚀 APS manuscript status monitor started...")
    print(f"Target: {ACC_CODE} | Author: {LAST_NAME} | Interval: {CHECK_INTERVAL} seconds")

    last_detail = None

    while True:
        try:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            general_status, latest_date, latest_detail = get_latest_status()

            if latest_detail is None:
                print(f"[{current_time}] Network request failed, retrying later...", end="\r")
            else:
                # First run initialization
                if last_detail is None:
                    last_detail = latest_detail
                    print(f"[{current_time}] Initial status recorded: {latest_detail}")

                    test_subject = f"[Test] APS Monitor Started for {ACC_CODE}"
                    test_body = f"Monitoring for your manuscript {ACC_CODE} has successfully started.\n\n" f"Current General Status: {general_status}\n" f"Latest Date: {latest_date}\n" f"Latest Detail: {latest_detail}\n\n" f"You will receive an email notification if there are any updates."
                    send_email(test_subject, test_body)

                # If status has changed
                elif latest_detail != last_detail:
                    print(f"\n🎉 [{current_time}] Status update detected!")
                    print(f"New Status: {latest_detail}")

                    subject = f"[Update] New progress on APS manuscript {ACC_CODE}!"
                    body = f"Great news, your manuscript status has been updated!\n\n" f"[Accession Code]: {ACC_CODE}\n" f"[Latest Date]: {latest_date}\n" f"[General Status]: {general_status}\n" f"[Detailed Progress]: {latest_detail}\n\n" f"Please check the APS system for more details."
                    send_email(subject, body)

                    last_detail = latest_detail

                # If status remains the same
                else:
                    print(f"[{current_time}] No changes. Monitoring in background... (Current: {latest_date})", end="\r")

        except Exception as e:
            print(f"\n[{current_time}] Error during monitoring: {e}")

        # Sleep until the next check
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor()
