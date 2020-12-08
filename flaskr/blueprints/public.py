import urllib
from flask import Blueprint, request, jsonify

public_bp = Blueprint('public', __name__, url_prefix='/public')


# 必应每日壁纸
@public_bp.route('/bing/wallpaper', methods=['GET'])
def getWallpaper():
  url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
  # 请求必应服务器
  req = urllib.request.Request(url)
  response = urllib.request.urlopen(req)
  return response.read().decode('utf-8')