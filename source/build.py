"""Build the self-contained Physcom website using only Python's standard library."""

from pathlib import Path
import base64
import json
import shutil

from content import PAGES, SKETCHES, SOURCES


SOURCE = Path(__file__).resolve().parent
PUBLIC = SOURCE.parent / "public"
VENDOR = SOURCE / "vendor"


def embedded_font(name):
    data = base64.b64encode((VENDOR / name).read_bytes()).decode()
    return "data:font/ttf;base64," + data


def build():
    PUBLIC.mkdir(parents=True, exist_ok=True)
    css = (SOURCE / "style.css").read_text(encoding="utf-8")
    css = css.replace("__THAI_FONT__", embedded_font("NotoSansThai.ttf"))
    css = css.replace("__CODE_FONT__", embedded_font("RobotoMono.ttf"))

    assets = {}
    for asset in sorted((SOURCE / "assets").iterdir()):
        if asset.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
            continue
        mime = "image/png" if asset.suffix.lower() == ".png" else "image/jpeg"
        assets[asset.stem] = (
            "data:" + mime + ";base64," + base64.b64encode(asset.read_bytes()).decode()
        )

    lab_images = json.loads((SOURCE / "lab-images.json").read_text(encoding="utf-8"))
    data = json.dumps(
        dict(pages=PAGES, sketches=SKETCHES, sources=SOURCES, assets=assets, labImages=lab_images),
        ensure_ascii=False,
    ).replace("</", "<\\/")
    paho = (VENDOR / "paho-mqtt-min.js").read_text(encoding="utf-8")
    app = (SOURCE / "app.js").read_text(encoding="utf-8")
    html = (SOURCE / "index.tpl").read_text(encoding="utf-8")
    for key, value in [
        ("__CSS__", css),
        ("__DATA__", data),
        ("__PAHO__", paho.replace("</script", "<\\/script")),
        ("__PAHO_JSON__", json.dumps(paho).replace("</", "<\\/")),
        ("__APP__", app.replace("</script", "<\\/script")),
    ]:
        html = html.replace(key, value)

    # Stable CRLF output preserves the delivered offline HTML on every platform.
    (PUBLIC / "index.html").write_bytes(html.replace("\n", "\r\n").encode("utf-8"))
    licenses = PUBLIC / "licenses"
    licenses.mkdir(exist_ok=True)
    for notice in sorted((SOURCE / "licenses").glob("*.txt")):
        shutil.copyfile(notice, licenses / notice.name)
    print(f"Built {len(PAGES)} topics and {len(SKETCHES) - 1} Arduino sketches: {PUBLIC / 'index.html'}")


if __name__ == "__main__":
    build()
