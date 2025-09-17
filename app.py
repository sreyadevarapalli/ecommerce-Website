import streamlit as st
import json

# --- Load products ---
with open("products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# --- Initialize session state for cart ---
if "cart" not in st.session_state:
    st.session_state.cart = []

# --- Helper functions ---
def add_to_cart(product, size, price):
    st.session_state.cart.append({
        "id": product["id"],
        "name": product["name"],
        "size": size,
        "price": price
    })
    st.success(f"✅ {product['name']} ({size}) added to cart!")

def show_products(category):
    st.header(category)
    cols = st.columns(3)
    items = [p for p in products if p["category"] == category]
    for i, product in enumerate(items):
        with cols[i % 3]:
            st.image(product["image"], width=200)
            st.subheader(product["name"])
            for size, price in product["price"].items():
                if st.button(f"Add {size} - ₹{price}", key=f"{product['id']}_{size}"):
                    add_to_cart(product, size, price)

def show_cart():
    st.header("🛒 Your Cart")
    if not st.session_state.cart:
        st.warning("Your cart is empty!")
        return
    total = 0
    for item in st.session_state.cart:
        st.write(f"{item['name']} ({item['size']}) - ₹{item['price']}")
        total += item['price']
    st.subheader(f"Total: ₹{total}")
    if st.button("Proceed to Checkout"):
        st.session_state.page = "Checkout"

def show_checkout():
    st.header("💳 Checkout")
    if not st.session_state.cart:
        st.warning("Your cart is empty!")
        return
    total = sum(item['price'] for item in st.session_state.cart)
    st.write("Please enter your details:")
    name = st.text_input("Full Name")
    address = st.text_area("Address")
    phone = st.text_input("Phone Number")
    if st.button("Pay Now"):
        if name and address and phone:
            st.success(f"✅ Payment Successful! Order placed for ₹{total}.")
            st.session_state.cart.clear()
        else:
            st.error("⚠️ Please fill all details!")

def show_about():
    st.header("ℹ️ About Us")
    st.write("""
    Welcome to our **Homemade Pickles, Sweets & Snacks Store**!  
    We bring you traditional flavors made with love and care.  
    100% homemade, hygienic, and authentic taste from our kitchen to your home.  
    """)

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Pickles", "Podis", "Sweets", "Snacks", "Cart", "Checkout", "About Us"])

# --- Page Routing ---
if page == "Home":
    st.title("🍴 Welcome to Our E-Commerce Store")
    st.image("images/HomeFoods.png", use_container_width=True)  # Your home image
    st.markdown("""
    ### 🏠 Homemade Goodness  
    Welcome to our **Homemade Pickles, Podis, Sweets & Snacks Store**!  
    Authentic taste, hygienic preparation, and made with love ❤️  
    Browse our categories to explore delicious varieties.
    """)
elif page == "Pickles":
    show_products("Pickles")
elif page == "Podis":
    show_products("Podis")
elif page == "Sweets":
    show_products("Sweets")
elif page == "Snacks":
    show_products("Snacks")
elif page == "Cart":
    show_cart()
elif page == "Checkout":
    show_checkout()
elif page == "About Us":
    show_about()
