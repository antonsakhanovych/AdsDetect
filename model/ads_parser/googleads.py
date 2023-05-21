import sys

from bs4 import BeautifulSoup
import requests, lxml, json

#request = sys.argv[1]
url = sys.argv[1]

params = {
    "hl": "en",
    "gl": "us"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36",
}

if __name__ == "__main__":
    #html = requests.get("https://www.google.com/search?", params=params, headers=headers)
    html = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(html.text, "lxml")

    ad_results = []

    for index, ad_result in enumerate(soup.select(".uEierd"), start=1):
        try:
            title = ad_result.select_one(".v0nnCb span").text
        except Exception as e:
            title = ""
        website_link = ad_result.select_one("a.sVXRqc")["data-pcu"]
        ad_link = ad_result.select_one("a.sVXRqc")["href"]
        try:
            displayed_link = ad_result.select_one(".qzEoUe").text
        except Exception as e:
            displayed_link = ""
        tracking_link = ad_result.select_one(".v5yQqb a.sVXRqc")["data-rw"]
        try:
            snippet = ad_result.select_one(".MUxGbd div span").text
        except Exception as e:
            snippet = ""
        phone = None if ad_result.select_one("span.fUamLb span") is None else ad_result.select_one("span.fUamLb span") .text

        inline_link_text = [title.text for title in ad_result.select("div.bOeY0b .XUpIGb a")]
        inline_link = [link["href"] for link in ad_result.select("div.bOeY0b .XUpIGb a")]

        ad_results.append({
            "position": index,
            "title": title,
            "phone": phone,
            "website_link": website_link,
            "displayed_link": displayed_link,
            "ad_link": ad_link,
            "tracking_link": tracking_link,
            "snippet": snippet,
            "sitelinks": [{"titles": inline_link_text, "links": inline_link}]
        })

    print(json.dumps(ad_results, indent=2))
