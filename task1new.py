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