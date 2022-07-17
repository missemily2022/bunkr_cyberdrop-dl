from bs4 import BeautifulSoup
import cloudscraper
import json

# Accepting Bunkr/CyberDrop URL from User
url = input("Enter your Bunkr/CyberDrop URL : ")

def bunkr_cyber(url):
    count = 1
    dl_msg = ""
    client = cloudscraper.create_scraper(allow_brotli=False)

    if "bunkr" in url:
        link_type = "Bunkr"
    elif "cyberdrop" in url: 
        link_type = "CyberDrop"
    else:
        return "\nURL Entered is not Supported!\n"
        exit()

    resp = client.get(url)
    if resp.status_code == 404:
        return "File not found/The link you entered is wrong!"
    soup = BeautifulSoup(resp.content, "html.parser")

    if link_type == "Bunkr":
        if "stream.bunkr.is" in url:
            return url.replace("stream.bunkr.is/v", "media-files.bunkr.is")
        json_data_element = soup.find("script", {"id": "__NEXT_DATA__"})
        json_data = json.loads(json_data_element.string)
        files = json_data["props"]["pageProps"]["files"]
        for file in files:
            item_url = "https://media-files.bunkr.is/" + file["name"]
            item_url = item_url.replace(" ", "%20")
            dl_msg += f"{count}. {item_url}\n"
            count += 1
    else:
        items = soup.find_all("a", {"class": "image"})
        for item in items:
            item_url = item["href"]
            item_url = item_url.replace(" ", "%20")
            dl_msg += f"{count}. {item_url}\n"
            count += 1
    fld_msg = f"Your provided {link_type} link is of Folder and I've Found {count - 1} files in the folder.\n"
    fld_link = f"\nFolder Link: {url}\n"
    final_msg = fld_link + "\n" + fld_msg + "\n" + dl_msg
    return final_msg

print(bunkr_cyber(url=url))