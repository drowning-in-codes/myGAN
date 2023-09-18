import cv2
import os.path
from tqdm import tqdm


def detect(filename, cascade_file="./lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)
    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = cascade.detectMultiScale(
        gray,
        # detector options
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(24, 24),
    )
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            image = image[int(y - 0.1 * h) : int(y + 0.9 * h), x : x + w]
        height, width, _ = image.shape
        if height > 0 and width > 0:
            image = cv2.resize(image, (64, 64))
            dir_path = "../assets/misaka_mikoto"
            cv2.imwrite(
                dir_path
                + "/crop_"
                + filename.split("_")[-2]
                + "."
                + filename.split(".")[-1],
                image,
            )
        else:
            return
    else:
        return


if __name__ == "__main__":
    # 遍历某个目录
    for root, dirs, files in os.walk("../gallery-dl/danbooru/misaka_mikoto"):
        pbar = tqdm(files)
        for idx, file in enumerate(pbar):
            pbar.set_postfix(index=idx, file=file)
            if not file.startswith("crop") and not file.endswith(".part"):
                detect(os.path.join(root, file))
