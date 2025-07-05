import streamlit as st
from db import add_expense, get_all_expenses, delete_expense
from datetime import date
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Expense Tracker", page_icon="💸")
st.title("💸 Personal Expense Tracker")

# --- Add Expense Form ---
st.subheader("Add New Expense")
with st.form("expense_form"):
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    expense_date = st.date_input("Date", value=date.today())
    notes = st.text_area("Notes (optional)")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        add_expense(amount, category, expense_date.strftime("%Y-%m-%d"), notes)
        st.success("✅ Expense added successfully!")

# --- Load Expenses ---
expenses = get_all_expenses()
df = pd.DataFrame(expenses, columns=["ID", "Amount", "Category", "Date", "Notes"])

if not df.empty:
    # --- Filter Section ---
    st.subheader("🔍 Filter Expenses")
    selected_category = st.selectbox("Filter by Category", ["All"] + sorted(df["Category"].unique().tolist()))

    if selected_category != "All":
        df = df[df["Category"] == selected_category]

    # --- Show Table with Delete Option ---
    st.subheader("📋 Expense History")

    for _, row in df.iterrows():
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"**₹{row['Amount']:.2f}** - {row['Category']} on {row['Date']}  \n📝 {row['Notes']}")
        with col2:
            if st.button("❌", key=f"del_{row['ID']}"):
                delete_expense(row["ID"])
                st.experimental_rerun()

    # --- Total Spent ---
    total_amount = df["Amount"].sum()
    st.markdown(f"### 💰 Total Spent: ₹{total_amount:.2f}")

    # --- Export to CSV ---
    st.subheader("⬇️ Export Data")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="expenses.csv",
        mime="text/csv"
    )

    # --- Pie Chart ---
    st.subheader("📊 Category-wise Spending")
    chart_data = df.groupby("Category")["Amount"].sum().reset_index()
    fig = px.pie(chart_data, values="Amount", names="Category", title="Spending by Category")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("No expenses to display yet. Add some above! 💸")
