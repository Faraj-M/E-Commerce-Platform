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
- **Response**: List of user objects

#### Get Current User
- **GET** `/api/accounts/users/me/`
- **Description**: Get authenticated user's profile
- **Authentication**: Required
- **Response**: Current user object

#### Update Current User
- **PUT** `/api/accounts/users/me/`
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

