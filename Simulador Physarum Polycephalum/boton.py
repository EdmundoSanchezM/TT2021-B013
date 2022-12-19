import pygame, sys
global textoBoton
textoBoton=''
class Button:
    global textoBoton
    def __init__(self,text,width,height,pos,elevation,gui_font,screen):
	#Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.screen=screen
        self.gui_font=gui_font
	# top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#475F77'
	# bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
        #text
        self.text = text
        self.text_surf = gui_font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        
    def change_text(self, newtext):
        self.text_surf = self.gui_font.render(newtext, True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 
        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation
        pygame.draw.rect(self.screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(self.screen,self.top_color, self.top_rect,border_radius = 12)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_click()
    def check_click(self):
        global textoBoton
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                self.change_text(f"{self.text}")
            else:
                self.dynamic_elecation = self.elevation
            if self.pressed == True:
                #print(self.text)
                self.pressed = False
                self.change_text(self.text)
                textoBoton=self.text
                
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'
            
def setTexto():
    global textoBoton
    aux=textoBoton
    textoBoton=''
    return aux

def buttons_draw(buttons):
    for b in buttons:
        b.draw()