import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 網頁基本設定
st.set_page_config(page_title="Smith Manoeuvre 模擬器", layout="wide")
st.title("Smith Manoeuvre 財富加速模擬器")
st.markdown("這是一個專為加拿大屋主設計的財務工具，展示如何透過合法的稅務優化，將無法抵稅的「壞債」轉換為能產生被動收入的「好債」。")

# 側邊欄：使用者輸入參數
st.sidebar.header("請輸入你的財務數據")
mortgage_principal = st.sidebar.number_input("目前房貸餘額 ($)", value=590000, step=10000)
mortgage_rate = st.sidebar.number_input("傳統房貸利率 (%)", value=4.99, step=0.1) / 100
heloc_rate = st.sidebar.number_input("HELOC 借貸利率 (%)", value=4.95, step=0.1) / 100
tax_rate = st.sidebar.number_input("你的最高邊際稅率 (%)", value=43.41, step=0.1) / 100
investment_yield = st.sidebar.number_input("預期投資回報率 (%)", value=6.72, step=0.1) / 100
monthly_payment = st.sidebar.number_input("每月預計繳納本金 ($)", value=1500, step=100)

# 核心數學計算 (簡化版年度投影)
years = 20
data = []
current_mortgage = mortgage_principal
current_invested = 0

# 稅後借款成本計算
after_tax_borrowing_cost = heloc_rate * (1 - tax_rate)

for year in range(1, years + 1):
    if current_mortgage > 0:
        # 傳統還款
        yearly_principal_paid = monthly_payment * 12
        
        # SM 加速器：投資產生的現金流與退稅
        annual_dividend = current_invested * investment_yield
        annual_tax_refund = (current_invested * heloc_rate) * tax_rate
        
        # 加速還款總額
        total_prepayment = yearly_principal_paid + annual_dividend + annual_tax_refund
        
        current_mortgage -= total_prepayment
        if current_mortgage < 0:
            current_mortgage = 0
            
        # 額度釋放並進行再投資
        current_invested += total_prepayment
        
    data.append({
        "Year": year,
        "傳統房貸 (壞債)": max(0, current_mortgage),
        "投資組合價值 (資產)": current_invested,
        "HELOC 餘額 (好債)": current_invested
    })

df = pd.DataFrame(data)

# 主畫面：數據儀表板
col1, col2, col3 = st.columns(3)
col1.metric("稅後實質借錢成本", f"{after_tax_borrowing_cost*100:.2f}%", "享有稅務抵扣")
col2.metric("投資與借錢的淨利差", f"{(investment_yield - after_tax_borrowing_cost)*100:.2f}%", "正向套利空間")

# 尋找壞債歸零的年份
payoff_year = df[df["傳統房貸 (壞債)"] == 0]["Year"].min()
if pd.isna(payoff_year):
    col3.metric("預計壞債結清時間", "> 20 年")
else:
    col3.metric("預計壞債結清時間", f"第 {int(payoff_year)} 年", "大幅縮短還款期")

# 繪製動態圖表
st.subheader("未來 20 年財富軌跡投影")
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Year"], y=df["傳統房貸 (壞債)"], mode='lines+markers', name='傳統房貸 (壞債)', line=dict(color='red')))
fig.add_trace(go.Scatter(x=df["Year"], y=df["投資組合價值 (資產)"], mode='lines+markers', name='投資組合價值 (資產)', line=dict(color='green')))
fig.add_trace(go.Scatter(x=df["Year"], y=df["HELOC 餘額 (好債)"], mode='lines', name='HELOC 餘額 (抵稅好債)', line=dict(color='orange', dash='dash')))

fig.update_layout(xaxis_title="執行年度", yaxis_title="金額 (加幣 $)", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

st.info("💡 這個模擬器假設所有投資收益與退稅，都 100% 再次投入償還傳統房貸，以達到最大的飛輪加速效果。")
