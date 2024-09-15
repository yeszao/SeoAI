from pydantic import BaseModel
from openai import OpenAI

from lib.config import OPENAI_API_KEY, OPENAI_API_MODEL


client = OpenAI(api_key=OPENAI_API_KEY)


class SeoResult(BaseModel):
    short_description: str
    revised_html: str


def generate_seo_content(html, keywords) -> SeoResult:

    messages=[
        {"role": "system", "content": "You are a Google SEO expert specializing in optimizing content without generating new HTML structures."},
        {"role": "assistant", "content": f"Here is the current HTML content that needs revision, not a full rewrite: \n\n{html}"},
        {"role": "assistant", "content": f"The relevant SEO keywords are: \n\n{keywords}"},
        {"role": "user", "content": "Please revise the existing HTML content without changing the structure. Focus on fixing syntax errors, improving readability, and incorporating SEO best practices where relevant."},
        {"role": "user", "content": "Also, generate a concise, SEO-friendly short description of the page that is less than 160 characters."}
    ]

    completion = client.beta.chat.completions.parse(
        model=OPENAI_API_MODEL,
        messages=messages,
        response_format=SeoResult,
    )

    return completion.choices[0].message.parsed


