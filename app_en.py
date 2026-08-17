import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Smith Manoeuvre Simulator", layout="wide")
st.title("Smith Manoeuvre Wealth Accelerator")
st.markdown("A financial tool designed for Canadian homeowners to demonstrate how to convert non-deductible 'bad debt' into tax-deductible 'good debt' that generates passive income.")

# Sidebar: User Inputs
st.sidebar.header("⚙️ Enter Your Financial Data")

with st.sidebar.expander("🔍 Estimate Marginal Tax Rate (Ontario)"):
    st.markdown("**(Based on 2026 Ontario combined tax brackets)**")
    income = st.number_input("Estimated Annual Income ($)", value=115000, step=5000)
    
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
        
    st.success(f"💡 Estimated Marginal Tax Rate: **{est_tax}%**")
    st.caption("👉 Enter this number in the 'Marginal Tax Rate' field below.")
    st.write("---")

property_value = st.sidebar.number_input("Property Value Estimate ($)", value=1000000, step=50000)
mortgage_principal = st.sidebar.number_input("Current Mortgage Balance ($)", value=590000, step=10000)
mortgage_rate = st.sidebar.number_input("Traditional Mortgage Rate (%)", value=4.99, step=0.1) / 100
amortization_years = st.sidebar.number_input("Remaining Amortization (Years)", value=25, step=1)
heloc_rate = st.sidebar.number_input("HELOC Borrowing Rate (%)", value=4.95, step=0.1) / 100
tax_rate = st.sidebar.number_input("Marginal Tax Rate (%)", value=37.91, step=0.1) / 100
investment_yield = st.sidebar.number_input("Expected Investment Yield (%)", value=6.72, step=0.1) / 100

heloc_limit = property_value * 0.65

# Create 4 Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔄 The Flywheel Concept", "🛡️ Tax Demystifier", "📊 Data Sandbox", "⚠️ Risks & FAQ"])

# --- Tab 1: Concept ---
with tab1:
    st.header("What is the Smith Manoeuvre?")
    st.markdown("The core of this strategy is making the same dollar do two things at once: **pay down your mortgage AND build an investment portfolio.** Here is how the 5-step flywheel works:")
    st.write("---")
    st.info("### Step 1: Regular Mortgage Payment ➡️ Principal Drops\nYou pay your regular mortgage using your daily income. As the principal drops, the bank's system reacts.")
    st.markdown("<h2 style='text-align: center;'>⬇️</h2>", unsafe_allow_html=True)
    st.warning("### Step 2: Bank Releases Room 🔓 (Readvanceable)\nFor every $1,000 of principal you pay off, your HELOC (Home Equity Line of Credit) limit automatically increases by $1,000.")
    st.markdown("<h2 style='text-align: center;'>⬇️</h2>", unsafe_allow_html=True)
    st.success("### Step 3: Borrow to Invest 📈\nYou borrow that $1,000 and invest it in income-producing assets in a non-registered account.\n*(💡 Your total debt hasn't increased; you've simply swapped non-deductible bad debt for tax-deductible good debt.)*")
    st.markdown("<h2 style='text-align: center;'>⬇️</h2>", unsafe_allow_html=True)
    st.error("### Step 4: Collect Dividends & Tax Refunds 💰\nThese assets pay you dividends. Furthermore, because you borrowed to invest, the CRA allows you to deduct the HELOC interest, resulting in a tax refund every spring.")
    st.markdown("<h2 style='text-align: center;'>🔄 The Flywheel Engages 🔄</h2>", unsafe_allow_html=True)
    st.info("### Step 5: Accelerate Mortgage Payoff 🚀\nYou take 100% of the dividends and tax refunds and apply them as prepayments against your traditional mortgage (Back to Step 1).\n\n**The Aha Moment 💡:** Next month, your principal drops faster ➡️ releases more room ➡️ buys more assets ➡️ generates more income! Your 25-year mortgage collapses rapidly.")

# --- Tab 2: Tax Demystifier ---
with tab2:
    st.header("Breaking the Myth: Is borrowing to invest too expensive?")
    after_tax_borrowing_cost = heloc_rate * (1 - tax_rate)
    st.markdown(f"Many people think if they borrow at **{heloc_rate*100:.2f}%**, they need an investment yielding more than that just to break even. This is false! In Canada, **interest on money borrowed to invest is 100% tax-deductible.**")
    st.info(f"### 🧮 After-Tax Cost Formula\n**Nominal Rate ({heloc_rate*100:.2f}%) × [ 1 - Marginal Tax Rate ({tax_rate*100:.2f}%) ] = Net After-Tax Cost ({after_tax_borrowing_cost*100:.2f}%)**")
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric(label="Nominal Borrowing Rate", value=f"{heloc_rate*100:.2f}%")
    col_b.metric(label="CRA Tax Refund Proportion", value=f"- {tax_rate*100:.2f}%")
    col_c.metric(label="True After-Tax Cost", value=f"{after_tax_borrowing_cost*100:.2f}%", delta="Massive Cost Reduction", delta_color="normal")
    
    st.write("---")
    st.subheader("Crucial Concept: Taxation of Investment Income")
    col_x, col_y, col_z = st.columns(3)
    be_interest = after_tax_borrowing_cost / (1 - tax_rate)
    be_div = after_tax_borrowing_cost / (1 - (tax_rate * 0.6)) 
    be_cap_gain = after_tax_borrowing_cost / (1 - (tax_rate * 0.5))
    
    with col_x:
        st.error("### 1. Interest Income\ne.g., GICs, Bonds")
        st.markdown("**Highly Taxed:** 100% of the income is added to your salary and taxed at your highest marginal rate.")
        st.metric(label="Pre-Tax Return Needed to Break Even", value=f"{be_interest*100:.2f}%")
        
    with col_y:
        st.warning("### 2. Eligible Dividends\ne.g., Big Banks, VDY")
        st.markdown("**Moderately Taxed:** Benefits from the Dividend Tax Credit. The effective tax rate is much lower than interest.")
        st.metric(label="Pre-Tax Return Needed to Break Even", value=f"{be_div*100:.2f}%")
        
    with col_z:
        st.success("### 3. Capital Gains\ne.g., Growth Stocks, EIT.UN")
        st.markdown("**The Ultimate Accelerator:** Only **50%** of the gain is taxable. The remaining 50% is tax-free.")
        st.metric(label="Pre-Tax Return Needed to Break Even", value=f"{be_cap_gain*100:.2f}%")

# --- Tab 3: Sandbox ---
with tab3:
    st.header("Data Sandbox: Real Amortization Engine")
    st.info(f"### 🏛️ The OSFI 65% Limit\nThe Office of the Superintendent of Financial Institutions (OSFI) mandates that HELOC borrowing cannot exceed **65% of the property's appraised value**.\n* Based on your ${property_value:,.0f} property, your HELOC cap is **${heloc_limit:,.0f}**.\n* **Fully Capitalized:** When your 'Good Debt' hits this purple ceiling, debt conversion stops, and you simply enjoy the passive income.")
    
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
            "Traditional Mortgage (Bad Debt)": max(0, current_mortgage),
            "Portfolio Value (Assets)": current_invested,
            "HELOC Balance (Good Debt)": current_invested
        })
        if current_mortgage == 0 and current_invested >= heloc_limit: break

    df = pd.DataFrame(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Regular Monthly Payment", f"${pmt:,.0f}", "Calculated automatically")
    
    payoff_year = df[df["Traditional Mortgage (Bad Debt)"] == 0]["Year"].min()
    if pd.isna(payoff_year):
        col2.metric("Bad Debt Paid Off In", f"{int(amortization_years)} Years (No Change)")
    else:
        col2.metric("Bad Debt Paid Off In", f"Year {int(payoff_year)}", f"Accelerated Payoff!")
        
    final_portfolio = df["Portfolio Value (Assets)"].iloc[-1]
    col3.metric("Final Portfolio Value", f"${final_portfolio:,.0f}", "100% Tax-Deductible Debt")

    st.subheader(f"Wealth Trajectory Projection (OSFI Cap: ${heloc_limit:,.0f})")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Year"], y=df["Traditional Mortgage (Bad Debt)"], mode='lines+markers', name='Traditional Mortgage (Bad Debt)', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df["Year"], y=df["Portfolio Value (Assets)"], mode='lines+markers', name='Portfolio Value (Assets)', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df["Year"], y=df["HELOC Balance (Good Debt)"], mode='lines', name='HELOC Balance (Good Debt)', line=dict(color='orange', dash='dash')))
    fig.add_hline(y=heloc_limit, line_dash="dot", line_color="purple", annotation_text="OSFI 65% Borrowing Limit", annotation_position="top left")
    fig.update_layout(xaxis_title="Years", yaxis_title="Amount (CAD $)", hovermode="x unified", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

# --- Tab 4: Risks & FAQ ---
with tab4:
    st.error("### 🛑 Disclaimer\n**This tool is for educational and mathematical demonstration purposes only and does NOT constitute professional financial or tax advice.**\nThe creator is not acting as your licensed financial advisor or accountant. The Smith Manoeuvre involves complex tax regulations and leverage. Strongly recommend consulting a CPA or financial planner before implementation.")
    
    st.header("The Golden Rules of Execution")
    st.markdown("If you decide to engage the flywheel, you must strictly follow these rules to avoid CRA penalties:")
    
    st.info("### 1. Maintain a Clean Paper Trail\nThe CRA is extremely strict about interest deductibility. Funds borrowed from the HELOC must flow **directly** to the investment account. Never mix it with your checking account for groceries or personal expenses. **A single contaminated transaction can ruin the tax deductibility of the entire account!**")
    st.warning("### 2. Open a Dedicated Non-Registered Account\nDo **NOT** invest this money in a TFSA or RRSP. Interest on money borrowed to invest in tax-sheltered accounts is not deductible. You must open a new, dedicated non-registered account solely for this strategy.")
    st.success("### 3. Absolute Cash Flow Discipline\nThis strategy relies on 100% discipline: **Available HELOC room is only for buying assets; generated dividends are only for prepaying the mortgage.**")
    
    st.write("---")
    
    st.header("Frequently Asked Questions (FAQ)")
    
    with st.expander("🤔 1. Is this legal? Will the CRA audit me?"):
        st.markdown("""
        **It is 100% legal.** 
        The strategy is grounded in the Supreme Court of Canada's 2001 landmark ruling (The Singleton Case). The court affirmed that **as long as the direct purpose of the borrowed funds is to earn investment income, the interest is tax-deductible.** 
        It's explicitly stated in Section 20(1)(c) of the *Income Tax Act*. As long as your paper trail is clean, the CRA fully recognizes this structure.
        """)
        
    with st.expander("📉 2. What if the stock market crashes? Will I lose my house?"):
        st.markdown("""
        **No, because your 'Total Debt' has not increased.**
        You are simply replacing traditional mortgage debt with HELOC debt. If your total debt is $600K and the market crashes, you still owe the bank $600K. Your monthly payments don't suddenly increase because stock prices fell.
        The real risk is your **psychological tolerance**. As long as you can endure the paper loss, continue servicing the debt with your income and dividends, and wait for the market to recover, you won't lose your house to a margin call.
        """)
        
    with st.expander("📈 3. What if the central bank raises interest rates?"):
        st.markdown("""
        **This is a real risk, but your high tax rate acts as a buffer.**
        Because the interest is tax-deductible, when HELOC rates rise, your tax refund also increases proportionately. 
        For example, if the rate jumps from 5% to 8%, at a 43% marginal tax rate, your actual after-tax cost only increases from ~2.8% to ~4.5%. As long as your portfolio yields stable cash flow, you have significant defensive padding against rate hikes.
        """)
        
    with st.expander("💰 4. Isn't it safer to just do nothing and pay off the mortgage?"):
        st.markdown("""
        **Doing nothing is an invisible but massive risk.**
        If you spend 25 years paying off your mortgage conventionally, you end up with a paid-off house containing 'Dead Equity'—it generates zero cash flow to buy your groceries in retirement. Meanwhile, inflation (2-3% annually) silently erodes your purchasing power.
        This strategy allows you to build a massive, income-generating portfolio alongside paying off your house, providing a stream of passive income for retirement.
        """)
