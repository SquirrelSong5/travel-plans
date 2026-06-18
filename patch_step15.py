#!/usr/bin/env python3
"""注入 Step 1.5 xhs_destination_brief（小红书 CLI 精读）并做轻量行程优化。"""
from __future__ import annotations

import json
from pathlib import Path


def patch_poi_note(day: dict, name_substr: str, append: str) -> bool:
    for p in day.get("pois") or []:
        if name_substr in (p.get("name") or ""):
            note = (p.get("note") or "").strip()
            if append not in note:
                p["note"] = f"{note} {append}".strip() if note else append
            return True
    return False


def xhs_note(feed_id: str, title: str) -> dict:
    return {
        "title": title,
        "url": f"https://www.xiaohongshu.com/explore/{feed_id}",
        "feed_id": feed_id,
        "platform": "xiaohongshu",
    }


def patch_xiamen(trip: dict) -> None:
    trip["party_size"] = 3
    trip["summary"] = (
        "厦门 4 天 3 晚（小红书 Step 1.5 精读对齐）。住思明区鹭江道锚点中山路/八市；"
        "鼓浪屿早班船、八市阿杰五香、厦大预约；6 月起酷暑+梅雨，户外备 Plan B。"
        "避雷跟团购物团、曾厝垵作酒店锚点、景区花茶/猪肉脯套路。"
    )
    trip["weather_plan"] = (
        "6 月底起厦门进入酷暑+梅雨季（小红书本地博主：6 月起巨热、雨天户外体验差）。"
        "出发前 1 天查实时天气；大雨改室内（沙坡尾/中山路/八市）；防晒+防蚊（植物园）。"
    )
    trip["xhs_destination_brief"] = {
        "city": "厦门",
        "keywords_searched": ["厦门 4天 攻略", "厦门 避雷", "厦门 景点"],
        "source": "xiaohongshu-cli",
        "degraded": False,
        "must_visit": [
            {"name": "鼓浪屿", "why": "多篇核心日；早班船 7:30–8:30 避旅行团"},
            {"name": "中山路 / 八市", "why": "思明区酒店锚点；八市阿杰五香/佳味再添"},
            {"name": "厦门大学 + 环岛路", "why": "厦大须预约；黄厝日出/白城日落经典组合"},
            {"name": "沙坡尾", "why": "文艺街区+双子塔夜景机位"},
            {"name": "厦门植物园", "why": "西门进+观光车；雨林喷雾/多肉区出片（可并入 Day3 弹性）"},
        ],
        "skip_or_caution": [
            {"name": "跟团/低价一日游", "why": "多篇实测购物团；景点各 10 分钟+推销"},
            {"name": "住曾厝垵作锚点", "why": "民宿环境参差；评论称景区民宿多烂，宜半日逛"},
            {"name": "住鼓浪屿", "why": "交通不便、民宿贵；除非体验岛民生活"},
            {"name": "鼓浪屿蜡像馆/贝壳馆", "why": "攻略普遍称不值"},
            {"name": "景区花茶/猪肉脯", "why": "试吃加糖、买回家发酸套路"},
            {"name": "环岛路路边揽客一日游", "why": "多篇避雷坑多"},
            {"name": "中山路网红奶茶（张三疯等）", "why": "性价比低"},
        ],
        "region_layout": [
            "Day1：落地 · 中山路/八市",
            "Day2：鼓浪屿全日 + 傍晚沙坡尾",
            "Day3：厦大 · 白城/曾厝垵 · 环岛路",
            "Day4：八市早茶 · 伴手礼 · 返程",
        ],
        "pace_hints": "每天 ≤4 POI；鼓浪屿带老人可约观光车；6 月起注意防暑",
        "weather_hints": "6 月酷暑+梅雨；雨天不建议冲户外打卡",
        "source_notes": [
            xhs_note("69ec5cff0000000038022cc7", "厦门游-千万不要抱团 刚回来亲身体验"),
            xhs_note("69ead7b70000000011023003", "终于有人把厦门景点讲明白了"),
            xhs_note("695b6c51000000001a02654d", "厦门3天2夜攻略 人均2k+"),
            xhs_note("69e387e0000000001a021e9c", "厦门无法超越的10个地方（免费）"),
        ],
        "web_search_supplement": (
            "船票：厦门轮渡公众号提前 1–3 天抢早班；厦大访客提前 3 天预约；"
            "南普陀/钟鼓索道须预约。"
        ),
    }
    for pb in trip.get("prebook") or []:
        if pb.get("item") == "鼓浪屿船票":
            pb["note"] = (
                "Day 2 抢 7:30–8:30 早班（小红书共识避人潮）；邮轮中心厦鼓码头；"
                "35 元/人；勿信路边低价一日游"
            )
            pb["deadline"] = "出发前 3 天（早班紧俏）"
    for d in trip["days"]:
        if d["day"] == 1:
            patch_poi_note(
                d,
                "中山路",
                "避雷：主街网红奶茶性价比低；小吃走支巷。",
            )
            patch_poi_note(
                d,
                "八市",
                "小红书推荐：阿杰五香、佳味再添；海鲜先问价再称重。",
            )
        if d["day"] == 2:
            patch_poi_note(
                d,
                "邮轮中心",
                "【小红书】7:30–8:30 上岛；勿报低价团。岛上避蜡像馆/花茶猪肉脯套路。",
            )
            patch_poi_note(
                d,
                "龙头路",
                "可试龙阳林氏海蛎煎、林锦记鱼丸；景区内花茶试吃勿冲动买。",
            )
        if d["day"] == 3:
            patch_poi_note(
                d,
                "曾厝垵",
                "半日逛即可；不宜作酒店锚点（小红书：民宿参差）。",
            )
            patch_poi_note(
                d,
                "白城沙滩",
                "经典日落点；6 月起午后暴晒，建议傍晚或清晨。",
            )
        if d["day"] == 4:
            patch_poi_note(
                d,
                "八市早茶",
                "八婆婆烧仙草、花生汤等；伴手礼避景区散装套路。",
            )


def patch_qingdao(trip: dict) -> None:
    trip["party_size"] = 3
    trip["summary"] = (
        "青岛 4 天 3 晚毕业游（小红书 Step 1.5 精读）。住青岛站/栈桥汉庭步行老城；"
        "信号山俯瞰、啤酒博物馆、八大关午后、五四广场延伸小麦岛；"
        "避雷栈桥边海鲜宰客、海鲜自挑防塞货；市区几乎无共享单车靠步行/打车。"
    )
    trip["weather_plan"] = (
        "6–7 月紫外线极强+海风凉（多篇小红书避雷帖）。备 SPF50+ 薄外套；"
        "暑期海边或有浒苔等变数，出发前查近 3 天海岸情况。"
    )
    trip["xhs_destination_brief"] = {
        "city": "青岛",
        "keywords_searched": ["青岛 毕业旅行 4天", "青岛 避雷", "青岛 4天3夜"],
        "source": "xiaohongshu-cli",
        "degraded": False,
        "must_visit": [
            {"name": "栈桥 + 老城步行", "why": "清晨退潮赶海；串联教堂/信号山/大学路"},
            {"name": "信号山", "why": "十几分钟登顶俯瞰老城；旋转台可不去"},
            {"name": "青岛啤酒博物馆", "why": "B 馆 45 含两杯；有行李寄存，适合返程前"},
            {"name": "八大关", "why": "下午 4 点左右光线好；花石楼 8 元性价比高"},
            {"name": "五四广场 / 奥帆 / 小麦岛", "why": "夜景+日落；海之恋公园人少（小麦岛旺季仍挤）"},
        ],
        "skip_or_caution": [
            {"name": "栈桥/景区海鲜大排档", "why": "多篇避雷宰客；勿信流动低价海鲜"},
            {"name": "团岛/市场海鲜加工", "why": "自挑海鲜防商家塞次货（小红书实测）"},
            {"name": "信号山旋转观景台", "why": "外景即可，旋转台性价比一般"},
            {"name": "台东前海沿（部分店）", "why": "有笔记称台东店踩雷；栈桥前海利群店可保留但控预期"},
            {"name": "指望共享单车", "why": "市区几乎无共享单车，靠腿+打车"},
            {"name": "景区散装特产", "why": "正品去超市/商超"},
        ],
        "region_layout": [
            "Day1：抵达 · 栈桥海边 · 啤酒街晚餐",
            "Day2：信号山 · 大学路 · 五四广场（可延伸小麦岛）",
            "Day3：啤酒博物馆 · 八大关 · 奥帆晚餐",
            "Day4：栈桥告别 · 返程",
        ],
        "pace_hints": "老城坡多穿运动鞋；每天 ≤4 POI；体力有限可参考低精力版拆午休",
        "weather_hints": "6–7 月晒+凉海风；浒苔/浪况出发前再查",
        "source_notes": [
            xhs_note("69a19a3b00000000150318d5", "青岛4天3夜超详细旅游攻略 infj满意"),
            xhs_note("69e21508000000001a025d6a", "青岛4天3晚 solo trip 详细版"),
            xhs_note("6a276868000000001503fdd9", "6-7月青岛避雷 突发坑整理"),
            xhs_note("68a2c792000000001d00d930", "武汉→青岛 4天低精力版"),
        ],
        "web_search_supplement": (
            "啤酒博物馆微信预约；轮渡抖音券可看橘子海日落（团岛线）；"
            "海鲜自购：营口路/团岛市场加工；旺季餐厅（开海等）提前订位。"
        ),
    }
    for pb in trip.get("prebook") or []:
        if "机票" in (pb.get("item") or ""):
            pr = pb.get("price")
            if isinstance(pr, dict):
                pr["quantity"] = 3
                pr["total_min"] = pr.get("min", 0) * 3
                pr["total_max"] = pr.get("max", 0) * 3
        if "啤酒博物馆" in (pb.get("item") or ""):
            pb["note"] = (
                "小红书：B 馆约 45 元含两杯啤酒，有行李寄存；建议 Day3 上午场"
            )
    for d in trip["days"]:
        if d["day"] == 1:
            patch_poi_note(
                d,
                "栈桥",
                "小红书：清晨西侧礁石赶海；10 点后旅行团扎堆。",
            )
        if d["day"] == 2:
            patch_poi_note(
                d,
                "信号山",
                "十几分钟登顶即可；旋转观景台可跳过，外景性价比更高。",
            )
            patch_poi_note(
                d,
                "五四广场",
                "16:00 后可打车至小麦岛日落；海之恋公园人少景美（备选）。",
            )
            patch_poi_note(
                d,
                "云霄路",
                "海鲜先问清斤两价；优于栈桥边大排档。",
            )
        if d["day"] == 3:
            patch_poi_note(
                d,
                "啤酒博物馆",
                "B 馆门票含两杯啤酒；喝完可寄存行李直奔机场/车站。",
            )
            patch_poi_note(
                d,
                "八大关",
                "建议 16:00 前后到；花石楼 8 元露台看海性价比高。",
            )
        if d["day"] == 4:
            patch_poi_note(
                d,
                "前海沿",
                "小红书台东店有踩雷帖；本店为栈桥前海利群店，仍建议先问价。",
            )


def main() -> None:
    base = Path(__file__).parent
    pairs = [
        (base / "xiamen-4d3n-draft.json", patch_xiamen),
        (base / "qingdao-2026-06-25-draft.json", patch_qingdao),
    ]
    for path, fn in pairs:
        trip = json.loads(path.read_text(encoding="utf-8"))
        fn(trip)
        path.write_text(json.dumps(trip, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"✅ patched {path.name}")


if __name__ == "__main__":
    main()
