from flask import Flask, render_template, request, redirect, url_for

from amazon import amazon_crawler
from noon import noon_crawler
from rustoleum_batch_code import convert_batch_to_mfg

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template('amazon-price.html')


@app.route("/rustoleum-batch-code", methods=['GET'])
def rustoleum_batch_code():
    return render_template('rustoleum-batch-code.html')


@app.route("/compute-batch-code", methods=['POST'])
def compute_batch_code():
    if request.method == 'POST':

        batch_code = request.form['batchCode']
        if batch_code == '':
            return render_template('rustoleum-batch-code.html', message='Please enter required fields')

        split_batch_code = batch_code.split(",")
        print(split_batch_code)
        batch_codes = convert_batch_to_mfg(batch_code)

        print(batch_codes)

    return render_template('rustoleum-batch-code.html', batch_codes=[])


@app.route('/crawler', methods=['GET', 'POST'])
def crawler():
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
                break
            elif "N" in item:
                table_data = noon_crawler(url)
                break

        return render_template('amazon-price.html', table_data=table_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.debug(True)
