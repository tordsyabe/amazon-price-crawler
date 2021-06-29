from flask import Flask, render_template, request, redirect, url_for


from amazon_crawler import AmazonCrawler
from amazon import price_crawler

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

        # data = AmazonCrawler(url).price_crawler()
        data = price_crawler(url)

        return render_template('amazon-price.html', table_data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.debug(True)
