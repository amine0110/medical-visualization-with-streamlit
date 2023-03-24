# Medical Images Visualization With Streamlit
In this small project, I will show you how you can use Streamlit and VTK to create a simple 3D visualizer that allows you to upload and visualize `NIFTI` files.


<p align="center">
  <img width="660" height="200" src="https://user-images.githubusercontent.com/37108394/206930410-4cf11236-9a59-4310-b809-3dccc8fd1f8f.png">
</p>

------------------------------------------------------------------------------

![image](https://user-images.githubusercontent.com/37108394/206930183-213929fd-0cab-4010-9791-a1bd0ddc99bc.png)
![image](https://user-images.githubusercontent.com/37108394/206930211-45fe3aea-2ff4-4551-8394-168de2655de6.png)
![image](https://user-images.githubusercontent.com/37108394/206930266-c2fc3fb5-b2b5-463a-a3f4-1c4b7f5d9098.png)

------------------------------------------------------------------------------
## Packages
- `pip install streamlit`
- `pip install streamlit-lottie`
- `pip install vtk`
- `pip install ipywidgets`
- `pip install itkwidgets`
- `pip install requests`
- `pip install glob2`
- `pip install pytest-shutil`

## Run locally
If you don't know how to host the application online, then you can host it and run it locally. These are the steps:
- Clone the repository: 
```
git clone https://github.com/amine0110/medical-visualization-with-streamlit
```
- Install the [Packages](https://github.com/amine0110/medical-visualization-with-streamlit/blob/main/README.md#packages) discussed above.
- Run the command:
```
streamlit run .\main.py
```

## Visualization only
If you are looking only to visualize the NIFTI files without having all the other options, then this is the part that you need to focus on:

```Python
path_to_file = glob(f'{temp_data_directory}/*.nii.gz')
if path_to_file:
    with st.container():
        reader = vtk.vtkNIFTIImageReader()
        reader.SetFileName(path_to_file[0])
        reader.Update()

        view_width = 1800
        view_height = 1600

          snippet = embed.embed_snippet(views=view(reader.GetOutput()))
          html = embed.html_template.format(title="", snippet=snippet)
          components.html(html, width=view_width, height=view_height)
```

## 📩 Newsletter
Stay up-to-date on the latest in computer vision and medical imaging! Subscribe to my newsletter now for insights and analysis on the cutting-edge developments in this exciting field.

https://pycad.co/join-us/

## 🆕 New
Learn how to effectively manage and process DICOM files in Python with our comprehensive course, designed to equip you with the skills and knowledge you need to succeed.

https://www.learn.pycad.co/course/dicom-simplified
