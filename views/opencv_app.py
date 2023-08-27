import base64
from io import BytesIO
import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os
import random
import pandas as pd

from components.utils import show_md_content

BACKGROUNDS_FOLDER = "assets/images/bg"
TINT_COLOR = (0, 0, 0)  # Black
TRANSPARENCY = .25  # Degree of transparency, 0-100%
OPACITY = int(255 * TRANSPARENCY)
PADDING = 100 #pixels
GRAY_COLOR = (128, 128, 128)  # Gray color (128, 128, 128) for gray text


def get_image_download_link(img):
	"""Generates a link allowing the PIL image to be downloaded
	in:  PIL image
	out: href string
	"""
	buffered = BytesIO()
	img.save(buffered, format="PNG")
	img_str = base64.b64encode(buffered.getvalue()).decode()
	href = f'<a download="Image.png" href="data:file/jpg;base64,{img_str}">Download PNG</a>'
	return href

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index = False, sheet_name='Sheet1',float_format="%.2f")
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_excel_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a download="download.xlsx" href="data:application/octet-stream;base64,{b64.decode()}" download="Your_File.xlsx">Download Excel file</a>' # decode b'abc' => abc

def get_csv_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a download="download.csv" href="data:file/csv;base64,{b64}">Download CSV file</a>'

def get_random_background_image():
    # Get a list of all files in the directory
    file_list = os.listdir(BACKGROUNDS_FOLDER)

    # Filter the list to keep only image files (you can add more extensions if needed)
    image_files = [f for f in file_list if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        raise FileNotFoundError("No image files found in the specified directory.")

    # Pick a random image file
    image_path = os.path.join(BACKGROUNDS_FOLDER, random.choice(image_files))
    return Image.open(image_path)

def generate_instagram_post(quote):
    # Set up image dimensions and background color
    width, height = 1080, 1080
    background_color = (255, 255, 255, 0)
    background_image = get_random_background_image()
    background_image = background_image.resize((width, height))

    # Create a new image
    image = Image.new('RGBA', (width, height), background_color)
    image.paste(background_image, (0, 0))

    # Set up font size and style
    font_size = 60
    font = ImageFont.truetype('arial.ttf', font_size)

    draw = ImageDraw.Draw(image)
    
    # Set text color (white text color remains for better readability on images)
    text_color = (255, 255, 255)

    draw = ImageDraw.Draw(image) 
    # Draw the quote text on the image
    #draw.text((x, y), quote, fill=text_color, font=font)

    # Split the text into multiple lines if it's too long to fit on a single line
    words = quote.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if draw.textsize(test_line, font=font)[0] <= width - 100:  # 40 is for some padding
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    text_width, text_height = draw.textsize(quote, font=font)

    # Calculate the height of the text box
    total_lines = len(lines)
    total_text_height = total_lines * text_height
    text_box_height = min(total_text_height, height // 2) + PADDING//2

    # Calculate the starting y-coordinate to center the text box vertically
    y_start = ((height - text_box_height) // 2)


    text_box_width = width - PADDING//2
    x1 = ((width - text_box_width) // 2) 
    y1 = ((height - text_box_height) // 2)  - PADDING//2
    x2 = x1 + text_box_width
    y2 = y1 + text_box_height + PADDING//2

    overlay = Image.new('RGBA', image.size, TINT_COLOR+(0,))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    draw.rectangle(((x1, y1), (x2, y2)), fill=TINT_COLOR+(OPACITY,))

    # Alpha composite these two images together to obtain the desired result.
    image = Image.alpha_composite(image, overlay)
    
    draw = ImageDraw.Draw(image) 

    shadow_offset = 5
    shadow_color = (0, 0, 0, 100)  # Shadow color (slightly transparent black)

    # Draw the quote text on the image, line by line
    for line in lines:
        line_width, line_height = draw.textsize(line, font=font)
        x = (width - line_width) // 2
        shadow_x = (width - draw.textsize(line, font=font)[0]) // 2 + shadow_offset
        draw.text((shadow_x, y_start + shadow_offset), line, fill=shadow_color, font=font)
        draw.text((x, y_start), line, fill=text_color, font=font)
        y_start += line_height


    # Write the text at the bottom right corner in gray color
    bottom_margin = 20
    text = "wooc.app"
    text_width, text_height = draw.textsize(text, font=font)
    text_x = width - text_width - bottom_margin
    text_y = height - text_height - bottom_margin
    draw.text((text_x, text_y), text, fill=GRAY_COLOR, font=font)

    image = image.convert("RGB") # Remove alpha for saving in jpg format.
    
    return image


def process_file(image_file, blur_rate, brightness_amount, apply_enhancement_filter, face_detection, classifier, scaleFactor, minNeighbors, minSize, RED, EXTRA_SPACE, resize_width, resize_height, interpolation_method):    
    #image = cv2.imread(image_file)

    original_image = Image.open(image_file)
    original_image = np.array(original_image)

    processed_image = blur_image(original_image, blur_rate)
    processed_image = brighten_image(processed_image, brightness_amount)

    if apply_enhancement_filter:
        processed_image = enhance_details(processed_image)
        
    if face_detection:
        classifier_path = cv2.data.haarcascades + 'haarcascade_'+classifier+'.xml'
        face_detector = cv2.CascadeClassifier(classifier_path)
        processed_image, rectangles = detect_faces(processed_image, face_detector, scaleFactor, minNeighbors, minSize, RED, EXTRA_SPACE)

    # st.text("Original Image vs Processed Image")
    # st.image([original_image, processed_image])

    if face_detection:
        new_size = (int(resize_width), int(resize_height))

        cropped_images = crop_rects(original_image, rectangles)
        for cropped_image in cropped_images:
            # st.image(cropped_image)
            resized_img = cv2.resize(cropped_image, new_size, interpolation = interpolation_method)
            # st.image(resized_img)

    return cropped_image, resized_img
def detect_faces(img, face_detector, scaleFactor, minNeighbors, minSize, color, extra_space):
    img = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
    rects = face_detector.detectMultiScale( gray, 
                                            scaleFactor=scaleFactor,
                                            minNeighbors=minNeighbors, 
                                            minSize=minSize, 
                                            flags=cv2.CASCADE_SCALE_IMAGE)

    # print(f'found {len(rects)} face(s)')
    
    return_rects = []

    for (x, y, w, h) in rects:
        
        extra_pixels = round(w*extra_space/100 if (w*extra_space/100) > (h*extra_space/100) else (h*extra_space/100))

        x1=(x-extra_pixels)
        y1=(y-extra_pixels)
        w1=(w+extra_pixels*2)
        h1=(h+extra_pixels*2)
        
        cv2.rectangle(img, (x1, y1, w1, h1), color, 2)
        cv2.putText(img, str((x1,y1,w1,h1)), (x - 5, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2) # creates green color text with text size of 0.5 & thickness size of 2

        return_rects.append((x1, y1, w1, h1))

    return img, return_rects

def crop_rects(img, rects):
    
    cropped_images = []

    for (x, y, w, h) in rects:
        cropped_image = img[y:y+h, x:x+w]
        cropped_images.append(cropped_image)
    
    return cropped_images

def brighten_image(image, amount):
    img_bright = cv2.convertScaleAbs(image, beta=amount)
    return img_bright


def blur_image(image, amount):
    blur_img = cv2.GaussianBlur(image, (11, 11), amount)
    return blur_img


def enhance_details(img):
    hdr = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
    return hdr

def main_loop():
    st.title("OpenCV Demo App")
    st.subheader("This app allows you to play with Image filters!")
    st.text("We use OpenCV and Streamlit for this demo")

    blur_rate = st.sidebar.slider("Blurring", min_value=0.5, max_value=3.5, value=1.5)
    brightness_amount = st.sidebar.slider("Brightness", min_value=-50, max_value=50, value=25)
    face_detection = st.sidebar.checkbox('Detect Faces', True)
    apply_enhancement_filter = st.sidebar.checkbox('Enhance Details')
    
    RED = (0, 0, 255)
    scaleFactor = st.sidebar.slider("Scale Factor", min_value=1.0, max_value=2.0, value=1.2)
    minNeighbors = st.sidebar.slider("Min Neighbors", min_value=1, max_value=10, value=4)
    min_face_size = st.sidebar.selectbox('Min Size', (2, 4, 8, 16, 24, 30, 60, 120), index=5)
    minSize = (min_face_size, min_face_size)
    EXTRA_SPACE = st.sidebar.slider("Extra Space", min_value=0, max_value=100, value=50)
    classifier = st.sidebar.selectbox('Classifier', ('frontalface_alt',
                                                     'frontalface_alt2',
                                                     'frontalface_alt_tree',
                                                     'frontalface_default',
                                                     'profileface',
                                                     'fullbody',
                                                     'upperbody',
                                                     'lowerbody',
                                                     'lefteye_2splits',
                                                     'righteye_2splits',
                                                     'eye',
                                                     'eye_tree_eyeglasses',
                                                     'smile'                                                     
                                                     ), index=0)
    
    interpolation_methods = {
    "nearest": cv2.INTER_NEAREST,
    "linear": cv2.INTER_LINEAR,
    "cubic": cv2.INTER_CUBIC,
    "area": cv2.INTER_AREA,
    "lanczos4": cv2.INTER_LANCZOS4
    }

    resizer_interpolation = st.sidebar.selectbox('Interpolation', interpolation_methods.keys(),index=4)

    resize_width = st.sidebar.text_input("Width (px)", "128")
    resize_height = st.sidebar.text_input("Height (px)", "128")

    image_file = st.file_uploader("Upload Your Image", type=['jpg', 'png', 'jpeg'])
    if not image_file:
        st.error("Not an image file")
    else:
            try:
                cropped_image, processed_image = process_file(image_file, blur_rate, brightness_amount, apply_enhancement_filter, face_detection, classifier, scaleFactor, minNeighbors, minSize, RED, EXTRA_SPACE, resize_width, resize_height, interpolation_methods[resizer_interpolation])
                st.image([cropped_image,processed_image])
            except:
                st.error("An error occurred")

    image_file_directory = st.text_input("Images Directory", "assets/images/photos")

    image_extensions = ['jpg', 'png', 'jpeg']
    is_image_file = lambda filename: any(filename.endswith('.' + ext) for ext in image_extensions)

    files = os.listdir(image_file_directory )
    st.write(str(len(files)) + " Files Found")
    files = [file for file in files if os.path.isfile(os.path.join(image_file_directory, file)) and is_image_file(file)]
    st.write(str(len(files)) + " Image Files Found")
    
    if st.button("Process All Files"):
        processed_files_path = os.path.join(image_file_directory,'processed')
        os.makedirs(processed_files_path, exist_ok=True)
        progress_bar = st.progress(0)
        processed_images = []

        for i, file in enumerate(files, start=1):
            st.write(file)
            try:
                cropped_image, processed_image = process_file(os.path.join(image_file_directory, file), blur_rate, brightness_amount, apply_enhancement_filter, face_detection, classifier, scaleFactor, minNeighbors, minSize, RED, EXTRA_SPACE, resize_width, resize_height, interpolation_methods[resizer_interpolation])
                processed_images.append(processed_image)
                st.image([cropped_image,processed_image])
                cv2.imwrite(os.path.join(processed_files_path,file), cv2.cvtColor(processed_image, cv2.COLOR_RGB2BGR))
            except Exception as e:
                st.error("An error occurred" + str(e))

            
            # update the progress bar
            progress_bar.progress(i / len(files))


        st.write("Files processed!")


def opencv_app(st):
    st.title('OpenCV')

    st.subheader("This app allows you to play with Image filters!")
    
    st.text("We use OpenCV and Streamlit for this demo")

    quote = st.text_input("Enter Quote")
    if quote != "":
        for i in range(0, 3):
            img = generate_instagram_post(quote)
            st.image(img, width=512)
            st.markdown(get_image_download_link(img), unsafe_allow_html=True)

    main_loop()
    