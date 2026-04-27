# Model Card — LewisMusicRecs

## Model Name
LewisMusicRecs

## Goal / Task
Given a user's sentence, the system suggests the five songs from the catalog most likely to match that sentence.

I used AI assistance in two main areas during this project.

**Feature development** — I used AI to help design and implement the structured prompting layer. This included deciding how to structure the system prompt so Llama would reliably return a valid JSON profile, choosing which fields to extract (genre, mood, energy, likes_acoustic), and writing the `parse_natural_language_to_profile()` function that connects the user's input to the existing recommender. AI helped me think through the design so the new layer could wrap the original scoring logic without modifying it.

**Understanding the Groq API** — I used AI to understand how the Groq API works, including how to authenticate with an API key via a `.env` file, how to use `response_format={"type": "json_object"}` to enforce structured output from the model, and how to handle the response object to extract the generated text. AI walked me through the differences between the Groq client and other APIs, which helped me get the integration working quickly without having to read through the full documentation on my own.

**One helpful AI suggestion** — AI helped me write the system prompt used in the Groq API call. It suggested listing the exact allowed genres and moods directly in the prompt and instructing the model to respond only with a JSON object containing the four required fields. This made the model's output predictable and easy to parse, and was the most important part of getting the structured prompting layer to work reliably.

**One unhelpful AI suggestion** — Early on, AI suggested implementing the natural language parsing using the Anthropic Claude API with Claude Haiku. While the implementation it proposed was functional, the Anthropic API requires paid credits, which I didn't have access to. This made the suggestion unusable and required switching to Groq's free API with Llama instead.

---

## Limitations and Future Improvements

The main limitation of the AI layer is that the model can occasionally return a genre or mood that doesn't exactly match the allowed values in the system prompt, which causes that preference to score zero in the recommender without any visible error to the user. A meaningful future improvement would be adding a fallback that detects an unrecognized value and either retries the API call or maps the output to the closest valid option, making the system more resilient to model drift.