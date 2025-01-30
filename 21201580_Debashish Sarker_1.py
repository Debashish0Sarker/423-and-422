'''#task1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
# Window
W_Width,W_Height =500, 500
raindrops=[]
rain_speed=2
rain_dir=0
back_color=[0.0, 0.0, 0.0]  # night
day_color=[1,1,1]

def init_raindrops(count=200):
    global raindrops
    raindrops=[]
    for i in range(count):
        raindrop={'x':random.randint(-W_Width//2,W_Width//2),'y':random.randint(-W_Height//2, W_Height//2),'z':0}
        raindrops.append(raindrop)
#each raindrop
def update_raindrops():
    for j in raindrops:
        j['x']+=rain_dir
        j['y']-=rain_speed
        if j['y']<-W_Height//2:
            reset(j)
#moves off screen
def reset(drop):
    drop['x']=random.randint(-W_Width//2, W_Width//2)
    drop['y']=random.randint(-W_Height//2, W_Height//2)

def draw_house():
    glBegin(GL_TRIANGLES)
    glColor3f(0.5,0.4,0.3)  # Roof
    glVertex2f(-100, 0)
    glVertex2f(100, 0)
    glVertex2f(0, 150)
    glEnd()

    glBegin(GL_LINES)
    # Walls
    glVertex2f(-100, 0)
    glVertex2f(-100, -150)
    glVertex2f(100, 0)
    glVertex2f(100, -150)
    glVertex2f(-100, -150)
    glVertex2f(100, -150)
    glEnd()

    # Door
    glBegin(GL_LINES)
    glVertex2f(-30, -150)
    glVertex2f(-30, -50)
    glVertex2f(30, -150)
    glVertex2f(30, -50)
    glVertex2f(-30, -50)
    glVertex2f(30, -50)
    glEnd()

def draw_raindrops():
    glColor3f(0,0.5,0.9)
    for j in raindrops:
        glBegin(GL_LINES)
        glVertex2f(j['x'],j['y'])
        glVertex2f(j['x'],j['y']-10)
        glEnd()

def keyboard_listener(key, x, y):
    global rain_dir, rain_speed,back_color
    if key==GLUT_KEY_LEFT:
        rain_dir -= 1
    elif key==GLUT_KEY_RIGHT:
        rain_dir += 1
    elif key==GLUT_KEY_UP:
        rain_speed += 1
    elif key==GLUT_KEY_DOWN:
        rain_speed -= 1
    elif key==b'n':  # night
        back_color=[0.0, 0.0, 0.0]
    elif key==b'd':  #day
        back_color=day_color

# Display callback function
def display():
    global back_color
    global day_color
    glClearColor(*back_color, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0,250, 0, 0, 0, 0, 1, 0)
    draw_house()
    draw_raindrops()
    glutSwapBuffers()

def animate():
    update_raindrops()
    glutPostRedisplay()
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, W_Width / W_Height, 1, 1000.0)
glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(50, 50)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutCreateWindow(b"Task1")
init_raindrops()
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboard_listener)
glutSpecialFunc(keyboard_listener)
glutMainLoop()
'''
#task2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

W_WIDTH, W_HEIGHT = 500, 500
frozen = False
last_blink = 0
speed=1
points=[]
blinked=False
previous_speed =speed 

def create_points(x, y):
    directions=[(1, 1), (1, -1), (-1, 1), (-1, -1)]
    a, b=random.choice(directions) 
    color=[]
    for i in range(3):
        color.append(random.uniform(0, 1))
    size=random.uniform(3, 8) 
    points.append({'x': x,'y': y,'a': a,'b': b,'color':color,'size':size})

def update():
    if frozen==True:
        return None
    else:
        for i in range(len(points)):
            points[i]['x']+=points[i]['a']*speed
            points[i]['y']+=points[i]['b']*speed
            if points[i]['x']>=W_WIDTH//2 or points[i]['x']<= -W_WIDTH//2:
                points[i]['a']*= -1
            if points[i]['y']>= W_HEIGHT//2 or points[i]['y']<= -W_HEIGHT//2:
                points[i]['b']*= -1

'''def blink():
    global last_blink
    time1 = time.time()
    if time1 - last_blink > 1
        last_blink = time1
        return True
    else:
        return False'''


def blinking():
    global blinked
    if blinked==False:
        blinked=True
        for i in range(len(points)):
            points[i]['color']=[0, 0, 0]
    else:
        blinked=False
        for i in range(len(points)):
            points[i]['color']=[random.uniform(0, 1) for j in range(3)] 

def draw_points():
    for i in range(len(points)):
        glColor3f(*points[i]['color'])
        glPointSize(points[i]['size']) 
        glBegin(GL_POINTS)
        glVertex2f(points[i]['x'],points[i]['y'])
        glEnd()

def freeze():
    global frozen,previous_speed,speed
    if frozen==True:
        previous_speed=speed
        speed=0 
        frozen=False
    else:
        speed=previous_speed
        frozen=True

def mouse_listener(button,state,x,y):
    if frozen or state!= GLUT_DOWN:
        return False
    #mouse Coordiantes
    gl_x= x-W_WIDTH//2
    gl_y=W_HEIGHT//2-y

    if button == GLUT_RIGHT_BUTTON:
        create_points(gl_x, gl_y)
        return True
    elif button==GLUT_LEFT_BUTTON:
        blinking()
        return True
    else:
        return False # No valid input


def keyboard_listener(key, x, y):
    global speed, frozen
    if key==b' ' and frozen==False:
        frozen=True
        freeze()
    elif key == b' ' and frozen == True:
        frozen=False
        freeze()
    elif key==GLUT_KEY_UP:
        speed+=1
    elif key==GLUT_KEY_DOWN:
        speed-=1
    elif key==GLUT_KEY_RIGHT:  
        for i in range(len(points)):
            points[i]['size']+=1 
    elif key==GLUT_KEY_LEFT: 
        for i in range(len(points)):
            points[i]['size']-= 1 


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_points()
    glutSwapBuffers()
def animate():
    if not frozen:
        update()
    glutPostRedisplay()
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glPointSize(5)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-W_WIDTH//2, W_WIDTH//2,-W_HEIGHT//2, W_HEIGHT//2)
glutInit()
glutInitWindowSize(W_WIDTH, W_HEIGHT)
glutInitWindowPosition(50, 50)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutCreateWindow(b"Task2")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutMouseFunc(mouse_listener)
glutKeyboardFunc(keyboard_listener)
glutSpecialFunc(keyboard_listener)
glutMainLoop()