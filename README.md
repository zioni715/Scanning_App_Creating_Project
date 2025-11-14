# 📸➡️📄 Mini Scanner

A Streamlit-based document scanning application that automatically detects, crops, and processes documents from camera images using advanced computer vision techniques.

## ✨ Features

> **✨ Smart Document Detection**
> - 🔍 Automatic document contour detection using edge detection and contour analysis
> - 📐 Perspective transformation for perfect document alignment
> - 🎯 High-quality document warping

> **🎨 Multiple Scan Modes**
> - 🗞️ **Onix**: Vintage newspaper-style effect
> - 🌈 **Color**: Original color preservation
> - ⚪ **Gray**: Grayscale conversion
> - ⬛ **BW**: Black & White conversion

> **✂️ Document Processing**
> - 🖼️ Auto-crop functionality to remove unnecessary background
> - 💡 Shadow and lighting correction
> - ✨ CLAHE (Contrast Limited Adaptive Histogram Equalization) for enhanced clarity
> - 🎨 Colored note removal feature with visual mask display

> **📥 Download**
> - 💾 Download scanned documents as PNG files

## 🚀 Installation

> ### 📋 Prerequisites
> - 🐍 Python 3.7 or higher
> - 📦 pip package manager

> ### 🔧 Setup
>
> 1. 📥 Clone the repository:
> ```bash
> git clone https://github.com/zioni715/Scanning_App_Creating_Project.git
> cd Scanning_App_Creating_Project
> ```
>
> 2. 💻 Install required dependencies:
> ```bash
> pip install -r requirements.txt
> ```

## 📖 Usage

> ▶️ Run the Streamlit application:
> ```bash
> streamlit run app.py
> ```
>
> 🌐 The application will open in your browser at `http://localhost:8501`

> ### 📖 How to Use
>
> 1. 📁 **Upload Image**: Click "Choose an image..." and select a JPG, JPEG, or PNG file containing your document
> 2. ⚙️ **Configure Settings** in the sidebar:
>    - 🎯 **Select Scan Mode**: Choose your desired output format
>    - 📐 **Auto Crop Document**: Enable/disable automatic document cropping
>    - 🎨 **Remove Colored Notes**: Enable to remove highlighter marks and colored annotations
> 3. 👁️ **View Results**: See the original, warped, and final scanned documents
> 4. 💾 **Download**: Click the download button to save your scanned document

## 📁 Project Structure

> ```
> Scanning_App_Creating_Project/
> ├── app.py              # Main Streamlit application
> ├── functions.py        # Core image processing functions
> ├── requirements.txt    # Python dependencies
> └── README.md          # This file
> ```

## 📦 Dependencies

> - 👁️ **opencv-python**: Computer vision library for image processing
> - 🔢 **numpy**: Numerical computing library
> - 🌐 **streamlit**: Web application framework
> - 🖼️ **Pillow**: Python Imaging Library

## 🔬 Technical Details

> ### 🔍 Document Detection Algorithm
> 1. 🎨 Convert image to grayscale and apply Gaussian blur
> 2. 📍 Perform Canny edge detection
> 3. 📦 Find contours and identify the largest quadrilateral
> 4. 🔄 Apply perspective transformation to straighten the document

> ### 🖼️ Image Processing
> - 🌑 **Shadow Removal**: Uses median blur and image division for lighting correction
> - ✨ **Contrast Enhancement**: CLAHE improves clarity in grayscale mode
> - 🎨 **Colored Note Removal**: HSV color space analysis with morphological operations

> ### 📊 Output Modes
> - 🗞️ **Onix/Color**: RGB or BGR color preservation
> - ⚪ **Gray**: Grayscale with CLAHE enhancement
> - ⬛ **BW**: Binary black and white conversion

## 💡 Tips for Best Results

> - 💡 Ensure good lighting on the document
> - 📐 Position the document at a slight angle (not flat) for better edge detection
> - 📸 Use high-quality camera images (JPG or PNG)
> - 🎨 For colored notes removal, ensure the notes are distinct in color from the document

## 📜 License

> 📖 This project is open source and available under the MIT License.

## 👤 Author

> 👨‍💻 Created by zioni715

---

> 📧 For issues or feature requests, please open an issue on the GitHub repository.