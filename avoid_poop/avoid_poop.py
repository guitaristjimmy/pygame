import pygame
import random

# 기본 초기화
pygame.init()

# 화면 크기 설정
screen_width = 480
screen_height = 640

screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption('똥 피하기')   # 게임 이름

# FPS
clock = pygame.time.Clock()

# ------------------------------------------------------------------------------------------------------------------

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 폰트, 좌표, 속도 등)

# 배경 이미지 불러오기
background = pygame.image.load('./bg.png')

# 스프라이트(캐릭터) 불러오기
character = pygame.image.load('./character.png')
character_size = character.get_rect().size      # 캐릭터 이미지 크기를 구해옴
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2    # 화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height     # 화면 세로 기준 가장 아래에 위치

# 이동할 좌표
to_x = 0

# 이동 속도
character_speed = 0.6

# 적 만들기
enemy = pygame.image.load('./enemy.png')
enemy_size = enemy.get_rect().size      # 캐릭터 이미지 크기를 구해옴
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_pos = random.randint(0,screen_width-enemy_width)    # 화면 가로의 절반 크기에 해당하는 곳에 위치
enemy_y_pos = 0     # 화면 세로 기준 가장 아래에 위치
enemy_speed = 0.6

# font 정의
game_font = pygame.font.Font(None, 40)      # 폰트 객체 생성 (폰트, 크기)

# 총 시간
total_time = 10

# 시작 시간
start_ticks = pygame.time.get_ticks()   # 시작 tick 을 받아옴

# 이벤트 루프
running = True  # 게임이 진행중인지 확인
while running:
    dt = clock.tick(60)     # 게임 호면의 초당 프레임 수

    print('fps : ' + str(clock.get_fps()))

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # 창이 닫히면
            running = False

        if event.type == pygame.KEYDOWN:    # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:  # 왼쪽 버튼
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:   # 오른쪽 버튼
                to_x += character_speed

        if event.type == pygame.KEYUP:      # 방향키 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
    # 게임 캐릭터 위치 정의
    character_x_pos += to_x * dt        # 프레임수에 따른 캐릭터 속도 보정
    enemy_y_pos += enemy_speed*dt

    if enemy_y_pos > screen_height:
        enemy_y_pos = 0
        enemy_x_pos = random.randint(0, screen_width-enemy_width)

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width-character_width:
        character_x_pos = screen_width - character_width

    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 충돌 체크
    if character_rect.colliderect(enemy_rect):
        print('충돌!!')
        running = False

    # 화면에 그리기
    screen.blit(background, (0, 0))     # 배경 그리기
    screen.blit(character, (character_x_pos, character_y_pos))      # 캐릭터 그리기
    screen.blit(enemy, (enemy_x_pos, enemy_y_pos))      # 적 그리기

    # 타이머 넣기
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks()-start_ticks) / 1000     # 경과 시간(ms)을 초단위(s)로 표시

    timer = game_font.render(str(round(total_time-elapsed_time, 1)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 경과시간을 초과하면 게임 종료
    if total_time-elapsed_time <= 0:
        print('time out')
        running = False

    pygame.display.update()     # 프레임당 게임화면 그리기

# 잠시 대기
pygame.time.delay(1000)

# pygame 종료
pygame.quit()
