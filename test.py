import urllib.request

try:
    response = urllib.request.urlopen('https://www.google.com')
    print("SSL connection successful.")
except Exception as e:
    print(f"SSL connection failed: {e}")

