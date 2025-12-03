from django import template

register = template.Library()

PRODUCT_IMAGES = {
    'smartphone': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&h=600&fit=crop',
    'laptop': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&h=600&fit=crop',
    'tablet': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&h=600&fit=crop',
    'wireless headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=600&fit=crop',
    'headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=600&fit=crop',
    'cotton t-shirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&h=600&fit=crop',
    'tshirt': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&h=600&fit=crop',
    'denim jeans': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&h=600&fit=crop',
    'jeans': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&h=600&fit=crop',
    'web development guide': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800&h=600&fit=crop',
    'python programming book': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&h=600&fit=crop',
    'book': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&h=600&fit=crop',
}

@register.filter
def product_image_url(product):
    if product.image:
        return product.image.url
    
    product_name_lower = product.name.lower()
    for key, url in PRODUCT_IMAGES.items():
        if key in product_name_lower:
            return url
    
    category_name_lower = product.category.name.lower()
    if 'electronics' in category_name_lower:
        return 'https://images.unsplash.com/photo-1468495244123-6c6c332eeece?w=800&h=600&fit=crop'
    elif 'clothing' in category_name_lower:
        return 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&h=600&fit=crop'
    elif 'book' in category_name_lower:
        return 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=800&h=600&fit=crop'
    
    return 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=600&fit=crop'

