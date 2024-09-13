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
        {"role": "assistant", "content": f"The current product detail html is: \n{html}"},
        {"role": "assistant", "content": f"The SEO keywords we want to use are: \n{keywords}"},
        {"role": "user", "content": "Generate me a revised version of the detailed html, correcting any syntax errors, fixing incoherent sentences, and friendly to SEO principles."},
        {"role": "user", "content": "And a short SEO-friendly description within 200 chars."},
        {"role": "user", "content": "The output should be in pure JSON dictionary with two keys: 'revised_html' and 'short_description'."},
    ]

    completion = client.beta.chat.completions.parse(
        model=OPENAI_API_MODEL,
        messages=messages,
        response_format=SeoResult,
    )

    return completion.choices[0].message.parsed


