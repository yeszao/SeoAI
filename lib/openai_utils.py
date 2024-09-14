from pydantic import BaseModel
from openai import OpenAI

from lib.config import OPENAI_API_KEY, OPENAI_API_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


class SeoResult(BaseModel):
    short_description: str
    revised_html: str


def generate_seo_content(html, keywords) -> SeoResult:

    messages=[
        {"role": "system", "content": "You are a Google SEO expert."},
        {"role": "assistant", "content": f"The current product detailed html is: \n{html}"},
        {"role": "assistant", "content": f"The SEO keywords are: \n{keywords}"},
        {"role": "user", "content": "Generate a revised version of the detailed html and a short description."},
        {"role": "user", "content": "The revised html should correct any syntax errors, fix incoherent sentences, and be friendly to SEO principles."},
        {"role": "user", "content": "The short description should be concise, informative, SEO-friendly and less than 160 characters."},
        {"role": "user", "content": "Remove any HTML tag attributes that are not necessary for SEO from revised HTML."},
    ]

    completion = client.beta.chat.completions.parse(
        model=OPENAI_API_MODEL,
        messages=messages,
        response_format=SeoResult,
    )

    return completion.choices[0].message.parsed


