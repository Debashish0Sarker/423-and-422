from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Shooter properties
shooter_x = WIDTH // 2
shooter_y = 50

# Game state
projectiles = []
falling_circles = []
circles_on_ground = 0
circles_hit = 0
freeze = False
game_over = False
paused = False

# Function to draw a line using the Midpoint Line Algorithm
def midpoint_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = convert(zone, x1, y1)
    x2, y2 = convert(zone, x2, y2)
    draw_line(zone, x1, y1, x2, y2)

# Function to draw the shooter (spaceship)
def draw_shooter():
    global shooter_x, shooter_y

    # Draw the body of the shooter using lines
    midpoint_line(shooter_x - 20, shooter_y, shooter_x + 20, shooter_y)  # Bottom part (horizontal)
    midpoint_line(shooter_x - 20, shooter_y, shooter_x - 10, shooter_y + 30)  # Left side diagonal
    midpoint_line(shooter_x + 20, shooter_y, shooter_x + 10, shooter_y + 30)  # Right side diagonal
    midpoint_line(shooter_x - 10, shooter_y + 30, shooter_x + 10, shooter_y + 30)  # Connecting the left and right sides (horizontal)
    midpoint_line(shooter_x - 10, shooter_y + 30, shooter_x, shooter_y + 50)  # Left bottom triangle line
    midpoint_line(shooter_x + 10, shooter_y + 30, shooter_x, shooter_y + 50)  # Right bottom triangle line

# Function to draw projectiles
def draw_projectiles():
    glBegin(GL_LINES)
    for proj in projectiles:
        glVertex2f(proj['x'], proj['y'])
        glVertex2f(proj['x'], proj['y'] + 20)
    glEnd()

# Function to draw falling circles
def draw_falling_circles():
    glColor3f(1.0, 1.0, 0.0)  # Set the falling circles color to yellow
    for circle in falling_circles:
        midpoint_circle(circle['x'], circle['y'], circle['r'])

# Function to draw a circle using the Midpoint Circle Drawing algorithm
def midpoint_circle(x0, y0, r):
    x = 0
    y = r
    d = 1 - r
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
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
    glEnd()

# Function to find the drawing zone for the line
def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = -1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx <= 0 and dy >= 0:
            zone = 3
        elif dx <= 0 and dy <= 0:
            zone = 4
        elif dx >= 0 and dy <= 0:
            zone = 7
    elif abs(dx) < abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx <= 0 and dy >= 0:
            zone = 2
        elif dx <= 0 and dy <= 0:
            zone = 5
        elif dx >= 0 and dy <= 0:
            zone = 6

    return zone

# Function to convert coordinates based on the zone
def convert(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y

# Function to convert original coordinates after drawing the line
def convert_original(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

# Function to draw a line based on the zone and coordinates
def draw_line(zone, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    inc_e = 2 * dy
    inc_ne = 2 * (dy - dx)
    y = y1
    x = x1
    while x < x2:
        og_x, og_y = convert_original(zone, x, y)
        draw_points(og_x, og_y)
        if d > 0:
            d = d + inc_ne
            y += 1
        else:
            d = d + inc_e
        x += 1

# Function to draw points (for the line)
def draw_points(x, y):
    glColor3f(1.0, 1.0, 1.0)  # Set color to white
    glVertex2f(x, y)

# Game update logic
def update(value):
    global projectiles, falling_circles, circles_on_ground, game_over

    if game_over or paused:
        glutTimerFunc(16, update, value + 1)
        return

    for proj in projectiles:
        proj['y'] += 5
    projectiles = [p for p in projectiles if p['y'] < HEIGHT]

    for circle in falling_circles:
        circle['y'] -= circle['speed']  # Move falling circles according to their speed
        if circle['y'] - circle['r'] <= 0:
            falling_circles.remove(circle)
            circles_on_ground += 1
            if circles_on_ground >= 3:
                game_over = True

    if value % 80 == 0:
        spawn_circle()

    glutPostRedisplay()
    glutTimerFunc(16, update, value + 1)

# Function to spawn a new falling circle with a speed parameter
def spawn_circle():
    new_circle = {
        'x': random.randint(20, WIDTH - 20),
        'y': HEIGHT,
        'r': random.randint(10, 30),
        'speed': random.randint(1, 2)  # Random speed for each falling circle
    }
    falling_circles.append(new_circle)

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the shooter, projectiles, and falling circles
    draw_shooter()
    draw_projectiles()
    draw_falling_circles()

    glutSwapBuffers()

# Keyboard function
def keyboard(key, x, y):
    global shooter_x, paused
    if not paused:  # Allow movement only if the game is not paused
        if key == b'a':
            shooter_x = max(20, shooter_x - 20)
        elif key == b'd':
            shooter_x = min(WIDTH - 20, shooter_x + 20)
        elif key == b' ':
            projectiles.append({'x': shooter_x, 'y': shooter_y + 20})

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)

# Initialize and run the game
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Space Shooter Game")
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, update, 0)
    glutMainLoop()

main()
