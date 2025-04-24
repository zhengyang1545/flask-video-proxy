from flask import Flask, request, Response, jsonify
import requests

app = Flask(__name__)

@app.route("/video")
def proxy_video():
    # 获取视频URL
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "视频 URL 缺失"}), 400

    # 设置请求头（防止反盗链）
    headers = {
        "Referer": "https://www.douyin.com/",  # 设置为Douyin视频页面的URL
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }

    try:
        # 请求视频流
        resp = requests.get(url, headers=headers, stream=True)

        # 检查响应状态码和内容类型
        if resp.status_code != 200:
            return jsonify({"error": "无法下载视频，状态码：" + str(resp.status_code)}), 500

        content_type = resp.headers.get('Content-Type', '')
        if 'video' not in content_type:
            return jsonify({"error": "返回的内容不是视频"}), 400

        # 返回视频流给客户端
        return Response(resp.iter_content(chunk_size=1024), content_type="video/mp4")

    except requests.RequestException as e:
        return jsonify({"error": f"请求失败：{str(e)}"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
