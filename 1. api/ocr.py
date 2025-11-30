import base64
import subprocess
import tempfile

def handler(request):
    if request.method != "POST":
        return {"error": "POST only"}, 400
    
    body = request.json()
    if "image" not in body:
        return {"error": "image missing"}, 400
    
    img_data = base64.b64decode(body["image"])

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    tmp.write(img_data)
    tmp.close()

    output = tmp.name + "_out"

    cmd = [
        "tesseract",
        tmp.name,
        output,
        "-l", "ben+eng",
        "--psm", "7"
    ]

    try:
        subprocess.run(cmd, check=True)
        text = open(output + ".txt").read()
    except Exception as e:
        return {"error": str(e)}, 500

    return {"text": text}
