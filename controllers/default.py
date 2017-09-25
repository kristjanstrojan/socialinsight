from insights.intelligentor import Intelligentor

@auth.requires_login()
def index():
    return dict()

@auth.requires_login()
def search():
    if request.vars.search:
        search = request.vars.search
        print(search)
        result = Intelligentor(search)
        return dict(result=result)


@auth.requires_login()
def _add_search():
    '''
    Adds a serach to a database.
    '''

    if request.vars:
        name          = request.vars.intel_name
        description   = request.vars.intel_description
        isearch       = request.vars.intel_search

        db.intel_search.insert(
            name=name,
            description=description,
            isearch=isearch
        )
        db.commit()

        return True
    else:
        return False


@auth.requires_login()
def _searches():
    result = db().select(db.intel_search.ALL)
    return dict(result=result)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
