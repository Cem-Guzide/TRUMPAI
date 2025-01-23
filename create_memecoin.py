import os
import aiohttp

PUMPFUN_API_KEY = os.getenv("PUMPFUN_API_KEY")

async def deploy_coin(highlight, stream_link):
    """Deploy a memecoin based on the highlight."""
    if not PUMPFUN_API_KEY:
        raise ValueError("Pump.fun API key is missing. Set it as an environment variable.")

    print("Deploying memecoin...")
    coin_name = f"TrumpCoin-{highlight[:5].upper()}"
    ticker = coin_name[:10].upper()
  
    payload = {
        "ticker": ticker,
        "name": coin_name,
        "stream_link": stream_link,
        "total_supply": 1000000
    }

    url = "https://api.pump.fun/v1/create_memecoin" 
    headers = {
        "Authorization": f"Bearer {PUMPFUN_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                print(f"Memecoin created successfully: {result}")
                return result
            else:
                error = await response.text()
                print(f"Error creating memecoin: {error}")
                raise RuntimeError(f"Failed to create memecoin: {response.status}")
