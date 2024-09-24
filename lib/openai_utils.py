from pydantic import BaseModel
from openai import OpenAI

from lib.config import OPENAI_API_KEY, OPENAI_API_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


class SeoResult(BaseModel):
    short_description: str
    revised_html: str


def generate_seo_content(html, keywords) -> SeoResult:

    messages=[
        {"role": "system", "content": "You are an expert Google SEO specialist with extensive knowledge of current best practices and algorithms."},
        {"role": "user", "content": f"Review the following HTML content:\n\n```html\n{html}\n```c"},
        {"role": "user", "content": f"SEO-relevant keywords:\n{keywords}"},
        {"role": "user", "content": "Revise the HTML while preserving its structure. Focus on correcting syntax, enhancing readability, optimizing for SEO, and prioritizing the use of both primary and long-tail keywords."},
        {"role": "user", "content": "Additionally, provide a concise, SEO-optimized meta description for the page, under 160 characters."}
    ]

    completion = client.beta.chat.completions.parse(
        model=OPENAI_API_MODEL,
        messages=messages,
        response_format=SeoResult,
    )

    return completion.choices[0].message.parsed


