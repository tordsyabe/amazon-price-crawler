url = "https://www.noon.com/uae-en/galaxy-tab-a-2019-8-0-inch-32gb-2gb-ram-wi-fi-4g-lte-black/N29806819A/p?o=e2b47c5875da809a"

urls = url.split("/")

print(urls)

if len(urls) > 1:
    for item in urls:

        if "www." in item:
            webpage = item
        if "N2" in item:
            asin = item

print(webpage, asin)