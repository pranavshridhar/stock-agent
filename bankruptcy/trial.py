import kaggle

# Download latest version
path = kaggle.dataset_download("fedesoriano/company-bankruptcy-prediction")

print("Path to dataset files:", path)