def _save_image(img):
    filename = input("filename [test.jpg]: ")
    img.save(filename if len(filename) > 0 else "test.jpg")

def _save_image(img, filename):
    img.save(filename)

