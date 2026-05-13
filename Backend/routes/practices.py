from fastapi import APIRouter

router=APIRouter()

@router.get("/")
def display():
    

    res=[
{
"id": 162,
"title": "Blue Frock",
"price": 29.99,
"quantity": 4,
"total": 119.96,
"discountPercentage": 12.13,
"discountedTotal": 105.41,
"thumbnail": "https://cdn.dummyjson.com/product-images/tops/blue-frock/thumbnail.webp"
},
{
"id": 113,
"title": "Generic Motorcycle",
"price": 3999.99,
"quantity": 3,
"total": 11999.97,
"discountPercentage": 12.1,
"discountedTotal": 10547.97,
"thumbnail": "https://cdn.dummyjson.com/product-images/motorcycle/generic-motorcycle/thumbnail.webp"
},
{
"id": 122,
"title": "iPhone 6",
"price": 299.99,
"quantity": 3,
"total": 899.97,
"discountPercentage": 6.69,
"discountedTotal": 839.76,
"thumbnail": "https://cdn.dummyjson.com/product-images/smartphones/iphone-6/thumbnail.webp"
}
]
    return res