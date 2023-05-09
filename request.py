import time
from bs4 import BeautifulSoup as soup
import requests

# Set the URL

url = "http://localhost:3000"


# Fetch the content from the URL

def get_website_content(website_url):
    response = requests.get(website_url)
    return response.text


def check_content(checking_enabled):
    data = get_website_content(url)

    morning_data = get_morning_bus_count(data)
    return_college_data = return_student_bus_count(data)
    return_admin_data = return_admin_bus_count(data)

    return_array = [morning_data, return_college_data, return_admin_data]

    while checking_enabled:

        time.sleep(5)

        new_website_content = get_website_content(url)

        if new_website_content != data:
            new_morning_data = get_morning_bus_count(new_website_content)
            new_return_college_data = return_student_bus_count(new_website_content)
            new_return_admin_data = return_admin_bus_count(new_website_content)

            new_return_array = [new_morning_data, new_return_college_data, new_return_admin_data]

            return new_return_array


def get_morning_bus_count(data):
    return soup(data, "html.parser").find("span", {"class": "morning-timing"}).text


def return_student_bus_count(data):
    return soup(data, "html.parser").find("span", {"class": "return-students-timing"}).text


def return_admin_bus_count(data):
    return soup(data, "html.parser").find("span", {"class": "return-admin-timing"}).text
