# -*- coding: utf-8 -*-
import os

from flask_dropzone import random_filename
from flask import render_template, Blueprint, request, current_app
from albumy.decorators import confirm_required, permission_required
from flask_login import login_required, current_user

from albumy.models import Photo
from albumy.extensions import db
from albumy.utils import  resize_image


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('main/index.html')


@main_bp.route('/upload', methods=['POST', 'GET'])
@login_required  # 验证登录状态
@confirm_required  # 验证确认状态
@permission_required('UPLOAD')  # 验证权限
def upload():
    if request.method == "POST" and 'file' in request.files:
        # 获取图片文件对象
        f = request.files.get('file')
        # 生成随机的文件名
        filename = random_filename(f.filename)
        # 保存图片
        f.save(os.path.join(current_app.config['ALBUMY_UPLOAD_PATH'], filename))
        # 裁剪图片
        filename_s = resize_image(f,filename,current_app.config['ALBUMY_PHOTO_SIZE']['small'])
        filename_m = resize_image(f,filename,current_app.config['ALBUMY_PHOTO_SIZE']['medium'])
        photo = Photo(
            # 创建文件记录
            filename=filename,
            filename_s = filename_s,
            filename_m = filename_m,
            author=current_user.get_current_object()
        )
        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')


@main_bp.route('/explore')
def explore():
    return render_template('main/explore.html')
