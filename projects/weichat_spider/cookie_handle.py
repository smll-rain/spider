# coding : utf-8
import re
import requests
url = "https://mmbiz.qpic.cn/mmbiz_png/xXrickrc6JTNPb4UupDtdoKcIIibxoaySriaNOOCuHIqtQl78P8ZyE4lre1gibrFc7fYpicWkjLAgO4OoApHQ2fJbQQ/640?wx_fmt=png"
respone = requests.get(url)
with open("./img.png", "wb") as f:
    f.write(respone.content)
