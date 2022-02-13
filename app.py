from flask import Flask, request, render_template, send_from_directory, redirect

from functions import find_tags, find_posts_by_tag, save_to_json

UPLOAD_FOLDER = "uploads/images"

app = Flask(__name__)


@app.route("/")
def page_index():
    tags = find_tags()

    return render_template('index.html', tags=tags)


@app.route("/tag")
def page_tag():
    tag = request.args.get("tag")
    posts = find_posts_by_tag(tag)

    return render_template('post_by_tag.html', tag=tag, posts=posts)


@app.route("/post", methods=["GET", "POST"])
def page_post_create():
    if request.method == "GET":
        return render_template('post_form.html')
    else:
        content = request.form.get("content")
        pic = request.files.get("picture")
        if not pic:
            return redirect("/post")

        picture_name = pic.filename

        if picture_name.split(".")[1].lower() not in ["jpg", "png", "jpeg"]:
            return "ошибка загрузки"

        path = UPLOAD_FOLDER + "/" + picture_name
        pic.save(path)
        pic_path = "/" + UPLOAD_FOLDER + "/" + picture_name

        post = {
            "pic": pic_path,
            "content": content
        }

        if not save_to_json(post):
            return "ошибка загрузки"

        return render_template('post_uploaded.html', post=post)


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


if __name__ == "__main__":
    app.run(debug=True)
