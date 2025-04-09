# ComfyUI Desktop

## Models
I tested the following checkpoint models:
- **Juggernaut XL** based on SDXL 1.0, available at [CivitAI](https://civitai.com/models/133005/juggernaut-xl).
- **DreamShaper 8** based on SD 1.5, available at [CivitAI](https://civitai.com/models/4384?modelVersionId=128713).

I experimented with different LoRAs, including:
- `aether_cloud_v1.safetensors`
- `super-realism.safetensors`

These were downloaded from Hugging Face and CIVITAI.

Additionally, I used two custom nodes:
- **ComfyUI Easy Use**
- **Was Node Suite**

---

## Image Generation Steps

![KSampler](/Capstone_2/KSampler.png)

### System Specifications
ComfyUI Desktop was deployed on:
- **MacBook Pro M3**
  - RAM: 18 GB
  - Storage: 500 GB HD

---

## Prompts

### Album Cover: Shades of Summer
**Prompt:**  
Album cover art, summer vibes, tropical, linework illustration, pastel colors, halftone background. Features palm trees, sun, ocean, and the text _'Shades of Summer Volume Two'_ in a bold sans-serif font. The color palette includes pink, yellow, and orange. Experiment with different color combinations, tropical plants, and layouts while maintaining a playful, vintage summer feel. Consider adding textures or changing the position of the sun and text.

**Original Image:**  
*![Original Image](/Capstone_2/album_cover_original.jpg)*

**AI-Generated Image:**  
*![AI-Generated Image](/Capstone_2/album_cover_AI.png)*

---

### Book Cover: Alice in Wonderland
**Prompt:**  
Children's book cover illustration for _'Alice's Adventures in Wonderland'_. Features Alice, the White Rabbit, and the Cheshire Cat in a whimsical forest setting. The style is colorful and playful, with purples, greens, and yellows dominating the palette. The text _'Alice's Adventures in Wonderland'_ is in an elegant serif font. Try different forest settings (e.g., mushroom forests, tea parties), change character poses, or explore alternative color schemes while keeping the magical and storybook-like quality.

**Original Image:**  
*![Original Image](/Capstone_2/book_cover_original.jpg)*

**AI-Generated Image:**  
*![AI-Generated Image](/Capstone_2/book_cover_AI.png)*

---

### Movie Cover: Terminator 2
**Prompt:**  
Movie poster for _'Terminator 2: Judgment Day'_. Features Arnold Schwarzenegger as the Terminator on a motorcycle, with a dark and gritty aesthetic. The color scheme is primarily black and white with red accents (glowing eyes). The text _'Terminator 2 Judgment Day'_ is in a bold, impactful font. Experiment with different action poses, lighting effects (e.g., rain, explosions), or incorporate futuristic elements while maintaining the iconic, action-packed, and slightly dystopian feel. Consider variations in the Terminator's weaponry or adding other characters from the movie.

**Original Image:**  
*![Original Image](/Capstone_2/movie_cover_original.jpg)*

**AI-Generated Image:**  
*![AI-Generated Image](/Capstone_2/movie_cover_AI.png)*

---

## Pipeline for SDXL

![Pipeline for SDXL](/Capstone_2/Pipeline%20for%20SDXL.png)

# ComfyUI on RunPod

### Models
I tested the following checkpoint model:
- **Flux1 Dev**

### Image Generation Steps

![KSampler](/Capstone_2/KSample%20for%20Flux1%20Dev.png)

### System Specifications
ComfyUI Desktop was deployed on:
- **RunPod.io**
  - GPU: A40
  - Storage: 100 GB HD

---

## Prompts (RunPod)

### Album Cover: Shades of Summer
*(Same prompt as above)*

**Original Image:**  
*![Original Image](/Capstone_2/album_cover_original.jpg)*

**AI-Generated Image:**  
*![AI-Generated Image](/Capstone_2/album_cover_AI_flux.png)*

---

### Book Cover: Alice in Wonderland
*(Same prompt as above)*

**Original Image:**  
*![Original Image](/Capstone_2/book_cover_original.jpg)*

**AI-Generated Image:**  
*![AI-Generated Image](/Capstone_2/book_cover_AI_flux.png)*

---

### Movie Cover: Terminator 2
*(Same prompt as above)*

**Original Image:**  
*![Original Image](/Capstone_2/movie_cover_original.jpg)*

**AI-Generated Image:**  
*![AI-Generated Image](/Capstone_2/movie_cover_AI_flux.png)*

---

## Pipeline for Flux1 Dev

![Pipeline for Flux1 Dev](/Capstone_2/Pipeline%20for%20Flux1%20Dev.png)

