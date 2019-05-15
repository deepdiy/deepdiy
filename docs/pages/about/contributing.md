# Installation

------

## Executable Version:

1. Download **win64 portable version**: https://github.com/deepdiy/deepdiy/releases

2. **Unzip** and go to 

   ```
   ./path_of_downloaded_package/deepdiy/DeepDIY.exe 
   ```

   

3. **Double click** DeepDIY.exe , Done!

## Source Code Version:

### Method 1:

1. Clone this repository

2. Run setup from the repository root directory

   ```python
   python3 setup.py install
   ```

   

### Method 2:

1. Clone this repository

2. Install dependencies

   ```python
   pip install -r requirements.txt
   ```

3. Install kivy.garden.matplotlib

   ```
   garden install --kivy matplotlib 
   ```

   

## Notice:

For OS X users, you may need to install kivy and kivy-garden manually. The 'garden' command is available only after kivy-garden is installed successfully. Please refer to following page:

https://kivy.org/doc/stable/installation/installation-osx.html