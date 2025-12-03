# API Documentation

This document describes the REST API endpoints available in the E-Commerce Platform.

## Base URL

- Development: `http://localhost:8000/api/`
- Production: `https://your-domain.com/api/`

## Authentication

Most endpoints require authentication. Use session-based authentication or include credentials in requests.

## Endpoints

### Catalog API

#### List Products
- **GET** `/api/catalog/products/`
- **Description**: Retrieve a paginated list of active products
- **Query Parameters**:
  - `search`: Search products by name or description
  - `ordering`: Order by `price`, `created_at` (prefix with `-` for descending)
  - `page`: Page number for pagination
- **Response**: Paginated list of products with details

#### Get Product
- **GET** `/api/catalog/products/{id}/`
- **Description**: Retrieve a single product by ID
- **Response**: Product object with full details

#### Products by Category
- **GET** `/api/catalog/products/by_category/?category={slug}`
- **Description**: Get all products in a specific category
- **Response**: List of products in the category

#### List Categories
- **GET** `/api/catalog/categories/`
- **Description**: Retrieve all product categories
- **Response**: List of categories

#### Get Category
- **GET** `/api/catalog/categories/{id}/`
- **Description**: Retrieve a single category by ID
- **Response**: Category object with details

### Accounts API

#### List Users (Admin only)
- **GET** `/api/accounts/users/`
- **Description**: Retrieve all users (staff only)
- **Authentication**: Required (staff only)
- **Response**: List of user objects

#### Get User
- **GET** `/api/accounts/users/{id}/`
- **Description**: Retrieve a single user by ID
- **Authentication**: Required (staff only or own profile)
- **Response**: User object

#### Create User
- **POST** `/api/accounts/users/`
- **Description**: Create a new user account
- **Request Body**: `{ "username": "string", "email": "string", "password": "string" }`
- **Response**: Created user object

#### Update User
- **PUT/PATCH** `/api/accounts/users/{id}/`
- **Description**: Update user information
- **Authentication**: Required (staff only or own profile)
- **Request Body**: User fields to update
- **Response**: Updated user object

#### Get Current User
- **GET** `/api/accounts/users/me/`
- **Description**: Get authenticated user's profile
- **Authentication**: Required
- **Response**: Current user object

#### Update Current User
- **PUT/PATCH** `/api/accounts/users/me/`
- **Description**: Update authenticated user's profile
- **Authentication**: Required
- **Request Body**: User fields (username, email, phone, address, etc.)
- **Response**: Updated user object

### Orders API

#### List Orders
- **GET** `/api/orders/orders/`
- **Description**: Retrieve user's orders (or all orders for staff)
- **Authentication**: Required
- **Response**: List of order objects

#### Get Order
- **GET** `/api/orders/orders/{id}/`
- **Description**: Retrieve a single order by ID
- **Authentication**: Required (must be order owner or staff)
- **Response**: Order object with items

#### Create Order
- **POST** `/api/orders/orders/`
- **Description**: Create a new order from cart
- **Authentication**: Required
- **Request Body**: Order details including shipping information
- **Response**: Created order object

#### Get Order Items
- **GET** `/api/orders/orders/{id}/items/`
- **Description**: Get all items in an order
- **Authentication**: Required
- **Response**: List of order item objects

### Payments API

#### List Payments
- **GET** `/api/payments/payments/`
- **Description**: Retrieve user's payments (or all payments for staff)
- **Authentication**: Required
- **Response**: List of payment objects

#### Get Payment
- **GET** `/api/payments/payments/{id}/`
- **Description**: Retrieve a single payment by ID
- **Authentication**: Required (must be payment owner or staff)
- **Response**: Payment object with order details

## Web Views (Non-API)

### Catalog Views
- **GET** `/` - Product list page
- **GET** `/product/<slug>/` - Product detail page

### Account Views
- **GET/POST** `/accounts/signup/` - User registration
- **GET/POST** `/accounts/login/` - User login
- **POST** `/accounts/logout/` - User logout
- **GET/POST** `/accounts/profile/` - User profile management

### Order Views
- **GET** `/orders/cart/` - Shopping cart view
- **POST** `/orders/cart/add/<product_id>/` - Add item to cart
- **GET** `/orders/cart/remove/<product_id>/` - Remove item from cart
- **POST** `/orders/cart/update/<product_id>/` - Update cart item quantity
- **GET/POST** `/orders/checkout/` - Checkout page
- **GET** `/orders/list/` - User's order list
- **GET** `/orders/<order_id>/` - Order detail page

### Payment Views
- **GET** `/payments/create/<order_id>/` - Create payment intent
- **GET** `/payments/success/<payment_id>/` - Payment success page
- **POST** `/payments/webhook/` - Stripe webhook endpoint

## Response Format

All API responses follow this structure:

### Success Response
```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2"
}
```

### Paginated Response
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Response
```json
{
  "detail": "Error message here"
}
```

## Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Example Usage

### Get Products
```bash
curl http://localhost:8000/api/catalog/products/
```

### Search Products
```bash
curl "http://localhost:8000/api/catalog/products/?search=laptop"
```

### Get Current User (with authentication)
```bash
curl -X GET http://localhost:8000/api/accounts/users/me/ \
  -H "Cookie: sessionid=your-session-id"
```

### Create Order
```bash
curl -X POST http://localhost:8000/api/orders/orders/ \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your-session-id" \
  -d '{
    "shipping_address": "123 Main St",
    "shipping_city": "City",
    "shipping_postal_code": "12345",
    "shipping_country": "US"
  }'
```
