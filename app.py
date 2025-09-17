import streamlit as st
import json

# Load product data
with open("products.json", "r") as f:
    products = json.load(f)

# Initialize cart in session state
if "cart" not in st.session_state:
    st.session_state.cart = []

# Show products by category
def show_products(category):
    st.header(category)
    for product in [p for p in products if p["category"] == category]:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(product["image"], width=180)
        with col2:
            st.subheader(product["name"])
            for size, price in product["price"].items():
                if st.button(f"Add {size} - ₹{price}", key=f"{product['id']}_{size}"):
                    st.session_state.cart.append({
                        "name": product["name"],
                        "size": size,
                        "price": price
                    })
                    st.success(f"Added {product['name']} ({size}) to cart")

# Show cart
def show_cart():
    st.header("🛒 Your Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        total = 0
        for item in st.session_state.cart:
            st.write(f"- {item['name']} ({item['size']}) - ₹{item['price']}")
            total += item["price"]
        st.subheader(f"Total: ₹{total}")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Pickles", "Podis", "Sweets", "Snacks", "Cart"])

# Pages
if page == "Home":
    st.title("🍴 Welcome to HomeFoods E-Commerce")
    st.image(
        "https://raw.githubusercontent.com/sreyadevarapalli/ecommerce-Website/main/images/Homefoods.png",
        width=700
    )
    st.write("Delicious homemade pickles, sweets, podis, and snacks delivered to your doorstep!")
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
