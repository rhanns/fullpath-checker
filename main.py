import os
import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import smtplib

# CSV file path
csv_file = 'urls.csv'

# Email settings
sender_email = "nick@fuseautotech.com"
receiver_email = "nick@fuseautotech.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "nick@fuseautotech.com"
smtp_password = os.getenv("fpchecker")


# Function to read URLs from CSV file
def read_urls_from_csv():
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        urls = [row[0] for row in reader if row]
    return urls


# Function to check if the script is present on the website
def check_website(url):
    # Script markers to look for
    start_marker = "<!-- Fullpath Starts -->"
    end_marker = "<!-- Fullpath Ends -->"

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
def send_email(urls_with_script, urls_without_script):
    message = "Subject: Script Checker Results\n\n"

    if urls_with_script:
        message += "The script was found on the following URLs:\n"
        for url in urls_with_script:
            message += f"{url}\n"
        message += "\n"

    if urls_without_script:
        message += "The script was not found on the following URLs:\n"
        for url in urls_without_script:
            message += f"{url}\n"
    else:
        message += "The script was found on all URLs."

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message)
    print("Email notification sent.")


# Main function
def main():
    urls = read_urls_from_csv()

    while True:
        urls_with_script = []
        urls_without_script = []

        for url in urls:
            if check_website(url):
                urls_with_script.append(url)
            else:
                urls_without_script.append(url)

        send_email(urls_with_script, urls_without_script)

        if not urls_without_script:
            print("Script found on all URLs. Exiting.")
            break

        print("Checking again in 1 hour.")
        time.sleep(3600)  # Wait for 1 hour (3600 seconds)


if __name__ == "__main__":
    main()