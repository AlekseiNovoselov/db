from API.tools import Select, Update, find
from API.Handlers.dbConnection import eUser

# 1
def createForumHelper(name, short_name, user):
    Update('INSERT INTO Forums (name, short_name, user) VALUES (%s, %s, %s)', (name, short_name, user, ))
    result = Select('select id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name, ))
    return ForumFormat(result)


def ForumFormat(forum):
    forum = forum[0]
    response = {
        'id': forum[0],
        'name': forum[1],
        'short_name': forum[2],
        'user': forum[3]
    }
    return response


#2
def detailForumHelper(short_name, related):
    result = Select('select id, name, short_name, user FROM Forums WHERE short_name = %s', (short_name,))
    if len(result) == 0:
        raise ("Cant find  forum " + short_name)
    result = ForumFormat(result)

    if "user" in related:
        result["user"] = eUser.detailUserHelper(result["user"])
    return result


#5
def listUsersForumHelper(short_name, optional):
    select = "SELECT distinct email FROM Users JOIN Posts ON Posts.user = Users.email " \
             " JOIN Forums on Forums.short_name = Posts.forum WHERE Posts.forum = %s "
    if "since_id" in optional:
        select += " AND Users.id >= " + str(optional["since_id"])
    if "order" in optional:
        select += " ORDER BY Users.name " + optional["order"]
    else:
        select += " ORDER BY Users.name DESC"
    if "limit" in optional:
        select += " LIMIT " + str(optional["limit"])

    resultArray = []
    result = Select(select, (short_name, ))
    if result != 0:
        for user in result:
            user = user[0]
            resultArray.append(eUser.detailUserHelper(user))
    return resultArray



