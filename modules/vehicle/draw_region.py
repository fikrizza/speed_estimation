import cv2
import numpy as np
import os


def draw_region(frame, save=False, filename="region_1", folder="region"):
    """
    draw region on the frame
    :param frame: frame to draw region on it, can be a path to image or numpy array
    :param save: save the region to a file
    :param filename: filename to save (the output will be filename.jpg and filename.txt in a folder)
    :param folder: folder to save the output
    """
    if type(frame) == str:
        frame = cv2.imread(frame)

    # print(
    #     """
    #       tutorial sangat singkat, klik pada layar untuk membuat titik regionnya
    #       setelah selesai tekan 'n' untuk meregister region tersebut.

    #       jika terdapat kesalahan tekan 'c' untuk menghapus semua region yang telah dibuat
    #       jika sudah selesai tekan 'q' untuk keluar dari program
    #     """
    # )

    # Create a copy of the frame to draw on
    img = frame.copy()
    regions = []
    region = []
    colors = [
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (255, 255, 0),
        (0, 255, 255),
        (255, 0, 255),
        (255, 255, 255),
        (0, 0, 0),
    ]
    color_cycle = 0

    # Define the callback function for mouse events
    def click_event(event, x, y, flags, params):
        nonlocal img, region
        if event == cv2.EVENT_LBUTTONDOWN:
            # Draw a circle on the image
            cv2.circle(img, (x, y), 5, colors[color_cycle], -1)
            region.append(x)
            region.append(y)
            cv2.imshow("draw region", img)

    # Create a window to display the image
    cv2.namedWindow("draw region")

    # Set the mouse callback function for the window
    cv2.setMouseCallback("draw region", click_event, {"img": img})

    # Display the image and wait for a key press
    cv2.putText(  # Display instructions
        img,
        "Click to define region. Press 'c' to clear. Press 'q' to finish and 'n' to next region",
        (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2,
    )
    cv2.imshow("draw region", img)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            if save:
                if not os.path.exists(folder):
                    os.makedirs(folder)

                if not os.path.exists(f"{folder}/{filename}"):
                    os.makedirs(f"{folder}/{filename}")

                with open(f"{folder}/{filename}/{filename}.txt", "w") as f:
                    f.write("copy this coordianates to the config yaml file\n\n")
                    f.write(str(regions))

                    cv2.imwrite(f"{folder}/{filename}/{filename}.jpg", img)
            break

        if key == ord("c"):
            region = []
            regions = []
            color_cycle = 0
            cv2.destroyAllWindows()
            cv2.namedWindow("draw region")
            img = frame.copy()
            cv2.setMouseCallback("draw region", click_event, {"img": img})

            cv2.putText(  # Display instructions
                img,
                "Click to define region. Press 'c' to clear. Press 'q' to finish and 'n' to next region",
                (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2,
            )
            cv2.imshow("draw region", img)

        if key == ord("n"): # gambar region dan reset region
            regions.append(region)
            try:
                for x in range(0, len(region),4):
                    cv2.line(img, (region[x] , region[x+1]), (region[x+2], region[x+3]), color_cycle, 5)   
                    color_cycle += 1
            except:
                print('Jumlah titik Koordinat yang harus anda masukkan adalah 4')
                region = []
                regions = []
                cv2.destroyAllWindows()
                cv2.namedWindow("draw region")
                img = frame.copy()
                cv2.setMouseCallback("draw region", click_event, {"img": img})

                cv2.putText(  # Display instructions
                    img,
                    "Click to define region. Press 'c' to clear. Press 'q' to finish and 'n' to next region",
                    (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    2,
                )
            cv2.imshow("draw region", img)

    cv2.destroyAllWindows()
    return region

# mas ini logika buat reshape nilai koordinat line
def reshape(frame, screen_width, screen_height, line):
    height, width, _ = frame.shape
    new_line = []

    for x in range(0, len(line), 4):
        x1, y1, x2, y2 = line[x:x+4]
        x1_new = (x1 * width) / screen_width
        x2_new = (x2 * width) / screen_width
        y1_new = (y1 * height) / screen_height
        y2_new = (y2 * height) / screen_height
        new_line.append(int(x1_new)) 
        new_line.append(int(y1_new))
        new_line.append(int(x2_new))
        new_line.append(int(y2_new))
        
    return new_line