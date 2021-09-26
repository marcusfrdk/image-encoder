import argparse
import os
import time

def get_arguments() -> dict:
    parser = argparse.ArgumentParser(description="Encode strings or files to an image as JSON.", usage="encode.py path")
    parser.add_argument("image", help="path to the image to be encoded.")
    parser.add_argument("data", help="data to be encoded, if the string is a path, the file will be encoded, else the provided string will be used.")
    parser.add_argument("-n", "--name", dest="name", metavar="", help="saves the encoded image with the name, will overwrite any existing file with the same name.")
    return parser.parse_args()


def extract_path(path: str) -> tuple:
    prepath = ""
    name = ""
    extension = ""

    # Get prepath
    if "/" in path:
        prepath = "".join([f"{x}/" for x in path.split("/")[0:-1]])

    # Get name
    if "." in path:
        name = path.split(".")[-2].replace("/", "")

        # Get extension
        extension = path.split(".")[-1]

    return prepath, name, extension


def encode(args: dict, input: str) -> None:
    try:
        lines = open(args.path, "rb").readlines()
        prepath, name, extension = extract_path(args.path)

        new_name = name + "-encoded" + f".{extension}"
        number = 1

        if args.name:
            new_name = args.name + f".{extension}"
        else:
            # Make sure file does not exist
            while os.path.exists(new_name):
                new_name = name + "-encoded" + f"-{number}" + f".{extension}"
                number += 1

        # Encoode file
        with open(new_name, "wb") as encoded_image:
            encoded_image.writelines(lines)
            encoded_image.write(bytes(input, "utf-8"))
            encoded_image.close()
    except:
        print("Failed to encode image, please try again.")


# def get_encoded_data(image: str) -> str:
#     encoded_data = ""

#     with open(image, "rb") as f:
#         content = f.read()
#         offset = content.index(bytes.fromhex("FFD9"))

#         f.seek(offset + 2)
#         encoded_data = bytes.decode(f.read())

#     return encoded_data


def parse_data(data: str) -> str:
    is_file = os.path.isfile(data)
    result = data
    if is_file:
        with open(data) as f:
            result = f.read()
    return result


def format_data(data: str) -> bytes:
    is_file = os.path.isfile(data)
    file_type = data.split(".")[-1] if "." in data and is_file else ""
    encoded_at = time.time()

    return bytes(str({
        "file_type": file_type,
        "encoded_at": encoded_at,
        "data": parse_data(data)
    }), "utf-8")


def validate_image(path: str) -> bool:
    valid_extensions = ("jpg", "jpeg", "png")

    is_file = os.path.isfile(path)
    extension_is_valid = path.split(".")[-1] in valid_extensions \
        if "." in path else False

    return is_file and extension_is_valid


def encode_image(args: dict)  -> None:
    data = format_data(args.data)

    # Get image and remove encoding
    image = ""
    with open(args.image, "rb") as of:
        content = of.read()
        offset = content.index(bytes.fromhex("FFD9")) + 2
        image = content[0:offset]
        of.close()

    with open("test.jpg", "wb") as nf:
        nf.write(image + data)
        nf.close()


def main() -> None:
    args = get_arguments()

    if validate_image(args.image):
        encode_image(args)
    else:
        print("Image is not valid.")
        


if __name__ == "__main__":
    main()