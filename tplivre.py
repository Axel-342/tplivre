import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape a single page
def scrape_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    books = []
    for article in soup.select('article.product_pod'):
        book = {}
        book['title'] = article.h3.a['title']
        book['price'] = float(article.select_one('p.price_color').get_text(strip=True).replace('£', ''))
        
        # Get rating
        rating_class = article.select_one('p.star-rating')['class']
        rating = rating_class[1]
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        book['rating'] = rating_map[rating]
        
        if book['rating'] >= 3 and book['price'] > 20.00:
            books.append(book)
    
    return books

# Scrape the first 10 pages
base_url = "https://books.toscrape.com/catalogue/page-{}.html"
all_books = []
for page_num in range(1, 11):
    page_url = base_url.format(page_num)
    all_books.extend(scrape_page(page_url))

# Create a DataFrame to display the books
df_books = pd.DataFrame(all_books, columns=['title', 'price', 'rating'])
print(df_books)

# Write to result.csv
df_books.to_csv('result.csv', index=False)
print("Les livres avec une note de 3 étoiles ou plus et un prix supérieur à 20.00€ ont été écrits dans 'result.csv'.")
