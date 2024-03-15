import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import smtplib

# Website URL to check
url = "https://www.karenradleyvw.com/"

# Script markers to look for
start_marker = "<!-- Fullpath Starts -->"
end_marker = "<!-- Fullpath Ends -->"

# Email settings
sender_email = "nick@fuseautotech.com"
receiver_email = "nick@fuseautotech.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "nick@fuseautotech.com"
smtp_password = "nlvk fpzf nkzi aaqn"

# Function to check if the script is present on the website
def check_website():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(url)
        html_content = driver.page_source
        if start_marker in html_content and end_marker in html_content:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking website: {e}")
        return False
    finally:
        driver.quit()

# Function to send an email notification
def send_email():
    message = f"Subject: Script Found on {url}\n\nThe script has been added to the website."
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message)
    print("Email notification sent.")

# Main function
def main():
    while True:
        if check_website():
            send_email()
            break
        else:
            print("Script not found. Checking again in 1 hour.")
            time.sleep(3600)  # Wait for 1 hour (3600 seconds)

if __name__ == "__main__":
    main()