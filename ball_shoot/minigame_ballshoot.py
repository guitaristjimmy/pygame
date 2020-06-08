import pygame
import os

# 기본 초기화
pygame.init()

# 화면 크기 설정
screen_width = 640
screen_height = 480

screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption('Ball Shoot')   # 게임 이름

# FPS
clock = pygame.time.Clock()

# ------------------------------------------------------------------------------------------------------------------

# 1. 사용자 게임 초기화 (배경화면, 게임 이미지, 폰트, 좌표, 속도 등)
current_path = os.path.dirname(__file__)        # 현재 파일의 위치 반환
image_path = os.path.join(current_path, 'images')       # 이미지 폴더 위치 반환

# 배경 이미지 불러오기
background = pygame.image.load(os.path.join(image_path, 'bg.png'))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, 'stage.png'))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, 'character.png'))
character_size = character.get_rect().size      # 캐릭터 이미지 크기를 구해옴
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2    # 화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height - stage_height     # 화면 세로 기준 가장 아래에 위치

# 이동할 좌표
character_to_x = 0

# 이동 속도
character_speed = 0.6

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, 'weapon.png'))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 2.4

# 공 만들기 (4개 따로 처리)
ball_images = [pygame.image.load(os.path.join(image_path, 'ball1.png')),
               pygame.image.load(os.path.join(image_path, 'ball2.png')),
               pygame.image.load(os.path.join(image_path, 'ball3.png')),
               pygame.image.load(os.path.join(image_path, 'ball4.png'))]
# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]

balls = []
# 최초 발생하는 큰 공
balls.append({
    'pos_x': 50,
    'pos_y': 50,
    'img_idx': 0,
    'to_x': 3,  # 음수면 왼쪽, 양수면 오른쪽
    'to_y': -6,
    'init_spd_y': ball_speed_y[0]})

# font 정의
game_font = pygame.font.Font(None, 40)      # 폰트 객체 생성 (폰트, 크기)

# 총 시간
total_time = 100

# 시작 시간
start_ticks = pygame.time.get_ticks()   # 시작 tick 을 받아옴

# 게임 종료 메시지
game_result = 'Game Over'

# 사라질 부기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

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
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:   # 오른쪽 버튼
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:   # 무기 발사(스페이스)
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:      # 방향키 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
    # 게임 캐릭터 위치 정의
    character_x_pos += character_to_x * dt        # 프레임수에 따른 캐릭터 속도 보정

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width-character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # x 방향으로 벽에 닿았을 때 튕겨나오기
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val['to_x'] *= (-1)

        # y 방향으로 벽에(stage) 닿았을 때 튕겨나오기
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val['to_y'] = ball_val['init_spd_y']
        else:
            ball_val['to_y'] += 0.5
        ball_val['pos_x'] += ball_val['to_x']
        ball_val['pos_y'] += ball_val['to_y']

    # 충돌 처리를 위한 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 케릭터 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 무기와 공 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                if ball_img_idx < 3:
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 공
                    balls.append({'pos_x': ball_pos_x + (ball_width/2) - (small_ball_width/2),
                                  'pos_y': ball_pos_y + (ball_height/2) - (small_ball_height/2),
                                  'img_idx': ball_img_idx+1,
                                  'to_x': -3,  # 음수면 왼쪽, 양수면 오른쪽
                                  'to_y': -6,
                                  'init_spd_y': ball_speed_y[ball_img_idx+1]})

                    # 오른쪽으로 튕겨나가는 공
                    balls.append({'pos_x': ball_pos_x + (ball_width/2) - (small_ball_width/2),
                                  'pos_y': ball_pos_y + (ball_height/2) - (small_ball_height/2),
                                  'img_idx': ball_img_idx+1,
                                  'to_x': 3,  # 음수면 왼쪽, 양수면 오른쪽
                                  'to_y': -6,
                                  'init_spd_y': ball_speed_y[ball_img_idx+1]})
                break
        else:
            continue
        break
    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우 게임 종료
    if len(balls) == 0:
        game_result = 'Mission Complete'
        running = False


    # 화면에 그리기기 ----------------------------------------------------------------------------------------------
    screen.blit(background, (0, 0))     # 배경 그리기

    # 무기 그리기
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val['pos_x']
        ball_pos_y = val['pos_y']
        ball_img_idx = val['img_idx']
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height-stage_height))     # 스테이지 그리기
    screen.blit(character, (character_x_pos, character_y_pos))      # 캐릭터 그리기

    # 타이머 넣기
    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks()-start_ticks) / 1000     # 경과 시간(ms)을 초단위(s)로 표시

    timer = game_font.render('TIME : '+str(round(total_time-elapsed_time, 1)), True, (0, 0, 0))
    screen.blit(timer, (10, 10))

    # 경과시간을 초과하면 게임 종료
    if total_time-elapsed_time <= 0:
        game_result = 'Time Over'
        print('Time Out')
        running = False

    pygame.display.update()     # 프레임당 게임화면 그리기

msg = game_font.render(game_result, True, (0, 0, 0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 잠시 대기
pygame.time.delay(2000)

# pygame 종료
pygame.quit()
