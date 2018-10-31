from adminbook.models import TRoot
import jsonpickle

def mainfunc(request):
    user = request.session.get('user','')

    if user:
        user = jsonpickle.loads(user)

    return {"user":user}
