import requests
from datetime import datetime

def front(imagepath, name="foo", date="bar"):
    """
    Args:
        url: fixed, corresponding to database storage.
        name(optional): String, specify the name for this image, default to 20201212_121212
        date(optional): datetime object, specify the date and time this image upload, default to now
        image: Bytes, buffer the image for upload

    Examples:
    >> from imageUpload import front
    >> front(imagepath="path/to/the/image.jpg or .png")

    """
    url = "http://140.112.183.138:3000/record/front/"
    image = open(imagepath, "rb")

    if name != "foo" and date != "bar":
        r = requests.post(url, data={"name": name, "date": date}, files={"image": image})
    else:
        r = requests.post(url, files={"image": image})

    if r.status_code == 200:
        print("Successully uploaded!")
        print(f"Responce time {r.elapsed.total_seconds()} s.")
    else:
        print(f"Error uploading... status code: {r.status_code}")

    image.close()


def side(section, imagepath, name="foo", date="bar", detection=False):
    """
    Args:
        url: fixed, corresponding to database storage.
        name(optional): String, specify the name for this image, default to 20201212_121212
        date(optional): datetime object, specify the date and time this image upload, default to now
        section: integer, specify the section this image belongs to
                A1~A8 = 1~8
                B1~B8 = 9~16
                ...
                F1~F8 = 41~48
        image: Bytes, buffer the image for upload
        detection (bool): determine whether immediate identification is required

    Examples:
    >> from imageUpload import side
    >> front(section=8, imagepath="path/to/the/image.jpg or .png")

    """

    url = "http://140.112.183.138:3000/record/side/"
    image = open(imagepath, "rb")


    data = {"section": section}
    if name != "foo":
        data["name"] = name
    if detection:
        data["detection"] = detection

    r = requests.post(url, data=data, files={"image": image})


    if r.status_code == 200:
        print("Successully uploaded!")
        print(f"Responce time {r.elapsed.total_seconds()} s.")
    else:
        print(f"Error uploading... status code: {r.status_code}")

    image.close()
