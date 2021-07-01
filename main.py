from flask import Flask, render_template, request, redirect, url_for

from amazon import amazon_crawler
from noon import noon_crawler

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('amazon-price.html')


@app.route('/amazon-scrape', methods=['GET', 'POST'])
def amazon_scrape():
    if request.method == 'POST':

        url = request.form['url']
        if url == '':
            return render_template('amazon-price.html', message='Please enter required fields')

        split_url = url.split("/")
        table_data = {}

        print(split_url)

        for item in split_url:
            if "B0" in item:
                table_data = amazon_crawler(url)
            elif "N" in item:
                table_data = noon_crawler(url)

        return render_template('amazon-price.html', table_data=table_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.debug(True)
