from django.shortcuts import render,redirect
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from PIL import Image
import numpy as np
import io
import base64
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request,"home.html")



def count_colors(image_data):
   
    
    # Reshape the array to be a list of pixels
    pixels = image_data.reshape(-1, image_data.shape[-1])
    
    # Use numpy to find unique rows (unique colors)
    unique_colors = np.unique(pixels, axis=0)
    
    # Return the number of unique colors
    return unique_colors.shape[0]

def compress(request):
    if request.method == 'POST':
        if('image' in request.FILES):
            num_colors = int(request.POST.get('num-colors'))
            
            image_file = request.FILES["image"]
            
            # Open the image
            img = Image.open(image_file)
            img = np.array(img)
            org_colors = count_colors(img)
            
            # Normalize and reshape the image
            org_img = img / 255.0
            org_img = org_img.reshape(img.shape[0] * img.shape[1], 3)
            
            # Perform KMeans clustering
            kmeans = MiniBatchKMeans(num_colors)
            kmeans.fit(org_img)
            new_colors = kmeans.cluster_centers_[kmeans.predict(org_img)]
            
            # Recolor the image
            img_recolored = new_colors.reshape(img.shape)
            
            # Convert to uint8 and save the new image
            img_recolored = (img_recolored * 255).astype(np.uint8)
            new_colors = count_colors(img_recolored)
            
            recolored_img = Image.fromarray(img_recolored)
            
            # Save the recolored image to a buffer
            buffer_recolored = io.BytesIO()
            recolored_img.save(buffer_recolored, format='PNG')
            buffer_recolored.seek(0)
            
            # Encode recolored image to base64
            img_recolored_base64 = base64.b64encode(buffer_recolored.read()).decode('utf-8')

            # Save the original image to a buffer
            buffer_original = io.BytesIO()
            Image.fromarray((org_img * 255).astype(np.uint8).reshape(img.shape)).save(buffer_original, format='PNG')
            buffer_original.seek(0)
            
            # Encode original image to base64
            img_original_base64 = base64.b64encode(buffer_original.read()).decode('utf-8')
            
            return render(request, 'new_image.html', {
                'original_image': img_original_base64, 
                'original_colors': org_colors,
                'output_image': img_recolored_base64, 
                'num_colors': num_colors
            })
        else:
            print("not in files")
        
    return redirect("home")