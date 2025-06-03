import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# --- Setup ---
st.set_page_config(page_title="Personal Budget Tracker", layout="centered")
st.title("💸 Personal Budget Tracker")

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# --- Input Section ---
st.subheader("Monthly Income and Expenses")
income_data = []
needs_data = []
wants_data = []

with st.form("income_form"):
    for i, month in enumerate(months):
        st.markdown(f"### {month}")
        col1, col2, col3 = st.columns(3)
        with col1:
            income = st.number_input(f"Income ({month})", min_value=0, key=f"income_{i}")
        with col2:
            needs = st.number_input(f"Needs ({month})", min_value=0, key=f"needs_{i}")
        with col3:
            wants = st.number_input(f"Wants ({month})", min_value=0, key=f"wants_{i}")

        income_data.append(income)
        needs_data.append(needs)
        wants_data.append(wants)
    
    submitted = st.form_submit_button("Hitung 🚀")

# --- Process Data ---
if submitted:
    saved = []
    investments = []

    for i in range(12):
        lefover = income_data[i] - needs_data[i] - wants_data[i]
        if lefover > 0:
            invested = int(lefover * 0.5)
            saved_amt = lefover - invested
        else:
            invested = 0
            saved_amt = max(0, lefover)
        investments.append(invested)
        saved.append(saved_amt)

    df = pd.DataFrame({
        'Month': months,
        'Income': income_data,
        'Needs': needs_data,
        'Wants': wants_data,
        'Savings': saved,
        'Invested': investments
    })

    income_arr = np.array(income_data)
    saving_rate = (np.array(saved) + np.array(investments)) / income_arr * 100
    df['Savings Rate (%)'] = saving_rate

    def label(rate):
        if rate < 10:
            return 'Too Risky'
        elif 10 <= rate <= 30:
            return 'Safe'
        else:
            return 'Very Good'

    df['Category'] = df['Savings Rate (%)'].apply(label)

    # --- Output Section ---
    st.subheader("📊 Hasil Perhitungan")
    st.dataframe(df.style.format({'Savings Rate (%)': '{:.2f}'}))

    # --- Plot 1: Savings Rate ---
    st.subheader("📈 Grafik Savings Rate per Bulan")
    fig1, ax1 = plt.subplots()
    sns.barplot(x='Month', y='Savings Rate (%)', data=df, ax=ax1)
    plt.title("Monthly Saving Rate (%)")
    st.pyplot(fig1)

    # --- Plot 2: Income vs Needs & Wants ---
    st.subheader("📉 Income vs Needs vs Wants")
    fig2, ax2 = plt.subplots()
    sns.lineplot(x='Month', y='Income', data=df, marker='o', label='Income', ax=ax2)
    sns.lineplot(x='Month', y='Needs', data=df, marker='o', label='Needs', ax=ax2)
    sns.lineplot(x='Month', y='Wants', data=df, marker='o', label='Wants', ax=ax2)
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(fig2)

    # --- Plot 3: Pie Chart Allocation ---
    st.subheader("🥧 Total Yearly Allocation")
    fig3, ax3 = plt.subplots()
    allocation = [
        df['Needs'].sum(),
        df['Wants'].sum(),
        df['Invested'].sum(),
        df['Savings'].sum()
    ]
    labels = ['Needs', 'Wants', 'Invested', 'Savings']
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

    ax3.pie(allocation, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
    ax3.axis('equal')
    st.pyplot(fig3)
