#! /usr/bin/python
'''
@author: avalanchy (at) google mail dot com
@version: 0.1; python 2.7; pygame 1.9.2pre; SDL 1.2.14; MS Windows XP SP3
@date: 2012-04-08
@license: This document is under GNU GPL v3

README on the bottom of document.

@font: from http://www.dafont.com/coders-crux.font
      more abuot license you can find in data/coders-crux/license.txt
'''

try:
    # Python 2
    xrange
except NameError:
    # Python 3, xrange is now named range
    xrange = range

import pygame
from pygame.locals import *

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()


def create_menu(choices, surface, menu_background_color=(0,0,0), background_color=(0,0,0)):
    menu = Menu()#necessary
    #menu.set_colors((255,255,255), (0,0,255), (0,0,0))#optional
    #menu.set_fontsize(64)#optional
    #menu.set_font('data/couree.fon')#optional
    #menu.move_menu(100, 99)#optional
    menu.init(choices, surface)#necessary
    menu.set_background_color(menu_background_color)
    if background_color != (0,0,0):
        menu.set_background(background_color)
    #menu.move_menu(0, 0)#optional
    menu.draw()#necessary
    return menu
    
class Menu:
    list = []
    fields = []
    font_size = 32
    font_path = 'menus/data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font
    surface = pygame.Surface
    number_field = 0
    color_background = (51,51,51)
    color_text =  (255, 255, 153)
    color_selection = (153,102,255)
    position_selection = 0
    position_wklejenia = (0,0)
    menu_width = 0
    menu_height = 0

    class Field:
        text = ''
        field = pygame.Surface
        field_rect = pygame.Rect
        selection_rect = pygame.Rect

    def move_menu(self, top, left):
        self.position_wklejenia = (top,left) 

    def set_colors(self, text, selection, background):
        self.color_background = background
        self.color_text =  text
        self.color_selection = selection

    def set_background(self, background):
        self.surface.fill(background)

    def set_background_color(self, background):
        self.color_background = background

    def set_text_color(self, color):
        self.color_text = color

    def set_selection_color(self, color):
        self.color_selection = color
        
    def set_fontsize(self,font_size):
        self.font_size = font_size
        
    def set_font(self, path):
        self.font_path = path
        
    def get_position(self):
        return self.position_selection
    
    def init(self, list, dest_surface):
        self.list = list
        self.surface = dest_surface
        self.number_field = len(self.list)
        self.create_structure()        
        
    def draw(self,move=0):
        if move:
            self.position_selection += move 
            if self.position_selection == -1:
                self.position_selection = self.number_field - 1
            self.position_selection %= self.number_field
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.color_background)
        selection_rect = self.fields[self.position_selection].selection_rect
        pygame.draw.rect(menu,self.color_selection,selection_rect)

        for i in xrange(self.number_field):
            menu.blit(self.fields[i].field,self.fields[i].field_rect)
        self.surface.blit(menu,self.position_wklejenia)
        return self.position_selection

    def create_structure(self):
        moveiecie = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.font_size)
        for i in xrange(self.number_field):
            self.fields.append(self.Field())
            self.fields[i].text = self.list[i]
            self.fields[i].field = self.font.render(self.fields[i].text, 1, self.color_text)

            self.fields[i].field_rect = self.fields[i].field.get_rect()
            moveiecie = int(self.font_size * 0.2)

            height = self.fields[i].field_rect.height
            self.fields[i].field_rect.left = moveiecie
            self.fields[i].field_rect.top = moveiecie+(moveiecie*2+height)*i

            width = self.fields[i].field_rect.width+moveiecie*2
            height = self.fields[i].field_rect.height+moveiecie*2            
            left = self.fields[i].field_rect.left-moveiecie
            top = self.fields[i].field_rect.top-moveiecie

            self.fields[i].selection_rect = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = self.surface.get_rect().centerx - self.menu_width / 2
        y = self.surface.get_rect().centery - self.menu_height / 2
        mx, my = self.position_wklejenia
        self.position_wklejenia = (x+mx, y+my) 


"""if __name__ == "__main__":
    surface = pygame.display.set_mode((854,480)) #0,6671875 and 0,(6) of HD resoultion
    surface.fill((51,51,51))
    '''First you have to make an object of a *Menu class.
    *init take 2 arguments. List of fields and destination surface.
    Then you have a 4 configuration options:
    *set_colors will set colors of menu (text, selection, background)
    *set_fontsize will set size of font.
    *set_font take a path to font you choose.
    *move_menu is quite interseting. It is only option which you can use before 
    and after *init statement. When you use it before you will move menu from 
    center of your surface. When you use it after it will set constant coordinates. 
    Uncomment every one and check what is result!
    *draw will blit menu on the surface. Be carefull better set only -1 and 1 
    arguments to move selection or nothing. This function will return actual 
    position of selection.
    *get_postion will return actual position of seletion. '''"""
        