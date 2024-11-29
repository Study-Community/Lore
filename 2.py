from PIL import Image

def resize_image(input_path, output_path, width, height):
    try:
        img = Image.open(input_path)
        img = img.resize((width, height))
        img.save(output_path)
        print(f"Image resized and saved to {output_path}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    input_path = input("Enter the input image path: ")
    output_path = input("Enter the output image path: ")
    width = int(input("Enter the width: "))
    height = int(input("Enter the height: "))
    resize_image(input_path, output_path, width, height)