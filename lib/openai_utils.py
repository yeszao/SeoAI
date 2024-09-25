from pydantic import BaseModel
from openai import OpenAI

from lib.config import OPENAI_API_KEY, OPENAI_API_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


class SeoResult(BaseModel):
    short_description: str
    revised_html: str


def generate_seo_content(html, keywords) -> SeoResult:
    messages = [
        {"role": "system", "content": "You are an expert Google SEO specialist with extensive knowledge of current best practices and algorithms. Your task is to optimize HTML content for search engines while maintaining readability and user experience."},
        {"role": "user", "content": f"Review the following HTML content:\n\n```html\n{html}\n```"},
        {"role": "user", "content": f"SEO keywords:\n{keywords}"},
        {"role": "user", "content": """Optimize the HTML content for SEO while preserving the original paragraph order and structure. Your optimization should include:
    1. Correct any HTML and statement syntax errors
    2. Enhance overall readability
    3. Optimize heading structure from H2 tag to include SEO keywords
    4. Naturally incorporate both primary and long-tail keywords throughout the content
    5. Add alt text to images, if any, using relevant keywords
    6. Insert relevant keywords to the content where appropriate and bold them for emphasis
    7. Don't wrap the content in <html> or <body> tags
    8. Reorganize the sentences to avoid repeated detection by search engines
    """},
        {"role": "user", "content": "Generate a concise, compelling meta description for the page, under 160 characters. Include the most important primary keyword and accurately summarize the page content."},
    ]

    completion = client.beta.chat.completions.parse(
        model=OPENAI_API_MODEL,
        messages=messages,
        response_format=SeoResult,
    )

    return completion.choices[0].message.parsed


