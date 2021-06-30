url = "https://www.amazon.ae/LOr%C3%A9al-Paris-Genius-Liquid-Moisturizer/dp/B07THLXZ59/ref=pd_bxgy_img_1/262-2641682-7355801?pd_rd_w=l6M5O&pf_rd_p=05f87c23-5f2e-4598-9ad2-99763df8de3e&pf_rd_r=W2H8J0XN8DBAHH2K4TD6&pd_rd_r=01d4b5bb-126f-4208-9971-0bb4a9164d92&pd_rd_wg=xbSIA&pd_rd_i=B07THLXZ59&psc=1"
url2 = "https://www.noon.com/uae-en/playstation-5-console-disc-version/N40633047A/p?o=fcb86993a7e25ded"

urls = url.split("/")
urls2 = url2.split("/")

print(urls2)

for item in urls2:
    if "B0" in item:
        print(item)
        break

