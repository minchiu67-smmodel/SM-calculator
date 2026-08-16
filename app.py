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

# 建立三個分頁
tab1, tab2, tab3 = st.tabs(["🔄 模組一：飛輪概念圖解", "📊 模組二：專屬數據沙盒", "🛡️ 模組三：稅務透視鏡"])

# --- 模組一 ---
with tab1:
    st.header("什麼是 Smith Manoeuvre？ (資金飛輪)")
    st.markdown("這個策略的核心，就是讓同一筆錢為你做兩件事：**同時消滅房貸，又同時累積資產。** 讓我們用 5 個簡單的步驟來看看它是如何運作的：")
    st.write("---")
    st.info("### 步驟 1：日常繳款 ➡️ 房貸本金減少\n每個月你用日常薪水繳交傳統房貸。只要「本金」減少了，銀行的連動系統就會立刻啟動。")
    st.markdown("<h2 style='text-align: center;'>⬇️</h2>", unsafe_allow_html=True)
    st.warning("### 步驟 2：銀行釋放額度 🔓 (Readvanceable)\n你的傳統房貸每還掉 $1,000 的本金，旁邊的 HELOC (理財型房貸) 抽屜就會自動多出 $1,000 的可用借款額度。")
    st.markdown("<h2 style='text-align: center;'>⬇️</h2>", unsafe_allow_html=True)
    st.success("### 步驟 3：借出額度 ➡️ 買入高息資產 📈\n你把這 $1,000 借出來放進投資帳戶，買入能穩定配息的資產。\n*(💡 此時你的總負債沒有增加，你只是把「不能抵稅的壞債」，轉換成了「能幫你賺錢的好債」)*")
    st.markdown("<h2 style='text-align: center;'>⬇️</h2>", unsafe_allow_html=True)
    st.error("### 步驟 4：收取股息 ＋ 獲取退稅 💰\n這些資產每個月會發放「股息」給你；到了隔年春天報稅時，因為這筆借款是用來投資的，加拿大稅務局 (CRA) 還會退回一筆「利息抵稅」的現金給你。")
    st.markdown("<h2 style='text-align: center;'>🔄 飛輪自動扣板機 🔄</h2>", unsafe_allow_html=True)
    st.info("### 步驟 5：加速砸向房貸 🚀\n你把賺到的「股息」和「退稅」，全部再次拿去還傳統房貸（回到步驟 1）。\n\n**這就是 Aha Moment 💡：** 下個月你的本金降得更快 ➡️ 釋放的額度更多 ➡️ 買的資產更多 ➡️ 領的股息更多！原本要 25 年的房貸，就這樣被暴風式地縮短了。")

# --- 模組二 ---
with tab2:
    st.header("輸入你的數據，看看真實的加速效果")
    after_tax_borrowing_cost = heloc_rate * (1 - tax_rate)

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

# --- 模組三 ---
with tab3:
    st.header("破解迷思：借錢投資真的太貴了嗎？")
    after_tax_borrowing_cost = heloc_rate * (1 - tax_rate)
    
    st.markdown("很多人以為借 **4.95%** 的錢，就必須找到至少配息 5% 的標的才不會虧本。這是錯的！因為 **「投資借貸的利息可以 100% 抵稅」**。")
    
    col_a, col_b = st.columns(2)
    col_a.metric(label="表面上的借貸利率 (Nominal Rate)", value=f"{heloc_rate*100:.2f}%")
    col_b.metric(label="真正的稅後借貸成本 (After-Tax Cost)", value=f"{after_tax_borrowing_cost*100:.2f}%", delta="因為政府幫你付了部分利息", delta_color="normal")
    
    st.write("---")
    st.subheader("不同投資標的的「損益平衡點 (Break-even Return)」")
    st.markdown("如果你的實質成本只有 2.80% 左右，那這筆錢去買不同的資產，**稅前要賺多少才能剛好打平？**")
    
    # 計算不同收入的稅率與損益平衡點
    cap_gain_tax_rate = tax_rate * 0.5
    eligible_div_tax_rate = tax_rate * 0.6 # 簡化的稅務抵免估值
    
    be_interest = after_tax_borrowing_cost / (1 - tax_rate)
    be_cap_gain = after_tax_borrowing_cost / (1 - cap_gain_tax_rate)
    be_div = after_tax_borrowing_cost / (1 - eligible_div_tax_rate)
    
    col_x, col_y, col_z = st.columns(3)
    
    with col_x:
        st.info("### 一般利息收入\n如 GIC 定存、債券")
        st.metric(label="需達到的稅前報酬", value=f"{be_interest*100:.2f}%")
        st.caption("利息收入沒有稅務優惠，所以你賺的利息必須完全等於你借款的利率才能打平。")
        
    with col_y:
        st.warning("### 加拿大合格股息\n如 VDY、大型銀行股")
        st.metric(label="需達到的稅前報酬", value=f"{be_div*100:.2f}%")
        st.caption("因為享有 Dividend Tax Credit，你的股息只要超過這個數字，就開始賺錢了。")
        
    with col_z:
        st.success("### 資本利得\n如 成長股、EIT.UN")
        st.metric(label="需達到的稅前報酬", value=f"{be_cap_gain*100:.2f}%")
        st.caption("加拿大最高效的收入！因為只有 50% 要課稅，損益平衡門檻極低。這就是為什麼 EIT.UN 的 96% 資本利得結構如此強大。")
