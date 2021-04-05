# Loading file, and obtaining long name components 
path = "./testfolder"
data_list = os.listdir(path) # Create a list of all files in the folder

current_file = data_list[2]
print(f"The file being used is {current_file}.")
components = current_file.split("_")
latticeT = components[0]
