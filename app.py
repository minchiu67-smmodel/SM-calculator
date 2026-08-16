import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 網頁基本設定
st.set_page_config(page_title="Smith Manoeuvre 模擬器", layout="wide")
st.title("Smith Manoeuvre 財富加速模擬器")
st.markdown("這是一個專為加拿大屋主設計的財務工具，展示如何透過合法的稅務優化，將無法抵稅的「壞債」轉換為能產生被動收入的「好債」。")

# 側邊欄：使用者輸入參數 (全域共用)
st.sidebar.header("⚙️ 請輸入你的財務數據")
mortgage_principal = st.sidebar.number_input("目前房貸餘額 ($)", value=590000, step=10000)
mortgage_rate = st.sidebar.number_input("傳統房貸利率 (%)", value=4.99, step=0.1) / 100
heloc_rate = st.sidebar.number_input("HELOC 借貸利率 (%)", value=4.95, step=0.1) / 100
tax_rate = st.sidebar.number_input("你的最高邊際稅率 (%)", value=43.41, step=0.1) / 100
investment_yield = st.sidebar.number_input("預期投資回報率 (%)", value=6.72, step=0.1) / 100
monthly_payment = st.sidebar.number_input("每月預計繳納本金 ($)", value=1500, step=100)

tab1, tab2 = st.tabs(["🔄 模組一：飛輪概念圖解", "📊 模組二：專屬數據沙盒"])

with tab1:
    st.header("什麼是 Smith Manoeuvre？ (資金迴圈)")
    st.markdown("""
    這個策略的核心，就是讓同一筆錢為你做兩件事：**同時消滅房貸，又同時累積資產。**
    下方的「資金水流圖 (Sankey Diagram)」展示了這個自動化的飛輪是如何運轉的：
    """)
    
    # 建立 Sankey Diagram
    fig_sankey = go.Figure(data=[go.Sankey(
        node = dict(
          pad = 30,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
          label = [
              "1. 薪水 (日常現金流)", 
              "2. 傳統房貸 (還本金消滅壞債)", 
              "3. 銀行 HELOC (額度自動釋放)", 
              "4. 投資帳戶 (買入高息資產)", 
              "5. 股息與退稅 (創造新現金流)", 
              "6. 加速砸向房貸 (飛輪啟動！)"
          ],
          color = ["#2CA02C", "#D62728", "#1F77B4", "#FF7F0E", "#9467BD", "#D62728"]
        ),
        link = dict(
          source = [0, 1, 2, 3, 4], # 節點起點
          target = [1, 2, 3, 4, 5], # 節點終點
          value = [100, 100, 100, 40, 40], # 水管粗細比例
          label = ["每月例行繳款", "1:1 自動連動", "借出投資", "產生被動收入", "再次還本金"]
        )
    )])
    
    fig_sankey.update_layout(height=450, font_size=14, margin=dict(l=0, r=0, t=20, b=20))
    st.plotly_chart(fig_sankey, use_container_width=True)
    
    st.success("💡 **Aha Moment (頓悟時刻):** 注意看最後一條紫色的水管！以前你的房貸只能靠薪水苦苦地還（最左邊綠色水管）；啟動 SM 後，你多了一支由「投資收益」與「稅務局退稅」組成的軍隊，每個月都在幫你一起消滅房貸。這就是它能將 25 年貸款暴縮的秘密。")

with tab2:
    st.header("輸入你的數據，看看真實的加速效果")
    
    # 稅後借款成本計算
    after_tax_borrowing_cost = heloc_rate * (1 - tax_rate)

    # 核心數學計算 (簡化版年度投影)
    years = 20
    data = []
    current_mortgage = mortgage_principal
    current_invested = 0

    for year in range(1, years + 1):
        if current_mortgage > 0:
            yearly_principal_paid = monthly_payment * 12
            annual_dividend = current_invested * investment_yield
            annual_tax_refund = (current_invested * heloc_rate) * tax_rate
            total_prepayment = yearly_principal_paid + annual_dividend + annual_tax_refund
            
            current_mortgage -= total_prepayment
            if current_mortgage < 0:
                current_mortgage = 0
                
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

    payoff_year = df[df["傳統房貸 (壞債)"] == 0]["Year"].min()
    if pd.isna(payoff_year):
        col3.metric("預計壞債結清時間", "> 20 年")
    else:
        col3.metric("預計壞債結清時間", f"第 {int(payoff_year)} 年", "大幅縮短還款期")

    st.subheader("未來 20 年財富軌跡投影")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Year"], y=df["傳統房貸 (壞債)"], mode='lines+markers', name='傳統房貸 (壞債)', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df["Year"], y=df["投資組合價值 (資產)"], mode='lines+markers', name='投資組合價值 (資產)', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df["Year"], y=df["HELOC 餘額 (好債)"], mode='lines', name='HELOC 餘額 (抵稅好債)', line=dict(color='orange', dash='dash')))

    fig.update_layout(xaxis_title="執行年度", yaxis_title="金額 (加幣 $)", hovermode="x unified", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("📌 這個圖表假設所有投資收益與年度退稅，都 100% 再次投入償還傳統房貸，以達到最大的飛輪加速效果。")
