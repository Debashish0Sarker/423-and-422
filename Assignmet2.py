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
shooter_width = 20
shooter_height = 60

# Game state
projectiles = []
falling_circles = []
circles_on_ground = 0
circles_hit = 0
freeze = False
game_over = False
paused = False

# Icons coordinates
pause_icon = {'x': 10, 'y': HEIGHT - 40, 'width': 20, 'height': 20}
restart_icon = {'x': 40, 'y': HEIGHT - 40, 'width': 20, 'height': 20}
cross_icon = {'x': 70, 'y': HEIGHT - 40, 'width': 20, 'height': 20}

# Function to draw the shooter
def draw_shooter():
    glBegin(GL_QUADS)
    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(shooter_x - shooter_width // 2, shooter_y)
    glVertex2f(shooter_x + shooter_width // 2, shooter_y)
    glVertex2f(shooter_x + shooter_width // 2, shooter_y + shooter_height)
    glVertex2f(shooter_x - shooter_width // 2, shooter_y + shooter_height)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(shooter_x - shooter_width // 2, shooter_y + shooter_height)
    glVertex2f(shooter_x + shooter_width // 2, shooter_y + shooter_height)
    glVertex2f(shooter_x, shooter_y + shooter_height + 20)
    glEnd()

# Function to draw projectiles
def draw_projectiles():
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 0.0)
    for proj in projectiles:
        glVertex2f(proj['x'], proj['y'])
        glVertex2f(proj['x'], proj['y'] + 20)
    glEnd()

# Function to draw falling circles
def draw_falling_circles():
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

# Collision detection and handling
def check_collisions():
    global projectiles, falling_circles, circles_hit, game_over
    for proj in projectiles[:]:
        proj_box = {'x': proj['x'] - 1, 'y': proj['y'], 'width': 2, 'height': 20}
        for circle in falling_circles[:]:
            circle_box = {
                'x': circle['x'] - circle['r'],
                'y': circle['y'] - circle['r'],
                'width': circle['r'] * 2,
                'height': circle['r'] * 2
            }
            if hasCollided(proj_box, circle_box):
                falling_circles.remove(circle)
                projectiles.remove(proj)
                circles_hit += 1
                break

    for circle in falling_circles[:]:
        circle_box = {
            'x': circle['x'] - circle['r'],
            'y': circle['y'] - circle['r'],
            'width': circle['r'] * 2,
            'height': circle['r'] * 2
        }
        shooter_box = {
            'x': shooter_x - shooter_width // 2,
            'y': shooter_y,
            'width': shooter_width,
            'height': shooter_height
        }
        if hasCollided(shooter_box, circle_box):
            game_over = True
            break

# Function to check collision between two AABBs
def hasCollided(box1, box2):
    return (box1['x'] < box2['x'] + box2['width'] and
            box1['x'] + box1['width'] > box2['x'] and
            box1['y'] < box2['y'] + box2['height'] and
            box1['y'] + box1['height'] > box2['y'])

# Function to spawn a new falling circle
def spawn_circle():
    new_circle = {
        'x': random.randint(20, WIDTH - 20),
        'y': HEIGHT,
        'r': random.randint(10, 30),
        'speed': random.randint(1, 2)
    }
    falling_circles.append(new_circle)

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
        circle['y'] -= circle['speed']
        if circle['y'] - circle['r'] <= 0:
            falling_circles.remove(circle)
            circles_on_ground += 1
            if circles_on_ground >= 3:
                game_over = True

    check_collisions()

    if value % 80 == 0:
        spawn_circle()

    glutPostRedisplay()
    glutTimerFunc(16, update, value + 1)

# Display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw shooter, projectiles, and circles
    draw_shooter()
    draw_projectiles()
    draw_falling_circles()

    # Draw Pause button
    glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    glVertex2f(10, HEIGHT - 40)
    glVertex2f(30, HEIGHT - 40)
    glVertex2f(30, HEIGHT - 20)
    glVertex2f(10, HEIGHT - 20)
    glEnd()

    # Draw Restart button
    glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex2f(40, HEIGHT - 40)
    glVertex2f(60, HEIGHT - 40)
    glVertex2f(60, HEIGHT - 20)
    glVertex2f(40, HEIGHT - 20)
    glEnd()

    # Draw Exit button
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(70, HEIGHT - 40)
    glVertex2f(90, HEIGHT - 40)
    glVertex2f(90, HEIGHT - 20)
    glVertex2f(70, HEIGHT - 20)
    glEnd()

    glutSwapBuffers()

# Keyboard function
def keyboard(key, x, y):
    global shooter_x, paused
    if not paused:
        if key == b'a':
            shooter_x = max(shooter_width // 2, shooter_x - 20)
        elif key == b'd':
            shooter_x = min(WIDTH - shooter_width // 2, shooter_x + 20)
        elif key == b' ':
            projectiles.append({'x': shooter_x, 'y': shooter_y + shooter_height})

# Mouse function
def mouse(button, state, x, y):
    global paused, game_over, circles_on_ground, circles_hit, projectiles, falling_circles

    # Invert the y-coordinate
    y = HEIGHT - y

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        print(f"Mouse clicked at: ({x}, {y})")  # Debugging: Print the mouse coordinates

        # Check Pause button
        if pause_icon['x'] <= x <= pause_icon['x'] + pause_icon['width'] and \
           pause_icon['y'] <= y <= pause_icon['y'] + pause_icon['height']:
            paused = not paused
            print("Pause button clicked.")  # Debugging: Verify button click

        # Check Restart button
        elif restart_icon['x'] <= x <= restart_icon['x'] + restart_icon['width'] and \
             restart_icon['y'] <= y <= restart_icon['y'] + restart_icon['height']:
            game_over = False
            paused = False
            circles_on_ground = 0
            circles_hit = 0
            projectiles.clear()
            falling_circles.clear()
            print("Restart button clicked.")  # Debugging: Verify button click

        # Check Exit button
        elif cross_icon['x'] <= x <= cross_icon['x'] + cross_icon['width'] and \
             cross_icon['y'] <= y <= cross_icon['y'] + cross_icon['height']:
            print("Exit button clicked.")  # Debugging: Verify button click
            glutLeaveMainLoop()


# Initialize OpenGL
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, WIDTH, 0, HEIGHT)

# Main function
def main():
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

if __name__ == "__main__":
    main()
