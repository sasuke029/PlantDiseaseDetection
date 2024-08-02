from django.http import JsonResponse
from django.shortcuts import render
from rembg import remove
import os
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
from django.conf import settings
from torch.nn import functional as F
from django.contrib.auth.decorators import login_required


# Create your views here.

# Load CSV data
disease_info = pd.read_csv(os.path.join(settings.BASE_DIR, 'tomato_disease_info (2).csv'), encoding='cp1252')
supplement_info = pd.read_csv(os.path.join(settings.BASE_DIR, 'supplement_info.csv'), encoding='cp1252')

# Load the CNN model
# Load the state dictionary with map_location set to 'cpu'
state_dict_path = os.path.join(settings.BASE_DIR, "plant_disease_model_1_latests.pt")
state_dict = torch.load(state_dict_path, map_location=torch.device('cpu'))
# Load the CNN model

model = CNN.CNN(11)
model.load_state_dict(state_dict)
model.eval()

@login_required(login_url="/authentication/login")
def index(request):
    context={}
    return render(request, 'prediction/index.html',context)


def prediction(image_path, model,threshold=0.6):
    try:
        image = Image.open(image_path)
        # Remove the background (if not already done in submit)
        image = remove(image)
        
        # Convert image to RGB if it has more than 3 channels
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        image = image.resize((224, 224))
        input_data = TF.to_tensor(image)
        
        # Check tensor shape after conversion
        print("Input tensor shape after conversion:", input_data.shape)
        
        # Reshape input_data if necessary
        if len(input_data.shape) == 3:
            input_data = input_data.unsqueeze(0)  # Add batch dimension if missing
        
        # Perform prediction
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        input_data = input_data.to(device)
        
        model.eval()
        with torch.no_grad():
            output = model(input_data)
            probabilities = F.softmax(output, dim=1)
            probabilities = probabilities.cpu().numpy()  # Move to CPU before converting to numpy
            index = np.argmax(probabilities)
            confidence = probabilities[0, index] # Convert to percentage

            if confidence < threshold:
                print(confidence)
                print("Confidence not achieved.")
                return -1,0.0
        
        return index, confidence
    except Exception as e:
        print("Error occurred during prediction:", e)
        return -1, 0.0


@login_required(login_url="/authentication/login")
def submit(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES['image']
        filename = image.name
        original_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
        
        os.makedirs(os.path.dirname(original_file_path), exist_ok=True)

        # Save the original image
        with open(original_file_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        # Open the saved image
        image = Image.open(original_file_path)
        
        # Remove the background
        image = remove(image)

         # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save the image after background removal
        processed_file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', f"{filename}")
        image.save(processed_file_path)

        # Pass processed_file_path to the prediction function
        index, confidence = prediction(processed_file_path, model)

        print(index)
        print(confidence)

        # Retrieve information based on prediction
        if index != -1:
            title = disease_info['disease_name'][index]
            description = disease_info['description'][index]
            prevent = disease_info['Possible Steps'][index]
            supplement_name = supplement_info['supplement name'][index]
            supplement_image_url = supplement_info['supplement image'][index]
            supplement_buy_link = supplement_info['buy link'][index]

            special_values = [3, 5, 7, 11, 15, 18, 20, 23, 24, 25, 28, 38]
            image_url = os.path.join(settings.MEDIA_URL, 'uploads', f"{filename}")

            # Prepare context data to pass to the template
            context = {
                'title': title,
                'desc': description,
                'prevent': prevent,
                'image_url': image_url,
                'pred': index,
                'sname': supplement_name,
                'simage': supplement_image_url,
                'buy_link': supplement_buy_link,
                'special_values': special_values,
                'confidence':confidence
            }
            
            # Render the submit.html template with the context data
            return render(request, 'prediction/submit.html', context)
        else:
            print("Error: Prediction index is None")
            # Optionally, you can pass an error message to the template
            context = {
                'error': "Prediction failed. Did not cross the threshold."
            }
            return render(request, 'prediction/error.html', context)
    
    # Render the submit.html template without any context data if the request method is not POST or 'image' is not in request.FILES
    return render(request, 'prediction/submit.html')