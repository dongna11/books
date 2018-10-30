from adminbook.models import TRoot


def mydata(request):
    #接受数据
    rootname=request.POST.get('name',' ')

    return {'rootname':rootname}