from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
import shortuuid
from api.models import ShortURL, TargetDevice
import json


@csrf_exempt
def index(req):
    if req.method == 'GET':
        return list_short_urls(req)
    elif req.method == 'POST':
        return create_short_url(req)


def create_short_url(req):
    body = json.loads(req.body.decode('utf-8'))

    if 'data' not in body:
        return JsonResponse({'error': 'Bad Request'}, status=400)

    data = body['data']

    if 'url' not in data:
        return JsonResponse({'error': 'Bad Request'}, status=400)

    short_url = ShortURL.objects.create(
        short_url=shortuuid.uuid(),
        target_url=data['url']
    )

    if 'devices' in data:
        for device_type, url in data['devices'].items():
            device_id = TargetDevice.device_name_to_id(device_type)
            if device_id is None:
                continue
            TargetDevice.objects.create(
                url=url,
                device_type=device_id,
                short_url=short_url
            )

    return JsonResponse({'data': short_url.as_dict()})


def list_short_urls(req):
    urls = ShortURL.objects.all()
    res = [obj.as_dict() for obj in urls]

    return JsonResponse({'data': res})


def redirect_url(req, url=None):
    try:
        short_url = ShortURL.objects.prefetch_related('target_devices').get(short_url=url)
    except ShortURL.DoesNotExist:
        return JsonResponse({'error': 'Short URL does not exist'}, status=404)

    short_url.redirects += 1
    short_url.save()

    is_mobile = req.user_agent.is_mobile
    is_tablet = req.user_agent.is_tablet
    target_device = None

    if is_mobile or is_tablet:
        device_type = TargetDevice.MOBILE if is_mobile else TargetDevice.TABLET
        try:
            target_device = TargetDevice.objects.get(short_url=short_url, device_type=device_type)
        except ShortURL.DoesNotExist:
            pass

    if target_device:
        # Return Device URL
        return redirect(target_device.url)
    else:
        # Return Desktop URL
        return redirect(short_url.target_url)
