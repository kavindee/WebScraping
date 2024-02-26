from bs4 import BeautifulSoup
import requests
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

base_url = 'https://ikman.lk/en/ads/sri-lanka/motorbikes-scooters?sort=relevance&buy_now=0&urgent=0&query=CT-100&page='


def meta_data_extraction(meta_url, req):
    meta_res = req.get(meta_url)
    if meta_res.status_code == 200:
        meta_soup = BeautifulSoup(meta_res.content, "lxml")

        # get location
        get_locations = meta_soup.find_all("a", {"class": "subtitle-location-link--1q5zA"})
        ct100_location = ' '.join(str(loc.find("span").text).strip() for loc in get_locations)

        # get price
        ct100_price = meta_soup.find("div", {"class": "amount--3NTpl"}).text

        # get mileages & manufactured year
        get_meta_tags = meta_soup.find_all("div", {"class": "word-break--2nyVq label--3oVZK"})
        for tag in get_meta_tags:
            try:
                if str(tag.text).__contains__("Mileage:"):
                    ct100_mileages = (tag.findNext()).text

                if str(tag.text).__contains__("Year of Manufacture:"):
                    ct100_manu_year = (tag.findNextSibling()).text
            except:
                continue

        return ct100_location, ct100_price, ct100_mileages, ct100_manu_year


def get_average_price_by_location(data_frame):
    # Convert 'Price' column to numeric
    data_frame['Price'] = data_frame['Price'].replace({'Rs ': '', ',': ''}, regex=True).astype(int)

    # grouping and calculating
    avg_price_by_location = data_frame.groupby('Location')['Price'].mean()

    # print(avg_price_by_location)

    return avg_price_by_location


def send_email(html_tbl):
    # Create email
    sender_email = "wmohankavinda@gmail.com"
    receiver_email = "test@gmail.com"
    password = "password123"
    subject = "Latest CT-100 selling data and average prices by Location"

    # Create message container
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach HTML table in email body
    message.attach(MIMEText(html_tbl, "html"))

    # Attach CSV file
    csv_filename = "ct100_metadata.csv"
    with open(csv_filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {csv_filename}")
    message.attach(part)

    # Connect to SMTP server and send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    return True


meta_data = []

with requests.Session() as ss:
    count = 1
    for page_no in range(5):
        page_url = str(base_url) + str(page_no + 1)
        page_response = ss.get(page_url)
        if page_response.status_code == 200:
            main_soup = BeautifulSoup(page_response.content, "lxml")

            ct_100_list = main_soup.find("ul", {"class": "list--3NxGO"})
            # print(len(ct_100_list))
            if ct_100_list:
                while count < 50:
                    for bike in ct_100_list:
                        try:

                            # geta meta data link
                            get_meta_data_link = bike.find("a", {"class": "card-link--3ssYv gtm-ad-item"})["href"]
                            meta_data_link = 'https://ikman.lk' + str(get_meta_data_link)
                            print(meta_data_link)

                            ct100_location, ct100_price, ct100_mileages, ct100_manu_year = meta_data_extraction(
                                meta_url=meta_data_link, req=ss)

                            meta_data.append((count, ct100_location, ct100_price, ct100_manu_year, ct100_mileages))
                            count = count + 1
                        except:
                            continue

    # print(meta_data)

# create dataframe
df_ct100 = pd.DataFrame(meta_data, columns=['Row Number', 'Location', 'Price', 'Years of Manufacture', 'Mileage'])

# Save DataFrame to CSV
df_ct100.to_csv('ct100_metadata1.csv', index=False)

avg_price = get_average_price_by_location(df_ct100)
print(avg_price)
# create html table from average price dataframe
# html_table_avg_price = avg_price.to_html(index=False)



# sending_email = send_email(html_table_avg_price)
