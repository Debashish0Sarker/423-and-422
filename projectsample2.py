from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Ball properties
BALL_SIZE = 5
BALL_SPEED = 5

# Obstacle properties
OBSTACLE_COUNT = 3
OBSTACLE_SIZE = 5
OBSTACLE_SPEED = 1

# Traps and other game elements
WATER_REGION = [(200, 300, 200, 300)]  # List of (x_min, x_max, y_min, y_max)
ENLARGE_PUMP = (500, 100)  # (x, y)
MINIMIZE_PUMP = (700, 400)  # (x, y)
TRAP_TIME_LIMIT = 500

# Keyboard state
keys = {b'w': False, b's': False, b'a': False, b'd': False}

# Ball class
class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.dx = 0
        self.dy = 0
        self.size = BALL_SIZE
        self.trap_timer = TRAP_TIME_LIMIT

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x - self.size <= 0 or self.x + self.size >= SCREEN_WIDTH:
            self.dx = 0
        if self.y - self.size <= 0 or self.y + self.size >= SCREEN_HEIGHT:
            self.dy = 0

        # Check water region effect
        for region in WATER_REGION:
            if region[0] <= self.x <= region[1] and region[2] <= self.y <= region[3]:
                self.dx *= 0.5
                self.dy *= 0.5

        # Decrease trap timer
        self.trap_timer -= 1
        if self.trap_timer <= 0:
            print("Time over! Ball eliminated.")
            glutLeaveMainLoop()

    def check_special_zones(self):
        global ENLARGE_PUMP, MINIMIZE_PUMP

        # Enlarge pump
        if abs(self.x - ENLARGE_PUMP[0]) < self.size and abs(self.y - ENLARGE_PUMP[1]) < self.size:
            self.size = min(self.size + 5, 30)
            print("Ball Enlarged!")

        # Minimize pump
        if abs(self.x - MINIMIZE_PUMP[0]) < self.size and abs(self.y - MINIMIZE_PUMP[1]) < self.size:
            self.size = max(self.size - 5, 5)
            print("Ball Minimized!")

    def draw(self):
        glBegin(GL_POINTS)
        for dx in range(-self.size, self.size + 1):
            for dy in range(-self.size, self.size + 1):
                glVertex2f(self.x + dx, self.y + dy)
        glEnd()

# Obstacle class
class Obstacle:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.dx = random.choice([-OBSTACLE_SPEED, OBSTACLE_SPEED])
        self.dy = random.choice([-OBSTACLE_SPEED, OBSTACLE_SPEED])

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x <= 0 or self.x >= SCREEN_WIDTH:
            self.dx = -self.dx
        if self.y <= 0 or self.y >= SCREEN_HEIGHT:
            self.dy = -self.dy

    def draw(self):
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

# Initialization
def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

# Handle keyboard input
def keyboard(key, x, y):
    global keys
    if key in keys:
        keys[key] = True


def keyboard_up(key, x, y):
    global keys
    if key in keys:
        keys[key] = False

# Update ball direction based on keyboard input
def update_ball_direction(ball):
    if keys[b'w']:
        ball.dy = BALL_SPEED
    elif keys[b's']:
        ball.dy = -BALL_SPEED
    else:
        ball.dy = 0

    if keys[b'd']:
        ball.dx = BALL_SPEED
    elif keys[b'a']:
        ball.dx = -BALL_SPEED
    else:
        ball.dx = 0

# Main game loop
ball = Ball()
obstacles = [Obstacle() for _ in range(OBSTACLE_COUNT)]

# GLUT display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw water region
    for region in WATER_REGION:
        glColor3f(0.0, 0.0, 1.0)  # Blue for water
        glBegin(GL_QUADS)
        glVertex2f(region[0], region[2])
        glVertex2f(region[1], region[2])
        glVertex2f(region[1], region[3])
        glVertex2f(region[0], region[3])
        glEnd()

    # Draw enlarge pump
    glColor3f(0.0, 1.0, 0.0)  # Green for enlarge pump
    glBegin(GL_POINTS)
    glVertex2f(*ENLARGE_PUMP)
    glEnd()

    # Draw minimize pump
    glColor3f(1.0, 0.0, 0.0)  # Red for minimize pump
    glBegin(GL_POINTS)
    glVertex2f(*MINIMIZE_PUMP)
    glEnd()

    # Move and draw ball
    update_ball_direction(ball)
    ball.move()
    ball.check_special_zones()
    glColor3f(1.0, 1.0, 1.0)  # White for ball
    ball.draw()

    # Move and draw obstacles
    for obstacle in obstacles:
        obstacle.move()
        glColor3f(1.0, 0.0, 0.0)  # Red for obstacles
        obstacle.draw()

    glutSwapBuffers()

# GLUT idle function
def idle():
    glutPostRedisplay()

# Main
if __name__ == "__main__ ":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutCreateWindow(b"Advanced Ball Game with OpenGL")
    init()
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutMainLoop()