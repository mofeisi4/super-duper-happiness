# 导入库
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 加载数据
data = pd.DataFrame({
    "Year": [2020, 2021, 2022, 2023],
    "GDP_Growth": [2.3, 8.1, 3.0, 5.2],
    "Youth_Unemployment": [14.2, 13.5, 14.5, 15.0],
    "SME_Employment_Share": [78, 75, 73, 72]  # 单位：%
})
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 构建回归模型
model = LinearRegression()
model.fit(data[["GDP_Growth"]], data["Youth_Unemployment"])

# 政策模拟函数
def policy_simulator(gdp_target, tax_cut, training_investment):
    # 预测基准失业率
    baseline_unemployment = model.predict([[gdp_target]])[0]
    
    # 计算政策效果
    tax_effect = baseline_unemployment * (tax_cut * 0.002)
    training_effect = (training_investment / 10) * 0.5
    adjusted_unemployment = baseline_unemployment - tax_effect - training_effect
    adjusted_unemployment = max(adjusted_unemployment, 0)  # 失业率不低于0
    
    # 输出结果
    print(f"目标GDP增速：{gdp_target}%")
    print(f"税收减免比例：{tax_cut}% → 降低失业率：{tax_effect:.2f}%")
    print(f"培训投入：{training_investment}亿元 → 降低失业率：{training_effect:.2f}%")
    print(f"预测青年失业率：{adjusted_unemployment:.1f}%")
    
    # 绘制柱状图
    plt.figure(figsize=(8,4))
    plt.bar(["基准失业率", "调整后失业率"], [baseline_unemployment, adjusted_unemployment], color=["gray", "blue"])
    plt.title("政策模拟结果")
    plt.ylabel("青年失业率 (%)")
    plt.ylim(0, 20)
    plt.xticks(rotation=45)  # 旋转X轴标签
    plt.tight_layout()       # 自动调整布局
    plt.savefig("policy_simulation.png", dpi=300, bbox_inches="tight")  # 保存图表
    plt.show()

# 手动输入参数并运行模拟
if __name__ == "__main__":
    # 手动设置参数
    gdp_target = float(input("请输入目标GDP增速（%）："))
    tax_cut = float(input("请输入税收减免比例（%）："))
    training_investment = float(input("请输入培训投入（亿元）："))
    
    # 运行政策模拟
    policy_simulator(gdp_target, tax_cut, training_investment)
