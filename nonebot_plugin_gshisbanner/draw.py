from io import BytesIO
from typing import List

from PIL.Image import Image as ImageType
from PIL import Image, ImageDraw, ImageFont

from .model import GachaDraw
from .config import plugin_config


class GameGachaBanner:
    def __init__(
        self,
        gacha_data: List[GachaDraw],
        gacha_name: str,
        gacha_type: str,
    ):
        self.num_rows = len(gacha_data)
        self.row_height = 30
        self.img_height = (self.num_rows + 1) * self.row_height
        self.font = ImageFont.truetype(plugin_config.pic_font_path, 18)
        self.gacha_name = gacha_name
        self.gacha_type = gacha_type
        self.col_widths = [
            len(f"{gacha_name}历史卡池") * 20,
            max([sum(len(x) for x in i.five_star) * 25 for i in gacha_data]),
            max([sum(len(x) for x in i.four_star) * 25 for i in gacha_data]),
            len(gacha_data[0].start.strftime("%Y-%m-%d %H:%M:%S")) * 12,
            len(gacha_data[0].end.strftime("%Y-%m-%d %H:%M:%S")) * 12,
        ]
        self.img_width = int(sum(self.col_widths))
        self.line_color = (0, 0, 0)
        self.line_width = 3
        self.gacha_data = gacha_data

    def _header(self, gacha_name, gacha_type) -> List[str]:
        return [
            f"{gacha_name}历史卡池",
            f"五星{gacha_type}",
            f"四星{gacha_type}",
            "开始时间",
            "结束时间",
        ]

    @property
    def get_header(self) -> List[str]:
        return self._header(self.gacha_name, self.gacha_type)

    def _create_image(self) -> ImageType:
        img = Image.new("RGB", (self.img_width, self.img_height), color=(255, 255, 255))
        self.draw = ImageDraw.Draw(img)
        return img

    def _draw_table(self) -> None:
        # 绘制水平线
        for i in range(self.num_rows + 1):
            y = i * self.row_height
            self.draw.line(
                [(0, y), (self.img_width, y)],
                fill=self.line_color,
                width=self.line_width,
            )

        # 绘制垂直线
        for i in range(len(self.get_header) - 1):
            x = sum(self.col_widths[: i + 1])
            self.draw.line(
                [(x, 0), (x, self.img_height)],
                fill=self.line_color,
                width=self.line_width,
            )

        # 绘制表头
        for col_idx, header_text in enumerate(self.get_header):
            x = sum(self.col_widths[:col_idx])
            bbox = self.draw.textbbox((0, 0), header_text, font=self.font)
            centered_x = x + (self.col_widths[col_idx] - bbox[2]) / 2
            self.draw.text((centered_x, 0), header_text, font=self.font, fill=(0, 0, 0))

        # 绘制数据行
        for row_idx, row_data in enumerate(self.gacha_data, start=1):
            for col_idx, cell_text in enumerate(
                [
                    "{}.{}  卡池{}".format(*row_data.version.split(".")),
                    "、".join(row_data.five_star),
                    "、".join(row_data.four_star),
                    row_data.start.strftime("%Y-%m-%d %H:%M:%S"),
                    row_data.end.strftime("%Y-%m-%d %H:%M:%S"),
                ]
            ):
                x = sum(self.col_widths[:col_idx])
                bbox = self.draw.textbbox((0, 0), str(cell_text), font=self.font)
                centered_x = x + (self.col_widths[col_idx] - bbox[2]) / 2
                y = row_idx * self.row_height
                self.draw.text(
                    (centered_x, y), str(cell_text), font=self.font, fill=(0, 0, 0)
                )

    def generate_table(self) -> bytes:
        img = self._create_image()
        self._draw_table()
        img_buffer = BytesIO()
        img.save(img_buffer, format="PNG")
        return img_buffer.getvalue()
