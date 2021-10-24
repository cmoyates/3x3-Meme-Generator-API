from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from fastapi import FastAPI, responses
from tempfile import NamedTemporaryFile
from shutil import copyfileobj
from os import remove

SIDE_LENGTH = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
THIRD = SIDE_LENGTH // 3

ALIGNMENTS = [
    ["Lawful Good", "Neutral Good", "Chaotic Good"],
    ["Lawful Neutral", "True Neutral", "Chaotic Neutral"],
    ["Lawful Evil", "Neutral Evil", "Chaotic Evil"],
]


def ImportImage(img_string: str):
    r = requests.get(img_string)
    img = Image.open(BytesIO(r.content))
    img = img.resize((THIRD, THIRD))
    return img


font = ImageFont.truetype("arial.ttf", 20)


def generate(input_array):
    image = Image.new("RGB", (SIDE_LENGTH, SIDE_LENGTH), color=WHITE)
    image_draw = ImageDraw.Draw(image)

    for i in range(3):
        for j in range(3):
            try:
                user_image = ImportImage(input_array[i][j])
                image.paste(user_image, (THIRD * i, THIRD * j))
            except:
                return f"Malformed input: Failed on image index {(i) * 3 + j}"

    for i in range(THIRD, SIDE_LENGTH, THIRD):
        image_draw.line([(0, i), (SIDE_LENGTH, i)], fill=BLACK, width=5)
        image_draw.line([(i, 0), (i, SIDE_LENGTH)], fill=BLACK, width=5)

    for i in range(3):
        for j in range(3):
            w, h = image_draw.textsize(ALIGNMENTS[i][j], font)
            image_draw.text(
                (THIRD // 2 + (THIRD * i) - w // 2, 5 + (THIRD * j)),
                ALIGNMENTS[i][j],
                font=font,
                align="center",
                fill=BLACK,
                stroke_width=1,
                stroke_fill=WHITE,
            )

    return image


# test_user_image = ImportImage("https://i.imgur.com/V73crmb.jpg")

app = FastAPI()


@app.get("/")
def return_root():
    return "Still working!"


@app.get("/api")
def return_image(
    lg: str, ng: str, cg: str, ln: str, tn: str, cn: str, le: str, ne: str, ce: str
):

    input_array = [[lg, ng, cg], [ln, tn, cn], [le, ne, ce]]

    file_name = "car.jpg"

    new_img = generate(input_array)
    if type(new_img) == str:
        return new_img

    new_img.save(file_name)
    temp_file_obj = NamedTemporaryFile(mode="w+b", suffix="jpg")
    pil_image = open(file_name, "rb")
    copyfileobj(pil_image, temp_file_obj)
    pil_image.close()
    remove(file_name)
    temp_file_obj.seek(0, 0)

    return responses.StreamingResponse(
        BytesIO(temp_file_obj.read()), media_type="image/jpg"
    )


@app.get("/test")
def test_image(image_url: str):
    try:
        ImportImage(image_url)
        return responses.Response(content="Valid")
    except:
        return responses.Response(content="Not Valid")


if __name__ == "__main__":
    app.run()
