import cv2
import os


def Video_to_Image(videoPath, imagePath):
    videoPath = videoPath
    imagePath = imagePath

    if os.path.isdir(videoPath) == False:
        print("Video Path dosen't exist.")
        return

    if os.path.isdir(imagePath) == False:
        os.mkdir(imagePath)

    fileList = os.listdir(videoPath)
    for file in fileList:
        cap = cv2.VideoCapture(videoPath + file)
        count = 0

        print("Now File: {file}".format(file=file))
        if cap.isOpened():
            while True:
                ret, image = cap.read()
                if not ret:
                    break
                file_name = file.split(".")[0]
                if os.path.isdir(imagePath + file_name) == False:
                    os.mkdir(imagePath + file_name)
                if int(cap.get(1)) % 60 == 0:
                    cv2.imwrite(
                        imagePath + file_name + "\\frame{num}.jpg".format(num=count),
                        image,
                    )
                    print(imagePath + file_name + "\\frame{num}.jpg".format(num=count))
                    count += 1
        else:
            print("Video connot open.")

        cap.release()


if __name__ == "__main__":
    Video_to_Image(".\\Source\\", ".\\Images\\")
