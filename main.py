import streamlit as st
import numpy as np
from PIL import Image
import seam_carving


def main():
    st.title("Image Resizer")
    original_img = st.file_uploader("Upload an image to resize", type=['jpg','jpeg','png'])
    with open('sample.jpg', "rb") as file:
        btn = st.download_button(label="Download a sample image to upload",data=file,file_name="sample.jpg")
    st.write("Note:  The program only implements shrinking the dimensions of an image.")
    if original_img is not None:
        uploaded(original_img)

def uploaded(original_img):
    image = Image.open(original_img).convert('RGB')
    o_height, o_width, _ = np.array(image).shape
    st.write("Uploaded image size (width x height): ",o_width,' x ', o_height)
    st.write("Please set the desired width and height of the resized image.")
    width = st.text_input('Width', placeholder='e.g. 300')
    height = st.text_input('Height', placeholder='e.g. 300')
    genre = st.radio("resized image file format",('jpg', 'png'))
    button_pressed = st.button('Resize')
    if height.isdigit() and width.isdigit():
        if o_height < int(height):
            st.write('<span style="color:red;">Error: Please set the height to be no greater than the original height ('+str(o_height)+').</span>',unsafe_allow_html=True)
        elif o_width < int(width):
            st.write('<span style="color:red;">Error: Please set the width to be no greater than the original width ('+str(o_width)+').</span>',unsafe_allow_html=True)
        elif button_pressed:
            placeholder = st.empty()
            placeholder.text(" Resizing... \nline This could take a couple of minutes (or more).")
            placeholder.text("Resizing... \nThis could take a couple of minutes (or more).")
            im = Image.fromarray(seam_carving.resize(np.array(image), (int(width), int(height)),energy_mode='backward',keep_mask=None))
            placeholder.empty()
            file_path = 'resized.jpg'
            if genre in ['png','PNG']:
                file_path = 'resized.png'
            im.save(file_path)
            with open(file_path, "rb") as file:
                btn = st.download_button(label="Download the resized image",data=file,file_name=file_path)
            st.image(im, caption='resized image', use_column_width='auto')

if __name__ == '__main__':
    main()
