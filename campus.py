import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Set page config with a vibrant theme
st.set_page_config(
    page_title="SmartBite Analytics",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Hide anchor link icon next to headers */
    [data-testid="stHeaderActionElements"] {
        display: none;
    }
    div[data-testid="StyledLinkIconContainer"] > a:first-child {
        display: none !important;
    }
    
    /* Global Font */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Metric Card Styling */
    [data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 5px solid #1e3c72;
    }
    
    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(30, 60, 114, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 60, 114, 0.4);
        color: white;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        background: white;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    /* Header Gradient */
    .header-text {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Session State Data (same logic, keep data intact)
if 'menu' not in st.session_state:
    st.session_state.menu = pd.DataFrame([
        {"item_id": 1, "item_name": "Samosa", "category": "Snacks", "price": 15.0, "stock": 50, "status": "Available"},
        {"item_id": 2, "item_name": "Masala Tea", "category": "Beverages", "price": 10.0, "stock": 100, "status": "Available"},
        {"item_id": 3, "item_name": "Cold Coffee", "category": "Beverages", "price": 30.0, "stock": 80, "status": "Available"},
        {"item_id": 4, "item_name": "Veg Burger", "category": "Fast Food", "price": 50.0, "stock": 30, "status": "Available"},
        {"item_id": 5, "item_name": "French Fries", "category": "Snacks", "price": 40.0, "stock": 40, "status": "Available"},
        {"item_id": 6, "item_name": "Paneer Roll", "category": "Fast Food", "price": 60.0, "stock": 25, "status": "Available"},
        {"item_id": 7, "item_name": "Veg Sandwich", "category": "Snacks", "price": 35.0, "stock": 5, "status": "Available"},
        {"item_id": 8, "item_name": "Cold Drink", "category": "Beverages", "price": 25.0, "stock": 0, "status": "Out of Stock"}
    ])

if 'orders' not in st.session_state:
    st.session_state.orders = pd.DataFrame(columns=['order_id', 'timestamp', 'total_amount'])

if 'order_items' not in st.session_state:
    st.session_state.order_items = pd.DataFrame(columns=['order_id', 'item_id', 'item_name', 'category', 'price', 'quantity', 'subtotal'])

# Helpers
def get_next_item_id():
    if st.session_state.menu.empty: return 1
    return st.session_state.menu['item_id'].max() + 1

def get_next_order_id():
    if st.session_state.orders.empty: return 1001
    return st.session_state.orders['order_id'].max() + 1

# Sidebar Redesign
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: white;'>🏫 Smart Bite</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #dbe2ef;'>Premium Dining Experience</p>", unsafe_allow_html=True)
    st.markdown("---")
    menu_option = st.radio(
        "Navigation",
        ["🍽️ Menu Management", "🛒 Place Order", "📜 Order History", "📊 Insights Dashboard"],
        index=0
    )
    st.markdown("---")
    st.markdown("<div style='text-align: center; opacity: 0.7; font-size: 0.8rem;'>Prambika Singh</div>", unsafe_allow_html=True)

# --- 1. Menu Management ---
if menu_option == "🍽️ Menu Management":
    st.markdown("<h1 class='header-text'>🍽️ Menu Management</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📋 Digital Menu", "➕ Add Delicacy", "⚙️ Inventory Control"])
    
    with tab1:
        st.markdown("### Explore the Menu")
        col_s, col_f = st.columns([2, 1])
        with col_s:
            search = st.text_input("🔍 Search by name...", placeholder="e.g. Coffee")
        with col_f:
            categories = ["All Categories"] + sorted(list(st.session_state.menu['category'].unique()))
            cat_filter = st.selectbox("🏷️ Filter by Category", categories)
            
        # Filter
        df_display = st.session_state.menu.copy()
        if search:
            df_display = df_display[df_display['item_name'].str.contains(search, case=False)]
        if cat_filter != "All Categories":
            df_display = df_display[df_display['category'] == cat_filter]
            
        # Visual Table
        st.dataframe(
            df_display[['item_name', 'category', 'price', 'stock', 'status']].rename(
                columns={'item_name': 'Item', 'category': 'Category', 'price': 'Price (₹)', 'stock': 'Available Stock', 'status': 'Status'}
            ).reset_index(drop=True),
            use_container_width=True
        )
        
    with tab2:
        st.markdown("### Add New Food Item")
        with st.container(border=True):
            with st.form("add_item_premium", clear_on_submit=True):
                col_n, col_c = st.columns(2)
                with col_n:
                    name = st.text_input("Delicacy Name*", placeholder="e.g. Garlic Bread")
                with col_c:
                    cat_list = sorted(list(st.session_state.menu['category'].unique()))
                    category = st.selectbox("Category*", cat_list + ["Create New Category"])
                    new_cat = st.text_input("Custom Category Name (if selected above)")
                    
                col_p, col_st = st.columns(2)
                with col_p:
                    price = st.number_input("Price (₹)*", min_value=0.0, step=5.0, format="%.2f")
                with col_st:
                    stock = st.number_input("Initial Stock*", min_value=0, step=10)
                    
                st.markdown("<br>", unsafe_allow_html=True)
                submit = st.form_submit_button("✨ Onboard Item")
                
                if submit:
                    final_cat = new_cat if category == "Create New Category" else category
                    if not name or not final_cat:
                        st.error("⚠️ Please provide all mandatory fields.")
                    elif price <= 0:
                        st.error("⚠️ Price must be greater than zero.")
                    elif st.session_state.menu['item_name'].str.lower().eq(name.lower()).any():
                        st.error(f"⚠️ '{name}' is already on the menu.")
                    else:
                        new_item = pd.DataFrame([{
                            "item_id": get_next_item_id(),
                            "item_name": name,
                            "category": final_cat,
                            "price": price,
                            "stock": stock,
                            "status": "Available" if stock > 0 else "Out of Stock"
                        }])
                        st.session_state.menu = pd.concat([st.session_state.menu, new_item], ignore_index=True)
                        st.success(f"🎉 **{name}** onboarded flawlessly!")
                        st.rerun()

    with tab3:
        st.markdown("### Inventory Control")
        if st.session_state.menu.empty:
            st.info("The kitchen is completely empty.")
        else:
            selected = st.selectbox("Select Item to Modify", st.session_state.menu['item_name'].tolist())
            idx = st.session_state.menu[st.session_state.menu['item_name'] == selected].index[0]
            curr = st.session_state.menu.iloc[idx]
            
            with st.container(border=True):
                col_st, col_stat = st.columns(2)
                with col_st:
                    up_stock = st.number_input("Restock Quantity", min_value=0, value=int(curr['stock']), step=5)
                with col_stat:
                    up_status = st.selectbox("Operational Status", ["Available", "Out of Stock"], 
                                             index=0 if curr['status'] == "Available" else 1)
                    
                # Auto-detect zero stock
                if up_stock == 0 and up_status == "Available":
                    up_status = "Out of Stock"
                elif up_stock > 0 and curr['stock'] == 0:
                    up_status = "Available"
                    
                if st.button("💾 Save Inventory Updates"):
                    st.session_state.menu.at[idx, 'stock'] = up_stock
                    st.session_state.menu.at[idx, 'status'] = up_status
                    st.success(f"✅ Stock data updated for **{selected}**.")
                    st.rerun()

# --- 2. Order System (GRID DESIGN) ---
elif menu_option == "🛒 Place Order":
    st.markdown("<h1 class='header-text'>🛒 Place Order</h1>", unsafe_allow_html=True)
    
    avail = st.session_state.menu[st.session_state.menu['status'] == "Available"]
    
    if avail.empty:
        st.error("🛑 Kitchen closed. No items available currently.")
    else:
        st.markdown("### Select Your Items Below")
        
        # Filtering for the grid
        cat_tabs = ["All Items"] + sorted(list(avail['category'].unique()))
        selected_tab = st.radio("Filter by Type", cat_tabs, horizontal=True)
        
        grid_df = avail.copy()
        if selected_tab != "All Items":
            grid_df = grid_df[grid_df['category'] == selected_tab]
            
        st.markdown("---")
        
        # GRID SYSTEM
        cols = st.columns(3)
        order_basket = []
        running_bill = 0.0
        
        for i, (_, row) in enumerate(grid_df.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"<h3 style='margin:0;'>{row['item_name']}</h3>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color:#666; font-size:0.9rem;'>🏷️ {row['category']}</span>", unsafe_allow_html=True)
                    st.markdown(f"<h4 style='color:#1e3c72; margin:10px 0;'>₹{row['price']:.2f}</h4>", unsafe_allow_html=True)
                    
                    # Stock alert styling
                    stock_color = "red" if row['stock'] < 10 else "green"
                    st.markdown(f"<span style='color:{stock_color}; font-weight:bold;'>📦 Left: {row['stock']}</span>", unsafe_allow_html=True)
                    
                    qty = st.number_input(
                        f"Add Qty:",
                        min_value=0,
                        max_value=int(row['stock']),
                        value=0,
                        step=1,
                        key=f"cart_{row['item_id']}"
                    )
                    
                    if qty > 0:
                        sub = qty * row['price']
                        running_bill += sub
                        order_basket.append({
                            "item_id": row['item_id'],
                            "item_name": row['item_name'],
                            "category": row['category'],
                            "price": row['price'],
                            "quantity": qty,
                            "subtotal": sub
                        })
                        
        if order_basket:
            st.markdown("<br><hr>", unsafe_allow_html=True)
            st.markdown(f"<h2 style='text-align:right; color:#1e3c72;'>🛒 Running Bill: ₹{running_bill:.2f}</h2>", unsafe_allow_html=True)
            
            col_dummy, col_btn = st.columns([3, 1])
            with col_btn:
                if st.button("🚀 Confirm & Process Order"):
                    ord_id = get_next_order_id()
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Process stock & order
                    for item in order_basket:
                        idx = st.session_state.menu[st.session_state.menu['item_id'] == item['item_id']].index[0]
                        new_st = st.session_state.menu.at[idx, 'stock'] - item['quantity']
                        st.session_state.menu.at[idx, 'stock'] = new_st
                        if new_st == 0:
                            st.session_state.menu.at[idx, 'status'] = "Out of Stock"
                            
                    # Save
                    st.session_state.orders = pd.concat([
                        st.session_state.orders,
                        pd.DataFrame([{"order_id": ord_id, "timestamp": ts, "total_amount": running_bill}])
                    ], ignore_index=True)
                    
                    for item in order_basket:
                        item['order_id'] = ord_id
                    st.session_state.order_items = pd.concat([
                        st.session_state.order_items,
                        pd.DataFrame(order_basket)
                    ], ignore_index=True)
                    
                    st.balloons()
                    st.success(f"🎉 Order #{ord_id} processed securely!")
                    st.rerun()

# --- 3. Order History ---
elif menu_option == "📜 Order History":
    st.markdown("<h1 class='header-text'>📜 Order Registry</h1>", unsafe_allow_html=True)
    
    if st.session_state.orders.empty:
        st.info("No historical transactions recorded yet.")
    else:
        ord_disp = st.session_state.orders.copy().sort_values(by='timestamp', ascending=False)
        ord_disp['total_amount'] = ord_disp['total_amount'].map('₹{:.2f}'.format)
        
        st.dataframe(
            ord_disp.rename(columns={'order_id':'Order ID', 'timestamp':'Date & Time', 'total_amount':'Revenue'}),
            use_container_width=True
        )
        
        st.markdown("### 🔍 Inspect Order Breakdown")
        sel_ord = st.selectbox("Pick Order ID", st.session_state.orders['order_id'].tolist())
        
        if sel_ord:
            breakdown = st.session_state.order_items[st.session_state.order_items['order_id'] == sel_ord].copy()
            breakdown['price'] = breakdown['price'].map('₹{:.2f}'.format)
            breakdown['subtotal'] = breakdown['subtotal'].map('₹{:.2f}'.format)
            
            st.dataframe(
                breakdown[['item_name', 'category', 'price', 'quantity', 'subtotal']].rename(
                    columns={'item_name':'Item', 'category':'Category', 'price':'Rate', 'quantity':'Qty'}
                ).reset_index(drop=True),
                use_container_width=True
            )

# --- 4. Dashboard & Insights ---
elif menu_option == "📊 Insights Dashboard":
    st.markdown("<h1 class='header-text'>📊 Operations Dashboard</h1>", unsafe_allow_html=True)
    
    # Analytics Math
    today = datetime.now().strftime("%Y-%m-%d")
    t_sales = 0.0
    t_orders = 0
    if not st.session_state.orders.empty:
        t_df = st.session_state.orders[st.session_state.orders['timestamp'].str.contains(today)]
        t_sales = t_df['total_amount'].sum()
        t_orders = len(t_df)
        
    l_stock = len(st.session_state.menu[(st.session_state.menu['stock'] < 10) & (st.session_state.menu['status'] == "Available")])
    
    # Metric Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Today's Gross Revenue", f"₹{t_sales:.2f}")
    with col2:
        st.metric("📦 Order Count Today", t_orders)
    with col3:
        st.metric("⚠️ Low Inventory Warning", l_stock)
        
    st.markdown("---")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown("### 🍕 Revenue Stream by Category")
        if st.session_state.order_items.empty:
            st.info("Data pending initial orders.")
        else:
            cat_data = st.session_state.order_items.groupby('category')['subtotal'].sum().reset_index()
            fig = px.pie(cat_data, values='subtotal', names='category', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
            fig.update_layout(margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)
            
    with col_c2:
        st.markdown("### 🔝 Top Performing Delicacies")
        if st.session_state.order_items.empty:
            st.info("Data pending initial orders.")
        else:
            top_data = st.session_state.order_items.groupby('item_name')['quantity'].sum().reset_index()
            top_data = top_data.sort_values(by='quantity', ascending=True).tail(5)
            fig = px.bar(top_data, x='quantity', y='item_name', orientation='h',
                         color='quantity', color_continuous_scale='Sunsetdark')
            fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
    st.markdown("---")
    st.markdown("### 🚨 Low Inventory Alerts")
    alert_df = st.session_state.menu[(st.session_state.menu['stock'] < 10) & (st.session_state.menu['status'] == "Available")]
    
    if alert_df.empty:
        st.success("✨ Clean slate! All inventory levels optimal.")
    else:
        st.warning("Refill orders recommended immediately:")
        st.dataframe(alert_df[['item_name', 'category', 'stock']].reset_index(drop=True), use_container_width=True)
