from homepage.cloudflare.client import CloudflareStreamClient

client = CloudflareStreamClient()

response = client.post(
    "/stream/keys",
    json={}
)

print(response)