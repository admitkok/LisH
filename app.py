from flask import Flask, render_template, request, url_for, flash, redirect
from datetime import datetime
import random
import string
from repo import Link, repository


class URLShortener:
    def __init__(self):
        pass
        # self.domain = "http://127.0.0.1:5000/"

    def shorten_url(self):
        chars = string.ascii_letters + string.digits
        identifier = ''.join(random.choice(chars) for _ in range(6))
        shortened_url = identifier
        return shortened_url


shortener = URLShortener()


app = Flask(__name__)
app.secret_key = 'your_secret_key'


def remove_table_link(link, page):
    repository.remove_link(link)
    return redirect(url_for(page))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def new_link():
    url = request.form.get('url')
    surl = shortener.shorten_url()
    link = Link(url=url, hash_id=surl, created_at=datetime.utcnow())
    repository.create(link)
    flash(surl, 'info')
    return redirect(url_for('index'))


@app.route('/table')
def table_page():
    links = repository.get()
    return render_template('table.html', links=links, repository=repository)


@app.route('/<hash_id>')
def red_endpoint(hash_id):
    a = repository.get(hash_id)
    repository.update(a, 1)
    return redirect(a.url)


if __name__ == "__main__":
    app.run(debug=True)
