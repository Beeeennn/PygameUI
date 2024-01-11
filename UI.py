from distutils.util import split_quoted
from posixpath import split
from time import sleep
import pygame
import threading
import Utilities as U
class Button():
    def __init__(self,x,y,image,image_hover,scale,screen):
        self.sheight = screen.get_height()
        self.swidth = screen.get_width()
        self.domsc = min(self.sheight,self.swidth)
        self.width  = image.get_width()
        self.height = image.get_height()
        self.image_hover = pygame.transform.scale(image_hover, (int(self.width*scale*self.domsc/100000),int(self.height*scale*self.domsc/100000)))
        self.image = pygame.transform.scale(image, (int(self.width*scale*self.domsc/100000),int(self.height*scale*self.domsc/100000)))
        self.width = self.image.get_width()
        self.height=self.image.get_height()
        self.rect  = self.image.get_rect()
        self.rect.topleft = (((x*self.swidth/1000)-(self.width/2)),((y*self.sheight/1000)-(self.height/2)))
        self.clicked = False

    def draw(self,surface):
        image = self.image
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            image=self.image_hover
            if pygame.mouse.get_pressed()[0] == 1:
                if self.clicked == False:
                    self.clicked = True
                    action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(image,(self.rect.x,self.rect.y)) #-(self.width/2))*self.swidth/1000
        return action




class Textbox:
    def __init__(self,font,font_size,empty_text,x,y,width,height,active_colour,passive_colour,active_text,inactive_text,buffer,hidden,screen):
        self.swidth = screen.get_width()
        self.sheight = screen.get_height()
        self.base_font = pygame.font.Font(font,font_size*self.sheight//1000)
        self.default = empty_text
        self.rect=pygame.Rect((x-(width/2))*self.swidth/1000,(y-(height/2))*self.sheight/1000,width*self.swidth/1000,height*self.sheight/1000)
        self.end_buffer = pygame.Rect(((x+width-buffer)-(width/2))*self.swidth/1000,(y-(height/2))*self.sheight/1000,buffer,height*self.sheight/1000)
        self.active_colour = active_colour
        self.passive_colour = passive_colour
        self.usertext = ""
        self.active = False
        self.active_text = active_text
        self.inactive_text = inactive_text
        self.hidden = hidden

        self.cursor = pygame.Rect((self.rect.topright),(3,self.rect.height-10))
        self.cursorposition = 0
        self.cursorshow = True
        self.thread_running = False

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.usertext = self.usertext[:(max(0,self.cursorposition-1))] + self.usertext[self.cursorposition:]
                    self.cursorposition=max(0,self.cursorposition-1)
                elif event.key == pygame.K_DELETE:
                    self.usertext = self.usertext[:self.cursorposition] + self.usertext[(min(len(self.usertext),self.cursorposition+1)):]
                elif event.key == pygame.K_LEFT:
                    self.cursorposition=max(0,self.cursorposition-1)
                elif event.key == pygame.K_RIGHT:
                    self.cursorposition=min(len(self.usertext),self.cursorposition+1)
                else:
                    self.usertext = (self.usertext[:self.cursorposition] + event.unicode + self.usertext[self.cursorposition:])
                    self.cursorposition=min(len(self.usertext),self.cursorposition+1)
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]==1:
            if self.rect.collidepoint(pos):
                self.active = True
            else:
                self.active = False
            self.cursorposition = len(self.usertext)
    def draw(self,screen):
        if self.active:
            cursorflicker = threading.Thread(target=self.cursorflicker,args=(0.5,))
            if not self.thread_running:
                cursorflicker.start()
            colour = self.active_colour
            text_colour = (self.active_text)
            if self.hidden:
                active_text = ""
                for i in range(len(self.usertext)):
                    active_text+="*"
            else:
                active_text = self.usertext
        else:
            colour=self.passive_colour
            text_colour = (self.inactive_text)
            if self.usertext == "":
                active_text = self.default
            else:
                if self.hidden:
                    active_text = ""
                    for i in range(len(self.usertext)):
                        active_text+="*"
                else:
                    active_text = self.usertext
        text_surfacel = self.base_font.render(active_text[:self.cursorposition],True,text_colour)
        text_surface2 = self.base_font.render(active_text[self.cursorposition:],True,text_colour)
        pygame.draw.rect(screen,colour,(self.rect))
        screen.blit(text_surfacel,(self.rect.x+5,self.rect.y+5))
        split = text_surfacel.get_rect(topleft = (self.rect.x+3,self.rect.y+10))
        self.cursor.midleft = split.midright
        screen.blit(text_surface2,(split.right+2,self.rect.y+5))
        if self.cursorshow and self.active:
            pygame.draw.rect(screen,self.active_text,(self.cursor))
        pygame.draw.rect(screen,colour,(self.end_buffer))
    
    def cursorflicker(self,secs):
        self.thread_running = True
        while self.active:
            sleep(secs)
            self.cursorshow = False
            sleep(secs)
            self.cursorshow = True
        self.thread_running = False

    def get_text(self):
        text=""+str(self.usertext)
        return text
    
    def clear(self):
        self.usertext = ""
        self.cursorposition = 0

class image():
    def __init__(self,x,y,image,scale,scaley,screen):
        self.sheight = screen.get_height()
        self.swidth = screen.get_width()
        self.width = image.get_width()
        self.height = image.get_height()
        self.domscale = min(self.sheight,self.swidth)
        if scaley == 0:
            self.image = pygame.transform.scale(image,(int(self.width*scale*self.domscale/100000),int(self.height*scale*self.domscale/100000)))
        else:
            self.image = pygame.transform.scale(image,(int(self.swidth*scale/1000),int(self.sheight*scaley/1000)))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.topleft = (((x*self.swidth/1000)-(self.width/2)),((y*self.sheight/1000)-(self.height/2)))
    def draw(self,screen):
        screen.blit(self.image,(self.rect.x, self.rect.y))

class background:
    def __init__(self,image,screen):
        self.image = pygame.transform.scale(image,(screen.get_width(),screen.get_height()))
    def draw(self,screen):
        screen.blit(self.image,(0,0))

class Flash:
    def __init__(self,x,y,font,size,colour,screen):
        self.swidth = screen.get_width()
        self.sheight = screen.get_height()
        self.base_font = pygame.font.Font(font,size*self.sheight//1000)
        self.colour = colour
        self.x = x*self.swidth/1000
        self.y = y*self.sheight/1000
        self.time = 0
        self.shown = False
    def draw(self,screen):
        if self.shown:
            text_surface = self.base_font.render(self.text,True,self.colour)
            screen.blit(text_surface,(self.x,self.y))

    def show(self,text,time):
        self.text = text
        flashthread = threading.Thread(target= self.flashtime, args=(time,))
        flashthread.start()
    def settime(self,shown):
        self.shown = shown
    def flashtime(self,secs):
        self.shown = True
        sleep(int(secs))
        self.shown = False
 
class Text:
    def __init__(self,x,y,font,size,colour,mid,screen):
        self.mid = mid
        self.swidth = screen.get_width()
        self.sheight = screen.get_height()
        self.base_font = pygame.font.Font(font,size*self.sheight//1000)
        self.colour = colour
        self.x = x*self.swidth/1000
        self.y = y*self.sheight/1000
        self.time = 0
        self.shown = False
    def draw(self,text,screen):
        text_surface = self.base_font.render(text,True,self.colour)
        if self.mid:
            width = text_surface.get_width()
            screen.blit(text_surface,(self.x-(width/2),self.y))
        else:
            screen.blit(text_surface,(self.x,self.y))    

class ScrollingTextbox:
    def __init__(self,font,font_size,empty_text,x,y,width,height,active_colour,passive_colour,active_text,inactive_text,buffer,hidden,back_col,screen):
        self.swidth = screen.get_width()
        self.sheight = screen.get_height()
        self.height = height
        self.base_font = pygame.font.Font(font,font_size*self.sheight//1000)
        self.default = empty_text
        self.rect=pygame.Rect((x-(width/2))*self.swidth/1000,(y-(height/2))*self.sheight/1000,width*self.swidth/1000,height*self.sheight/1000)
        self.outrect=pygame.Rect(((x-(width/2))*self.swidth/1000)-(self.base_font.get_height()),((y-(height/2))*self.sheight/1000)-(self.base_font.get_height()),(width*self.swidth/1000)+(2*self.base_font.get_height()),(height*self.sheight/1000)+(2*self.base_font.get_height()))
        self.active_colour = active_colour
        self.passive_colour = passive_colour
        self.active = False
        self.active_text = active_text
        self.inactive_text = inactive_text
        self.hidden = hidden
        self.back_col = back_col

        self.words = [""]
        self.lines = [""]
        self.lineno = 0
        self.cursorline = 0

        self.scrolled = 0

        self.cursor = pygame.Rect((self.rect.topright),(3,1.2*self.base_font.get_height()))
        self.cursorposition = 0
        self.cursorshow = True
        self.thread_running = False

    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.lines[self.cursorline] = self.lines[self.cursorline][:(max(0,self.cursorposition-1))] + self.lines[self.cursorline][self.cursorposition:]
                    self.cursorposition=self.cursorposition-1
                    if self.cursorposition<0 and self.cursorline>0:
                        self.cursorline-=1
                        self.cursorposition = len(self.lines[self.cursorline])
                    if self.cursorposition<0:
                        self.cursorposition = 0
                elif event.key == pygame.K_DELETE:
                    self.lines[self.cursorline] = self.lines[self.cursorline][:self.cursorposition] + self.lines[self.cursorline][(min(len(self.lines[self.cursorline]),self.cursorposition+1)):]
                elif event.key == pygame.K_LEFT:
                    self.cursorposition=self.cursorposition-1
                    if self.cursorposition<0 and self.cursorline>0:
                        self.cursorline-=1
                        self.cursorposition = len(self.lines[self.cursorline])
                    if self.cursorposition <0:
                        self.cursorposition = 0
                elif event.key == pygame.K_RIGHT:
                    self.cursorposition=self.cursorposition+1
                    if self.cursorposition > len(self.lines[self.cursorline]):
                        self.cursorposition = len(self.lines[self.cursorline])
                    if self.cursorposition>=len(self.lines[self.cursorline]) and self.cursorline<len(self.lines)-1:
                        if self.lines[self.cursorline+1] !="":
                            self.cursorline += 1
                            self.cursorposition = 0
                #up is -, down is +
                elif event.key == pygame.K_UP:
                    if self.cursorline > 0:
                        self.cursorline-=1
                        self.cursorposition = min(self.cursorposition,len(self.lines[self.cursorline]))
                elif event.key == pygame.K_DOWN:
                    if self.cursorline < len(self.lines)-1:
                        if self.lines[self.cursorline+1] !="":
                            self.cursorline+=1
                            self.cursorposition = min(self.cursorposition,len(self.lines[self.cursorline]))
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    try:
                        self.lines[self.cursorline] = (self.lines[self.cursorline][:self.cursorposition] + event.unicode + self.lines[self.cursorline][self.cursorposition:])
                        self.cursorposition=min(len(self.lines[self.cursorline]),self.cursorposition+1)
                    except:
                        pass
                for pos in range(len(self.lines)):
                    try:
                        end_surface = self.base_font.render(self.lines[pos],True,self.active_text)
                        end = end_surface.get_rect(topleft = (self.rect.x+3,self.rect.y+10))
                    except:
                        pass
                    if len(self.lines) >= pos+2:
                        if len(self.lines[pos+1])>0:
                            end_surface1 = self.base_font.render(self.lines[pos]+self.lines[pos+1][0],True,self.active_text)
                            end1 = end_surface1.get_rect(topleft = (self.rect.x+3,self.rect.y+10))
                            if end1.right < self.rect.right:
                                firstchar = self.lines[pos+1][0]
                                self.lines[pos] = self.lines[pos] + firstchar
                                self.lines[pos+1] = self.lines[pos+1][1:]
                                if self.lines[len(self.lines)-1] == "":
                                    self.lines = self.lines[:-1]
                    if end.right > self.rect.right:
                        if pos+1 <= len(self.lines):
                            if self.lines[len(self.lines)-1] != "":
                                self.lines = self.lines+[""]
                        lastchar = self.lines[pos][-1:]
                        self.lines[pos] = self.lines[pos][:-1]
                        self.lines[pos+1] = lastchar + self.lines[pos+1]
                        if self.cursorposition >= len(self.lines[self.cursorline]):
                            self.cursorposition = 1
                            self.cursorline+=1
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]==1:
            if self.rect.collidepoint(pos):
                self.active = True
            else:
                self.active = False
            try:
                self.cursorposition = len(self.lines[self.cursorline])
            except:
                pass
       
    def draw(self,screen):
        if self.active:
            cursorflicker = threading.Thread(target=self.cursorflicker,args=(0.5,))
            if not self.thread_running:
                cursorflicker.start()
            colour = self.active_colour
            text_colour = (self.active_text)
        else:
            colour=self.passive_colour
            text_colour = (self.inactive_text)
        pygame.draw.rect(screen,colour,(self.rect))
        if self.lines != [""] or self.active:
            y_offset = 0
            for pos in range(len(self.lines)):
                if pos != self.cursorline:
                    line_surface = self.base_font.render(self.lines[pos],True,text_colour)
                    line = line_surface.get_rect(topleft = (self.rect.x+3,self.rect.y+10+y_offset+self.scrolled))
                    linetop = line.top
                    linbot = line.bottom
                    if linetop < self.rect.bottom and linbot >self.rect.top:
                        screen.blit(line_surface,(self.rect.x+3,self.rect.y+10+y_offset+self.scrolled))
                else:
                    text_surfacel = self.base_font.render(self.lines[pos][:self.cursorposition],True,text_colour)
                    text_surface2 = self.base_font.render(self.lines[pos][self.cursorposition:],True,text_colour)
                    screen.blit(text_surfacel,(self.rect.x+3,self.rect.y+10+y_offset+self.scrolled))
                    split = text_surfacel.get_rect(topleft = (self.rect.x+3,self.rect.y+10+y_offset+self.scrolled))
                    self.cursor.bottomleft = split.bottomright
                    screen.blit(text_surface2,(split.right+2,self.rect.y+10+y_offset+self.scrolled))
                    if self.cursorshow and self.active:
                        pygame.draw.rect(screen,self.active_text,(self.cursor))
                y_offset+=self.base_font.get_height()
            if self.cursor.bottom>=self.rect.bottom:
                self.scrolled-=self.base_font.get_height()
            if self.cursor.top <= self.rect.top:
                self.scrolled+=self.base_font.get_height()
        else:
            text_surface = self.base_font.render(self.default,True,text_colour)
            screen.blit(text_surface,(self.rect.x+5,self.rect.y+5))
        pygame.draw.rect(screen,self.back_col,(self.outrect),self.base_font.get_height())
    def cursorflicker(self,secs):
        self.thread_running = True
        while self.active:
            sleep(secs)
            self.cursorshow = False
            sleep(secs)
            self.cursorshow = True
        self.thread_running = False
    def clear_text(self):
        self.lines=[""]
        self.cursorline = 0
        self.cursorposition = 0
    def get_text(self,user):
        text = ""
        for line in self.lines:
            text += line
        text+= " "
        text = (f"{user.nickname}: {text}")
        return text
        
class Button():
    # Initialize button with toggle, position, images for different states, scale, selection state, and screen
    def __init__(self, x, y, image, image_hover, image_selected, scale, selected, screen):
        # Screen dimensions and scaling factors
        self.sheight = screen.get_height()
        self.swidth = screen.get_width()
        self.domsc = min(self.sheight, self.swidth)

        # Scale images for button states
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale * self.domsc / 100000), int(self.height * scale * self.domsc / 100000)))
        self.image_hover = pygame.transform.scale(image_hover, (int(self.width * scale * self.domsc / 100000), int(self.height * scale * self.domsc / 100000)))
        self.image_select = pygame.transform.scale(image_selected, (int(self.width * scale * self.domsc / 100000), int(self.height * scale * self.domsc / 100000)))

        # Adjust size and position
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.topleft = (((x * self.swidth / 1000) - (self.width / 2)), ((y * self.sheight / 1000) - (self.height / 2)))

        # Button state variables
        self.clicked = False
        self.selected = selected

    # Draw button on screen and handle click events
    def draw(self, surface):
        image = self.image
        action = False
        pos = pygame.mouse.get_pos()

        # Change image on hover and handle click
        if self.rect.collidepoint(pos):
            image = self.image_hover
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
                self.selected = True

        # Change image if button is selected
        if self.selected:
            image = self.image_select

        # Reset click state when mouse button is released
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button image
        surface.blit(image, (self.rect.x, self.rect.y))
        return action

    # Deselect the button
    def deselect(self):
        self.selected = False

class FileDisplay:
    # FileDisplay class for showing file content or messages
    def __init__(self, font, font_size, x, y, width, height, text_col, back_col, text, screen):
        # Initialize file display properties
        self.swidth = screen.get_width()
        self.sheight = screen.get_height()
        self.height = height
        self.width = width
        self.base_font = pygame.font.Font(font,font_size*self.sheight//1000)
        self.rect=pygame.Rect((x-(width/2))*self.swidth/1000,(y-(height/2))*self.sheight/1000,width*self.swidth/1000,height*self.sheight/1000)
        self.outrect=pygame.Rect(((x-(width/2))*self.swidth/1000)-(self.base_font.get_height()),((y-(height/2))*self.sheight/1000)-(self.base_font.get_height()),(width*self.swidth/1000)+(2*self.base_font.get_height()),(height*self.sheight/1000)+(2*self.base_font.get_height()))
        self.width = self.rect.width
        self.active = False
        self.back_col = back_col
        self.text_col = text_col
        self.y_offset = 0
        self.running = True
        
        self.lines = []
        self.split_text(text)
        self.scrolled = len(self.lines)#-4

    # Handle keyboard and mouse events for scrolling
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            # Scroll up or down
            if event.key == pygame.K_UP and self.scrolled > 0:
                self.y_offset += self.base_font.get_height()
                self.scrolled -= 1
            elif event.key == pygame.K_DOWN and self.scrolled < len(self.lines) - 3:
                self.y_offset -= self.base_font.get_height()
                self.scrolled += 1

        # Activate or deactivate on mouse click
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1:
            self.active = self.rect.collidepoint(pos)

    # Split input text into lines for display
    def split_text(self, text):
        self.lines = []
        words = text.split()
        while words:
            line_words = []
            while words:
                line_words.append(words.pop(0))
                fw, fh = self.base_font.size(' '.join(line_words + words[:1]))
                if fw > self.width:
                    break
            line = ' '.join(line_words)
            self.lines.append(line)

    # Draw the file content or message
    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),self.rect)
        fw,fh = self.base_font.size("line")
        y_off = 0 #(max(0,((len(self.lines)-4)*fh)))*-1
        for line in self.lines:
            ty = self.rect.y + self.y_offset + y_off + 10
            tx = self.rect.x + 3
            font_surface = self.base_font.render(line,True,self.text_col)
            line = font_surface.get_rect(topleft = (tx,ty))
            linetop = line.top
            linebot = line.bottom
            if linebot < self.rect.bottom and linetop > self.rect.top - 5:
                screen.blit(font_surface,(tx,ty))
            y_off+=fh


class slider():
    def __init__(self,slidercolour1,slidercolour2,xpos,ypos,title,min,max,startpos,width,toggleheight,togglewidth):
        self.title = title
        self.xpos = xpos
        self.ypos = ypos
        self.slidercolour2 = slidercolour2
        self.slidercolour1 = slidercolour1
        self.max = max
        self.min = min
        self.sliderpos = startpos
        self.width = width
        self.togheight = toggleheight
        self.togglewidth = togglewidth
        self.sliderrect = pygame.Rect(0,0,0,0)
        self.togglerect = pygame.Rect(0,0,0,0)
        self.selected = False
        self.otherselected = False

        self.sliderrect = pygame.Rect(0,0,0,0)
        self.togglerect = pygame.Rect(0,0,0,0)
    def draw_slider(self,screen):

        sheight = screen.get_height()
        swidth = screen.get_width()
        width = swidth*self.width/1000
        xpos = (swidth*self.xpos/1000)-width/2
        ypos = sheight*self.ypos/1000

        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1:
            if self.togglerect.collidepoint(pos):
                if not self.otherselected:
                    self.selected = True
            else:
                self.otherselected = True
        else:
            self.selected = False
            self.otherselected = False

        if self.selected:

            spacing = width/(self.max-self.min)

            self.sliderpos = ((pos[0]-xpos)/spacing)+self.min
            self.sliderpos = round(self.sliderpos)
            self.sliderpos = min(max(self.min,self.sliderpos),self.max)

        toggleheight = self.togheight*sheight/1000
        togglewidth = self.togglewidth*swidth/1000
        toggleposx = ((self.sliderpos-self.min)*width/(self.max-self.min))+xpos-(togglewidth/2)
        toggleposy = ypos - ((toggleheight/2) - 2)

        font = pygame.font.Font(None,int(toggleheight))
        toptext = (self.title + " - " + str(self.sliderpos))
        text_surface1 = font.render(toptext,True,self.slidercolour2)
        text_surface2 = font.render(self.title,True,self.slidercolour2)
        titlewidth = text_surface2.get_width()
        titleheight = text_surface1.get_height()
        screen.blit(text_surface1, ((xpos+(width/2)-(titlewidth/2)), (self.togglerect.top-(2+titleheight))))

        self.sliderrect = pygame.Rect(xpos,ypos,width,4)
        self.togglerect = pygame.Rect(toggleposx,toggleposy,togglewidth,toggleheight)
        
        pygame.draw.rect(screen,self.slidercolour1, self.sliderrect)
        pygame.draw.rect(screen,self.slidercolour2, self.togglerect)

        return self.sliderpos
