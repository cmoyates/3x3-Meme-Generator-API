from PIL import Image, ImageDraw, ImageFont

CIRCLE_RADIUS = 80
SPACING = 8

BACKGROUND_BLUE = (30, 144, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
COLOR_LIST = [WHITE, RED, YELLOW]

font = ImageFont.truetype("arial.ttf", 32)

def generate_board_image(board):
    image = Image.new(
        "RGB", (CIRCLE_RADIUS * 2 * 7, CIRCLE_RADIUS * 2 * 6 + 40), color=BACKGROUND_BLUE
    )
    image_draw = ImageDraw.Draw(image)

    for i in range(7):
        for j in range(6):
            image_draw.ellipse(
                (
                    i * 2 * (CIRCLE_RADIUS) + SPACING,
                    j * 2 * (CIRCLE_RADIUS) + SPACING,
                    (i * 2 + 2) * (CIRCLE_RADIUS) - SPACING,
                    (j * 2 + 2) * (CIRCLE_RADIUS) - SPACING,
                ),
                fill=COLOR_LIST[board[j][i]+1],
            )
        w, h = image_draw.textsize(str(i+1), font)
        image_draw.text(
            ((CIRCLE_RADIUS * (i*2 + 1)) - w // 2, CIRCLE_RADIUS * 2 * 6),
            str(i+1),
            font=font,
            align="center",
            fill=WHITE,
        )
    return image