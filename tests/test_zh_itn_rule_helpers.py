from __future__ import annotations

import unittest

from light_text_process.rules.zh_itn import (
    finalize_outputs,
    _compact_zh_itn_spacing,
    _normalize_zh_itn_exact_hours,
    _normalize_zh_itn_negative_money,
    _parse_zh_integer,
    _prepare_zh_itn_input,
    _restore_zh_ascii_electronic,
    _segment_zh_itn_tokens,
)


class ChineseITNRuleHelperTests(unittest.TestCase):
    def test_zh_itn_helper_restores_ascii_electronic_tokens(self) -> None:
        self.assertEqual(
            _restore_zh_ascii_electronic("邮箱test艾特example点com网址https冒号斜杠斜杠example点com斜杠a杠b"),
            "邮箱test@example.com网址https://example.com/a-b",
        )

    def test_zh_itn_helpers_segment_and_compact_embedded_tokens(self) -> None:
        self.assertEqual(
            _normalize_zh_itn_exact_hours("会议七点整开始十二点整结束二十五点整"),
            "会议07:00开始12:00结束二十五点整",
        )
        self.assertEqual(
            _normalize_zh_itn_negative_money("亏损负十二点五美元负三元"),
            "亏损-12.5美元-3元",
        )
        self.assertEqual(
            _prepare_zh_itn_input("我有一百二十三美元四十五美分电话加八六一三八零零一三八零零零"),
            "我有123.45美元电话+8613800138000",
        )
        self.assertEqual(
            _prepare_zh_itn_input("客服四零零杠八零零杠一二三四电话零一零杠一二三四五六七八"),
            "客服400-800-1234电话010-12345678",
        )
        self.assertEqual(
            _prepare_zh_itn_input("手机号幺三八零零幺三八零零零账号六二二二幺二三四五六七八九零幺二"),
            "手机号13800138000账号6222123456789012",
        )
        self.assertEqual(
            _prepare_zh_itn_input("银行卡六二二二空格一二三四空格五六七八空格九零一二"),
            "银行卡6222123456789012",
        )
        self.assertEqual(
            _prepare_zh_itn_input("电话加八六幺三八零零幺三八零零零转幺二三"),
            "电话+8613800138000转123",
        )
        self.assertEqual(
            _prepare_zh_itn_input("工号一二三四坐席A零八分机零零七"),
            "工号1234坐席A零八分机007",
        )
        self.assertEqual(
            _prepare_zh_itn_input("日期二零二六年六月十五号金额一百二十三元四角五分余额九角九分血压一百二十杠八十毫米汞柱"),
            "日期2026年06月15日 金额123.45元余额0.99元血压120/80mmHg",
        )
        self.assertEqual(
            _prepare_zh_itn_input("价格一千二百三十四块五毛六余额五分"),
            "价格1234.56元余额0.05元",
        )
        self.assertEqual(
            _prepare_zh_itn_input("嗯我有一块零五然后押金两毛五"),
            "我有1.05元然后押金0.25元",
        )
        self.assertEqual(
            _prepare_zh_itn_input("呃电话幺三八零零幺三八零零零哈"),
            "电话13800138000",
        )
        self.assertEqual(
            _prepare_zh_itn_input("价格三块五押金五毛余额五分钱"),
            "价格3.5元押金0.5元余额0.05元",
        )
        self.assertEqual(
            _prepare_zh_itn_input("评分四点八分满分五分得分九分满分十分"),
            "评分4.8/5得分9/10",
        )
        self.assertEqual(
            _prepare_zh_itn_input("价格十二点五元每斤速度八十公里每小时"),
            "价格12.5元/斤速度80km/h",
        )
        self.assertEqual(
            _prepare_zh_itn_input("金额一百二十三元整预算五十块整"),
            "金额123元预算50元",
        )
        self.assertEqual(
            _prepare_zh_itn_input("预算一万二收入三亿五营收二十万八"),
            "预算1.2万元收入3.5亿元营收20.8万元",
        )
        self.assertEqual(
            _prepare_zh_itn_input("编号A杠一二三比例三比二范围三到五天负百分之十二点五"),
            "编号A-123比例3:2范围3-5天-12.5%",
        )
        self.assertEqual(
            _prepare_zh_itn_input("增长正百分之十二下降负百分之三点五"),
            "增长+12%下降-3.5%",
        )
        self.assertEqual(
            _prepare_zh_itn_input("增长率百分之十二点五折扣百分之五十"),
            "增长率12.5%折扣50%",
        )
        self.assertEqual(
            _prepare_zh_itn_input("比例百分之二十到三十温度二十到三十度室温二十到三十摄氏度"),
            "比例20-30%温度20-30°C室温20-30°C",
        )
        self.assertEqual(
            _prepare_zh_itn_input("气温负五到五度室温零下五到五摄氏度华氏零下五度"),
            "气温-5-5°C室温-5-5°C-5°F",
        )
        self.assertEqual(
            _prepare_zh_itn_input("订单满一百减二十买一送一评分四点八分库存零件"),
            "订单满100减20买1送1评分4.8分库存0件",
        )
        self.assertEqual(
            _prepare_zh_itn_input("比例二分之一分数四分之三"),
            "比例二分之一分数四分之三",
        )
        self.assertEqual(
            _prepare_zh_itn_input("容量五百一十二兆字节缓存一百二十八千字节电流二十毫安"),
            "容量512MB缓存128KB电流20mA",
        )
        self.assertEqual(
            _prepare_zh_itn_input("吞吐一百二十兆字节每秒帧率六十帧每秒延迟十二毫秒内存二吉比字节"),
            "吞吐120MB/s帧率60fps延迟12ms内存2GiB",
        )
        self.assertEqual(
            _prepare_zh_itn_input("文件一点五GB下载一百二十兆字节每秒网速一百兆比特每秒"),
            "文件1.5GB下载120MB/s网速100Mbps",
        )
        self.assertEqual(
            _prepare_zh_itn_input("时长两小时三十分钟四十五秒角度九十度频率四十八千赫兹"),
            "时长2h30min45s角度90°频率48kHz",
        )
        self.assertEqual(
            _prepare_zh_itn_input("耗时一小时三十分钟等待两分三十秒冷却五百毫秒"),
            "耗时1h30min等待2min30s冷却500ms",
        )
        self.assertEqual(
            _prepare_zh_itn_input("时长一个半小时距离两公里半重量三千克半"),
            "时长1.5h距离两点五公里重量三点五千克",
        )
        self.assertEqual(
            _prepare_zh_itn_input("身高六英尺长度十二英寸重量五磅体积二盎司距离三英里速度五十五英里每小时"),
            "身高6ft长度12in重量5lb体积2oz距离3mi速度55mph",
        )
        self.assertEqual(
            _prepare_zh_itn_input("邮编一零零零八零公式三加五等于八，容量一升"),
            "邮编100080公式3+5=8，容量一升",
        )
        self.assertEqual(
            _prepare_zh_itn_input("误差千分之一明天六月十六日排名第二十一编号XJ杠二零二六杠零六"),
            "误差1‰明天06月16日排名第21编号XJ-2026-06",
        )
        self.assertEqual(_prepare_zh_itn_input("第二十一世纪第三名"), "21世纪第3名")
        self.assertEqual(_prepare_zh_itn_input("上午九点到下午六点营业晚上八点到九点维护"), "09:00-18:00营业20:00-21:00维护")
        self.assertEqual(
            _prepare_zh_itn_input("周一到周五营业周六到周日休息"),
            "周一-周五营业周六-周日休息",
        )
        self.assertEqual(
            _prepare_zh_itn_input("有效期二零二六年六月十五日到二零二六年六月二十日"),
            "有效期2026年06月15日-2026年06月20日",
        )
        self.assertEqual(
            _prepare_zh_itn_input("下午三点开会晚上八点零五分维护早上七点出发"),
            "15:00开会20:05维护07:00出发",
        )
        self.assertEqual(
            _prepare_zh_itn_input("上午九点半开会下午三点一刻提醒晚上八点三刻结束"),
            "09:30开会15:15提醒20:45结束",
        )
        self.assertEqual(
            _prepare_zh_itn_input("日期二零二六杠零六杠十五版本二零二六杠零六时区UTC加八温度负十二"),
            "日期2026-06-15版本二零二六杠零六时区UTC+8温度-12",
        )
        self.assertEqual(
            _prepare_zh_itn_input("室温零下三度体感零下五摄氏度"),
            "室温-3°C体感-5°C",
        )
        self.assertEqual(_prepare_zh_itn_input("版本三点十点四构建二零二六点零六编号NO十二"), "版本3.10.4构建2026.06编号NO12")
        self.assertEqual(_prepare_zh_itn_input("日期二零二六年六月"), "日期2026-06")
        self.assertEqual(
            _prepare_zh_itn_input("日期二零二六零六一五版本二零二六零六阈值x大于等于五y小于等于十增长三倍"),
            "日期2026-06-15版本二零二六零六阈值x>=5y<=10增长3倍",
        )
        self.assertEqual(
            _prepare_zh_itn_input("金额一点二万元预算三亿元增长二点五万"),
            "金额1.2万元预算3亿元增长2.5万",
        )
        self.assertEqual(
            _prepare_zh_itn_input("他今年五岁买了三件商品来了十二人试了两次"),
            "他今年5岁买了3件商品来了12人试了2次",
        )
        self.assertEqual(
            _prepare_zh_itn_input("面积八十平方米体积三立方米土地二平方公里浓度百分之零点零五"),
            "面积80m²体积3m³土地2km²浓度0.05%",
        )
        self.assertEqual(_prepare_zh_itn_input("摄氏二十三度华氏七十二度"), "23°C72°F")
        self.assertEqual(
            _compact_zh_itn_spacing("单价 3.5 元 每平方米面积80m²"),
            "单价3.5元/m²面积80m²",
        )
        self.assertEqual(
            _compact_zh_itn_spacing(
                _segment_zh_itn_tokens(
                    _prepare_zh_itn_input(
                        "电话一三八零零一三八零零零座机零一零杠一二三四五六七八周三八点零五分开会"
                    )
                )
            ),
            "电话13800138000座机010-12345678周三08:05开会",
        )
        self.assertEqual(
            _prepare_zh_itn_input("价格十元到二十元比例百分之十到百分之二十重量五到十千克"),
            "价格10-20元比例10-20%重量5-10kg",
        )
        self.assertEqual(
            _prepare_zh_itn_input("利率上行二十五个基点信用利差扩大三点五个基点用户一点二万营收三亿元"),
            "利率上行25bp信用利差扩大3.5bp用户1.2万营收3亿元",
        )
        self.assertEqual(
            _prepare_zh_itn_input("电阻十欧姆电流二安电压三点三毫伏电容四十七微法功率五瓦"),
            "电阻10Ω电流2A电压3.3mV电容47µF功率5W",
        )
        self.assertEqual(
            _prepare_zh_itn_input("力五牛顿压强一百零一帕气压零点一兆帕加速度九点八米每二次方秒转速三千转每分流量二升每分钟"),
            "力5N压强101Pa气压0.1MPa加速度9.8m/s²转速3000rpm流量2L/min",
        )
        self.assertEqual(
            _prepare_zh_itn_input("分辨率一千九百二十乘一千零八十尺寸十乘二十厘米"),
            "分辨率1920x1080尺寸10x20cm",
        )
        self.assertEqual(
            _prepare_zh_itn_input("增长二个百分点误差一乘以十的负五次方光速三乘以十的八次方米每秒"),
            "增长2pp误差1e-5光速3e8m/s",
        )
        self.assertEqual(
            _prepare_zh_itn_input("二零二六年第二季度收入增长第三季度二零二六展望改善财年二零二六预算"),
            "2026Q2收入增长2026Q3展望改善FY2026预算",
        )
        self.assertEqual(
            _prepare_zh_itn_input("订单号A B杠一二三四发票INV杠二零二六杠零零一快递单号SF一二三四五六七八九零电话四一五杠五五五杠零一二三转四五"),
            "订单号AB-1234发票INV-2026-001快递单号SF1234567890电话415-555-0123转45",
        )
        self.assertEqual(
            _prepare_zh_itn_input("地址十二号楼三单元五零二室车位B二杠一二三门牌八杠一"),
            "地址12号楼3单元502室车位B2-123门牌8-1",
        )
        self.assertEqual(
            _prepare_zh_itn_input("房间号A一二零八座位B零三会议室三零五"),
            "房间号A1208座位B03会议室305",
        )
        self.assertEqual(
            _prepare_zh_itn_input("手机号幺三八零零幺三八零零零尾号幺二三四"),
            "手机号13800138000尾号1234",
        )
        self.assertEqual(
            _prepare_zh_itn_input("工号幺二三四分机幺零七房间幺二零八"),
            "工号1234分机107房间1208",
        )
        self.assertEqual(
            _prepare_zh_itn_input("日期二零二六斜杠零六斜杠十五时间一四冒号三零"),
            "日期2026/06/15时间14:30",
        )
        self.assertEqual(
            _prepare_zh_itn_input("日期二零二六点零六点十五回访时间一四点三十分"),
            "日期2026.06.15回访时间14:30",
        )
        self.assertEqual(
            _prepare_zh_itn_input("工单号A B C井号一二三四"),
            "工单号ABC#1234",
        )
        self.assertEqual(
            _prepare_zh_itn_input("订单编号A B C冒号一二三四"),
            "订单编号ABC:1234",
        )
        self.assertEqual(
            _prepare_zh_itn_input("工单X下划线一二三参数q等于hello下划线world"),
            "工单X_123参数q=hello_world",
        )
        self.assertEqual(
            _prepare_zh_itn_input(
                "文件report下划线v二点零点pdf路径斜杠data斜杠input杠零一斜杠test点csv"
                "账号艾特light下划线user话题井号AI二零二六"
            ),
            "文件report_v2.0.pdf路径/data/input-01/test.csv账号@light_user话题#AI2026",
        )
        self.assertEqual(
            _compact_zh_itn_spacing(
                _prepare_zh_itn_input(
                    "链接https冒号斜杠斜杠example点com斜杠a杠b问号q等于hello下划线world与n等于一二三井号top"
                )
            ),
            "链接https://example.com/a-b?q=hello_world&n=123#top",
        )
        self.assertEqual(
            _prepare_zh_itn_input(
                "链接https冒号斜杠斜杠example点com斜杠a杠b问号q等于hello下划线world与n等于一二三井号top"
            ),
            "链接https冒号斜杠斜杠example点com斜杠a杠b问号q等于hello下划线world与n=123井号top",
        )
        self.assertEqual(
            _prepare_zh_itn_input(
                "MAC AA冒号BB冒号CC冒号DD冒号EE冒号FF"
                "UUID五五零e八四零零杠e二九b杠四一d四杠a七一六杠四四六六五五四四零零零零"
                "颜色井号FF五七三三"
            ),
            "MAC AA:BB:CC:DD:EE:FFUUID550e8400-e29b-41d4-a716-446655440000颜色#FF5733",
        )
        self.assertEqual(
            _prepare_zh_itn_input(
                "温度七十二华氏度温差三百开尔文服务器一二七点零点零点一冒号八零八零"
                "IPv6二零零一冒号零db八冒号冒号一"
                "ISBN九七八杠七杠一一一杠一二三四五杠六DOI一零点一零零零斜杠xyz一二三"
            ),
            "温度72°F温差300K服务器127.0.0.1:8080"
            "IPv62001:0db8::1ISBN978-7-111-12345-6DOI10.1000/xyz123",
        )
        self.assertEqual(_prepare_zh_itn_input("版本v二点零点一杠beta点三"), "版本v2.0.1-beta.3")
        self.assertEqual(
            _prepare_zh_itn_input("接口返回HTTP四零四端口八零八零截止到二零二六杠零六杠一五T一四冒号三零冒号零五Z"),
            "接口返回HTTP404端口8080截止到2026-06-15T14:30:05Z",
        )
        self.assertEqual(
            _prepare_zh_itn_input("按Ctrl加C再按Cmd加Shift加P时间二零二六杠零六杠一五一四冒号三零冒号零五"),
            "按Ctrl+C再按Cmd+Shift+P时间2026-06-15 14:30:05",
        )
        self.assertEqual(
            _prepare_zh_itn_input("截止二零二六杠零六杠一五十四点三十分零五秒"),
            "截止2026-06-15 14:30:05",
        )
        self.assertEqual(
            _prepare_zh_itn_input("会议十四点三十分开始七点零五分备份误差正负零点五毫米x约等于五"),
            "会议14:30开始07:05备份误差±0.5mmx≈5",
        )
        self.assertEqual(
            _prepare_zh_itn_input("营业时间九点到十八点三十分会议十四点三十分到十五点四十五分"),
            "营业时间09:00-18:30会议14:30-15:45",
        )
        self.assertEqual(
            _prepare_zh_itn_input("我有一百二十三元四角五分押金五十块五毛"),
            "我有123.45元押金50.5元",
        )
        self.assertEqual(
            _prepare_zh_itn_input("x约等于五y小于等于十z大于等于三a不等于b"),
            "x≈5y<=10z>=3a!=b",
        )
        self.assertEqual(_compact_zh_itn_spacing("温度72华氏度温差300开尔文"), "温度72°F温差300K")
        self.assertEqual(
            _prepare_zh_itn_input("车牌京A一二三四五护照E一二三四五六七八身份证一一零一零五一九九零零三零七八六一X"),
            "车牌京A12345护照E12345678身份证11010519900307861X",
        )
        self.assertEqual(
            _prepare_zh_itn_input("统一社会信用代码九一一一零一零五M A零零零一二三四五"),
            "统一社会信用代码91110105MA00012345",
        )
        self.assertEqual(
            _prepare_zh_itn_input("地址北京市朝阳区建国路八十八号A座一二零八室十二楼邮编一零零零八零"),
            "地址北京市朝阳区建国路88号A座1208室12楼邮编100080",
        )
        self.assertEqual(
            _prepare_zh_itn_input("血糖五点六毫摩尔每升血压一百二十毫米汞柱气压一百零一千帕"),
            "血糖5.6mmol/L血压120mmHg气压101kPa",
        )
        self.assertEqual(
            _prepare_zh_itn_input("维生素D二十五国际单位每升药物二微克每毫升激素五十纳克每毫升样本二十微升"),
            "维生素D25IU/L药物2µg/mL激素50ng/mL样本20µL",
        )
        self.assertEqual(
            _prepare_zh_itn_input("酸碱度pH七点四噪声三十分贝功率密度八十瓦每平方米扭矩五牛米电池五千毫安时"),
            "酸碱度pH7.4噪声30dB功率密度80W/m²扭矩5N·m电池5000mAh",
        )
        self.assertEqual(
            _prepare_zh_itn_input("会议七点零五分零九秒开始，电话四零零杠八零零杠一二三四，八折概率百分之零点零五"),
            "会议07:05:09开始，电话400-800-1234，8折概率0.05%",
        )
        self.assertEqual(
            _prepare_zh_itn_input("账号六二二二一二三四五六七八九零一二，八折"),
            "账号6222123456789012，8折",
        )
        self.assertEqual(
            _segment_zh_itn_tokens("二零二六年六月十五日 我有一百二十三元"),
            "二零二六年六月十五日 我有 一百二十三元",
        )
        self.assertEqual(
            _segment_zh_itn_tokens("我有五十元和一百二十三元钱"),
            "我有 五十元 和 一百二十三元 钱",
        )
        self.assertEqual(
            _segment_zh_itn_tokens("室温负三点五摄氏度湿度百分之十二点五"),
            "室温 负三点五摄氏度 湿度 百分之十二点五",
        )
        self.assertEqual(
            _segment_zh_itn_tokens("面积九十平米速度八十千米每小时"),
            "面积 九十平米 速度 八十千米每小时",
        )
        self.assertEqual(
            _segment_zh_itn_tokens("比例二分之一分数四分之三"),
            "比例 二分之一 分数 四分之三",
        )
        self.assertEqual(
            _segment_zh_itn_tokens("会议在七点三十分开始电话一三五零一二三四五六七"),
            "会议在 七点三十分 开始电话 一三五零一二三四五六七",
        )
        self.assertEqual(_segment_zh_itn_tokens("一百二十三元"), "一百二十三元")
        self.assertEqual(
            _compact_zh_itn_spacing("2026年06月15日 我有 123元 钱"),
            "2026年06月15日 我有123元钱",
        )
        self.assertEqual(
            _compact_zh_itn_spacing("会议在 07:30 开始 电话 13501234567"),
            "会议在07:30开始 电话13501234567",
        )
        self.assertEqual(_compact_zh_itn_spacing("速度 80km每小时"), "速度80km/h")
        self.assertEqual(
            _compact_zh_itn_spacing("我有 USD12 GBP3 和 €12.5"),
            "我有12美元3英镑和12.5欧元",
        )
        self.assertEqual(
            _compact_zh_itn_spacing("速度10米 每秒 网速100mbps 容量16gb 电压220v"),
            "速度10m/s网速100Mbps容量16GB电压220V",
        )
        self.assertEqual(
            _compact_zh_itn_spacing("加速度 9.8米每二次方秒 流量 2L每分钟 压强 101pa"),
            "加速度9.8m/s²流量2L/min压强101Pa",
        )
        self.assertEqual(
            _compact_zh_itn_spacing("坐标北纬39.9deg东经116.4度"),
            "坐标北纬39.9°东经116.4°",
        )
        self.assertEqual(_compact_zh_itn_spacing("容量 1升 面积 80m²"), "容量1L面积80m²")
        self.assertEqual(_compact_zh_itn_spacing("密度 5kg每平方米"), "密度5kg/m²")
        self.assertEqual(_compact_zh_itn_spacing("温度 -3.5摄氏度"), "温度-3.5°C")
        self.assertEqual(
            _compact_zh_itn_spacing("邮箱user点name加tag@example点co点uk"),
            "邮箱user.name+tag@example.co.uk",
        )
        self.assertEqual(_compact_zh_itn_spacing("第十二届会议 第三名"), "第12届会议 第3名")
        self.assertEqual(_compact_zh_itn_spacing("编号A一二三B 编号ABC一二三"), "编号A123B 编号ABC123")

    def test_zh_integer_parser_handles_common_ordinal_numbers(self) -> None:
        self.assertEqual(_parse_zh_integer("三"), 3)
        self.assertEqual(_parse_zh_integer("十二"), 12)
        self.assertEqual(_parse_zh_integer("二十一"), 21)
        self.assertEqual(_parse_zh_integer("一百二十三"), 123)
        self.assertEqual(_parse_zh_integer("一千零二"), 1002)
        self.assertEqual(_parse_zh_integer("一亿二千万三千"), 120003000)

    def test_zh_itn_finalize_outputs_restores_spoken_markup(self) -> None:
        self.assertEqual(
            finalize_outputs(["标题：客户信息换行手机号13800138000"]),
            ["标题：客户信息\n手机号13800138000"],
        )
        self.assertEqual(
            finalize_outputs(["文件名左书名号测试右书名号空格路径斜杠data斜杠input省略号"]),
            ["文件名《测试》 路径/data/input……"],
        )
        self.assertEqual(
            finalize_outputs(["账号小明艾特example下划线corp井号vip参数q等号hello"]),
            ["账号小明@example_corp#vip参数q=hello"],
        )
        self.assertEqual(
            finalize_outputs(["密码A加号B减号C星号D百分号"]),
            ["密码A+B-C*D%"],
        )
        self.assertEqual(
            finalize_outputs(["核验通过对勾未通过叉号备注待复核"]),
            ["核验通过✓未通过×备注待复核"],
        )
        self.assertEqual(
            finalize_outputs(["姓名制表符张三换行备注空行完成"]),
            ["姓名\t张三\n备注\n\n完成"],
        )
        self.assertEqual(
            finalize_outputs(["项目符号检查身份证换行项目符号确认手机号"]),
            ["- 检查身份证\n- 确认手机号"],
        )
        self.assertEqual(
            finalize_outputs(["一级标题会议纪要换行二级标题待办事项换行项目符号确认手机号"]),
            ["# 会议纪要\n## 待办事项\n- 确认手机号"],
        )
        self.assertEqual(
            finalize_outputs(["编号一确认身份换行编号二确认手机号"]),
            ["1. 确认身份\n2. 确认手机号"],
        )
        self.assertEqual(
            finalize_outputs(["加粗开始重要客户加粗结束换行代码开始status_code代码结束"]),
            ["**重要客户**\n`status_code`"],
        )
        self.assertEqual(
            finalize_outputs(["模板左大括号name冒号张三右大括号标签左尖括号vip右尖括号"]),
            ["模板{name：张三}标签<vip>"],
        )
        self.assertEqual(
            finalize_outputs(["路径C：反斜杠Users反斜杠test正则A竖线B波浪号tmp"]),
            ["路径C：\\Users\\test正则A|B~tmp"],
        )


if __name__ == "__main__":
    unittest.main()
