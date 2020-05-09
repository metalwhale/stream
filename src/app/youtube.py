from . import app
from flask import Response, jsonify, request, stream_with_context
import http
import pafy
import requests

@app.route("/youtube_info")
def youtube_info():
    info = {}
    video = _youtube(request.args.get("video_id"))
    if video:
        info["status"] = "Ok"
        info["info"] = {
            "title": video.title
        }
    else:
        info["status"] = "Error"
    return jsonify(info)

@app.route("/youtube_audio")
def youtube_audio():
    video = _youtube(request.args.get("video_id"))
    no_content = Response("", http.client.NO_CONTENT)
    if not video:
        return no_content
    valid_urls = [s.url for s in video.audiostreams if s.extension == "m4a"]
    if len(valid_urls) == 0:
        return no_content
    url = valid_urls[0]
    req = requests.get(url, stream = True)
    return Response(
        stream_with_context(req.iter_content(chunk_size=1024)),
        content_type = req.headers["content-type"]
    )

def _youtube(video_id):
    try:
        return pafy.new(f"http://www.youtube.com/watch?v={video_id}")
    except ValueError:
        return None
