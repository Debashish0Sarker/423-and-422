from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
WIDTH=500
HEIGHT=500

shooter_x=WIDTH//2
shooter_y=50
shooter_width=20
shooter_height=60

bullets=[]
falling_circles=[]
circle_on_ground=0
hits=0
gameover=False
paused=False
pause_icon={'x':10,'y': HEIGHT-40,'width':20,'height':20}
restart_icon={'x':240,'y':HEIGHT-40,'width':20,'height':20}
cross_icon={'x':470,'y': HEIGHT - 40,'width':20,'height':20}



def midpoint_line(x1,y1,x2,y2):
    if x1>x2:
        x1,x2 =x2,x1
        y1,y2 =y2,y1
    zone = find_zone(x1,y1,x2,y2) 
    x1, y1 = convert(zone,x1,y1)  
    x2, y2 = convert(zone, x2, y2)  
    dx=x2-x1
    dy=y2-y1
    d=2*dy-dx  
    incE=2*dy 
    incNE=2*(dy - dx)
    x=x1
    y=y1
    while x<=x2:
        og_x,og_y=convert_back(zone, x, y)
        glVertex2f(og_x,og_y) 
        if d>0: 
            y+=1
            d+=incNE
        else: 
            d+=incE
        x+= 1
def midpoint_circle(x0, y0, r):
    x=0
    y=r
    d=1-r
    glBegin(GL_POINTS)
    while x <= y:
        glVertex2f(x0 + x, y0 + y)
        glVertex2f(x0 - x, y0 + y)
        glVertex2f(x0 + x, y0 - y)
        glVertex2f(x0 - x, y0 - y)
        glVertex2f(x0 + y, y0 + x)
        glVertex2f(x0 - y, y0 + x)
        glVertex2f(x0 + y, y0 - x)
        glVertex2f(x0 - y, y0 - x)
        x+=1
        if d<0:
            d+=2*x+1
        else:
            y-=1
            d+=2*(x - y) + 1
    glEnd()

def find_zone(x1,y1,x2,y2):
    dx=x2-x1
    dy=y2-y1
    if abs(dx)>abs(dy):
        if dx>0 and dy>0:
            return 0
        elif dx<0 and dy>0:
            return 3
        elif dx<0 and dy<0:
            return 4
        else:
            return 7
    else:
        if dx>0 and dy>0:
            return 1
        elif dx<0 and dy>0:
            return 2
        elif dx<0 and dy<0:
            return 5
        else:
            return 6

def convert(zone,x,y) :

    if (zone == 0) :
        return x,y
    elif (zone == 1) :
        return y,x
    elif (zone == 2) :
        return -y,x
    elif (zone == 3) :
        return -x,y
    elif (zone == 4) :
        return -x,-y
    elif (zone == 5) :
        return -y,-x
    elif (zone == 6) :
        return -y,x
    elif (zone == 7) :
        return x,-y

def convert_back(zone,x,y) :
    if (zone == 0) :
        return x,y
    elif (zone == 1) :
        return y,x
    elif (zone == 2) :
        return -y,-x
    elif (zone == 3) :
        return -x,y
    elif (zone == 4) :
        return -x,-y
    elif (zone == 5) :
        return -y,-x
    elif (zone == 6) :
        return y,-x
    elif (zone == 7) :
        return x,-y
   
def draw_shooter():
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POINTS)#square
    midpoint_line(shooter_x-shooter_width,shooter_y,shooter_x+shooter_width,shooter_y)  # Bottom
    midpoint_line(shooter_x+shooter_width,shooter_y,shooter_x+shooter_width,shooter_y+shooter_height)  # Right
    midpoint_line(shooter_x+shooter_width,shooter_y+shooter_height,shooter_x-shooter_width,shooter_y+shooter_height)  # Top
    midpoint_line(shooter_x-shooter_width,shooter_y+shooter_height,shooter_x-shooter_width,shooter_y)  # Left
    
    glEnd()
    glBegin(GL_POINTS)#triangle
    midpoint_line(shooter_x-shooter_width,shooter_y+shooter_height,shooter_x+shooter_width,shooter_y+shooter_height)
    midpoint_line(shooter_x+shooter_width,shooter_y+shooter_height,shooter_x,shooter_y+shooter_height+20)
    midpoint_line(shooter_x,shooter_y+shooter_height+20,shooter_x-shooter_width,shooter_y+shooter_height)
    glEnd()

def draw_bullets():
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 0.0)
    for b in bullets:
        glVertex2f(b['x'],b['y'])
        glVertex2f(b['x'],b['y']+20)

    '''glBegin(GL_POINTS) 
    for b in bullets:
        midpoint_line(b['x'], b['y'], b['x'], b['y'] + 20) 
    glEnd()'''
    glEnd()

def draw_falling_circles():
    glColor3f(1, 0, 0)
    for c in falling_circles:
        midpoint_circle(c['x'],c['y'],c['r'])

def check_collision():
    global bullets,falling_circles,hits,gameover
    for b in bullets:
        bullet_box={'x': b['x']-1,'y':b['y'],'width':2,'height': 20}
        for circle in falling_circles:
            circle_box = {'x': circle['x'] - circle['r'], 'y': circle['y'] - circle['r'], 'width': circle['r'] * 2, 'height': circle['r'] * 2}
            if hascollided(bullet_box, circle_box):
                bullets.remove(b)
                falling_circles.remove(circle)
                hits += 1
                break
    for circle in falling_circles:
        shooter_box = {'x': shooter_x-shooter_width, 'y': shooter_y, 'width': shooter_width * 2, 'height': shooter_height}
        circle_box = {'x': circle['x']-circle['r'], 'y':circle['y']-circle['r'],'width': circle['r']*2,'height': circle['r']*2}
        if hascollided(shooter_box, circle_box):
            gameover = True
            break
def hascollided(box1, box2):
    return (box1['x'] < box2['x'] + box2['width'] and
            box1['x'] + box1['width'] > box2['x'] and
            box1['y'] < box2['y'] + box2['height'] and
            box1['y'] + box1['height'] > box2['y'])

def spawn_circle():
    falling_circles.append({
        'x':random.randint(20, WIDTH - 20),
        'y':HEIGHT,
        'r':random.randint(10, 30),
        'speed':random.randint(1, 2)
    })

def update(value):
    global bullets, falling_circles, circle_on_ground, gameover
    if gameover or paused:
        glutTimerFunc(1, update, value + 1)
        return
    for b in bullets:
        b['y']+=5
        if b['y']>HEIGHT:
            bullets.remove(b)
    for c in falling_circles:
        c['y']-=c['speed']
        if c['y']-c['r'] <= 0:
            falling_circles.remove(c)
            circle_on_ground += 1
            if circle_on_ground == 3:
                gameover = True
    check_collision()
    if value%75==0:
        spawn_circle()
 
    glutPostRedisplay()
    glutTimerFunc(16, update, value + 1)
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_shooter()
    draw_bullets()
    draw_falling_circles()
    # Pause button
    glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex2f(pause_icon['x'],pause_icon['y'])
    glVertex2f(pause_icon['x']+pause_icon['width'], pause_icon['y'])
    glVertex2f(pause_icon['x']+pause_icon['width'], pause_icon['y'] + pause_icon['height'])
    glVertex2f(pause_icon['x'],pause_icon['y'] + pause_icon['height'])
    glEnd()
    # Restart button
    glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex2f(restart_icon['x'],restart_icon['y'])
    glVertex2f(restart_icon['x']+restart_icon['width'], restart_icon['y'])
    glVertex2f(restart_icon['x']+restart_icon['width'], restart_icon['y'] + restart_icon['height'])
    glVertex2f(restart_icon['x'],restart_icon['y'] + restart_icon['height'])
    glEnd()
    # Exit button
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(cross_icon['x'], cross_icon['y'])
    glVertex2f(cross_icon['x'] + cross_icon['width'], cross_icon['y'])
    glVertex2f(cross_icon['x'] + cross_icon['width'], cross_icon['y'] + cross_icon['height'])
    glVertex2f(cross_icon['x'], cross_icon['y'] + cross_icon['height'])
    glEnd()
    #print(f"Score: {hits}")
    glutSwapBuffers()

def keyboard(key, x, y):
    global shooter_x, paused
    if key==b'a' and not paused:
        shooter_x=max(shooter_width,shooter_x-20)
    elif key==b'd' and not paused:
        shooter_x=min(WIDTH - shooter_width, shooter_x + 20)
    elif key == b' ' and not paused:
        bullets.append({'x': shooter_x, 'y':shooter_y+shooter_height})

def mouse(button, state,x, y):
    global paused, gameover, circle_on_ground, hits, bullets, falling_circles
    y = HEIGHT - y 
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if pause_icon['x'] <= x <= pause_icon['x']+pause_icon['width'] and pause_icon['y'] <= y <= pause_icon['y'] + pause_icon['height']:
            paused = not paused 
        elif restart_icon['x'] <= x <= restart_icon['x'] + restart_icon['width'] and restart_icon['y'] <= y <= restart_icon['y'] + restart_icon['height']:
            gameover = False
            paused = False
            circle_on_ground = 0
            hits = 0
            bullets.clear()
            falling_circles.clear()
            print("Starting Over") 
        elif cross_icon['x'] <= x <= cross_icon['x'] + cross_icon['width'] and cross_icon['y'] <= y <= cross_icon['y'] + cross_icon['height']:
            print(f"Goodbye! Final Score: {hits}")
            glutLeaveMainLoop() 

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WIDTH, HEIGHT)
glutCreateWindow(b"Shooter Game")
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
init()
glutTimerFunc(0, update, 0)
glutMainLoop()
