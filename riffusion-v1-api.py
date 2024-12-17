import modal
from diffusers import StableDiffusionPipeline
import torch
import torchaudio
import io
import base64

stub = modal.Stub("riffusion-v1-api")

image = modal.Image.debian_slim().pip_install(
    "torch",
    "torchaudio",
    "diffusers",
    "transformers",
    "accelerate",
    "scipy"
)

@stub.function(
    image=image,
    gpu="A10G",
    timeout=600
)
@modal.web_endpoint(method="POST")
def generate_audio(prompt: str):
    pipe = StableDiffusionPipeline.from_pretrained(
        "riffusion/riffusion-model-v1",
        torch_dtype=torch.float16
    ).to("cuda")
    
    with torch.autocast("cuda"):
        image = pipe(prompt).images[0]
    
    # Convert spectrogram image to audio
    audio = spectrogram_to_audio(image)
    
    # Encode audio to base64
    buffer = io.BytesIO()
    torchaudio.save(buffer, audio, 44100, format="wav")
    audio_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return {"audio": audio_base64, "message": f"Generated audio for prompt: {prompt}"}

def spectrogram_to_audio(spectrogram_image):
    # Convert PIL Image to tensor
    tensor = torch.tensor(np.array(spectrogram_image)).permute(2, 0, 1).float()
    
    # Normalize
    tensor = (tensor - tensor.min()) / (tensor.max() - tensor.min())
    
    # Convert to mel spectrogram
    mel_spec = tensor[0]  # Assuming the spectrogram is in the first channel
    
    # Invert mel spectrogram to audio
    audio = torchaudio.transforms.GriffinLim()(mel_spec.unsqueeze(0))
    
    return audio

@stub.local_entrypoint()
def main():
    stub.generate_audio.serve()
