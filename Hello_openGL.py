from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


def draw_points(x, y):
    '''
    glPointSize(5) #pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glVertex2f(x,y) #jekhane show korbe pixel
    glEnd()

    glPointSize(20)  # pixel size. by default 1 thake
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    glVertex(400, y)
    glEnd()

    glLineWidth(5)  # pixel size. by default 1 thake
    glBegin(GL_LINES)
    glVertex2f(x,y)  # jekhane show korbe pixel
    glColor3f(1.0,0.0,1.0)
    glVertex2f(200,250)
    glEnd()'''

    glLineWidth(15)  # pixel size. by default 1 thake
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)  # jekhane show korbe pixel
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(450, 250)
    glVertex2f(350,450)

    glEnd()

    '''glLineWidth(5)  # pixel size. by default 1 thake
    glBegin(GL_QUADS)
    glVertex2f(x, y)  # jekhane show korbe pixel
    glColor3f(1.0, 0.0, 1.0)
    glVertex2f(450, 250)
    glVertex2f(450, 350)
    glVertex2f(250, 400)
    glEnd()'''
    glLineWidth(5)  # pixel size. by default 1 thake
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, y)  # jekhane show korbe pixel
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(450, 250)
    glVertex2f(350, 450)

    glEnd()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    glColor3f(1.0, 1.0, 0.0) #konokichur color set (RGB)
    #call the draw methods here
    draw_points(250, 250)
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(showScreen)

glutMainLoop()