import json
from API.Handlers.dbConnection import eForum, eThread, eUser, ePost
from API.tools import getResponse, generateError, generateUncorrect, generateUserExist, getParam, generateUnvalidRequest
from API.tools import requirePost, requireGet, getOptional, tryParam, getRelated, getParamRelated, getRelated1

#1
@requirePost
def createForum(request):
    requiredData = ["name", "short_name", "user"]
    try:
        requestData = json.loads(request.body)
    except Exception as e:
        return generateUnvalidRequest(e.message)
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        createForum = eForum.createForumHelper(name=requestData["name"], short_name=requestData["short_name"], user=requestData["user"])
    except Exception as e:
        return generateError(e.message)
    return getResponse(createForum)

#2
@requireGet
def detailsForum(request):
    requestData = getParam(request)
    requiredData = ["forum"]
    related = getRelated(requestData)
    dataRelated = ["user"]
    if ( getParamRelated(request, dataRelated) == 1):
        return generateUncorrect()
    print(related)
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        detailForum = eForum.detailForumHelper(short_name=requestData["forum"], related=related)
    except Exception as e:
        return generateError(e.message)
    return getResponse(detailForum)

#3
@requireGet
def listPostsForum(request):
    related = getRelated1(request)
    requestData = getParam(request)
    requiredData = ["forum"]
    optional = getOptional(request=requestData, values=["limit", "order", "since"])
    try:
        if ( tryParam(input=requestData, required=requiredData) == 1):
            return generateUncorrect()
        listPostsForum = ePost.listPostHelper(table="forum", id=requestData["forum"],
                                       related=related, option=optional)
    except Exception as e:
        return generateError(e.message)
    return getResponse(listPostsForum)

#4
@requireGet
def listThreadsForum(request):
    required = ["forum"]
    related = getRelated1(request)
    request = getParam(request)
    optional = getOptional(request=request, values=["limit", "order", "since"])
    try:
        if ( tryParam(input=request, required=required) == 1):
            return generateUncorrect()
        listThreadsForum = eThread.listThreadHelper(table="forum", id=request["forum"], related=related, params=optional)
    except Exception as e:
        return generateError(e.message)
    return getResponse(listThreadsForum)

#5
@requireGet
def listUsersForum(request):
    request_data = getParam(request)
    required_data = ["forum"]
    optional = getOptional(request=request_data, values=["limit", "order", "since_id"])
    try:
        if ( tryParam(input=request_data, required=required_data) == 1):
            return generateUncorrect()
        listUsersForum = eForum.listUsersForumHelper(request_data["forum"], optional)
    except Exception as e:
        return generateError(e.message)
    return getResponse(listUsersForum)