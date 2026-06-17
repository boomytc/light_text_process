# 关于法语拼写的说明

由于 1990 年的拼写改革，目前法语数字在书面表达上存在两种约定：

1. **改革版** 所有复合词都使用连字符连接：
例如 `1122 -> mille-cent-vingt-deux`

2. **传统版** 只有 17 到 99（含）之间的数字才使用连字符（有例外）：
例如 `1122 -> mille cent vingt-deux`

由于上游 ASR 的训练数据在书写约定上各有不同，NeMo 的法语 ITN 在规范化时对两种风格都兼容，例如：

```
	python inverse_normalize.py "mille-cent-vingt-deux" --language="fr"  --> 1122
	python inverse_normalize.py "mille cent vingt-deux" --language="fr"  --> 1122
```

因此，在货币换算中（尤其是美元的小单位）存在一定歧义，例如：

```
	300 -> "trois-cents" # 改革版拼写
	300 -> "trois cents" # 传统版拼写
	3 ¢ -> "trois cents" # 两者均有效
```

此类情况下基数词优先。

```
python inverse_normalize.py "trois cents" --language="fr" -> 300
```
