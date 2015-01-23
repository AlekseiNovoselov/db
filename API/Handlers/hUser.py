import json
from API.Handlers.dbConnection import eUser, ePost
from API.tools import getResponse, generateError, generateUncorrect, generateUserExist, getParam, generateUnvalidRequest
from API.tools import requirePost, requireGet, getOptional, tryParam

#1
@requirePost
def createUser(request):
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    requiredData = ["email", "username", "name", "about"]
    option = getOptional(request=requestData, values=["isAnonymous"])
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        createUser = eUser.createUserHelper(email=requestData["email"], username=requestData["username"],
                               about=requestData["about"], name=requestData["name"], optional=option)
        if createUser == 1:
            return generateUserExist()
    except Exception as e:
        return generateError(e.message)
    return getResponse(createUser)

#2
@requireGet
def detailsUser(request):
    print "detail user"
    requestData = getParam(request)
    print requestData
    requiredData = ["user"]
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            print "error here"
            return generateUncorrect()
        print "here"
        detailsUser = eUser.detailUserHelper(email=requestData["user"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(detailsUser)

#3
@requirePost
def followUser(request):
    requiredData = ["follower", "followee"]
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        followUser = eUser.followUserHelper(email1=requestData["follower"], email2=requestData["followee"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(followUser)

#4
@requireGet
def listFollowers(request):
    requestData = getParam(request)
    requiredData = ["user"]
    param = getOptional(request=requestData, values=["limit", "order", "since_id"])
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        listFollowers = eUser.listFollowersUserHelper(email=requestData["user"], fol1="follower", optional=param)
    except Exception as e:
        return generateError(e.message)
    return getResponse(listFollowers)

#5
@requireGet
def listFollowing(request):
    requestData = getParam(request)
    requiredData = ["user"]
    param = getOptional(request=requestData, values=["limit", "order", "since_id"])
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        listFollowing = eUser.listFollowersUserHelper(email=requestData["user"], fol1="followee", optional=param)
    except Exception as e:
        return generateError(e.message)
    return getResponse(listFollowing)

#6
@requireGet
def listPost(request):
    requestData = getParam(request)
    requiredData = ["user"]
    option = getOptional(request=requestData, values=["limit", "order", "since"])
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        listPost = ePost.listPostHelper(table="user", id=requestData["user"], related=[], option=option)
    except Exception as e:
        return generateError(e.message)
    return getResponse(listPost)

#7
@requirePost
def unfollowUser(request):
    requiredData = ["follower", "followee"]
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        unfollowUser = eUser.unfollowUserHelper(email1=requestData["follower"], email2=requestData["followee"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(unfollowUser)

#8
@requirePost
def updateProfile(request):
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    requiredData = ["user", "name", "about"]
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        updateProfile = eUser.updateUserProfileHelper(email=requestData["user"], name=requestData["name"], about=requestData["about"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(updateProfile)
