import tkinter
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import easyocr
from sympy.multipledispatch.dispatcher import source

##윈도우 생성
wnd = tkinter.Tk()
wnd.title("Image Reader")
wnd.geometry("500x700")

##OCR 준비
reader = easyocr.Reader(['ko'], gpu=False)

imgWidth = 200
imgHeight = 200

##cv로 불러온 이미지를 Label에 적합한 데이터로 변환
def ConvertToLabelImage(data):
    color = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    ary = Image.fromarray(color).resize((imgWidth, imgHeight))
    result = ImageTk.PhotoImage(ary)
    return result

##이미지 데이터를 텍스트로 변환해주는 함수
def ImgToText():
    ##원본 이미지
    filepath = filedialog.askopenfilename(filetypes=[("이미지 파일", "*.png;*.jpg;*.jpeg;*")])
    sourceImg = cv2.imread(filepath, cv2.IMREAD_COLOR)

    ##엣지 검출
    cannyImg = cv2.Canny(sourceImg, 50, 150)

    ##2진화 이미지
    grayImg = cv2.cvtColor(sourceImg, cv2.COLOR_BGR2GRAY)
    _, binImg = cv2.threshold(grayImg, 127, 255, cv2.THRESH_BINARY)

    ##가우시안 블러
    blurImg = cv2.GaussianBlur(sourceImg, (5, 5), 0)

    ##텍스트 변환
    text_results[1] = reader.readtext(sourceImg)
    text_results[2] = reader.readtext(cannyImg)
    text_results[3] = reader.readtext(binImg)
    text_results[4] = reader.readtext(blurImg)

    ##label에 맞는 형식으로 변환
    img1 = ConvertToLabelImage(sourceImg)
    img2 = ConvertToLabelImage(cannyImg)
    img3 = ConvertToLabelImage(binImg)
    img4 = ConvertToLabelImage(blurImg)

    ##img1~4 변수가 가비지 컬렉터에 제거되는걸 방지하면서 라벨의 이미지를 업데이트
    ##https://stackoverflow.com/questions/3482081/how-to-update-the-image-of-a-tkinter-label-widget
    img1_label.config(image=img1)
    img1_label.image = img1

    img2_label.config(image=img2)
    img2_label.image = img2

    img3_label.config(image=img3)
    img3_label.image = img3

    img4_label.config(image=img4)
    img4_label.image = img4

    ##텍스트 컨트롤 초기화
    text_control.delete("1.0", tkinter.END)

    ##기본으로 원본 이미지를 읽은 텍스트를 출력하게
    for (bbox, text, prob) in text_results[1]:
        text_control.insert(tkinter.INSERT, f"{text}, 정확도 - {prob * 100 :.2f}%\n")

    return

def update_text_control(index):
    text_control.delete("1.0", tkinter.END)

    for (bbox, text, prob) in text_results[index]:
        text_control.insert(tkinter.INSERT, f"{text}, 정확도 - {prob * 100 :.2f}%\n")

    return

##이미지 불러오는 버튼
load_btn = tkinter.Button(wnd, text="불러오기", command=ImgToText, width=10)
load_btn.pack(side="bottom", pady=10)

##원본 이미지와 처리된 이미지들을 모아두는 묶음
panel = tkinter.Frame(wnd)
panel.pack(side="top", pady=10)

##기본 이미지 불러오기
default_img = cv2.imread("data\\default.bmp", cv2.IMREAD_COLOR)
input_img = ConvertToLabelImage(default_img)

##텍스트를 저장하기 위한 변수
text_results = {
    1: reader.readtext(default_img),
    2: reader.readtext(default_img),
    3: reader.readtext(default_img),
    4: reader.readtext(default_img)
}

##이미지 출력용 라벨
img1_label = tkinter.Label(panel, image=input_img, width=imgWidth, height=imgHeight)
img1_label.grid(row=0, column=0)
img1_label.bind("<Button-1>", lambda event: update_text_control(1))

img2_label = tkinter.Label(panel, image=input_img, width=imgWidth, height=imgHeight)
img2_label.grid(row=1, column=0)
img2_label.bind("<Button-1>", lambda event: update_text_control(2))

img3_label = tkinter.Label(panel, image=input_img, width=imgWidth, height=imgHeight)
img3_label.grid(row=0, column=1)
img3_label.bind("<Button-1>", lambda event: update_text_control(3))

img4_label = tkinter.Label(panel, image=input_img, width=imgWidth, height=imgHeight)
img4_label.grid(row=1, column=1)
img4_label.bind("<Button-1>", lambda event: update_text_control(4))

text_control = tkinter.Text(wnd, wrap="word", width=500 ,height=20)
text_control.pack()

##생성된 윈도우 유지
wnd.mainloop()





