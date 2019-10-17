from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from .models import BookInfo
import json
from django.core import signing
import time
import hashlib
from django.core.cache import cache


HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = 'WH_WUHAO'
SALT = 'www.xiaocao'
TIME_OUT = 30 * 60  # 30min

def encrypt(obj):
    """加密"""
    value = signing.dumps(obj, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value

def decrypt(src):
    """解密"""
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    print(type(raw))
    return raw


def create_token(username):
    """生成token信息"""
    # 1. 加密头信息
    header = encrypt(HEADER)
    # 2. 构造Payload
    payload = {"username": username, "iat": time.time()}
    payload = encrypt(payload)
    # 3. 生成签名
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()
    token = "%s.%s.%s" % (header, payload, signature)
    cache.set(username, token, TIME_OUT)
    return token

def get_payload(token):
    payload = str(token).split('.')[1]
    payload = decrypt(payload)
    return payload

# 通过token获取用户名
def get_username(token):
    payload = get_payload(token)
    return payload['username']
    pass

#检查token
def check_token(token):
    username = get_username(token)
    last_token = cache.get(username)
    if last_token:
        return last_token == token
    return False

# Create your views here.
# post 和 get 同时支持时
#登录接口

@csrf_exempt
def index(request):
    if request.method == 'GET':
        a = request.GET.get('xiaocao')
    else:
        a = request.POST.get('xiaocao')
    try:
        bookInfo = BookInfo.objects.get(pk=a)
        token = create_token(bookInfo.id)
        data = {'title':bookInfo.tittle,"token":token }
        print("登录成功")
        b= {"data":data}
        b['code'] =200
        b['c'] = 0

    except BookInfo.DoesNotExist:
        b={}
        b['c'] = 0
        b['m'] = '登录失败'
    return JsonResponse(b)


def test(request):
    response = HttpResponse()
    data = {"data":"成功"}
    response.content = json.dumps(data)
    response.status_code = 200
    response['name'] = 'xuanli' #设置header
    response.set_cookie("TOKEN", "token") #设置cookie
    return response




# def testAPI(request):
#     return  HttpResponse()





