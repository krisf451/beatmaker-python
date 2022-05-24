import pygame
from pygame import mixer
pygame.init()

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Beat Maker')
label_font = pygame.font.Font('Roboto-Bold.ttf', 32)
medium_font = pygame.font.Font('Roboto-Bold.ttf', 24)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True

# load in sounds
hi_hat = mixer.Sound('sounds/hi hat.WAV')
snare = mixer.Sound('sounds/snare.WAV')
kick = mixer.Sound('sounds/kick.WAV')
clap = mixer.Sound('sounds/clap.wav')
crash = mixer.Sound('sounds/crash.wav')
tom = mixer.Sound('sounds/tom.WAV')
pygame.mixer.set_num_channels(instruments * 3)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                clap.play()
            if i == 4:
                crash.play()
            if i == 5:
                tom.play()


def draw_grid(clicks, beat):
    boxes = []
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)
    colors = [gray, white, white]

    # hi hat
    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (30, 30))
    # snare
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30, 130))
    # kick
    kick_text = label_font.render('Bass Drum', True, white)
    screen.blit(kick_text, (30, 230))
    # clap
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30, 330))
    # crash
    crash_text = label_font.render('Crash', True, white)
    screen.blit(crash_text, (30, 430))
    # tom
    tom_text = label_font.render('Floor Tom', True, white)
    screen.blit(tom_text, (30, 530))
    for i in range(6):
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 3)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // beats) + 205,
                                                   (j * 100) + 5, ((WIDTH - 200) // beats) - 10,
                                                   ((HEIGHT - 200) // instruments) - 10], 0, 3)
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200,
                                                   (j * 100), ((WIDTH - 200) // beats),
                                                   ((HEIGHT - 200) // instruments)], 5, 5)
            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200,
                                             (j * 100), ((WIDTH - 200) // beats),
                                             ((HEIGHT - 200) // instruments)], 2, 5)
            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats), instruments * 100], 5, 3)
    return boxes


run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT - 100))
    # bpm stuff
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (308, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (370, HEIGHT - 100))
    bmp_add_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 150, 48, 48], 0, 5)
    bmp_sub_rect = pygame.draw.rect(screen, gray, [510, HEIGHT - 100, 48, 48], 0, 5)
    bmp_addFive_rect = pygame.draw.rect(screen, gray, [565, HEIGHT - 150, 48, 48], 0, 5)
    bmp_subFive_rect = pygame.draw.rect(screen, gray, [565, HEIGHT - 100, 48, 48], 0, 5)
    add_text = medium_font.render('+1', True, white)
    sub_text = medium_font.render('-1', True, white)
    addFive_text = medium_font.render('+5', True, white)
    subFive_text = medium_font.render('-5', True, white)
    screen.blit(add_text, (520, HEIGHT - 140))
    screen.blit(sub_text, (520, HEIGHT - 90))
    screen.blit(addFive_text, (575, HEIGHT - 140))
    screen.blit(subFive_text, (575, HEIGHT - 90))
    # beats stuff
    beats_rect = pygame.draw.rect(screen, gray, [630, HEIGHT - 150, 165, 100], 5, 5)
    beats_text = medium_font.render('Beats In Loop', True, white)
    screen.blit(beats_text, (638, HEIGHT - 130))
    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (700, HEIGHT - 100))
    beat_add_rect = pygame.draw.rect(screen, gray, [805, HEIGHT - 150, 48, 48], 0, 5)
    beat_sub_rect = pygame.draw.rect(screen, gray, [805, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render('+1', True, white)
    sub_text2 = medium_font.render('-1', True, white)
    screen.blit(add_text2, (815, HEIGHT - 140))
    screen.blit(sub_text2, (815, HEIGHT - 90))

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            elif bmp_add_rect.collidepoint(event.pos):
                bpm += 1
            elif bmp_sub_rect.collidepoint(event.pos):
                bpm -= 1
            elif bmp_addFive_rect.collidepoint(event.pos):
                bpm += 5
            elif bmp_subFive_rect.collidepoint(event.pos):
                bpm -= 5
            elif beat_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beat_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)


    beat_length = 3600 // bpm
    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
pygame.quit()
