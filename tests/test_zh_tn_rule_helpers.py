from __future__ import annotations

import unittest

from light_text_process.rules.zh_tn import (
    _format_zh_integer,
    _prepare_zh_tn_input,
    _replace_zh_tn_digit_ordinals,
    _replace_zh_tn_numeric_dates,
    _verbalize_zh_ascii_electronic,
    _verbalize_zh_ipv4_addresses,
)


class ChineseTNRuleHelperTests(unittest.TestCase):
    def test_zh_tn_helper_verbalizes_ascii_electronic_tokens(self) -> None:
        self.assertEqual(
            _verbalize_zh_ascii_electronic("邮箱 test@example.com，网址 https://example.com/a-b。"),
            "邮箱 test艾特example点com，网址 https冒号斜杠斜杠example点com斜杠a杠b。",
        )
        self.assertEqual(
            _verbalize_zh_ipv4_addresses("IP 192.168.0.1。"),
            "IP 一九二点一六八点零点一。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("文件 report_v2.0.pdf，路径 /data/input-01/test.csv，账号 @light_user，话题 #AI2026。"),
            "文件 report下划线v二点零点pdf,路径 斜杠data斜杠input杠零一斜杠test点csv,"
            "账号 艾特light下划线user,话题 井号AI二零二六。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("链接 https://example.com/a-b?q=hello_world&n=123#top。"),
            "链接 https冒号斜杠斜杠example点com斜杠a杠b问号q等于hello下划线world与n等于一二三井号top。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("MAC AA:BB:CC:DD:EE:FF，UUID 550e8400-e29b-41d4-a716-446655440000，颜色 #FF5733。"),
            "MAC AA冒号BB冒号CC冒号DD冒号EE冒号FF,"
            "UUID 五五零e八四零零杠e二九b杠四一d四杠a七一六杠四四六六五五四四零零零零,"
            "颜色 井号FF五七三三。",
        )
        self.assertEqual(
            _prepare_zh_tn_input(
                "温度 72°F，温差 300K，服务器 127.0.0.1:8080，IPv6 2001:0db8::1，"
                "ISBN 978-7-111-12345-6，DOI 10.1000/xyz123。"
            ),
            "温度 七十二华氏度,温差 三百开尔文,服务器 一二七点零点零点一冒号八零八零,"
            "IPv六 二零零一冒号零DB八冒号冒号一,ISBN 九七八杠七杠一一一杠一二三四五杠六,"
            "DOI 一零点一零零零斜杠XYZ一二三。",
        )
        self.assertEqual(_prepare_zh_tn_input("版本 v2.0.1-beta.3。"), "版本 v二点零点一杠beta点三。")
        self.assertEqual(
            _prepare_zh_tn_input("接口返回 HTTP 404，端口 8080，截止到 2026-06-15T14:30:05Z。"),
            "接口返回 HTTP 四零四,端口 八零八零,截止到 二零二六杠零六杠一五T一四冒号三零冒号零五Z。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("按 Ctrl+C，再按 Cmd+Shift+P。时间 2026-06-15 14:30:05。优惠 8折。"),
            "按 Ctrl加C,再按 Cmd加Shift加P。时间 二零二六杠零六杠一五 一四冒号三零冒号零五。优惠 八折。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("会议 14:30 开始，备份 07:05。误差 ±0.5mm，x≈5。"),
            "会议 十四点三十分 开始,备份 七点零五分。误差 正负零点五毫米,x约等于五。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("营业时间 09:00-18:30，会议 14:30~15:45。"),
            "营业时间 九点整到十八点三十分,会议 十四点三十分到十五点四十五分。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("周一-周五营业，周六-周日休息。"),
            "周一到周五营业,周六到周日休息。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("有效期 2026年6月15日-2026年6月20日。"),
            "有效期 二零二六年六月十五日到二零二六年六月二十日。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("他今年 5岁，买了 3件商品，来了 12人，试了 2次。"),
            "他今年 五岁,买了 三件商品,来了 十二人,试了 二次。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("我有¥123.45，押金￥50.5。"),
            "我有一百二十三元四角五分,押金人民币五十元五角。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("客服电话 010-12345678，手机号 138 0013 8000。"),
            "客服电话 零一零杠一二三四五六七八,手机号 一三八零零一三八零零零。",
        )

    def test_zh_tn_helper_formats_digit_ordinals(self) -> None:
        self.assertEqual(_format_zh_integer(12), "十二")
        self.assertEqual(_format_zh_integer(1002), "一千零二")
        self.assertEqual(
            _replace_zh_tn_numeric_dates("今天 2026-06-15 和 2026/6/15 和 2026.6.15 和 2026-13-40"),
            "今天 2026年6月15日 和 2026年6月15日 和 2026年6月15日 和 2026-13-40",
        )
        self.assertEqual(
            _prepare_zh_tn_input("日期 20260615，版本 202606，阈值 x>=5，y<=10。"),
            "日期 二零二六年六月十五日,版本 二零二六零六,阈值 x大于等于五,y小于等于十。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("日期 2026-06，月份 2026年6月。"),
            "日期 二零二六年六月,月份 二零二六年六月。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("阈值 x!=5，y≠10。"),
            "阈值 x不等于五,y不等于十。",
        )
        self.assertEqual(_prepare_zh_tn_input("a!=b，x≈5。"), "a不等于b,x约等于五。")
        self.assertEqual(
            _prepare_zh_tn_input("范围 3-5天，编号 A-123，网速 100Mbps，速度 10m/s。"),
            "范围 三到五天,编号 A杠一二三,网速 一百兆比特每秒,速度 十米每秒。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("编号No.5，序号No.12，账号@light_user，话题#AI2026。"),
            "编号五,序号十二,账号艾特light下划线user,话题井号AI二零二六。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("电量 5kWh，容量 512MB，缓存 128KB，流量 500mL，电流 20mA。"),
            "电量 五千瓦时,容量 五百一十二兆字节,缓存 一百二十八千字节,流量 五百毫升,电流 二十毫安。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("面积 80㎡，容量 1L，公式 10×20=200。"),
            "面积 八十平方米,容量 一升,公式 十乘二十等于二百。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("房间面积80㎡，租金12元/㎡。"),
            "房间面积八十平方米,租金十二元每平方米。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("密度5kg/m³，面密度5kg/m²。"),
            "密度五千克每立方米,面密度五千克每平方米。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("单价 3.5元/㎡，摄氏23度，华氏72度。"),
            "单价 三点五元每平方米,摄氏二十三度,华氏七十二度。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("室温 -3℃，体感 -5°C，温差 ±2℃。"),
            "室温 负三摄氏度,体感 负五摄氏度,温差 正负二摄氏度。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("密度 5kg/m²。"),
            "密度 五千克每平方米。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("血糖 5.6mmol/L，血压 120mmHg，气压 101kPa。"),
            "血糖 五点六毫摩尔每升,血压 一百二十毫米汞柱,气压 一百零一千帕。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("药物 2µg/mL，激素 50ng/mL，样本 20µL。"),
            "药物 二微克每毫升,激素 五十纳克每毫升,样本 二十微升。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("噪声 30dB，功率密度 80W/m²，扭矩 5N·m，电池 5000mAh。"),
            "噪声 三十分贝,功率密度 八十瓦每平方米,扭矩 五牛米,电池 五千毫安时。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("评分 4.8/5，得分 9/10。"),
            "评分四点八分满分五分,得分九分满分十分。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("价格 12.5元/斤，速度 80公里/小时。"),
            "价格 十二点五元每斤,速度 八十公里每小时。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("吞吐 120MB/s，帧率 60fps，延迟 12ms，内存 2GiB。"),
            "吞吐 一百二十兆字节每秒,帧率 六十帧每秒,延迟 十二毫秒,内存 二吉比字节。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("时长 2h 30min 45s，角度 90deg，频率 44.1kHz。"),
            "时长 二小时 三十分钟 四十五秒,角度 九十度,频率 四十四点一千赫兹。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("身高 6ft，长度 12in，重量 5lb，体积 2oz，距离 3mi。"),
            "身高 六英尺,长度 十二英寸,重量 五磅,体积 二盎司,距离 三英里。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("误差 1‰，利率 3.5‰，排名第21。"),
            "误差 千分之一,利率 千分之三点五,排名第二十一。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("增长 +12%，下降 -3.5%。"),
            "增长 正百分之十二,下降 负百分之三点五。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("体温36.5度，温差±2度，湿度40%-60%。"),
            "体温三十六点五度,温差正负二度,湿度百分之四十到百分之六十。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("温度 20-30℃，气温 -5-5°F。"),
            "温度 二十到三十摄氏度,气温 负五到五华氏度。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("订单满100减20。"),
            "订单满一百减二十。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("利率上行 25bp，信用利差扩大 3.5bps，用户 1.2万。"),
            "利率上行 二十五个基点,信用利差扩大 三点五个基点,用户 一点二万。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("电阻 10Ω，电流 2A，电压 3.3mV，电容 47µF。"),
            "电阻 十欧姆,电流 二安,电压 三点三毫伏,电容 四十七微法。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("力 5N，压强 101Pa，气压 0.1MPa，加速度 9.8m/s²，转速 3000rpm，流量 2L/min。"),
            "力 五牛顿,压强 一百零一帕,气压 零点一兆帕,加速度 九点八米每二次方秒,转速 三千转每分,流量 二升每分钟。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("分辨率 1920x1080，尺寸 10×20cm。"),
            "分辨率 一千九百二十乘一千零八十,尺寸 十乘二十厘米。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("增长 2pp，误差 1e-5，光速 3×10^8m/s。"),
            "增长 二个百分点,误差 一乘以十的负五次方,光速 三乘以十的八次方米每秒。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("Q3 2026收入增长，2026 Q4展望改善，FY2026预算。"),
            "二零二六年第三季度收入增长,二零二六年第四季度展望改善,二零二六财年预算。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("订单号 AB-1234，发票 INV-2026-001，快递单号 SF1234567890，电话 415-555-0123 转45。"),
            "订单号 AB杠一二三四,发票 INV杠二零二六杠零零一,快递单号 SF一二三四五六七八九零,电话 四一五杠五五五杠零一二三 转四五。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("车牌 京A12345，护照 E12345678，身份证 11010519900307861X。"),
            "车牌 京A一二三四五,护照 E一二三四五六七八,身份证 一一零一零五一九九零零三零七八六一X。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("地址 北京市朝阳区建国路88号A座1208室，12楼，邮编100080。"),
            "地址 北京市朝阳区建国路八十八号A座一二零八室,十二楼,邮编一零零零八零。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("预算 USD 12.50，成本 EUR 3，人民币 CNY 1,234.00。"),
            "预算 十二点五美元,成本 三欧元,人民币 一千二百三十四人民币。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("我有 $123.45、€50、£6、HK$7。电话 +86 13800138000。"),
            "我有 一百二十三点四五美元、五十欧元、六英镑、七港元。电话 加八六 一三八零零一三八零零零。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("访问 www.example.com。时区 UTC+8 和 GMT-5，温度 -12，增量 +5。"),
            "访问 www点example点com。时区 UTC加八 和 GMT减五,温度 负十二,增量 正五。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("时长 01:02:03。电话 400-800-1234，账号 6222 1234 5678 9012。"),
            "时长 一小时二分钟三秒。电话 四零零杠八零零杠一二三四,账号 六二二二一二三四五六七八九零一二。",
        )
        self.assertEqual(_prepare_zh_tn_input("车位B2-123，门牌8-1。"), "车位B二杠一二三,门牌八杠一。")
        self.assertEqual(
            _prepare_zh_tn_input("日期 2026.06.15，血压 120/80mmHg。"),
            "日期 二零二六年六月十五日,血压 一百二十杠八十毫米汞柱。",
        )
        self.assertEqual(
            _prepare_zh_tn_input("第21世纪，第3层，第12页，第1名。"),
            "第二十一世纪,第三层,第十二页,第一名。",
        )
        self.assertEqual(
            _replace_zh_tn_digit_ordinals("第 12 届第3名第1002期"),
            "第十二届第三名第一千零二期",
        )


if __name__ == "__main__":
    unittest.main()
