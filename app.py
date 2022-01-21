from datetime import datetime
import time, webbrowser, pyautogui
dt = lambda fmt: datetime.now().strftime(str(fmt))

# Read pmi.txt and load as variable
def PMI_ALL(path='pmi.txt'):
    pmi = {}
    with open(path, 'r') as f:
        for line in f.readlines():
            pmi_pair = line.split('=')
            if pmi_pair[0][0] == '#':
                continue
            pmi_pair[1] = pmi_pair[1].split('\n')[0]
            pmi[pmi_pair[0]] = pmi_pair[1]
    return pmi


# Determine upcoming lesson slot
# def lesson(t=int(dt('%H%M')), dow=int(dt('%w'))):
def lesson(t=950, dow=2):  # Testing
    slot = -1
    if 730 <= t < 825:
        slot = 0
    elif 825 <= t < 900:
        slot = 1
    elif 900 <= t < 940:
        slot = 2
    elif 940 <= t < 1035:
        slot = 3
    elif 1035 <= t < 1115:
        slot = 4
    elif 1115 <= t < 1210:
        slot = 5
    elif 1210 <= t < 1345:
        slot = 6
    elif 1345 <= t < 1420:
        slot = 7
    elif 1420 <= t < 1505:
        slot = 8
    elif 1505 <= t < 1540:
        slot = 9
    elif 1540 <= t < 1635:
        slot = 10
    else:
        return
    
    lsn = (dow, slot)
    if lsn in ((1, 0), (2, 0), (5, 0)):
        return
    return lsn


# Determine subject by DoW and slot
def subj(lesson_ident: tuple):
    dow = lesson_ident[0]
    slot = lesson_ident[1]
    cls = PMI_ALL()['CLASS(V/I)'].upper()
    subjs = (
        ('', '', 'HRT', 'HRT', '',),
        ('PE' if cls == 'I' else 'ENG', 'C_SL', 'CHI' if cls == 'I' else 'TOK', 'ENG', 'ASSEMBLY',),
        ('CHI', 'C_SL', 'B_SL', 'ENG', 'C_SL',),
        ('CHI', 'MATHS_SL/HL', 'B_SL', 'B_SL', 'C_SL',),
        # Recess
        ('TOK', 'CHI', 'B_SL', 'B_SL', 'C_SL',),
        ('TOK', 'CHI', 'TOK' if cls == 'I' else 'CHI', 'MATHS_SL/HL', 'ENG' if cls == 'I' else 'PE',),
        # Lunch
        ('MATHS_SL/HL', 'A_SL', 'ENG', 'A_SL', 'PE' if cls == 'I' else 'ENG',),
        ('MATHS_SL/HL', 'A_SL', 'ENG', 'A_SL', 'MATHS_SL/HL',),
        # Break
        ('ENG' if cls == 'I' else 'PE', 'ENG', 'REFLE', 'A_SL', 'CHI',),
        ('A_HL', 'B_HL', 'MATHS_HL', 'C_HL', 'CHI',),
        ('A_HL', 'B_HL', 'MATHS_HL', 'C_HL', 'EE',),
    )
    return subjs[slot][dow-1]


# Join Zoom automatically if able, else show message
def join(subj: str):
    
    if subj == 'REFLE':
        print('Please choose the subject manually, this window will close in 30 seconds.')
        print('RE: https://zoom.us/j/4287727803')
        print('FLE: https://zoom.us/j/5168805269')
        time.sleep(30)
        return
    
    pmi = PMI_ALL()[subj]
    if 9 <= len(pmi) <= 11:
        halt = input(f'Joining {subj} lesson, confirm? (Press ENTER to continue, close this window if not.)')
        url = f'https://zoom.us/j/{pmi}'
        webbrowser.open(url)
        time.sleep(5)  # Wait for browser to load page
        pyautogui.press('left')
        pyautogui.press('enter')
        return
    
    if subj[-3:] == '_HL':
        print('No upcoming lesson. Closing window in 3 seconds.')
        time.sleep(3)
        return
    
    print('Invalid PMI in pmi.txt! Please correct accordingly.')
    time.sleep(3)
    return


# Script
def main():
    
    if not lesson():
        print('No upcoming lesson. Closing window in 3 seconds.')
        time.sleep(3)
        return
    
    join(subj(lesson()))
    return


if __name__ == '__main__':
    main()
