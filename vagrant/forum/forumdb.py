#
# Database access functions for the web forum.
# 
import psycopg2
import bleach


## Database connection
DB = psycopg2.connect("dbname=forum")

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    query_cursor = DB.cursor()

    query_all = "SELECT content, time from posts ORDER BY time ASC;"

    query_cursor.execute(query_all)

    posts = ({'content': str(row[0]), 'time': str(row[1])}
    for row in query_cursor.fetchall())
    #posts = query_cursor.fetchall()
    return posts


## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    bleach_cleaned_content = bleach.clean(content)
    print bleach_cleaned_content
    bleach_linkified_content = bleach.linkify(bleach_cleaned_content)
    print bleach_linkified_content
    insert_cursor = DB.cursor()

    insert_post = """INSERT INTO posts (content) values (%s);"""

    insert_cursor.execute(insert_post, (bleach_linkified_content,))
    insert_cursor.execute("commit;")