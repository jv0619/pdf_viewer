import fitz
import math
from tkinter import PhotoImage


class Viewer:

    def __init__(self, file, width):
        self.filepath = file
        self.pdf = fitz.open(self.filepath)
        self.page = self.pdf.load_page(0)
        self.width, self.height = self.page.rect.width, self.page.rect.height
        self.zoom = width/self.width


    def get_metadata(self):
        metadata = self.pdf.metadata
        total_pages = self.pdf.page_count
        return metadata, total_pages

    def get_page(self, page_num):
        mat = fitz.Matrix(self.zoom, 1)
        page = self.pdf.load_page(page_num)
        pix = page.get_pixmap(matrix=mat)
        px1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
        imgdata = px1.tobytes("ppm")
        return PhotoImage(data=imgdata), self.height

    def get_all_text(self, page_num):
        page = self.pdf.load_page(page_num)
        text = page.get_text('text')
        return text


