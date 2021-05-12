import cv2
import os
from PIL import Image
from numpy import dot
from numpy.linalg import norm
import numpy as np
from gaze_tracking import GazeTracking


def Video_to_Image(videoPath, imagePath):
    print("[O] Video to Image function is running...")
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
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                # if int(cap.get(1)) % fps == 0:
                if int(cap.get(1)) % 100 == 0:
                    cv2.imwrite(
                        imagePath + file_name + "\\frame{num}.jpg".format(num=count),
                        image,
                    )
                    print(imagePath + file_name + "\\frame{num}.jpg".format(num=count))
                    count += 1
        else:
            print("Video connot open.")

        cap.release()
    print("[=] Video to Image function is closing...")


def read_gaze(dirPath):
    # 디렉토리 내 디렉터리, 파일 recursive하게 읽는 건 나중에 하고
    # 우선 주어진 한 디렉터리에 대해서만 진행
    print("[O] Read left eye gaze is running...")
    gaze = GazeTracking()
    left = []
    target_dir = dirPath
    fileList = os.listdir(target_dir)
    for file in fileList:
        image = Image.open(target_dir + "\\" + file)
        data = np.asarray(image)
        # print(data.shape)     # (720 ,1280, 3)
        gaze.refresh(data)
        left_pupil = gaze.pupil_left_coords()
        left.append(left_pupil)
    print(left)
    print("[=] Read left eye gaze is closing...")
    return left


def list_to_vector(list):
    vet = np.empty((0, 2), int)
    for i in list:
        if i != None:
            a = i[0]
            b = i[1]
            vet = np.append(vet, np.array([[a, b]]), axis=0)
        else:
            vet = np.append(vet, np.array([[0, 0]]), axis=0)
    return vet


def cosine_sim(VA, VB):
    # assume that len(VA) == len(VB)
    sim_array = []
    if len(VA) < len(VB):
        length = len(VA)
    else:
        length = len(VB)
    for i in range(length):
        A = VA[i]
        B = VB[i]
        sim = dot(A, B) / (norm(A) * norm(B))
        sim_array.append(sim)
    return sim_array


if __name__ == "__main__":
    # video to image
    Video_to_Image(".\\Source\\", ".\\Images\\")
    # read left eye or right eye
    # make list to 2-dimension vector
    v1 = list_to_vector(read_gaze(".\\Images\\1"))
    v2 = list_to_vector(read_gaze(".\\Images\\4"))
    print(v1)
    print(v2)

    # given two student's vector, calculate cosine similarity
    re = cosine_sim(v1, v2)
    print(re)
