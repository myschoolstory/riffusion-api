# Riffusion API

This repository contains the code for a Riffusion API, which generates audio based on text prompts using the Riffusion-v1 model from HuggingFace. The API is designed to run on Modal.com's infrastructure.

## Overview

The Riffusion API allows you to generate audio spectrograms from text prompts and convert them into audio files. It utilizes the Stable Diffusion pipeline with the Riffusion model to create spectrograms, which are then converted to audio using the Griffin-Lim algorithm.

## Requirements

- A Modal.com account
- Python 3.7 or higher

## Setup Instructions

1. **Clone the Repository**: Start by cloning this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/riffusion-api.git
   cd riffusion-api
   ```

2. **Install the Modal CLI**: Ensure you have the Modal CLI installed:
   ```bash
   pip install modal
   ```

3. **Authenticate with Modal**: You will need to authenticate your Modal account:
   ```bash
   modal token new
   ```

## Deployment

To deploy the API to Modal, run the following command:
```bash
modal deploy riffusion_api.py
```
After successful deployment, Modal will provide you with an endpoint URL.

## Usage

To use the API, send a POST request to the endpoint with a JSON payload that includes the "prompt" key. Here’s an example using `curl`:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"prompt": "upbeat electronic music"}' https://your-modal-endpoint.modal.run
```

### Response Format

The API will respond with a JSON object containing:
- **audio**: A base64-encoded WAV file of the generated audio.
- **message**: A confirmation message that includes the input prompt.

### Example Response

```json
{
  "audio": "base64_encoded_audio_string",
  "message": "Generated audio for prompt: upbeat electronic music"
}
```

## Limitations

- The quality of the generated audio may vary since the conversion from spectrogram to audio is an approximation.
- The API has a timeout limit of 600 seconds per request.
- The model runs on an A10G GPU on Modal's infrastructure.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

Feel free to adjust any sections as necessary, especially URLs and specific instructions that pertain to your implementation or deployment environment.
