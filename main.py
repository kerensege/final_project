

import cv2

# טוענים את הסרטון
video_path = "C:/Users/keren segev/Desktop/DJI.MP4"
cap = cv2.VideoCapture(video_path)

# הולכים לפריים 500

cap.set(cv2.CAP_PROP_POS_FRAMES, 41200)


# קוראים את הפריים
ret, frame = cap.read()
if ret:
    cv2.imwrite("frame_test.png", frame)  # שמירת הפריים כתמונה לבדיקה
    print("Frame saved as frame_test.png")
else:
    print("Failed to extract frame")

cap.release()


from PIL import Image
import pytesseract

# הגדרת הנתיב ל-Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# טוענים את התמונה ששמרנו
image = Image.open("frame_test.png")



import cv2
import numpy as np
from PIL import Image
import pytesseract

# טוענים את התמונה
image = cv2.imread("frame_test.png")

# הופכים לגווני אפור
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# חידוד תמונה
kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])
sharpened = cv2.filter2D(gray, -1, kernel)

# הגברת ניגודיות בלי להפוך לשחור-לבן
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
contrast = clahe.apply(sharpened)

# שמירת תמונה משופרת
cv2.imwrite("frame_test_improved.png", contrast)



# חיתוך אזור הסוללה (שני את הקואורדינטות לפי מיקום הטקסט)
x, y, w, h = 423, 13, 18, 11  # שנה לפי המיקום בפועל
battery_roi = contrast[y:y+h, x:x+w]

# שמירת התמונה החתוכה
cv2.imwrite("battery_region_improved.png", battery_roi)

# OCR עם מגבלת תווים (רק מספרים ואחוזים)
battery_text = pytesseract.image_to_string(battery_roi, config="--psm 7 -c tessedit_char_whitelist=0123456789%")
print("🔋 אחוז סוללה מזוהה:", battery_text)


# חיתוך אזור הגובה (שנה את הקואורדינטות X, Y, W, H לפי המיקום בפועל)
x, y, w, h = 143, 334, 35, 14  # מיקום הגובה
altitude_roi = image[y:y+h, x:x+w]
altitude_text = pytesseract.image_to_string(altitude_roi, config="--psm 7 -c tessedit_char_whitelist=0123456789. ")
cv2.imwrite("altitude_region.png", altitude_roi)
print("🌍 גובה:", altitude_text)

# חיתוך אזור המרחק (שנה את הקואורדינטות X, Y, W, H לפי המיקום בפועל)
x, y, w, h = 206, 334, 47, 14  # מיקום המרחק
distance_roi = image[y:y+h, x:x+w]
distance_text = pytesseract.image_to_string(distance_roi, config="--psm 7 -c tessedit_char_whitelist=0123456789. ")
cv2.imwrite("distance_region.png", distance_roi)
print("📏 מרחק:", distance_text)


# שמירה לקובץ
with open("drone_data.txt", "w") as file:
    file.write(f"סוללה: {battery_text}\n")
    file.write(f"מרחק: {distance_text}\n")
    file.write(f"גובה: {altitude_text}\n")

print("📄 הנתונים נשמרו בקובץ 'drone_data.txt'.")
