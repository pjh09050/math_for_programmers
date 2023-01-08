import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import matplotlib.cm
from vectors import *
from math import *

# 3장에서 사용한 셰이딩 메커니즘을 사용
def normal(face):
    return(cross(subtract(face[1], face[0]), subtract(face[2], face[0])))

blues = matplotlib.cm.get_cmap('Blues')

def shade(face,color_map=blues,light=(1,2,3)):
    return color_map(1 - dot(unit(normal(face)), unit(light)))


# 8면체의 기하학적 구조와 광원을 명시해야 한다.
light = (1,2,3)
faces = [
    [(1,0,0), (0,1,0), (0,0,1)],
    [(1,0,0), (0,0,-1), (0,1,0)],
    [(1,0,0), (0,0,1), (0,-1,0)],
    [(1,0,0), (0,-1,0), (0,0,-1)],
    [(-1,0,0), (0,0,1), (0,1,0)],
    [(-1,0,0), (0,1,0), (0,0,-1)],
    [(-1,0,0), (0,-1,0), (0,0,1)],
    [(-1,0,0), (0,0,-1), (0,-1,0)],
]


pygame.init()
display = (400,400) # 400x400 픽셀
window = pygame.display.set_mode(display, DOUBLEBUF|OPENGL) 
# PyGame에게 그래픽스 엔진으로 OpenGL을 사용해야 함을 알려주고, 더블 버퍼링(double-buffering)이라는 내장 최적화 옵션을 사용해야 함을 알려준다.

gluPerspective(45, 1, 0.1, 50.0) # 장면을 바라볼 떄의 투영법을 묘사, 시야각이 45도이고 가로세로비가 1:1 설정, 성능 최적화 차원에서 두 수 0.1과 50.0은 렌더링되는 z좌표의 한계이다.
glTranslatef(0.0,0.0, -5) # z축에서 5단위 위에서 장면을 관찰하고 있음을 나타낸다. 장면이 벡터 (0,0,-5)만큼 멀어진다.
glEnable(GL_CULL_FACE) # 관찰자와 멀어지는 다각형을 자동으로 숨기는 OpenGL옵션을 작동
glEnable(GL_DEPTH_TEST) # 가까이에 있는 다각형이 멀리에 있는 다각형 위에 나타나도록 렌더링한다.
glCullFace(GL_BACK) # 우리를 향하는 다각형이 다른 다각형 뒤에 가려지면 자동으로 숨기는 OpenGL옵션 작동

# 단일 프레임을 렌더링하기 위해, 벡터에 대해 반복하면서 각 벡터에 셰이딩을 넣고 OpenGL로 그리고 PyGame으로 프레임을 업데이트한다.
clock = pygame.time.Clock() # PyGame의 시간 진행을 측정하고자 시계를 초기화한다.
while True:
    for event in pygame.event.get(): # 반복할 떄마다 PyGame이 받은 event를 확인해 사용자가 윈도를 닫은 경우 종료한다.
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    clock.tick() # 시간이 지났어야 함을 시계에 알린다.
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glBegin(GL_TRIANGLES) # OpenGL에 삼각형을 그리고 있음을 전달한다.
    for face in faces:
        color = shade(face,blues,light)
        for vertex in face:
            glColor3fv((color[0], color[1], color[2])) # 각 면(삼각형)의 각 점에 셰이딩에 기반한 색을 설정한다.
            glVertex3fv(vertex) # 현재 삼각형의 다음 꼭짓점을 명시한다.
    glEnd()
    pygame.display.flip() # PyGame에 애니메이션의 최신 프레임이 준비되었음을 알려서 화면에 나타나게 한다.
    print(clock.get_fps()) # 8면체를 렌더링하고 다시 렌더링하는 비율(초당 프레임)의 순간 값을 확인해 출력한다.
