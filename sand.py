import requests

response = requests.get("https://newsapi.org/v2/everything?q=tesla&from=2023-03-25&sortBy=publishedAt&apiKey=ba734fb2d537440d9e3dcb4b0d0b3f8a")

data = response.json()

news = [n for n in data["articles"] if data["articles"].index(n) < 3]

print(data)
print(news)
