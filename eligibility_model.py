import streamlit as st
import joblib

# Load the model
purchase_model = joblib.load('user_purchase_prediction.joblib')

def model():
    st.header('Promotion Eligibility Model')

    st.write(' ')

    # Section 1: Determine Customer Segment
    st.write('**Input user data.**')
    col1, col2 = st.columns(2)
    with col1:
        purchase_frequency = st.number_input('Purchase Frequency', min_value=0, step=1, format='%d')
    with col2:
        total_spending = st.number_input('Total Spending (USD)', min_value=0, step=1000, format='%d')

    if purchase_frequency == 0 and total_spending == 0:
        customer_segment = 'Visitor'
    elif total_spending < 2600:
        if purchase_frequency == 1:
            customer_segment = 'Bronze'
        else:
            customer_segment = 'Repeat Prospect'
    else:
        if purchase_frequency > 1:
            customer_segment = 'Potential Loyalist'
        else:
            customer_segment = 'High Spender'
    if st.button('Classify User'):
        st.write('User Segment:', customer_segment)

    st.write(' ')

    # Section 2: Input variables
    st.write('**Input user activity for the product.**')
    product_categories = ['Electronic Appliances', "Men's Fashion", 'Mobile & Accessories', 'Cleaning supplies', 'Digital Devices', 'Accessories', 'Stationary', 'Digital Content', 'Fitness', "Women's Fashion", 'Household Supplies', 'Smart Wearables', 'Home Appliances', 'Pet Care', 'Gardening', 'Camera Accessories', 'eCommerce', 'Baby Care', 'Laptop & Desktop', 'Gaming Accessories', 'Musical Instruments', 'Kitchen Appliances', 'Entertainment Systems', 'Software', 'Pendrives', 'Home Decor', 'Electricals', 'Furnitures', 'Religious items', 'Artwork', 'Car Accessories', 'Kids Fashion', 'Motorbike Accessories', 'Toys', 'Music', 'Gifts', 'Tv & Appliances', 'Bags and Luggage', 'Industrial', 'Grocery', 'Winter Wear', 'Personal Care', "Men's Bottom Wear", "Men's Top Wear", 'Shoe care', 'Computer Peripherals', 'Healthcare Appliances', 'Laptop Accessories', 'Smart Home Appliances', 'Storage', 'Bed room', 'Tools and Utility', 'Lightings', 'Space saving', "Men's Grooming", 'Food and drinks', 'School Supplies', 'Sports', 'Women western', 'Footwear', 'Essentials', 'Desktop Accessories', 'Kitchen and dining', 'Home furnishing', 'Utilities', 'Lock and Security', 'Personal Safety', 'Kitchen Storage', 'Books', 'Food essentials', 'Bike care', 'Women Footwear', 'Camera', 'Network component', 'Movies', 'Tablets', 'Sports Accessories']
    top_categories = ['Tablets', 'Digital Devices', 'Laptop & Desktop', "Women's Fashion", 'Mobile & Accessories', 'Furnitures', 'Home Appliances']
    product_category = st.selectbox('Product Category', product_categories)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        session_count = st.number_input('Session Count', min_value=0, step=1, format='%d')
        first_app_open = st.number_input('First App Open', min_value=0, step=1, format='%d')
    with col2:
        search = st.number_input('Search', min_value=0, step=1, format='%d')
        product_view = st.number_input('Product View', min_value=0, step=1, format='%d')
    with col3:
        read_reviews = st.number_input('Read Reviews', min_value=0, step=1, format='%d')
        add_to_wishlist = st.number_input('Add to Wishlist', min_value=0, step=1, format='%d')
    with col4:
        click_wishlist_page = st.number_input('Click Wishlist Page', min_value=0, step=1, format='%d')
    if st.button('Predict Purchase'):
        predicted = purchase_model.predict([[session_count, first_app_open, search, product_view, read_reviews, add_to_wishlist, click_wishlist_page]])
        st.write('Predicted Purchase:', 'Yes' if predicted[0] == 1 else 'No')

    st.write(' ')

    # Section 3: User outcome
    st.write('**Did the user end up making purchase for this product?**')
    actual_purchase = st.selectbox('Select Outcome', ['Yes', 'No'])

    st.write(' ')

    if st.button('Proceed Eligibility'):
        prediction = purchase_model.predict([[session_count, first_app_open, search, product_view, read_reviews, add_to_wishlist, click_wishlist_page]])
        if customer_segment in ['Potential Loyalist', 'High Spender']:
            if prediction[0] == 1 and actual_purchase == 'Yes':
                st.write('User is not eligible for tailored promotion.')
            elif prediction[0] == 1 and actual_purchase == 'No':
                st.write('User is eligible for tailored promotion.')
            elif prediction[0] == 0 and actual_purchase == 'Yes':
                st.write('User is not eligible for tailored promotion.')
            elif prediction[0] == 0 and actual_purchase == 'No':
                if product_category in top_categories:
                    st.write('User is eligible for tailored promotion.')
                else:
                    st.write('User is not eligible for tailored promotion.')
        elif customer_segment in ['Repeat Prospect', 'Bronze', 'Visitor']:
            if prediction[0] == 1 and actual_purchase == 'Yes':
                st.write('User is not eligible for tailored promotion.')
            elif prediction[0] == 1 and actual_purchase == 'No':
                if product_category in top_categories:
                    st.write('User is eligible for tailored promotion.')
                else:
                    st.write('User is not eligible for tailored promotion.')
            elif prediction[0] == 0 and actual_purchase == 'Yes':
                st.write('User is not eligible for tailored promotion.')
            elif prediction[0] == 0 and actual_purchase == 'No':
                st.write('User is not eligible for tailored promotion.')