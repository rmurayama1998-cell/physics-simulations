# 公開済みシミュレーションの一覧ページ(index.html)を生成する（python make_page.py）
# QRコードはSVGでページに埋め込むので、index.html 1つで完結する
import html
import io

import qrcode
from qrcode.image.svg import SvgPathImage

B = "https://rmurayama1998-cell.github.io/"
SELF = B + "physics-simulations/"   # この一覧ページ自身のURL

SECTIONS = [
    ("波", [
        ("進行波の波形", "wave-simulator/remake/traveling.html", "パルスや連続波が進むようす。v = fλ を確かめる"),
        ("波と媒質の振動", "wave-simulator/remake/oscillation.html", "y-x グラフと y-t グラフを見比べる"),
        ("波の合成と定常波", "wave-simulator/remake/composite-wave.html", "重ね合わせ、定常波の腹と節"),
        ("縦波と横波表示", "wave-simulator/remake/longitudinal.html", "縦波の媒質の動きと横波表示"),
        ("波の反射（自由端・固定端）", "wave-simulator/remake/reflection.html", "端で反射した波と定常波"),
        ("弦の固有振動", "wave-simulator/remake/eigen-vibration.html", "基本振動・倍振動、定常波にならない波"),
        ("気柱の共鳴（閉管・開管）", "wave-simulator/remake/air-column.html", "閉管・開管の基本振動と倍振動"),
        ("波の干渉", "wave-simulator/remake/interference.html", "2つの波源、強め合い・弱め合いと経路差"),
        ("波の反射（反射の法則）", "wave-simulator/remake/reflection-law.html", "入射角＝反射角になる理由"),
        ("波の屈折（屈折の法則）", "wave-simulator/remake/refraction.html", "境界で波面が曲がる理由"),
        ("うなり", "wave-simulator/remake/beat.html", "振動数が少し違う2つの音の重なり"),
    ]),
    ("波（探究用）", [
        ("波の基本量シミュレータ", "wave-simulator/", "振幅・波長・振動数と y-x・y-t グラフ"),
        ("波の基本式を見つけよう", "wave-simulator/discover.html", "生徒が自分で v = fλ を見つける"),
        ("縦波の横波表示 変換ツール", "wave-simulator/longitudinal.html", "変位の矢印を90°回して横波表示に"),
        ("弦の振動・気柱の共鳴", "wave-simulator/resonance.html", "波長を変えて共鳴する所を探す"),
        ("重ね合わせ・反射・定常波", "wave-simulator/superposition.html", "2つの波の重ね合わせと反射"),
    ]),
    ("ホイヘンスの原理", [
        ("反射の法則", "huygens-simulator/hansha.html", "素元波の作図で反射の法則を導く"),
        ("屈折の法則", "huygens-simulator/kussetsu.html", "素元波の作図で屈折の法則を導く"),
    ]),
    ("光", [
        ("フィゾーの実験", "fizeau-simulator/", "回転する歯車で光の速さを測る（3D）"),
    ]),
    ("熱", [
        ("熱運動とブラウン運動", "thermal-motion-simulator/", "温度と分子の速さ、微粒子の不規則な動き"),
        ("水の加熱シミュレーション", "water-heating-simulation/", "加熱曲線と分子のようすを連動して表示"),
        ("水100gの加熱曲線", "water-heating-simulation/water_heating_curve_100g.html", "−100℃ → 200℃ の温度変化"),
    ]),
]


def qr_svg(url):
    img = qrcode.make(url, error_correction=qrcode.constants.ERROR_CORRECT_M,
                      image_factory=SvgPathImage, box_size=10, border=2)
    buf = io.BytesIO()
    img.save(buf)
    svg = buf.getvalue().decode("utf-8")
    svg = svg[svg.index("<svg"):]                     # XML宣言を除く
    return svg.replace("<svg ", '<svg class="qr" role="img" aria-label="QRコード" ', 1)


cards = []
n = 0
for title, items in SECTIONS:
    cards.append(f'<section><h2>{html.escape(title)}</h2><div class="grid">')
    for name, path, desc in items:
        n += 1
        url = B + path
        cards.append(
            f'<a class="card" href="{url}" target="_blank" rel="noopener">'
            f'{qr_svg(url)}'
            f'<div class="body"><div class="name">{html.escape(name)}</div>'
            f'<div class="desc">{html.escape(desc)}</div>'
            f'<div class="url">{html.escape(url)}</div></div></a>')
    cards.append("</div></section>")

page = open("template.html", encoding="utf-8").read()
page = page.replace("{{CARDS}}", "\n".join(cards)).replace("{{COUNT}}", str(n))
page = page.replace("{{SELF_QR}}", qr_svg(SELF)).replace("{{SELF}}", SELF)
open("index.html", "w", encoding="utf-8").write(page)
print(f"index.html: {n} 件")

# 一覧ページ自身のQRコード（掲示・配布用、誤り訂正レベルH）
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=20, border=4)
qr.add_data(SELF)
qr.make(fit=True)
qr.make_image(fill_color="black", back_color="white").save("qr.png")
qrcode.make(SELF, error_correction=qrcode.constants.ERROR_CORRECT_H,
            image_factory=SvgPathImage, box_size=20, border=4).save("qr.svg")
print(f"qr.png: {SELF}")
