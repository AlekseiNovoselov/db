from API.tools import Select, Update, find
from API.connection import connect
from API.Handlers.dbConnection import eForum, eUser, eThread

#1
def createPostHelper(date, thread, message, user, forum, optional):
    find(table="Threads", id="id", value=thread)
    find(table="Forums", id="short_name", value=forum)
    find(table="Users", id="email", value=user)
    parentTmp = ""
    if len(Select("SELECT Threads.id FROM Threads JOIN Forums ON Threads.forum = Forums.short_name "
                                "WHERE Threads.forum = %s AND Threads.id = %s", (forum, thread, ))) == 0:
        raise Exception("no thread with id = " + thread + " in forum " + forum)
    if "parent" in optional:
        tmp = Select("SELECT Posts.id FROM Posts JOIN Threads ON Threads.id = Posts.thread "
                             "WHERE Posts.id = %s AND Threads.id = %s", (optional["parent"], thread, ))
        if len(tmp) == 0:
            raise Exception("Cant find post with id = " + optional["parent"])
        else:
            parentTmp = str(tmp[0][0])
    query = "INSERT INTO Posts (message, user, forum, thread, date"
    values = "(%s, %s, %s, %s, %s"
    parameters = [message, user, forum, thread, date]

    for param in optional:
        query += ", "+param
        values += ", %s"
        parameters.append(optional[param])

    query += ", mathPath"
    values += ", %s"
    a = Select("Select id from Forums where short_name = %s", (forum, ))

    var = str(a[0][0]) + "." + str(thread)
    if len(parentTmp) != 0:
        var += "." + parentTmp
    parameters.append(var)

    query += ") VALUES " + values + ")"

    update = "UPDATE Threads SET posts = posts + 1 WHERE id = %s"


    print("\n\n\n\n")
    print(query)
    print("\n\n\n\n")

    connection = connect()
    with connection:
        cursor = connection.cursor()
        try:
            connection.begin()
            cursor.execute(update, (thread, ))
            cursor.execute(query, parameters)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise Exception("Database error: " + e.message)
        post_id = cursor.lastrowid
        cursor.close()

    connection.close()
    post = postQueryHelper(post_id)
    del post["dislikes"]
    del post["likes"]
    del post["parent"]
    del post["points"]
    return post

def postQueryHelper(id):
    select = Select('select date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, parent, points, thread, user FROM Posts WHERE id = %s', (id, ))
    if len(select) == 0:
        return None
    return postFormat(select)

def postFormat(post):
    post = post[0]
    response = {
        'date': str(post[0]),
        'dislikes': post[1],
        'forum': post[2],
        'id': post[3],
        'isApproved': bool(post[4]),
        'isDeleted': bool(post[5]),
        'isEdited': bool(post[6]),
        'isHighlighted': bool(post[7]),
        'isSpam': bool(post[8]),
        'likes': post[9],
        'message': post[10],
        'parent': post[11],
        'points': post[12],
        'thread': post[13],
        'user': post[14],
    }
    return response

#2
def detailsPostHepler(postid, option):
    post = postQueryHelper(postid)
    if post is None:
        return 1

    if "user" in option:
        post["user"] = eUser.detailUserHelper(post["user"])
    if "forum" in option:
        post["forum"] = eForum.detailForumHelper(short_name=post["forum"], related=[])
    if "thread" in option:
        post["thread"] = eThread.detailsThreadHelper(thread=post["thread"], related=[])

    return post

#3
def listPostHelper(table, id, related, option):
    if table == "user":
        find(table="Users", id="email", value=id)
    if table == "forum":
        find(table="Forums", id="short_name", value=id)
    if table == "thread":
        find(table="Threads", id="id", value=id)
    select = "SELECT id FROM Posts WHERE " + table + " = %s "
    par = [id]
    if "since" in option:
        select += " AND date >= %s"
        par.append(option["since"])
    if "order" in option:
        select += " ORDER BY date " + option["order"]
    else:
        select += " ORDER BY date DESC "
    if "limit" in option:
        select += " LIMIT " + str(option["limit"])
    query = Select(query=select, params=par)
    post_list = []
    for id in query:
        id = id[0]
        post_list.append(detailsPostHepler(postid=id, option=related))
    return post_list

#4
def removePostHelper(postid):
    find(table="Posts", id="id", value=postid)
    Update("UPDATE Threads SET posts = posts - 1 WHERE id = (SELECT thread FROM Posts WHERE id = %s)", (postid, ))
    Update("UPDATE Posts SET isDeleted = true WHERE Posts.id = %s", (postid, ))
    return {
        "post": postid
    }

#5
def restorePostHelper(postid):
    find(table="Posts", id="id", value=postid)
    Update("UPDATE Threads SET posts = posts + 1 WHERE id = (SELECT thread FROM Posts WHERE id = %s)", (postid, ))
    Update("UPDATE Posts SET isDeleted = false WHERE Posts.id = %s", (postid, ))
    return {
        "post": postid
    }

#6
def updatePostHelper(id, message):
    find(table="Posts", id="id", value=id)
    Update('UPDATE Posts SET message = %s WHERE id = %s', (message, id, ))
    return detailsPostHepler(postid=id, option=[])

#7
def votePostHelper(id, vote):
    find(table="Posts", id="id", value=id)
    if vote == -1:
        Update("UPDATE Posts SET dislikes=dislikes+1, points=points-1 where id = %s", (id, ))
    else:
        Update("UPDATE Posts SET likes=likes+1, points=points+1  where id = %s", (id, ))
    return detailsPostHepler(postid=id, option=[])
