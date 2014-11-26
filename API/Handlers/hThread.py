import json
from API.Handlers.dbConnection import eThread
from API.Handlers.dbConnection import ePost
from API.tools import getResponse, generateError, generateUncorrect, getParam, generateUnvalidRequest
from API.tools import requirePost, requireGet, getOptional, tryParam, getRelated, getParamRelated

#1
@requirePost
def closeThread(request):
    requiredData = ["thread"]
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        closeThread = eThread.closeThreadHelper(thread=requestData["thread"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(closeThread)

#2
@requirePost
def createThread(request):
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    requiredData = ["forum", "title", "isClosed", "user", "date", "message", "slug"]
    option = getOptional(request=requestData, values=["isDeleted"])
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        createThread = eThread.createThreadHelper(forum=requestData["forum"], title=requestData["title"], isClosed=requestData["isClosed"],
                                     user=requestData["user"], date=requestData["date"], message=requestData["message"],
                                     slug=requestData["slug"], optional=option)
    except Exception as e:
        return generateError(e.message)
    return getResponse(createThread)

#3
@requireGet
def detailsThread(request):
    requestData = getParam(request)
    requiredData = ["thread"]
    related = getRelated(requestData)
    dataRelated = ["user","forum"]
    if ( getParamRelated(request, dataRelated) == 1):
        return generateUncorrect()
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        detailsThread = eThread.detailsThreadHelper(thread=requestData["thread"],related=related)
    except Exception as e:
        return generateError(e.message)
    return getResponse(detailsThread)

#4
@requireGet
def listThread(request):
    requestData = getParam(request)
    id = None
    try:
        id = requestData["forum"]
        table = "forum"
    except KeyError:
        try:
            id = requestData["user"]
            table = "user"
        except KeyError:
            return generateError("No user or forum parameters setted")
    optional = getOptional(request=requestData, values=["limit", "order", "since"])
    try:
        listThread = eThread.listThreadHelper(table=table, id=id, related=[], params=optional)
    except Exception as e:
        return generateError(e.message)
    return getResponse(listThread)

#5
@requireGet
def listPostsThread(request):
    requestData = getParam(request)
    requiredData = ["thread"]
    table = "thread"
    optional = getOptional(request=requestData, values=["limit", "order", "since"])
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        listPostThread = ePost.listPostHelper(table=table, id=requestData["thread"], related=[], option=optional)
    except Exception as e:
        return generateError(e.message)
    return getResponse(listPostThread)

#6
@requirePost
def openThread(request):
    requiredData = ["thread"]
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        openThread = eThread.openThreadHelper(thread=requestData["thread"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(openThread)

#7
@requirePost
def removeThread(request):
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    requiredData = ["thread"]
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        removeThread = eThread.removeThreadHelper(threadid=requestData["thread"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(removeThread)

#8
@requirePost
def restoreThread(request):
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    requiredData = ["thread"]
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        restoreThread = eThread.restoreThreadHelper(threadid=requestData["thread"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(restoreThread)

#9
@requirePost
def subscribeThread(request):
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    requiredData = ["thread", "user"]
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        subscribeThread = eThread.subscribeThreadHelper(user=requestData["user"], thread=requestData["thread"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(subscribeThread)

#10
@requirePost
def unsubscribeThread(request):
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    requiredData = ["thread", "user"]
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        subscribeThread = eThread.unsubscribeThreadHelper(user=requestData["user"], thread=requestData["thread"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(subscribeThread)

#11
@requirePost
def updateThread(request):
    requiredData = ["thread", "slug", "message"]
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        updateThread = eThread.updateThreadHelper(thread=requestData["thread"], slug=requestData["slug"], message=requestData["message"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(updateThread)

#12
@requirePost
def voteThread(request):
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    requiredData = ["thread", "vote"]
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        voteThread = eThread.voteThreadHelper(thread=requestData["thread"], value=requestData["vote"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(voteThread)