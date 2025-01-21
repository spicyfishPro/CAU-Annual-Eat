import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# 设置中文字体
font_path = "./font/NotoSansCJKtc-Regular.otf"
if os.path.exists(font_path):
    from matplotlib import font_manager

    font_prop = font_manager.FontProperties(fname=font_path)
    plt.rcParams["font.family"] = font_prop.get_name()
else:
    print("警告：未找到指定的中文字体。中文可能无法正常显示。")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = [
        "Arial Unicode MS"
    ]  # 尝试使用系统中的其他中文支持字体

plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 读取JSON数据
with open("consumption_records.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 转换为DataFrame
df = pd.DataFrame(data)

# 数据预处理
# 转换日期
df["txdate"] = pd.to_datetime(df["txdate"], format="%Y-%m-%d %H:%M:%S")

# 转换交易金额为浮点数
df["txamt"] = df["txamt"].astype(float)

# 只保留消费记录（txamt为负数）
df = df[df["txamt"] < 0]

# 添加额外的时间列（如年份、月份等）
df["year"] = df["txdate"].dt.year
df["month"] = df["txdate"].dt.month
df["day"] = df["txdate"].dt.day

# 统计每月消费总额
monthly_expense = df.groupby(["year", "month"])["txamt"].sum().reset_index()
monthly_expense["txamt"] = monthly_expense["txamt"].abs()  # 转为正数便于展示

# 统计每个商家的消费总额
merchant_expense = df.groupby("mername")["txamt"].sum().abs().reset_index()
merchant_expense = merchant_expense.sort_values(by="txamt", ascending=False)

# 绘制每月消费趋势图
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=monthly_expense, x="month", y="txamt", hue="year", marker="o"
)
plt.title(
    "每月消费总额趋势",
    fontproperties=font_prop if os.path.exists(font_path) else None,
)
plt.xlabel(
    "月份", fontproperties=font_prop if os.path.exists(font_path) else None
)
plt.ylabel(
    "消费金额（元）",
    fontproperties=font_prop if os.path.exists(font_path) else None,
)
plt.legend(title="年份")
plt.xticks(range(1, 13))
plt.grid(True)

# 保存每月消费趋势图
plt.tight_layout()
plt.savefig("monthly_expense_trend.png")
plt.close()

print("已保存每月消费趋势图：monthly_expense_trend.png")

# 绘制各商家消费分布柱状图（前10名）
top_n = 10
top_merchants = merchant_expense.head(top_n)

plt.figure(figsize=(14, 7))
sns.barplot(data=top_merchants, x="mername", y="txamt", palette="viridis")
plt.title(
    f"消费最多的前{top_n}个商家",
    fontproperties=font_prop if os.path.exists(font_path) else None,
)
plt.xlabel(
    "商家名称", fontproperties=font_prop if os.path.exists(font_path) else None
)
plt.ylabel(
    "消费金额（元）",
    fontproperties=font_prop if os.path.exists(font_path) else None,
)
plt.xticks(rotation=45, ha="right")

# 保存各商家消费分布柱状图
plt.tight_layout()
plt.savefig("./img/top_merchants_expense.png")
plt.close()

print("已保存各商家消费分布柱状图：top_merchants_expense.png")

# 绘制消费金额分布的直方图（可选）
plt.figure(figsize=(10, 6))
sns.histplot(df["txamt"].abs(), bins=30, kde=True, color="skyblue")
plt.title(
    "消费金额分布",
    fontproperties=font_prop if os.path.exists(font_path) else None,
)
plt.xlabel(
    "消费金额（元）",
    fontproperties=font_prop if os.path.exists(font_path) else None,
)
plt.ylabel(
    "频数", fontproperties=font_prop if os.path.exists(font_path) else None
)

# 保存消费金额分布直方图
plt.tight_layout()
plt.savefig("./img/expense_distribution.png")
plt.close()

print("已保存消费金额分布直方图：expense_distribution.png")

# 绘制消费比例饼图（前10个商家）
plt.figure(figsize=(8, 8))
# 为了不让饼图过于拥挤，只选择前10个商家
plt.pie(
    top_merchants["txamt"],
    labels=top_merchants["mername"],
    autopct="%1.1f%%",
    startangle=140,
    colors=sns.color_palette("viridis", top_n),
)
plt.title(
    f"消费最多的前{top_n}个商家占比",
    fontproperties=font_prop if os.path.exists(font_path) else None,
)

# 保存饼图
plt.tight_layout()
plt.savefig("./img/top_merchants_pie_chart.png")
plt.close()

print("已保存各商家消费比例饼图：top_merchants_pie_chart.png")
