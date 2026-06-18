#!/usr/bin/env python3
"""注入 Step 1.5 xhs_destination_brief 并做轻量行程优化。"""
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


def patch_xiamen(trip: dict) -> None:
    trip["party_size"] = 3
    trip["summary"] = (
        "厦门 4 天 3 晚（对齐 Step 1.5 攻略）。住鹭江道如忆锚点中山路/八市；"
        "鼓浪屿早班船、八市海鲜、厦大预约；避雷中山路网红奶茶与景区海鲜宰客。"
    )
    trip["xhs_destination_brief"] = {
        "city": "厦门",
        "keywords_searched": ["厦门 4天 攻略", "厦门 避雷", "厦门 鼓浪屿 早班船"],
        "source": "webfetch-degraded",
        "degraded": True,
        "must_visit": [
            {"name": "鼓浪屿", "why": "多篇攻略核心日；须早班船 7:30–8:30 上岛"},
            {"name": "中山路 / 八市", "why": "落地烟火气+本地海鲜；酒店步行可达"},
            {"name": "厦门大学 + 环岛路", "why": "攻略 Day3 标配；厦大须提前预约"},
            {"name": "沙坡尾", "why": "文艺日落区；与 Day2 傍晚顺路"},
        ],
        "skip_or_caution": [
            {"name": "住曾厝垵", "why": "多篇称交通乱、过度商业化；可半日逛不宜作酒店锚点"},
            {"name": "中山路网红奶茶（张三疯等）", "why": "攻略普遍称贵且一般"},
            {"name": "景区海鲜大排档", "why": "先问价再称重；优先八市加工"},
            {"name": "鼓浪屿低价一日游团", "why": "购物团陷阱"},
        ],
        "region_layout": [
            "Day1：落地 · 中山路/八市（酒店区）",
            "Day2：鼓浪屿全日 + 傍晚沙坡尾",
            "Day3：厦大 · 白城/曾厝垵 · 环岛路",
            "Day4：八市早茶 · 伴手礼 · 返程",
        ],
        "pace_hints": "每天 ≤4 POI；鼓浪屿全天步行；早班船避旅行团",
        "weather_hints": "6 月底梅雨季；户外段备 Plan B（沙坡尾/中山路室内）",
        "source_notes": [
            {
                "title": "厦门四天三晚旅游攻略(2026保姆级)",
                "url": "https://www.15386.cn/post/151775.html",
            },
            {
                "title": "厦门3天2夜懒人攻略（鼓浪屿早班船）",
                "url": "https://sg.trip.com/moments/detail/xiamen-21-143402827",
            },
            {
                "title": "厦门旅游避坑（轮渡/海鲜/住宿）",
                "url": "https://m.cncn.net/blog/1337051",
            },
        ],
        "web_search_supplement": (
            "鼓浪屿船票：厦门轮渡有限公司公众号，建议提前 1–3 天抢 7:30–8:30 班次；"
            "厦大访客：提前 3 天预约；南普陀免费预约。"
        ),
    }
    for pb in trip.get("prebook") or []:
        if pb.get("item") == "鼓浪屿船票":
            pb["note"] = (
                "Day 2 抢 7:30–8:30 早班（攻略共识避人潮）；邮轮中心厦鼓码头出发；"
                "35 元/人；3 人共 105 元；提前 1–3 天放票"
            )
            pb["deadline"] = "出发前 3 天（早班船紧俏）"
    for d in trip["days"]:
        if d["day"] == 2:
            patch_poi_note(
                d,
                "邮轮中心",
                "【攻略】建议 7:30–8:30 班次上岛，10 点后旅行团扎堆。",
            )
        if d["day"] == 1:
            patch_poi_note(
                d,
                "中山路",
                "避雷：主街网红奶茶（张三疯等）性价比低，小吃走支巷。",
            )
        if d["day"] == 3:
            patch_poi_note(
                d,
                "曾厝垵",
                "半日逛即可；攻略不建议住此（交通乱），本行程住中山路锚点。",
            )


def patch_qingdao(trip: dict) -> None:
    trip["party_size"] = 3
    trip["summary"] = (
        "青岛 4 天 3 晚毕业游（对齐 Step 1.5 攻略）。住栈桥火车站汉庭；"
        "老城步行+地铁；栈桥清晨、啤酒博物馆、八大关、五四广场；"
        "避雷栈桥周边海鲜大排档，海鲜可营口路自购加工。"
    )
    trip["xhs_destination_brief"] = {
        "city": "青岛",
        "keywords_searched": ["青岛 4天 毕业旅行", "青岛 避雷", "青岛 小麦岛"],
        "source": "webfetch-degraded",
        "degraded": True,
        "must_visit": [
            {"name": "栈桥", "why": "地标；清晨退潮赶海/喂海鸥优于正午桥上拥挤"},
            {"name": "信号山 / 大学路", "why": "老城全景+文艺街区；步行顺路"},
            {"name": "青岛啤酒博物馆", "why": "毕业游高频；须预约早场"},
            {"name": "八大关", "why": "万国建筑+第二海水浴场"},
            {"name": "五四广场 / 奥帆", "why": "夜景地标；可延伸小麦岛日落"},
        ],
        "skip_or_caution": [
            {"name": "栈桥/景区海鲜大排档", "why": "多篇避雷宰客；勿点流动摊贩低价海鲜"},
            {"name": "信号山旋转观景台", "why": "攻略称山顶 360° 台性价比一般，外景即可"},
            {"name": "景区散装特产", "why": "正品去超市/商超"},
        ],
        "region_layout": [
            "Day1：抵达 · 栈桥海边 · 啤酒街晚餐",
            "Day2：信号山 · 大学路 · 五四广场（可延伸小麦岛日落）",
            "Day3：啤酒博物馆 · 八大关 · 奥帆晚餐",
            "Day4：栈桥告别 · 返程",
        ],
        "pace_hints": "每天 ≤4 POI；老城坡多穿运动鞋；海边日落放下午",
        "weather_hints": "6 月底紫外线强+海风凉；备 SPF50+ 薄外套",
        "source_notes": [
            {
                "title": "青岛旅游避坑大实话（2026）",
                "url": "https://zhuanlan.zhihu.com/p/2032546114658883144",
            },
            {
                "title": "青岛4天3晚经典行程避坑",
                "url": "https://m.cncn.net/blog/1290495",
            },
            {
                "title": "青岛4日游省钱避雷",
                "url": "https://www.163.com/dy/article/KQ8TUGF10556JHRB.html",
            },
        ],
        "web_search_supplement": (
            "啤酒博物馆微信公众号预约；小麦岛无门票，建议 16:00 后看日落（距五四广场约 2km）；"
            "海鲜自购推荐营口路市场加工。"
        ),
    }
    for pb in trip.get("prebook") or []:
        if "机票" in (pb.get("item") or ""):
            pr = pb.get("price")
            if isinstance(pr, dict):
                pr["quantity"] = 3
                pr["total_min"] = pr.get("min", 0) * 3
                pr["total_max"] = pr.get("max", 0) * 3
    for d in trip["days"]:
        if d["day"] == 1:
            patch_poi_note(
                d,
                "栈桥",
                "攻略：清晨退潮西侧礁石区赶海更出片；避开 10 点后旅行团高峰。",
            )
        if d["day"] == 2:
            patch_poi_note(
                d,
                "五四广场",
                "若体力允许 16:00 后步行/打车至小麦岛看日落（攻略高频，约 2km）。",
            )
            patch_poi_note(
                d,
                "云霄路",
                "海鲜先问清斤两价再点；云霄路优于栈桥边大排档。",
            )
        if d["day"] == 3:
            patch_poi_note(
                d,
                "八大关",
                "花石楼露台看海性价比高；新人拍照多，上午光线柔和。",
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
