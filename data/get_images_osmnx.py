'''
[Environment setting] (using virtual environment)
.\{your_path_name}\Scripts\activate

[run the program]
python get_images_osmnx.py --city {city name} --output 256x256_global --icount {your quota left} --key {your API key}

[leave virtual environment]
deactivate
'''


# code starts here
'''
import osmnx as ox
import geopandas as gpd
import requests         # HTTP req for API
import os               # filesys
import csv
import random
import argparse
from csv import writer

# step_size =  0.001

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", help="The city name you want to generate GPS coordinates from", required=True, type=str)
    parser.add_argument("--output", help="The output folder where the images will be stored, (defaults to: 256x256/)", default='256x256/', type=str)
    parser.add_argument("--icount", help="The amount of images to pull (defaults to 10)", default=10, type=int)
    parser.add_argument("--key", help="Your Google Street View API Key", type=str, required=True)
    return parser.parse_args()

args = get_args()
url = 'https://maps.googleapis.com/maps/api/streetview'
start_from = 0

def main():

    # Open and create all the necessary files & folders
    os.makedirs(args.output, exist_ok=True)
    file_path = os.path.join(args.output, 'picture_coords.csv')
    if not os.path.exists(file_path):
        start_from = 0
        coord_output_file = open(file_path, 'w', newline='')
        csv_writer = writer(coord_output_file)
        csv_writer.writerow(['index', 'latitude', 'longitude', 'city'])
    else:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            start_from = sum(1 for row in reader) - 1  # Subtract 1 to exclude the header row
        coord_output_file = open(file_path, 'a', newline='')
        csv_writer = writer(coord_output_file)

    # create the graph G
    G = ox.graph_from_place(args.city + ", Canada", network_type = 'drive')
    Gp = ox.project_graph(G)
    
    total_request = successful_data = 0
    while(True):    # 在配額用完前盡量跑
        if total_request >= (args.icount-5):    # 如果配額快達標就不要抓了
            break

        # get some random point in the graph G
        points = ox.utils_geo.sample_points(ox.convert.to_undirected(Gp), 100) # generate some random point
        points_gdf = gpd.GeoSeries(points, crs=Gp.graph['crs'])
        points_latlon = points_gdf.to_crs(epsg=4326)

        # get image of each point
        for point in points_latlon:
            if total_request >= (args.icount-5):    # 如果配額快達標就不要抓了
                break
            print('request', total_request)
            total_request = total_request + 1
            lon = round(point.x, 4)
            lat = round(point.y, 4)
            print(f"Longitude: {lon}, Latitude: {lat}")
            addressLoc = (lat, lon)

            # Set the parameters for the API call to Google Street View
            heading = str(90 * random.randint(0, 3))
            params = {
                'key': args.key,
                'size': '256x256',
                'source': 'outdoor',
                'location': str(addressLoc[0]) + ',' + str(addressLoc[1]),  # 注意這裡的順序，latitude 在前
                'heading': heading,
                'pitch': '-20',
                'fov': '90'
            }

            response = requests.get(url, params)
            # coordinate w/ no images
            if len(response.content) < 10000:
                # handle the non-existing image
                print(f"{addressLoc} No image available. Received blank images.")
                continue
            
            else:   
                # Save the first image to the output folder
                with open(os.path.join(args.output, f'streetview{start_from + successful_data}_{heading}.jpg'), "wb") as file:
                    file.write(response.content)
                # Save the coordinates to the output file
                csv_writer.writerow([start_from + successful_data, f'streetview{start_from + successful_data}_{heading}.jpg', addressLoc[0], addressLoc[1], "Canada"])  # 注意這裡的順序，latitude 在前
                print(f"{addressLoc} Received image successfully.")            
                
                
                # get the images of other angles
                # for angle in [90, 180, 270]:
                    # Set the parameters for the API call to Google Street View
                #    params = {
                #        'key': args.key,
                #        'size': '640x640',
                #        'source': 'outdoor',
                #        'location': str(addressLoc[0]) + ',' + str(addressLoc[1]),  # 注意這裡的順序，latitude 在前
                #        'heading': str(angle),
                #        'pitch': '-20',
                #        'fov': '90'
                #    }
                #   response = requests.get(url, params)
                #    if len(response.content) < 10000:
                #        # handle the non-existing image
                #        print(f"{addressLoc}, {angle} Error: No image available. Received blank images.")
                #        continue
                #    else:
                #        # Save the image to the output folder
                #        with open(os.path.join(args.output, f'streetview{start_from + successful_data}_{angle}.jpg'), "wb") as file:
                #            file.write(response.content)
                
                successful_data = successful_data + 1
                # total_request = total_request + 3


    coord_output_file.close()
    print(f"\nProcess is done, total request = {total_request}, successful data = {successful_data}(hit rate = {round(successful_data/total_request, 4)})")
    print("    !!! Please remember to deactivate the env before leaving !!!\n")

if __name__ == '__main__':
    main()
'''