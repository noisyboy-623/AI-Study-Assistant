# services/summarizer_service.py

class SummarizerService:
    def __init__(self):
        # later we’ll integrate Cohere / OpenAI here
        pass

    async def generate_summary(self, text: str, max_length: int = 100, min_length: int = 30) -> str:
        # temporary dummy logic
        words = text.split()
        shortened = " ".join(words[:max_length])
        return shortened + ("..." if len(words) > max_length else "")
