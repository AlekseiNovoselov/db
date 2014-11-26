from API.tools import Select, Update, find
from API.Handlers.dbConnection import eUser
from API.Handlers.dbConnection import eForum

#1
def closeThreadHelper(thread):
    find(table="Threads", id="id", value=thread)
    Update("UPDATE Threads SET isClosed = 1 WHERE id = %s", (thread, ))
    response = {
        "thread": thread
    }
    return response
#2
def createThreadHelper(forum, title, isClosed, user, date, message, slug, optional):
    find(table="Users", id="email", value=user)
    find(table="Forums", id="short_name", value=forum)
    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]
    select = Select('select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE slug = %s', (slug, )
    )
    if len(select) == 0:
        Update('INSERT INTO Threads (forum, title, isClosed, user, date, message, slug, isDeleted) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (forum, title, isClosed, user, date, message, slug, isDeleted, )
        )
        select = Select(
            'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
            'FROM Threads WHERE slug = %s', (slug, )
        )
    response = threadFormat(select)
    del response["dislikes"]
    del response["likes"]
    del response["points"]
    del response["posts"]
    return response

def threadFormat(thread):
    thread = thread[0]
    format = {
        'date': str(thread[0]),
        'forum': thread[1],
        'id': thread[2],
        'isClosed': bool(thread[3]),
        'isDeleted': bool(thread[4]),
        'message': thread[5],
        'slug': thread[6],
        'title': thread[7],
        'user': thread[8],
        'dislikes': thread[9],
        'likes': thread[10],
        'points': thread[11],
        'posts': thread[12],
    }
    return format

#3
def detailsThreadHelper(thread, related):
    print ("I am here")
    select = Select(
        'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE id = %s', (thread, )
    )
    if len(select) == 0:
        raise Exception('No thread exists with id=' + str(thread))
    select = threadFormat(select)

    print (related)
    if "user" in related:
        select["user"] = eUser.detailUserHelper(select["user"])
    if "forum" in related:
        select["forum"] = eForum.detailForumHelper(short_name=select["forum"], related=[])

    return select
#4
def listThreadHelper(table, id, related, params):
    if table == "forum":
        find(table="Forums", id="short_name", value=id)
    if table == "user":
        find(table="Users", id="email", value=id)
    select = "SELECT id FROM Threads WHERE " + table + " = %s "
    parameters = [id]

    if "since" in params:
        select += " AND date >= %s"
        parameters.append(params["since"])
    if "order" in params:
        select += " ORDER BY date " + params["order"]
    else:
        select += " ORDER BY date DESC "
    if "limit" in params:
        select += " LIMIT " + str(params["limit"])

    result = Select(query=select, params=parameters)
    threadArray= []

    if u'forum' in related:
            print("Forum in related HElper")
    if u'user' in related:
        print("User in related helper")
    for id in result:
        id = id[0]
        threadArray.append(detailsThreadHelper(thread=id, related=related))
    return threadArray

#5
def listPostsThreadHelper(thread, optional):
    return "Ok"

#6
def openThreadHelper(thread):
    find(table="Threads", id="id", value=thread)
    Update("UPDATE Threads SET isClosed = 0 WHERE id = %s", (thread, ))
    response = {
        "thread": thread
    }
    return response

#7
def removeThreadHelper(threadid):
    find(table="Threads", id="id", value=threadid)
    Update("UPDATE Threads SET isDeleted = 1 WHERE id = %s", (threadid, ))
    postsIds = Select("SELECT id FROM Posts WHERE thread = %s;", (threadid, ))
    for postId in postsIds:
        Update("UPDATE Posts SET isDeleted = 1 WHERE id = %s",(postId, ))
    result = {
        "thread": threadid
    }
    return result

#8
def restoreThreadHelper(threadid):
    find(table="Threads", id="id", value=threadid)
    Update("UPDATE Threads SET isDeleted = 0 WHERE id = %s", (threadid, ))
    postsIds = Select("SELECT id FROM Posts WHERE thread = %s;", (threadid, ))
    for postId in postsIds:
        Update("UPDATE Posts SET isDeleted = 0 WHERE id = %s",(postId, ))
    result = {
        "thread": threadid
    }
    return result

#9
def subscribeThreadHelper(user, thread):
    find(table="Threads", id="id", value=thread)
    find(table="Users", id="email", value=user)
    select = Select('select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (user, thread, ))
    if len(select) == 0:
        Update('INSERT INTO Subscriptions (thread, user) VALUES (%s, %s)', (thread, user, ))
        select = Select('select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (user, thread, ))
    answer = {
        "thread": select[0][0],
        "user": select[0][1]
    }
    return answer

#10
def unsubscribeThreadHelper(user, thread):
    find(table="Threads", id="id", value=thread)
    find(table="Users", id="email", value=user)

    select = Select('select thread, user FROM Subscriptions WHERE user = %s AND thread = %s', (user, thread, ))
    if len(select) == 0:
        raise Exception("user " + user + " does not subscribe thread #" + str(thread))
    Update('DELETE FROM Subscriptions WHERE user = %s AND thread = %s', (user, thread, ))

    answer = {
        "thread": select[0][0],
        "user": select[0][1]
    }
    return answer

#11
def updateThreadHelper(thread, slug, message):
    find(table="Threads", id="id", value=thread)
    Update('UPDATE Threads SET slug = %s, message = %s WHERE id = %s', (slug, message, thread, ))

    return detailsThreadHelper(thread=thread, related=[])

#12
def voteThreadHelper(thread, value):
    find(table="Threads", id="id", value=thread)
    if value == -1:
        Update("UPDATE Threads SET dislikes=dislikes+1, points=points-1 where id = %s", (thread, ))
    else:
        Update("UPDATE Threads SET likes=likes+1, points=points+1  where id = %s", (thread, ))
    return detailsThreadHelper(thread=thread, related=[])
