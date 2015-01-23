from API.tools import Select, Update, find

# 1
def createUserHelper(email, username, about, name, optional):
    try:
        isAnonymous = 0
        if "isAnonymous" in optional:
            isAnonymous = optional["isAnonymous"]
        if Update(
                'INSERT INTO Users (email, about, name, username, isAnonymous) VALUES (%s, %s, %s, %s, %s)',
                (email, about, name, username, isAnonymous, )) != -1:
            user = Select('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s',
                          (email, ))
        else:
            return 1
    except Exception as e:
        raise Exception(e.message)

    return userFormat(user)


def userFormat(user):
    user = user[0]
    user_response = {
        'about': user[1],
        'email': user[0],
        'id': user[3],
        'isAnonymous': bool(user[2]),
        'name': user[4],
        'username': user[5]
    }
    return user_response


#2
def followerListHelper(email, type):
    where = "followee"
    if type == "followee":
        where = "follower"
    tmp = Select("SELECT " + type + " FROM Followers WHERE " + where + " = %s ", (email, ))
    result = []
    if tmp != 0:
        for el in tmp:
            result.append(el[0])
    print result
    return result


def userInThreadHelper(email):
    s_list = []
    subscriptions = Select('select thread FROM Subscriptions WHERE user = %s', (email, ))
    if subscriptions != 0:
        for el in subscriptions:
            s_list.append(el[0])
    return s_list


def detailUserHelper(email):
    tmp = (Select('select email, about, isAnonymous, id, name, username FROM Users WHERE email = %s', (email, )))
    print tmp
    if len(tmp) == 1:
        user = userFormat(tmp)
        print user
        user["followers"] = followerListHelper(email, "follower")
        print "1"
        user["following"] = followerListHelper(email, "followee")
        print "2"
        user["subscriptions"] = userInThreadHelper(email)
        print "3"
    else:
        return 1
    return user


#4
def listFollowersUserHelper(email, fol1, optional):
    find(table="Users", id="email", value=email)
    if fol1 == "followee":
        fol2 = "follower"
    else:
        fol2 = "followee"

    query = "SELECT Users.email, about, isAnonymous, Users.id, name, username FROM Followers JOIN Users ON Users.email = Followers." + fol1 + \
            " WHERE " + fol2 + " = %s "
    resultArray = []
    if "since_id" in optional:
        query += " AND Users.id >= " + str(optional["since_id"])
    if "order" in optional:
        query += " ORDER BY Users.name " + optional["order"]
    else:
        query += " ORDER BY Users.name DESC "
    if "limit" in optional:
        query += " LIMIT " + str(optional["limit"])

    resultSelect = Select(query=query, params=(email, ))

    for tmp in resultSelect:
        user = {
            'about' : tmp[1],
            'email' : tmp[0],
            'id' : tmp[3],
            'isAnonymous' : tmp[2],
            'name' : tmp[4],
            'username' : tmp[5],
            "followers" : followerListHelper(tmp[0], "follower"),
            "following" : followerListHelper(tmp[0], "followee"),
            "subscriptions" : userInThreadHelper(tmp[0])
        }
        resultArray.append(user)
    return resultArray

#3
def followUserHelper(email1, email2):
    Update('INSERT INTO Followers (follower, followee) VALUES (%s, %s)', (email1, email2, ))
    return detailUserHelper(email1)


#7
def unfollowUserHelper(email1, email2):
    Update('DELETE FROM Followers WHERE follower = %s AND followee = %s', (email1, email2, ))
    return detailUserHelper(email1)


#8
def updateUserProfileHelper(email, about, name):
    Update('UPDATE Users SET email = %s, about = %s, name = %s WHERE email = %s',
           (email, about, name, email, ))
    return detailUserHelper(email)





