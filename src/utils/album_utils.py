import cv2
from src.utils.image_utils import show_image

def show_album(images: list[str], album_date: str, max_width: int, max_height: int):

  photo_index = 0
  photos_length = len(images)

  show_photos = True
  while show_photos:
    image_filename = images[photo_index]

    window_name = f"{album_date} - Photo #{photo_index + 1}"
    show_image(image_filename, window_name, max_width, max_height)

    k = cv2.waitKey(33)
    if k == ord('q'):
      show_photos = False
      cv2.destroyWindow(window_name)
    elif k == ord('n'):
      cv2.destroyWindow(window_name)
      photo_index = (photo_index + 1) % photos_length
      continue
