from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('data.json', 'r') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        with open('data.json', 'r') as f:
            blog_posts = json.load(f)

        new_post = {
            "id": len(blog_posts) + 1,
            "title": title,
            "author": author,
            "content": content
        }

        blog_posts.append(new_post)

        with open('data.json', 'w') as f:
            json.dump(blog_posts, f)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    with open('data.json', 'r') as f:
        blog_posts = json.load(f)

    blog_posts = [p for p in blog_posts if p['id'] != post_id]

    with open('data.json', 'w') as f:
        json.dump(blog_posts, f)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)