import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import soundfile as sf
from solana.rpc.async_api import AsyncClient
from pumpfun import create_memecoin  

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

def analyze_livestream(audio_path):
    """Analyze the livestream audio and extract key highlights."""
    print("Transcribing the livestream...")
    speech, rate = sf.read(audio_path)
    inputs = processor(speech, sampling_rate=rate, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(inputs.input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]

    print("Extracting highlights...")
    keywords = ["important", "breaking", "historic", "vote", "America"]
    highlights = [line for line in transcription.splitlines() if any(word in line for word in keywords)]

    if highlights:
        print(f"Highlights found: {highlights}")
        return highlights
    else:
        print("No significant highlights found.")
        return None

async def deploy_coin(highlight, stream_link):
    """Deploy a memecoin based on the highlight."""
    print("Deploying memecoin...")
    coin_name = f"TrumpCoin-{highlight[:5].upper()}"
    ticker = coin_name[:10].upper()
    
    async with AsyncClient("https://api.mainnet-beta.solana.com") as client:
        response = await create_memecoin(client, ticker, stream_link, total_supply=1000000)
        print(f"Memecoin created: {response}")
        return response

async def process_stream(audio_path, stream_link):
    """Process the stream by analyzing it and deploying a memecoin."""
    highlights = analyze_livestream(audio_path)
    
    if highlights:
        await deploy_coin(highlights[0], stream_link)
    else:
        print("Stream analysis complete, but no highlights for coin deployment.")
