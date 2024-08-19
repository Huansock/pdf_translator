from pdf2image import convert_from_path
from openai import OpenAI
import base64
import re
import os
from pathlib import Path
import requests


class ai_translator:
    def __init__(self):
        pass

    def _encode_image(image_path: Path):
        # Function to encode the image
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    @classmethod
    def translate(
        cls,
        pdf_name: str = None,
        src_lang: str = None,
        dst_lang: str = None,
        api_key: str = "",
    ):
        client = OpenAI()
        print(f"type of pdf_name = {type(pdf_name)}")
        print(pdf_name)
        name2store = f"{pdf_name}_{src_lang}_to_{dst_lang}"
        pdf_path = f"media/pdfs/{pdf_name}.pdf"
        output_path_base = "media/output_images/{pdf_name}_page_{index}.jpg"

        images = convert_from_path(pdf_path)

        for i, image in enumerate(images):
            img_path = output_path_base.format(pdf_name=pdf_name, index=i + 1)
            image.save(img_path, "JPEG")

        md_path = f"media/markdowns/{name2store}.md"

        i = 0
        open(md_path, "w")
        while i < len(images):
            current_image_path = output_path_base.format(pdf_name=pdf_name, index=i + 1)
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful, professional image translator.",
                },
                {
                    "role": "system",
                    "name": "example_user",
                    "content": "You are a helpful, image translator from source english to korean. response type is raw markdown. organize the output and remove redundanz.translate it in korean",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"You are a helpful, image translator from source {src_lang} to {dst_lang}. response type is raw markdown. organize the output and remove redundanz. write running header small.Emphasize the title of the paragraph.",
                        },
                    ],
                },
            ]

            messages[2]["content"].append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{cls._encode_image(current_image_path)}"
                    },
                }
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                n=1,
                max_tokens=16383,
                temperature=0,
            )
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful, professional image translator.",
                    },
                    {
                        "role": "system",
                        "name": "example_user",
                        "content": "You are a helpful, image translator from source english to korean. response type is raw markdown. organize the output and remove redundanz.translate it in korean",
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"You are a helpful, image translator from source {src_lang} to {dst_lang}. response type is raw markdown. organize the output and remove redundanz. write running header small.Emphasize the title of the paragraph.",
                            },
                        ],
                    },
                ],
                "max_tokens": 16383,
                "n": 1,
                "temperature": 0,
            }

            payload["messages"][2]["content"].append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{cls._encode_image(current_image_path)}"
                    },
                }
            )

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
            )

            # remove ```markdown ``` part
            result = response.choices[0].message.content
            result = re.sub(r"^```markdown", "", result, count=1)
            result = re.sub(r"```(?![\s\S]*```)", "", result)

            # open markdown file

            file = open(md_path, "a+")
            file.write(result)
            file.write(f"\npage -{i+1}-\n")

            # remove pdf file
            file.close()
            os.remove(current_image_path)
            # increase i
            i += 1
        os.remove(f"media/pdfs/{pdf_name}.pdf")
