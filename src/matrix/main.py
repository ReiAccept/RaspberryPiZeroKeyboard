import time
import RPi.GPIO as GPIO


class keypad(object):
    KEYPAD = [
        ['ESC', 'F1', 'F2', 'F3','F4','F5','F6','F7','F8','F9','F10','F11','F12',''],
        ['TILDE', '1', '2', '3','4','5','6','7','8','9','0','-','=','BACKSPACE'],
        ['TAB', 'Q', 'W', 'E','R','T','Y','U','I','O','P','[',']','\\'],
        ['CAPS', 'A', 'S', 'D','F','G','H','J','K','L',';','\'','','ENTER'],
        ['LSHIFT', '', 'Z', 'X','C','V','B','N','M',',','.','/','','RSHIFT'],
        ['LCTRL', 'LWIN', 'LALT', '','','SPACE','','','','','RALT','RWIN','FN','RCTRL']]
    ROW = [26, 19, 13, 6, 5, 0]  # 行
    COLUMN = [21, 20, 16, 12, 1, 7, 8, 25, 24, 23, 18, 15, 14, 4]  # 列


def getkey():
    for i in range(len(keypad.COLUMN)):  # 设置列输出低
        GPIO.setup(keypad.COLUMN[i], GPIO.OUT)
        GPIO.output(keypad.COLUMN[i], GPIO.LOW)
    for j in range(len(keypad.ROW)):  # 设置行为输入、上拉
        GPIO.setup(keypad.ROW[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 检测行是否有键按下，有则读取行值
    RowVal = -1
    for i in range(len(keypad.ROW)):
        RowStatus = GPIO.input(keypad.ROW[i])
        if RowStatus == GPIO.LOW:
            RowVal = i
            #print('RowVal=%s' % RowVal)
# 若无键按下,则退出，准备下一次扫描
    if RowVal < 0 or RowVal > 3:
        exit()
        return

# 若第RowVal行有键按下，跳过退出函数，对掉输入输出模式
# 第RowVal行输出高电平，
    GPIO.setup(keypad.ROW[RowVal], GPIO.OUT)
    GPIO.output(keypad.ROW[RowVal], GPIO.HIGH)
# 列为下拉输入
    for j in range(len(keypad.COLUMN)):
        GPIO.setup(keypad.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 读取按键所在列值
    ColumnVal = -1
    for i in range(len(keypad.COLUMN)):
        ColumnStatus = GPIO.input(keypad.COLUMN[i])
        if ColumnStatus == GPIO.HIGH:
            ColumnVal = i
# 等待按键松开
            while GPIO.input(keypad.COLUMN[i]) == GPIO.HIGH:
                time.sleep(0.05)
                #print ('ColumnVal=%s' % ColumnVal)
# 若无键按下，返回
    if ColumnVal < 0 or ColumnVal > 13:
        exit()
        return

    exit()
    return keypad.KEYPAD[RowVal][ColumnVal]


def exit():
    for i in range(len(keypad.ROW)):
        GPIO.setup(keypad.ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for j in range(len(keypad.COLUMN)):
        GPIO.setup(keypad.COLUMN[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
key = None
while True:
    key = getkey()
    if not key == None:
        print('You enter the  key:', key)

# 编程思路：假如S1键按下，先扫描行（列），即行输入，列输出高。此时接第一行的引脚必然会被拉高。
# 设置接第一行的引脚为输出高，列输入。此时接第一列的引脚必然会被拉高。这样我们就得到了第一行第一列的按键被按下。
