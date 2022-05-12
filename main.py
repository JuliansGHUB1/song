import pygame
import time

pygame.init()
screen = pygame.display.set_mode((1200, 1000))
color1 = 'Blue'
color = screen.fill(color1)
pygame.display.set_caption("Music Player")
time_array = [0]

musicList = ["Song1.ogg", "Song2.ogg", "Song3.ogg"]

timeList = []
global paused
paused = False
colorcount = 0

class Button(pygame.sprite.Sprite):
    def __init__(self, posx, posy, file1, file2):
        super().__init__()
        self.posx = posx
        self.posy = posy
        self.file1 = file1
        self.file2 = file2
        self.image = pygame.image.load(file1)
        self.rect = self.image.get_rect()
        self.rect.center = (posx, posy)
    def update(self, currently_paused):
        if currently_paused == False:
            self.image = pygame.image.load(self.file2)
            self.rect = self.image.get_rect()
            self.rect.center = (self.posx, self.posy)
            button_group.draw(screen)
            pygame.display.flip()

        else:
            self.image = pygame.image.load(self.file1)
            self.rect = self.image.get_rect()
            self.rect.center = (self.posx, self.posy)
            button_group.draw(screen)
            pygame.display.flip()



Button1 = Button(600,500, "Pause.png", "Play.png")

button_group = pygame.sprite.GroupSingle()
button_group.add(Button1)





def colorchange():
    global colorcount
    colorlist = ['Blue', 'Red', 'Purple', 'Green']
    color = screen.fill(colorlist[colorcount])
    colorcount = colorcount + 1
    if colorcount == len(colorlist) - 1:
        colorcount = 0



def checkquit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

def pause():
    global paused
    global seconds
    global sub
    print("pausd is", paused)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] == True and paused == False:
        print("runnning")
        seconds = 0
        sub = 0
        button_group.update(paused)
        paused = True
        pygame.mixer.music.pause()
#### you may ask: if we end up running this once(in the scenario where space is hit and pause = false), wouldn't
#### it be futile because the next iteration paused will be true?
#### NO! because even though pause is true, when paused() is called again, all that will happen is it will check
#### if condition 1(space = true and pause = false) is true, and since pause = True it is not true so this will not be run
#### it will check the second condition, and when it checks it will not run either because the player has not hit the up button yet
#### so it works really well bc we keep the sub variable at 0 until the point where paused = False again
    if keys[pygame.K_UP] == True and paused == True:
        print("running1")
        seconds = 1
        button_group.update(paused)
        paused = False
        pygame.mixer.music.unpause()




def timer(t):
    global seconds
    global subtractor
    seconds = 1
    while t > 0:
        start_time = time.time()
        mouseevent = pygame.mouse.get_pressed()
        pygame.display.update()
        keys = pygame.key.get_pressed()
        checkquit()
        ##time.sleep(seconds)
        print("start time is", start_time, "time.time() is", time.time())

        if mouseevent[0] == True:
            print("running mouseevent")
           ## time_array.append(time.time())
          ##  if time_array[-1] - time_array[-2] > 1:
            if time.time() - time_array[-1] > 0.5:
                print("a second has elapsed since last pause")
                t = 0
                time_array.append(time.time())
                print("the newest time at which we have pause has been added to the time array list")
                print("this list's purpose is to append the various times at which we skip songs so that we can")
                print("make sure that the time time a(current skip) - time x(previous skip) is greater than 1")
                print("this means one second has elapsed since the last skip, and this prevents multiple clicks in a short time")
                print("from resulting in a quick succession of skips")

        else:
            subtractor = time.time() - start_time
            pause()
            if paused == True:
                subtractor = sub

            t = t - subtractor
            print(t)

def getlistofsonglengths():
    for i in musicList:
        peek = pygame.mixer.Sound(i)
        print("length",(peek.get_length()))
        timeList.append((peek.get_length()))


songcounter = 0

def getTitle(a):
    title = ''
    for i in a:
        if i == '.':
            break
        else:
            title = title + i
    return(title)

def playMusic():
    getlistofsonglengths()
    pygame.display.update()
    global songcounter
    for i in musicList:
        colorchange()
        music = pygame.mixer.music.load(musicList[songcounter])
        pygame.mixer.music.play()
        pygame.display.set_caption(getTitle(musicList[songcounter]))
        timewaited = int(timeList[songcounter])
        timer(timewaited)
        songcounter = songcounter + 1
        print("Reach here", songcounter)

playMusic()