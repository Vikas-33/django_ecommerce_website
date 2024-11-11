Django E-commerce Platform
This is a simple Django-based e-commerce application with features for user authentication, product management, and a seller dashboard. The project is designed for educational purposes, demonstrating the core functionalities of a basic e-commerce platform.

Features
User Registration and Authentication: Secure registration, login, and logout functionalities.
Product Management: Users with a seller profile can add, update, and delete products.
Shopping Cart: Customers can add products to their cart and adjust quantities.
Seller Dashboard: Sellers have access to a dashboard displaying their products and sales.
Category Filtering: Products can be filtered by category.
Responsive Design: The UI is built using Bootstrap for a responsive, mobile-friendly experience.
Installation

Clone the repository:

bash
Copy code
   git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


Set up a virtual environment:

bash
Copy code
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`


Install dependencies:

bash
Copy code
   pip install -r requirements.txt


Apply migrations:

bash
Copy code
   python manage.py migrate


Run the development server:

bash
Copy code
   python manage.py runserver


Access the application: Open http://127.0.0.1:8000 in your web browser.

Project Structure
Templates: Contains HTML files for different pages (home, product details, cart, dashboard).
Models: Defines models for User Profiles, Products, Cart, etc.
Views: Contains the logic for handling requests and rendering pages.
Static: Contains CSS, JS, and image files.
Usage
Sign up as a regular user or seller.
Browse products as a customer and add items to your cart.
Access the seller dashboard if you are a seller to manage products.
Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.
