from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


def fetch_post_by_id(post_id):
    """Fetch a single post by its ID from the JSON file."""
    with open('data.json', 'r') as f:
        blog_posts = json.load(f)
    return next((p for p in blog_posts if p['id'] == post_id), None)


@app.route('/')
def index():
    """Display all blog posts."""
    with open('data.json', 'r') as f:
        blog_posts = json.load(f)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new blog post."""
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
    """Delete a blog post by its ID."""
    with open('data.json', 'r') as f:
        blog_posts = json.load(f)

    blog_posts = [p for p in blog_posts if p['id'] != post_id]

    with open('data.json', 'w') as f:
        json.dump(blog_posts, f)

    return redirect(url_for('index'))


@app.route('/like/<int:post_id>')
def like(post_id):
    """Increment the like count of a blog post."""
    with open('data.json', 'r') as f:
        blog_posts = json.load(f)

    for p in blog_posts:
        if p['id'] == post_id:
            p['likes'] += 1

    with open('data.json', 'w') as f:
        json.dump(blog_posts, f)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update an existing blog post."""
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        with open('data.json', 'r') as f:
            blog_posts = json.load(f)

        for p in blog_posts:
            if p['id'] == post_id:
                p['title'] = request.form.get('title')
                p['author'] = request.form.get('author')
                p['content'] = request.form.get('content')

        with open('data.json', 'w') as f:
            json.dump(blog_posts, f)

        return redirect(url_for('index'))

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)