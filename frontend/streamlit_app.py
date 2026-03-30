import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import date

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="SpendWise",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

BACKEND_URL = "https://spend-wise--dudalashatakshi.replit.app/"

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #f9f7ff 0%, #eef4ff 45%, #fef6fb 100%);
}

/* Main title */
.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #6a11cb, #2575fc, #ff4b8b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.3rem;
}

.sub-title {
    text-align: center;
    color: #5b5b7a;
    font-size: 1.05rem;
    margin-bottom: 1.8rem;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    border: 1px solid rgba(255,255,255,0.6);
    margin-bottom: 18px;
}

.metric-card {
    padding: 18px;
    border-radius: 18px;
    color: white;
    font-weight: 700;
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.metric-purple {
    background: linear-gradient(135deg, #6a11cb, #8e54e9);
}

.metric-blue {
    background: linear-gradient(135deg, #2193b0, #6dd5ed);
}

.metric-pink {
    background: linear-gradient(135deg, #ff4b8b, #ff7eb3);
}

.metric-green {
    background: linear-gradient(135deg, #11998e, #38ef7d);
}

.section-heading {
    font-size: 1.4rem;
    font-weight: 700;
    color: #2e2e4d;
    margin-top: 8px;
    margin-bottom: 12px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1f1c2c 0%, #3d2c8d 100%);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: none;
    padding: 0.65rem 1rem;
    font-weight: 700;
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    color: white;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(37,117,252,0.25);
}

/* Inputs */
.stTextInput > div > div > input,
.stNumberInput input,
.stDateInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
    border-radius: 12px !important;
}

/* Small tag */
.tag {
    display: inline-block;
    padding: 6px 12px;
    background: linear-gradient(90deg, #ffecd2, #fcb69f);
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #5c3d2e;
    margin-bottom: 12px;
}

/* Info box */
.info-box {
    padding: 14px;
    border-radius: 14px;
    background: linear-gradient(135deg, #eef7ff, #f5eeff);
    border-left: 5px solid #7b61ff;
    margin-bottom: 10px;
    color: #2e2e4d;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False


# -----------------------------
# Helper Functions
# -----------------------------
def show_header():
    st.markdown('<div class="main-title">💸 SpendWise</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">Track expenses smartly, visualize your spending beautifully, and manage users with a powerful admin dashboard.</div>',
        unsafe_allow_html=True
    )


def signup_user(name, email, password):
    url = f"{BACKEND_URL}/signup"
    payload = {
        "name": name,
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    return response


def login_user(email, password):
    url = f"{BACKEND_URL}/login"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, json=payload)
    return response


def logout_user(user_id):
    url = f"{BACKEND_URL}/logout/{user_id}"
    response = requests.post(url)
    return response


def get_dashboard(user_id):
    url = f"{BACKEND_URL}/dashboard/{user_id}"
    response = requests.get(url)
    return response


def add_expense(user_id, title, amount, category, expense_date, description):
    url = f"{BACKEND_URL}/expenses"
    payload = {
        "user_id": user_id,
        "title": title,
        "amount": amount,
        "category": category,
        "date": str(expense_date),
        "description": description
    }
    response = requests.post(url, json=payload)
    return response


def get_expenses(user_id):
    url = f"{BACKEND_URL}/expenses/{user_id}"
    response = requests.get(url)
    return response


def filter_expenses(user_id, category=None, start_date=None, end_date=None):
    params = {}
    if category and category != "All":
        params["category"] = category
    if start_date:
        params["start_date"] = str(start_date)
    if end_date:
        params["end_date"] = str(end_date)

    url = f"{BACKEND_URL}/expenses/filter/{user_id}"
    response = requests.get(url, params=params)
    return response


def delete_expense(expense_id):
    url = f"{BACKEND_URL}/expenses/{expense_id}"
    response = requests.delete(url)
    return response


def update_expense(expense_id, title, amount, category, expense_date, description):
    url = f"{BACKEND_URL}/expenses/{expense_id}"
    payload = {
        "title": title,
        "amount": amount,
        "category": category,
        "date": str(expense_date),
        "description": description
    }
    response = requests.put(url, json=payload)
    return response


def get_login_activity(user_id):
    url = f"{BACKEND_URL}/login-activity/{user_id}"
    response = requests.get(url)
    return response


def get_admin_dashboard(admin_email):
    url = f"{BACKEND_URL}/admin/dashboard"
    response = requests.get(url, params={"admin_email": admin_email})
    return response


def get_all_users(admin_email):
    url = f"{BACKEND_URL}/admin/users"
    response = requests.get(url, params={"admin_email": admin_email})
    return response


def toggle_user_status(user_id, admin_email):
    url = f"{BACKEND_URL}/admin/users/{user_id}/toggle-active"
    response = requests.put(url, params={"admin_email": admin_email})
    return response


def show_metric_cards(total_count, total_amount, category_count, recent_count):
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card metric-purple">
            <div style="font-size:0.95rem;">📌 Total Entries</div>
            <div style="font-size:1.8rem; margin-top:6px;">{total_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card metric-blue">
            <div style="font-size:0.95rem;">💰 Total Spent</div>
            <div style="font-size:1.8rem; margin-top:6px;">₹ {total_amount:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card metric-pink">
            <div style="font-size:0.95rem;">🧾 Categories Used</div>
            <div style="font-size:1.8rem; margin-top:6px;">{category_count}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card metric-green">
            <div style="font-size:0.95rem;">⚡ Recent Records</div>
            <div style="font-size:1.8rem; margin-top:6px;">{recent_count}</div>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------
# Auth Screen
# -----------------------------
def auth_screen():
    show_header()

    left, mid, right = st.columns([1, 1.2, 1])

    with mid:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="tag">✨ Smart • Simple • Colorful • Full Stack</div>', unsafe_allow_html=True)

        auth_mode = st.radio("Choose an option", ["Login", "Sign Up"], horizontal=True)

        if auth_mode == "Login":
            st.markdown('<div class="section-heading">🔐 Welcome Back</div>', unsafe_allow_html=True)
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.button("Login to SpendWise"):
                if not email or not password:
                    st.warning("Please enter email and password.")
                else:
                    try:
                        response = login_user(email, password)
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.logged_in = True
                            st.session_state.user_id = data["user"]["id"]
                            st.session_state.user_name = data["user"]["name"]
                            st.session_state.user_email = data["user"]["email"]
                            st.session_state.is_admin = data["user"]["is_admin"]
                            st.success("Login successful.")
                            st.rerun()
                        else:
                            st.error(response.json().get("detail", "Login failed."))
                    except Exception:
                        st.error("Could not connect to backend. Make sure FastAPI is running.")

        else:
            st.markdown('<div class="section-heading">📝 Create Your Account</div>', unsafe_allow_html=True)
            name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            password = st.text_input("Create Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Create Account"):
                if not name or not email or not password or not confirm_password:
                    st.warning("Please fill all the fields.")
                elif password != confirm_password:
                    st.warning("Passwords do not match.")
                else:
                    try:
                        response = signup_user(name, email, password)
                        if response.status_code == 200:
                            st.success("Account created successfully. Please login now.")
                        else:
                            st.error(response.json().get("detail", "Signup failed."))
                    except Exception:
                        st.error("Could not connect to backend. Make sure FastAPI is running.")

        st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# User Dashboard
# -----------------------------
def user_dashboard_page():
    show_header()
    st.markdown(f'<div class="section-heading">👋 Hello, {st.session_state.user_name}</div>', unsafe_allow_html=True)

    try:
        response = get_dashboard(st.session_state.user_id)

        if response.status_code != 200:
            st.error("Unable to load dashboard.")
            return

        data = response.json()

        total_count = data.get("total_expenses_count", 0)
        total_amount = data.get("total_amount_spent", 0.0)
        category_summary = data.get("category_summary", [])
        recent_expenses = data.get("recent_expenses", [])
        insights = data.get("insights", [])

        show_metric_cards(
            total_count=total_count,
            total_amount=total_amount,
            category_count=len(category_summary),
            recent_count=len(recent_expenses)
        )

        c1, c2 = st.columns([1.2, 1])

        with c1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">📊 Category-wise Spending</div>', unsafe_allow_html=True)

            if category_summary:
                df_cat = pd.DataFrame(category_summary)
                fig_pie = px.pie(
                    df_cat,
                    names="category",
                    values="total_amount",
                    hole=0.45,
                    title="Expenses by Category"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No expense data available yet.")

            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">🧠 SpendWise Insights</div>', unsafe_allow_html=True)

            if insights:
                for insight in insights:
                    st.markdown(f'<div class="info-box">{insight}</div>', unsafe_allow_html=True)
            else:
                st.info("No insights available yet.")

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">🕒 Recent Expenses</div>', unsafe_allow_html=True)

        if recent_expenses:
            df_recent = pd.DataFrame(recent_expenses)
            if "created_at" in df_recent.columns:
                df_recent = df_recent.drop(columns=["created_at"])
            st.dataframe(df_recent, use_container_width=True)
        else:
            st.info("No recent expenses found.")

        st.markdown('</div>', unsafe_allow_html=True)

    except Exception:
        st.error("Backend connection error.")


# -----------------------------
# Add Expense Page
# -----------------------------
def add_expense_page():
    show_header()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">➕ Add New Expense</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        title = st.text_input("Expense Title")
        amount = st.number_input("Amount (₹)", min_value=1.0, step=1.0)
        category = st.selectbox(
            "Category",
            ["Food", "Travel", "Shopping", "Bills", "Health", "Education", "Entertainment", "Other"]
        )

    with col2:
        expense_date = st.date_input("Expense Date", value=date.today())
        description = st.text_area("Description")

    if st.button("Save Expense"):
        if not title.strip():
            st.warning("Please enter expense title.")
        else:
            try:
                response = add_expense(
                    st.session_state.user_id,
                    title,
                    amount,
                    category,
                    expense_date,
                    description
                )

                if response.status_code == 200:
                    st.success("Expense added successfully.")
                else:
                    st.error(response.json().get("detail", "Failed to add expense."))
            except Exception:
                st.error("Backend connection error.")

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# View Expenses Page
# -----------------------------
def view_expenses_page():
    show_header()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">📂 Expense History</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)

    with f1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All", "Food", "Travel", "Shopping", "Bills", "Health", "Education", "Entertainment", "Other"]
        )
    with f2:
        start_date = st.date_input("Start Date", value=None)
    with f3:
        end_date = st.date_input("End Date", value=None)

    if st.button("Apply Filters"):
        try:
            response = filter_expenses(
                st.session_state.user_id,
                category=category_filter,
                start_date=start_date,
                end_date=end_date
            )
        except Exception:
            response = None
            st.error("Backend connection error.")
    else:
        try:
            response = get_expenses(st.session_state.user_id)
        except Exception:
            response = None
            st.error("Backend connection error.")

    if response and response.status_code == 200:
        expenses = response.json()

        if expenses:
            df = pd.DataFrame(expenses)

            show_cols = ["id", "title", "amount", "category", "date", "description"]
            available_cols = [col for col in show_cols if col in df.columns]
            st.dataframe(df[available_cols], use_container_width=True)

            st.markdown("---")
            st.markdown("### ✏️ Edit Expense")

            expense_ids = df["id"].tolist()
            selected_expense_id = st.selectbox("Select Expense ID to Edit", expense_ids)

            selected_row = df[df["id"] == selected_expense_id].iloc[0]

            col1, col2 = st.columns(2)
            with col1:
                new_title = st.text_input("Edit Title", value=selected_row["title"], key="edit_title")
                new_amount = st.number_input("Edit Amount", min_value=1.0, value=float(selected_row["amount"]), key="edit_amount")
                new_category = st.selectbox(
                    "Edit Category",
                    ["Food", "Travel", "Shopping", "Bills", "Health", "Education", "Entertainment", "Other"],
                    index=["Food", "Travel", "Shopping", "Bills", "Health", "Education", "Entertainment", "Other"].index(selected_row["category"]) if selected_row["category"] in ["Food", "Travel", "Shopping", "Bills", "Health", "Education", "Entertainment", "Other"] else 0,
                    key="edit_category"
                )
            with col2:
                new_date = st.date_input("Edit Date", value=pd.to_datetime(selected_row["date"]).date(), key="edit_date")
                new_description = st.text_area("Edit Description", value=selected_row["description"] if pd.notna(selected_row["description"]) else "", key="edit_desc")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Update Expense"):
                    try:
                        update_response = update_expense(
                            selected_expense_id,
                            new_title,
                            new_amount,
                            new_category,
                            new_date,
                            new_description
                        )
                        if update_response.status_code == 200:
                            st.success("Expense updated successfully.")
                            st.rerun()
                        else:
                            st.error(update_response.json().get("detail", "Update failed."))
                    except Exception:
                        st.error("Backend connection error.")

            with c2:
                if st.button("Delete Expense"):
                    try:
                        delete_response = delete_expense(selected_expense_id)
                        if delete_response.status_code == 200:
                            st.success("Expense deleted successfully.")
                            st.rerun()
                        else:
                            st.error(delete_response.json().get("detail", "Delete failed."))
                    except Exception:
                        st.error("Backend connection error.")

        else:
            st.info("No expenses found.")
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# Reports Page
# -----------------------------
def reports_page():
    show_header()

    try:
        response = get_expenses(st.session_state.user_id)
        if response.status_code != 200:
            st.error("Unable to fetch expense data.")
            return

        expenses = response.json()
        if not expenses:
            st.info("No expense data available for reports.")
            return

        df = pd.DataFrame(expenses)
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.strftime("%Y-%m")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">📈 Monthly Spending Report</div>', unsafe_allow_html=True)

        monthly_summary = df.groupby("month", as_index=False)["amount"].sum()
        fig_bar = px.bar(monthly_summary, x="month", y="amount", title="Monthly Expense Trend")
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">🥧 Category Distribution</div>', unsafe_allow_html=True)
            cat_summary = df.groupby("category", as_index=False)["amount"].sum()
            fig_pie = px.pie(cat_summary, names="category", values="amount", title="Category Share")
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">📋 Raw Summary</div>', unsafe_allow_html=True)
            summary_df = df.groupby("category", as_index=False)["amount"].agg(["sum", "count"]).reset_index()
            summary_df.columns = ["Category", "Total Amount", "Entries"]
            st.dataframe(summary_df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception:
        st.error("Backend connection error.")


# -----------------------------
# Login Activity Page
# -----------------------------
def login_activity_page():
    show_header()

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">🧾 Your Login Activity</div>', unsafe_allow_html=True)

    try:
        response = get_login_activity(st.session_state.user_id)

        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No login activity found.")
        else:
            st.error("Failed to load login activity.")
    except Exception:
        st.error("Backend connection error.")

    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# Admin Dashboard
# -----------------------------
def admin_dashboard_page():
    show_header()
    st.markdown('<div class="section-heading">🛡️ Admin Control Center</div>', unsafe_allow_html=True)

    try:
        response = get_admin_dashboard(st.session_state.user_email)

        if response.status_code != 200:
            st.error("Unable to load admin dashboard.")
            return

        data = response.json()

        total_users = data.get("total_users", 0)
        total_admins = data.get("total_admins", 0)
        active_users = data.get("active_users", 0)
        total_expense_entries = data.get("total_expense_entries", 0)
        total_system_expense_amount = data.get("total_system_expense_amount", 0.0)
        total_login_records = data.get("total_login_records", 0)
        recent_logins = data.get("recent_logins", [])
        users = data.get("users", [])

        show_metric_cards(
            total_count=total_users,
            total_amount=total_system_expense_amount,
            category_count=total_expense_entries,
            recent_count=total_login_records
        )

        c1, c2 = st.columns(2)

        with c1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">👥 User Status Overview</div>', unsafe_allow_html=True)

            status_df = pd.DataFrame({
                "Type": ["Active Users", "Admins", "Other Users"],
                "Count": [active_users, total_admins, max(total_users - total_admins, 0)]
            })
            fig_status = px.bar(status_df, x="Type", y="Count", title="System Users Overview")
            st.plotly_chart(fig_status, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">⚡ Expense Usage Overview</div>', unsafe_allow_html=True)

            usage_df = pd.DataFrame({
                "Metric": ["Expense Entries", "Login Records"],
                "Value": [total_expense_entries, total_login_records]
            })
            fig_usage = px.pie(usage_df, names="Metric", values="Value", title="System Activity Share")
            st.plotly_chart(fig_usage, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">🧑‍💼 Registered Users</div>', unsafe_allow_html=True)

        if users:
            users_df = pd.DataFrame(users)
            st.dataframe(users_df, use_container_width=True)

            st.markdown("### 🔄 Activate / Deactivate User")

            non_admin_users = [u for u in users if not u.get("email") == st.session_state.user_email]

            if non_admin_users:
                user_options = {
                    f"{u['name']} ({u['email']})": u["user_id"]
                    for u in non_admin_users
                }

                selected_user_label = st.selectbox("Select User", list(user_options.keys()))
                selected_user_id = user_options[selected_user_label]

                if st.button("Toggle User Active Status"):
                    toggle_response = toggle_user_status(selected_user_id, st.session_state.user_email)
                    if toggle_response.status_code == 200:
                        st.success(toggle_response.json().get("message", "User status updated."))
                        st.rerun()
                    else:
                        st.error(toggle_response.json().get("detail", "Failed to update user status."))
        else:
            st.info("No users found.")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-heading">🕒 Recent Login Activity</div>', unsafe_allow_html=True)

        if recent_logins:
            recent_df = pd.DataFrame(recent_logins)
            st.dataframe(recent_df, use_container_width=True)
        else:
            st.info("No recent login records found.")

        st.markdown('</div>', unsafe_allow_html=True)

    except Exception:
        st.error("Backend connection error.")


# -----------------------------
# Logout
# -----------------------------
def do_logout():
    try:
        logout_user(st.session_state.user_id)
    except Exception:
        pass

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.is_admin = False
    st.success("Logged out successfully.")
    st.rerun()


# -----------------------------
# Sidebar Navigation
# -----------------------------
def sidebar_navigation():
    st.sidebar.markdown("## 💼 SpendWise Panel")
    st.sidebar.markdown(f"**User:** {st.session_state.user_name}")
    st.sidebar.markdown(f"**Email:** {st.session_state.user_email}")

    if st.session_state.is_admin:
        menu = st.sidebar.radio(
            "Navigate",
            ["Admin Dashboard", "User Dashboard", "Add Expense", "View Expenses", "Reports", "Login Activity", "Logout"]
        )
    else:
        menu = st.sidebar.radio(
            "Navigate",
            ["User Dashboard", "Add Expense", "View Expenses", "Reports", "Login Activity", "Logout"]
        )

    return menu


# -----------------------------
# Main App
# -----------------------------
def main():
    if not st.session_state.logged_in:
        auth_screen()
    else:
        menu = sidebar_navigation()

        if menu == "User Dashboard":
            user_dashboard_page()
        elif menu == "Add Expense":
            add_expense_page()
        elif menu == "View Expenses":
            view_expenses_page()
        elif menu == "Reports":
            reports_page()
        elif menu == "Login Activity":
            login_activity_page()
        elif menu == "Admin Dashboard":
            admin_dashboard_page()
        elif menu == "Logout":
            do_logout()


if __name__ == "__main__":
    main()
