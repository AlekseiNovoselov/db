from API.tools import Select, Update, find
from API.Handlers.dbConnection import eUser
from API.Handlers.dbConnection import eForum


#2
def createThreadHelper(forum, title, isClosed, user, date, message, slug, optional):
    isDeleted = 0
    if "isDeleted" in optional:
        isDeleted = optional["isDeleted"]
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

def threadFormat2(thread):
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
    select = Select(
        'select date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts '
        'FROM Threads WHERE id = %s', (thread, )
    )
    if len(select) == 0:
        raise Exception('No thread exists with id=' + str(thread))
    select = threadFormat(select)

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
    select = "SELECT date, forum, id, isClosed, isDeleted, message, slug, title, user, dislikes, likes, points, posts FROM Threads WHERE " + table + " = %s "
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
    if result != 0:
        for tmp in result:
            answer = threadFormat2(tmp)
            if "user" in related:
                answer["user"] = eUser.detailUserHelper(answer["user"])
            if "forum" in related:
                answer["forum"] = eForum.detailForumHelper(short_name=answer["forum"], related=[])
            threadArray.append(answer)
    return threadArray

#7
def removeThreadHelper(threadid):
    Update("UPDATE Threads SET isDeleted = 1, posts = 0 WHERE id = %s", (threadid, ))
    postsIds = Select("SELECT id FROM Posts WHERE thread = %s;", (threadid, ))
    for postId in postsIds:
        Update("UPDATE Posts SET isDeleted = 1 WHERE id = %s",(postId, ))
    result = {
        "thread": threadid
    }
    return result

#8
def restoreThreadHelper(threadid):
    postsIds = Select("SELECT id FROM Posts WHERE thread = %s;", (threadid, ))
    if postsIds == 0:
        par = 0
    else:
        par = len(postsIds)
    Update("UPDATE Threads SET isDeleted = 0, posts = %s WHERE id = %s", (par, threadid, ))
    for postId in postsIds:
        Update("UPDATE Posts SET isDeleted = 0 WHERE id = %s",(postId, ))
    result = {
        "thread": threadid
    }
    return result

#1
def closeThreadHelper(thread):
    Update("UPDATE Threads SET isClosed = 1 WHERE id = %s", (thread, ))
    response = { "thread": thread }
    return response

#6
def openThreadHelper(thread):
    Update("UPDATE Threads SET isClosed = 0 WHERE id = %s", (thread, ))
    response = { "thread": thread }
    return response


#9
def subscribeThreadHelper(user, thread):
    Update('INSERT INTO Subscriptions (thread, user) VALUES (%s, %s)', (thread, user, ))
    answer = { "thread": thread, "user": user }
    return answer

#10
def unsubscribeThreadHelper(user, thread):
    Update('DELETE FROM Subscriptions WHERE user = %s AND thread = %s', (user, thread, ))
    answer = { "thread": thread, "user": user }
    return answer

#11
def updateThreadHelper(thread, slug, message):
    Update('UPDATE Threads SET slug = %s, message = %s WHERE id = %s', (slug, message, thread, ))
    return detailsThreadHelper(thread=thread, related=[])

#12
def voteThreadHelper(thread, value):
    if value == -1:
        Update("UPDATE Threads SET dislikes=dislikes+1, points=points-1 where id = %s", (thread, ))
    else:
        Update("UPDATE Threads SET likes=likes+1, points=points+1  where id = %s", (thread, ))
    return detailsThreadHelper(thread=thread, related=[])
