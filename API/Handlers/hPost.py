import json
from API.Handlers.dbConnection import ePost
from API.tools import getResponse, generateError, generateUncorrect, generateUserExist, getParam, generateUnvalidRequest
from API.tools import requirePost, requireGet, getOptional, tryParam, getRelated, getParamRelated, generateNotFound

#1
@requirePost
def createPost(request):
    print "createPostLexaloris"
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    requiredData = ["user", "forum", "thread", "message", "date"]
    optionalData = ["parent", "isApproved", "isHighlighted", "isEdited", "isSpam", "isDeleted"]
    option = getOptional(request=requestData, values=optionalData)
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        createPost = ePost.createPostHelper(date=requestData["date"], thread=requestData["thread"],
                                message=requestData["message"], user=requestData["user"],
                                forum=requestData["forum"], optional=option)
    except Exception as e:
        return generateError(e.message)
    return getResponse(createPost)

#2
@requireGet
def detailPost(request):
    requestData = getParam(request)
    requiredData = ["post"]
    relating = getRelated(requestData)
    dataRelated = ["forum","user","thread"]
    if ( getParamRelated(request, dataRelated) == 1):
        return generateUncorrect()
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        detailPost = ePost.detailsPostHepler(postid = requestData["post"], option=relating)
        if detailPost == 1:
            return generateNotFound()
    except Exception as e:
        return generateError(e.message)
    return getResponse(detailPost)

#3
@requireGet
def listPost(request):
    requestData = getParam(request)
    id = None
    try:
        id = requestData["forum"]
        table = "forum"
    except KeyError:
        try:
            id = requestData["thread"]
            table = "thread"
        except KeyError:
            return generateError("ListPost Error")
    optional = getOptional(request=requestData, values=["limit", "order", "since"])
    try:
        listPost = ePost.listPostHelper(table=table, id=id, related=[], option=optional)
    except Exception as e:
        return generateError(e.message)
    return getResponse(listPost)

#4
@requirePost
def removePost(request):
    requiredData = ["post"]
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        removePost = ePost.removePostHelper(postid=requestData["post"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(removePost)

#5
@requirePost
def restorePost(request):
    requiredData = ["post"]
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        removePost = ePost.restorePostHelper(postid=requestData["post"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(removePost)

#6
@requirePost
def updatePost(request):
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    requiredData = ["post", "message"]
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        updatePost = ePost.updatePostHelper(id=requestData["post"], message=requestData["message"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(updatePost)

#7
@requirePost
def votePost(request):
    requiredData = ["post", "vote"]
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        votePost = ePost.votePostHelper(id=requestData["post"], vote=requestData["vote"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(votePost)