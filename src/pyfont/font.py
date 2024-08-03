import pygame as pg
from math import ceil

class Font:
    def __init__(self, image: pg.Surface, padding=1):
        self.image = image
        self.char_key = []
        self.load_font_key('abcdefghijklmnopqrstuvwxyz1234567890.,;-?!_')
        self.char_dict = {}
        self.font_width = self.image.get_width()//len(self.char_key)
        self.font_height = self.image.get_height()
        self.padding = padding
        self.load_font()
    
    def load_font_key(self, chars):
        for char in chars:
            self.char_key.append(char)

    def load_font(self):
        for i in range(len(self.char_key)):
            letter = pg.Surface((self.font_width, self.font_height))
            letter.blit(self.image, (-i*self.font_width, 0))
            if i%2==0:
                letter.set_colorkey((0, 0, 255))
            else:
                letter.set_colorkey((255, 0, 0))
            white = pg.Surface((self.font_width, self.font_height))
            white.fill((255, 255, 255))
            white.blit(letter, (0, 0))
            white.set_colorkey((0, 0, 0))
            self.char_dict[self.char_key[i]] = white

    def get_paragraph(self, text_list, max_char_per_line):
        char_count = 0
        lines = []
        line = []
        for word in text_list:
            if char_count+len(word)<=max_char_per_line:
                char_count+=len(word)
                line.append(word)
                char_count+=1
            elif char_count==0:
                line.append(word)
                lines.append(line)
                line = []
                char_count = 0
            else:
                lines.append(line)
                char_count = len(word)
                line = [word]
                char_count+=1

        if line:
            lines.append(line)
        return lines

    def render(self, screen: pg.Surface, text: str, x: float, y: float, colour: tuple | list[tuple], size=0, style='left', alpha=255, box_width=0, highlighting=None):
        if size==0:
            size = self.font_width
        
        ratio = size/self.font_width
        scaled_height = ceil(ratio*self.font_height)
        scaled_padding = ceil(ratio*self.padding)
        
        text_list = text.split(' ')

        max_char_per_line = len(text)
        if box_width!=0:
            max_char_per_line = box_width//(size+scaled_padding)

        paragraph = self.get_paragraph(text_list, max_char_per_line)
        start_x, start_y = x, y

        if style=='center':
            start_y = y-(scaled_height+scaled_padding)*(len(paragraph)-1)/2
        
        count = 0
        for line_num, line in enumerate(paragraph):
            char_count = 0
            if style=='center':
                start_x = x-(size+scaled_padding)*(len(' '.join(line))-1)/2
            for word in line:
                for char in word:
                    char = char.lower()
                    letter = self.char_dict[char]
                    letter.set_colorkey((255, 255, 255))
                    coloured_letter = pg.Surface((self.font_width, self.font_height))
                    if highlighting is None:
                        coloured_letter.fill(colour)
                    else:
                        c = colour[int(highlighting[count])]
                        coloured_letter.fill(c)
                    coloured_letter.blit(letter, (0, 0))
                    letter = pg.transform.scale(coloured_letter, (size, scaled_height))
                    letter.set_colorkey((0, 0, 0))
                    letter.set_alpha(alpha)
                    screen.blit(letter, 
                                (start_x+(size+scaled_padding)*char_count-size//2, 
                                 start_y+(scaled_height+scaled_padding)*line_num-scaled_height//2))
                    char_count += 1
                    count += 1
                char_count += 1
                count += 1
        
    def text_width(self, text, size):
        if size==0:
            size = self.font_width
            
        ratio = size/self.font_width
        scaled_padding = ceil(ratio*self.padding)

        return len(text)*(size+scaled_padding)

    def text_height(self, text, size=0, width=0):
        if size==0:
            size = self.font_width
            
        ratio = size/self.font_width
        scaled_height = ceil(ratio*self.font_height)
        scaled_padding = ceil(ratio*self.padding)

        if width:
            text_list = text.split(' ')
            max_char_per_line = width//(size+scaled_padding)
            char_count = 0
            num_lines = 1
            for word in text_list:
                if char_count == 0:
                    if len(word)>max_char_per_line:
                        num_lines+=1
                    else: 
                        char_count+=len(word)
                elif char_count+len(word)>max_char_per_line:
                    num_lines+=1
                    char_count = len(word)
                else:
                    char_count+=len(word)
                char_count+=1
            return num_lines*(scaled_height+scaled_padding)
        else:
            return scaled_height+scaled_padding

    def char_height(self, size=0):
        if size==0:
            size = self.font_width
        
        ratio = size/self.font_width
        scaled_height = ceil(ratio*self.font_height)

        return scaled_height
        
