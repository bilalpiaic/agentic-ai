

def post_data(post_id):
    return {
        "id": post_id,
        "title": f"Post {post_id}",
        "content": f"Content of post {post_id}"
    }


def filter_posts(posts, search_query):
    return [post for post in posts if search_query in post['title'] or search_query in post['content']]