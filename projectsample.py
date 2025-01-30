from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math 
import time
import random
      
# Window dimensions
window_width = 800
window_height = 600

# Ball properties
ball_pos = [0.0, -0.5]
ball_velocity = [0.0, 0.0]  # x, y velocity
ball_radius = 0.05
gravity = -0.002
jump_strength = 0.03

# Wall properties
walls = []  # List of walls, each with position and gap
wall_speed = 0.01    
wall_width = 0.1
gap_height = 0.4
spawn_interval = 2.0  # Seconds between wall spawns

# Game state
last_wall_spawn = time.time() 
game_over = False

def draw_ball():
    """Draw the ball as a filled circle."""
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(1.0, 0.5, 0.0)
    glVertex2f(ball_pos[0], ball_pos[1])
    for angle in range(361):
        angle_rad = angle * 3.14159 / 180
        x = ball_radius * math.cos(angle_rad)
        y = ball_radius * math.sin(angle_rad)
        glVertex2f(ball_pos[0] + x, ball_pos[1] + y)
    glEnd()

def draw_walls():
    """Draw all walls."""
    glColor3f(0.0, 0.5, 1.0)
    for wall in walls:
        x = wall[0]
        gap_y = wall[1]
        # Top part of the wall
        glBegin(GL_QUADS)
        glVertex2f(x, 1.0)
        glVertex2f(x + wall_width, 1.0)
        glVertex2f(x + wall_width, gap_y + gap_height / 2)
        glVertex2f(x, gap_y + gap_height / 2)
        glEnd()
        # Bottom part of the wall
        glBegin(GL_QUADS)
        glVertex2f(x, -1.0)
        glVertex2f(x + wall_width, -1.0)
        glVertex2f(x + wall_width, gap_y - gap_height / 2)
        glVertex2f(x, gap_y - gap_height / 2)
        glEnd()

def spawn_wall():
    """Spawn a new wall at the right edge of the screen."""
    gap_y = random.uniform(-0.6, 0.6)
    walls.append([1.0, gap_y])

def update_walls():
    """Move walls and remove those off-screen."""
    global game_over
    for wall in walls:
        wall[0] -= wall_speed
        # Collision detection
        if abs(wall[0] - ball_pos[0]) < wall_width and not (wall[1] - gap_height / 2 < ball_pos[1] < wall[1] + gap_height / 2):
            game_over = True
    walls[:] = [wall for wall in walls if wall[0] > -1.0]

def update_ball():
    """Update ball position and handle gravity and collisions."""
    global game_over
    ball_velocity[1] += gravity
    ball_pos[1] += ball_velocity[1]

    # Floor and ceiling collisions
    if ball_pos[1] - ball_radius < -1.0 or ball_pos[1] + ball_radius > 1.0:
        game_over = True

def keyboard(key, x, y):
    """Handle keyboard input for jumping and movement."""
    if key == b' ' and not game_over:  # Space for jump
        ball_velocity[1] = jump_strength

def display():
    """Render the scene."""
    glClear(GL_COLOR_BUFFER_BIT)
    draw_ball()
    draw_walls()
    glutSwapBuffers()

def idle():
    """Update game logic continuously."""
    global last_wall_spawn, game_over

    if game_over:
        print("Game Over!")
        glutLeaveMainLoop()
        return

    current_time = time.time()
    if current_time - last_wall_spawn > spawn_interval:
        spawn_wall()
        last_wall_spawn = current_time

    update_ball()
    update_walls()
    time.sleep(0.01)
    glutPostRedisplay()

def main():
    """Set up the OpenGL environment and run the game loop."""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Flappy Ball Game")

    # Set up orthographic projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

    # Set callbacks
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)

    # Start the main loop
    glutMainLoop()

if __name__ == "__main__":
    main()
