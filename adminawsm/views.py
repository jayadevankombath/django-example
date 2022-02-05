from django.http import HttpResponse, JsonResponse

from coupons import models as coupon_models

def coupons_list(request):
    """ List all coupons """

    if request.method == 'GET':
        couponObjs = coupon_models.Coupon.objects.all().values()
        coupon_list = list(couponObjs)
        return JsonResponse(coupon_list, safe=False)
    else:
        return HttpResponse("Method Not Allowed", content_type="text/plain", status=405)

def coupons_add(request):

    if request.method == 'POST':
        cpn_code = request.POST['coupon_code']
        exp_date = request.POST['expire_date']
        type = request.POST['coupon_type']
        offer = request.POST['offer_value']
        cpn_desc = request.POST['coupon_description']

        couponObj =  coupon_models.Coupon.objects.create(
            coupon_code = cpn_code,
            expiry_date = exp_date,
            offer_value = offer,
            coupon_description = cpn_desc)

        if type == 'Percentage':
            couponObj.type = coupon_models.Coupon.Types.PERCENTAGE
            couponObj.save()
        else:
            couponObj.save()
    
    return HttpResponse("Method Not Allowed", content_type="text/plain", status=405)

def coupon_edit(request, **kwargs):
    """ Edit coupon """

    if request.method == 'GET':
        coupon_id = kwargs['id']
        couponObjs = coupon_models.Coupon.objects.filter(id=coupon_id).values()
        coupon = list(couponObjs)

        return JsonResponse(coupon, safe=False, status=200)

    return HttpResponse("Method Not Allowed", content_type="text/plain", status=405)

def update_coupon(request, **kwargs):
    """ Update coupon """

    cpn_id = kwargs['id']

    if request.method == 'POST':
        try:
            couponObj = coupon_models.Coupon.objects.get(id=cpn_id)
            couponObj.coupon_code = request.POST['coupon_code']
            couponObj.expiry_date = request.POST['expire_date']
            couponObj.offer_value = request.POST['offer_value']
            couponObj.coupon_description = request.POST['coupon_description']

            cpn_type = request.POST['coupon_type']

            if cpn_type == 'Percentage':
                couponObj.type =  coupon_models.Coupon.Types.PERCENTAGE
                couponObj.save()
            else:
                couponObj.save()

            return coupons_list(request)

        except Exception as e:
            return HttpResponse(e, content_type="text/plain")
    else:
        return HttpResponse("Method Not Allowed", content_type="text/plain", status=405)

def coupon_approve(request, **kwargs):
    """ Coupon approve """

    cpn_id = kwargs['id']
    couponObj = coupon_models.Coupon.objects.get(id=cpn_id)
    couponObj.status = coupon_models.Coupon.Status.APPROVED
    couponObj.save()

    return coupons_list(request)

def coupon_delete(request, **kwargs):
    """ Delete coupon """

    cpn_id = kwargs['id']
    couponObj = coupon_models.Coupon.objects.get(id=cpn_id)
    couponObj.delete()

    return coupons_list(request)

