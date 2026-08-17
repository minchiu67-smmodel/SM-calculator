import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 網頁基本設定
st.set_page_config(page_title="Smith Manoeuvre 模擬器", layout="wide")
st.title("Smith Manoeuvre 財富加速模擬器")
st.markdown("這是一個專為加拿大屋主設計的財務工具，展示如何透過合法的稅務優化，將無法抵稅的「壞債」轉換為能產生被動收入的「好債」。")

# 側邊欄：使用者輸入參數
st.sidebar.header("⚙️ 請輸入你的財務數據")

with st.sidebar.expander("🔍 不知道自己的邊際稅率？點此估算"):
    st.markdown("**(以安大略省 2026 綜合稅階為例)**")
    income = st.number_input("請輸入你的預估年薪 ($)", value=115000, step=5000)
    
    if income <= 53891: est_tax = 20.05
    elif income <= 58523: est_tax = 23.15
    elif income <= 94907: est_tax = 29.65
    elif income <= 107785: est_tax = 31.48
    elif income <= 111814: est_tax = 33.89
    elif income <= 117045: est_tax = 37.91
    elif income <= 150000: est_tax = 43.91
    elif income <= 181440: est_tax = 44.97
    elif income <= 220000: est_tax = 48.26
    elif income <= 258482: est_tax = 51.97
    else: est_tax = 53.53
        
    st.success(f"💡 你的邊際稅率約為：**{est_tax}%**")
    st.caption("👉 請將這個數字填入下方的「最高邊際稅率」欄位中。")
    st.write("---")

property_value = st.sidebar.number_input("房屋最新預估市值 ($)", value=1000000, step=50000)
mortgage_principal = st.sidebar.number_input("目前房貸餘額 ($)", value=590000, step=10000)
mortgage_rate = st.sidebar.number_input("傳統房貸利率 (%)", value=4.99, step=0.1) / 100
amortization_years = st.sidebar.number_input("剩餘貸款年數 (Amortization)", value=25, step=1)
heloc_rate = st.sidebar.number_input("HELOC 借貸利率 (%)", value=4.95, step=0.1) / 100
tax_rate = st.sidebar.number_input("你的最高邊際稅率 (%)", value=37.91, step=0.1) / 100
investment_yield = st.sidebar.number_input("預期投資回報率 (%)", value=6.72, step=0.1) / 100

heloc_limit = property_value * 0.65

# 建立四個分頁
tab1, tab2, tab3, tab4 = st.tabs(["🔄 模組一：飛輪概念圖解", "🛡️ 模組二：稅務透視鏡", "📊 模組三：專屬數據沙盒", "⚠️ 模組四：風險與常見問題 (FAQ)"])

# --- 模組一：飛輪概念 ---
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

# --- 模組二：稅務透視鏡 ---
with tab2:
    st.header("破解迷思：借錢投資真的太貴了嗎？")
    after_tax_borrowing_cost = heloc_rate * (1 - tax_rate)
    st.markdown(f"很多人以為借 **{heloc_rate*100:.2f}%** 的錢，就必須找到至少配息一樣多的標的才不會虧本。這是錯的！因為在加拿大，**「為了投資而借款的利息，可以 100% 用來抵稅」**。")
    st.info(f"### 🧮 稅後成本公式\n**名目借貸利率 ({heloc_rate*100:.2f}%) × [ 1 - 你的邊際稅率 ({tax_rate*100:.2f}%) ] = 稅後實質成本 ({after_tax_borrowing_cost*100:.2f}%)**")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="表面借貸利率 (Nominal Rate)", value=f"{heloc_rate*100:.2f}%")
    col_b.metric(label="CRA 退稅比例 (Tax Refund)", value=f"- {tax_rate*100:.2f}%")
    col_c.metric(label="真正稅後成本 (Net Cost)", value=f"{after_tax_borrowing_cost*100:.2f}%", delta="實質成本大幅降低", delta_color="normal")
    
    st.write("---")
    st.subheader("必懂觀念：三種投資收入的稅務差異")
    col_x, col_y, col_z = st.columns(3)
    be_interest = after_tax_borrowing_cost / (1 - tax_rate)
    be_div = after_tax_borrowing_cost / (1 - (tax_rate * 0.6)) 
    be_cap_gain = after_tax_borrowing_cost / (1 - (tax_rate * 0.5))
    
    with col_x:
        st.error("### 1. 一般利息 (Interest)\n例如：GIC 定存、債券")
        st.markdown("**稅務重災區：** 賺到的每一塊錢都要 **100%** 併入年薪，用最高稅率課稅。")
        st.metric(label="不虧本需達到的稅前報酬", value=f"{be_interest*100:.2f}%")
        
    with col_y:
        st.warning("### 2. 合格股息 (Eligible Dividend)\n例如：五大銀行股、VDY")
        st.markdown("**中等優惠：** 政府提供「股息稅務抵免」，實質稅率通常只有一般利息的一半。")
        st.metric(label="不虧本需達到的稅前報酬", value=f"{be_div*100:.2f}%")
        
    with col_z:
        st.success("### 3. 資本利得 (Capital Gains)\n例如：成長型 ETF、EIT.UN")
        st.markdown("**終極加速器：** 加拿大稅法最大禮物！賺到的錢只有 **50%** 需要課稅。")
        st.metric(label="不虧本需達到的稅前報酬", value=f"{be_cap_gain*100:.2f}%")

# --- 模組三：真實數據沙盒 ---
with tab3:
    st.header("專屬數據沙盒：真實的本息攤還加速引擎")
    st.info(f"### 🏛️ 什麼是 OSFI 65% 天花板限制？\n加拿大金融糾察隊 (OSFI) 規定，任何房屋的理財型房貸 (HELOC) 借款總額，**絕對不能超過房屋最新市值的 65%**。\n* 以你的房屋估價 ${property_value:,.0f} 為例，你的 HELOC 借款上限就是 **${heloc_limit:,.0f}**。\n* **破關時刻：** 當你的橘色好債碰到這條天花板時，代表你能轉換的債務已經達到法規極限，這稱為「完全資本化」。")
    
    monthly_mortgage_rate = mortgage_rate / 12
    n_months = int(amortization_years * 12)
    pmt = mortgage_principal * (monthly_mortgage_rate * (1 + monthly_mortgage_rate)**n_months) / ((1 + monthly_mortgage_rate)**n_months - 1) if monthly_mortgage_rate > 0 and n_months > 0 else 0

    current_mortgage = mortgage_principal
    current_invested = 0
    data = []

    for year in range(1, int(amortization_years) + 1):
        for month in range(12):
            if current_mortgage > 0:
                interest_portion = current_mortgage * monthly_mortgage_rate
                principal_portion = pmt - interest_portion
                if principal_portion > current_mortgage: principal_portion = current_mortgage
                current_mortgage -= principal_portion
                
                available_heloc = heloc_limit - current_invested
                borrow_amount = min(principal_portion, available_heloc)
                if borrow_amount > 0: current_invested += borrow_amount
                
                monthly_dividend = current_invested * (investment_yield / 12)
                current_mortgage -= monthly_dividend
                
                available_heloc_2 = heloc_limit - current_invested
                borrow_amount_2 = min(monthly_dividend, available_heloc_2)
                if borrow_amount_2 > 0: current_invested += borrow_amount_2
                
        if current_mortgage > 0:
            annual_tax_refund = (current_invested * heloc_rate) * tax_rate
            current_mortgage -= annual_tax_refund
            
            available_heloc_3 = heloc_limit - current_invested
            borrow_amount_3 = min(annual_tax_refund, available_heloc_3)
            if borrow_amount_3 > 0: current_invested += borrow_amount_3
            if current_mortgage < 0: current_mortgage = 0
                
        data.append({
            "Year": year,
            "傳統房貸 (壞債)": max(0, current_mortgage),
            "投資組合價值 (資產)": current_invested,
            "HELOC 餘額 (好債)": current_invested
        })
        if current_mortgage == 0 and current_invested >= heloc_limit: break

    df = pd.DataFrame(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("每月例行房貸繳款", f"${pmt:,.0f}", "由系統自動精算")
    
    payoff_year = df[df["傳統房貸 (壞債)"] == 0]["Year"].min()
    if pd.isna(payoff_year):
        col2.metric("預計壞債結清時間", f"{int(amortization_years)} 年 (無變化)")
    else:
        col2.metric("預計壞債結清時間", f"第 {int(payoff_year)} 年", f"提早還清壞債！")
        
    final_portfolio = df["投資組合價值 (資產)"].iloc[-1]
    col3.metric("結清時擁有的投資組合", f"${final_portfolio:,.0f}", "全數為抵稅好債")

    st.subheader(f"未來財富軌跡投影 (OSFI 上限：${heloc_limit:,.0f})")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Year"], y=df["傳統房貸 (壞債)"], mode='lines+markers', name='傳統房貸 (壞債)', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df["Year"], y=df["投資組合價值 (資產)"], mode='lines+markers', name='投資組合價值 (資產)', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df["Year"], y=df["HELOC 餘額 (好債)"], mode='lines', name='HELOC 餘額 (抵稅好債)', line=dict(color='orange', dash='dash')))
    fig.add_hline(y=heloc_limit, line_dash="dot", line_color="purple", annotation_text="OSFI 65% 借款天花板", annotation_position="top left")
    fig.update_layout(xaxis_title="執行年度", yaxis_title="金額 (加幣 $)", hovermode="x unified", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- 模組四：風險與常見問題 (FAQ) ---
with tab4:
    st.error("### 🛑 免責聲明 (Disclaimer)\n**本網頁工具僅供教育與數學概念展示之用，絕非專業的財務或投資建議。**\n開發者並非持牌財務顧問或會計師，無法為您的投資結果承擔風險。Smith Manoeuvre 涉及複雜的稅務法規與高槓桿操作，強烈建議在實際執行前，**務必諮詢您的專屬會計師 (CPA) 或理財顧問！**")
    
    st.header("執行此策略的致命鐵則")
    st.markdown("如果決定要啟動這個飛輪，請務必嚴格遵守以下規則，否則可能會面臨 CRA 的稅務懲罰：")
    
    st.info("### 1. 資金軌跡必須「絕對乾淨」 (Clean Paper Trail)\n從 HELOC 借出來的錢必須**「直接」**轉入你的投資帳戶。絕對不能先轉到你的日常支票帳戶，更不能用來買菜或旅遊。**只要混入了一分錢的私人消費，整個帳戶的抵稅資格就會被污染！**")
    st.warning("### 2. 必須開設全新「非註冊帳戶」 (Non-Registered Account)\n這筆錢**絕對不能**放進 TFSA 或 RRSP！你必須在券商開立一個全新的、專門只為了這個策略運作的非註冊帳戶。")
    st.success("### 3. 極度自律的現金流管理\n這個策略的成功建立在 100% 的紀律上：**釋放的額度只能買資產，產生的股息只能拿去還房貸。**")
    
    st.write("---")
    
    st.header("常見問題解答 (FAQ)")
    st.markdown("針對大家最擔心的幾個痛點，我們來一一破解：")
    
    with st.expander("🤔 1. 這是合法的嗎？會不會被 CRA (稅務局) 查水表？"):
        st.markdown("""
        **完全合法。** 
        這個策略的基礎建立在加拿大最高法院 2001 年的指標性判決（The Singleton Case）上。法院裁定：**只要你借錢的「直接目的」是為了產生投資收入，該筆借貸的利息就完全可以抵稅。** 
        
        這不是法律漏洞，而是加拿大稅法《所得稅法》(Income Tax Act) 第 20(1)(c) 條的明文規定。只要你的資金軌跡乾淨，CRA 完全認可這種操作。
        """)
        
    with st.expander("📉 2. 如果股市大崩盤，我是不是會破產或房子被法拍？"):
        st.markdown("""
        **不會，因為你的「總負債」其實並沒有增加。**
        
        你只是把「原本就要還的傳統房貸」轉換成了「HELOC 投資貸款」。假設你的總負債是 60 萬，如果今天股市崩盤，你的投資組合價值腰斬，你依然欠銀行 60 萬。你每個月要還給銀行的錢，並不會因為股市大跌而突然變多。
        
        真正的風險在於你的**心理素質**。只要你能扛住帳面虧損，繼續用薪水繳房貸、領取股息，並等待市場回溫，你就不會因為市場波動而失去房子。
        """)
        
    with st.expander("📈 3. 如果央行一直升息，HELOC 借款利息變得很貴怎麼辦？"):
        st.markdown("""
        **這是最真實的風險，但高稅率會成為你的緩衝墊。**
        
        因為投資利息可以抵稅，當央行升息導致 HELOC 利率上升時，你明年春天拿到的「退稅金」也會等比例變大。
        
        例如，如果 HELOC 利率從 5% 暴增到 8%，在 43.41% 的邊際稅率下，你的「稅後實質成本」其實只從 2.8% 增加到 4.5%。只要你的資產配置能提供穩定的現金流，你依然有足夠的防禦力來度過高息週期。
        """)
        
    with st.expander("💰 4. 什麼都不做，乖乖把房貸還清不是最安全嗎？"):
        st.markdown("""
        **「不投資」本身就是一種隱形的巨大風險。**
        
        當你花 25 年乖乖還清房貸時，你擁有一棟沒有貸款的房子。但這棟房子裡的錢是「死錢 (Dead Equity)」，它不會產生任何現金流來幫你付水電費或退休生活費。同時，每年 2% 到 3% 的通貨膨脹，正在無情地侵蝕你現金的購買力。
        
        這個策略的意義，就是在你還清房貸的同一天，幫你免費建立起一個幾十萬加幣的投資組合，為你的退休生活提供源源不絕的被動收入。
        """)
