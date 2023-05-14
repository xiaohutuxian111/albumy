# -*- coding: utf-8 -*-
import os
import PIL
from PIL import Image
from urllib.parse import urlparse, urljoin
from flask import request, url_for, redirect, flash, current_app
from authlib.jose import jwt, JoseError

from albumy.models import User
from albumy.settings import Operations
from albumy.extensions import db


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


def redirect_back(default='main.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))


def resize_image(image, filename, base_width):
    """
    裁剪图片
    :param image:
    :param filename:
    :param base_width:
    :return:
    """
    filename, ext = os.path.splitext(filename)
    img = Image.open(image)
    if img.size[0] <= base_width:
        return filename + ext
    w_percent = (base_width / float(img.size[0]))
    h_size = int(float(img.size[1]) * float(w_percent))
    img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)

    filename += current_app.config["ALBUMY_PHOTO_SUFFIX"][base_width] + ext
    img.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename), optimize=True, quality=85)
    return filename


def generate_token(user, operation, expire_in=None, **kwargs):
    """
    生成随机令牌
    https://blog.csdn.net/weixin_43863487/article/details/123784400
    """
    # 签名算法
    header = {'alg': 'HS256'}
    # 用于签名的密钥
    key = current_app.config['SECRET_KEY']
    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return jwt.encode(header=header, payload=data, key=key)


def validate_token(user, token, operation, new_password=None):
    """用于验证用户注册和修改密码后邮箱的token，并完成相应的确认操作"""
    key = current_app.config['SECRET_KEY']
    try:
        data = jwt.decode(token, key)
        print(data)
    except JoseError:
        return False
    if operation != data.get('operation') or user.id != data.get('id'):
        user.confirmed = True
    elif operation == Operations.CONFIRM:
        user.confirmed = True
    elif operation == Operations.RESET_PASSWORD:
        user.set_password(new_password)
    elif operation == Operations.CHANGE_EMAIL:
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if User.query.filter_by(email=new_email).first() is not None:
            return False
        user.email = new_email
    else:
        return False

    db.session.commit()
    return True
