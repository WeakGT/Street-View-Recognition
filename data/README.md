

## Building Env(if you haven't had one)
1. Enter the data directory
2. Create a virtual environment: `python -m venv myenv`
3. Install required modules: `pip install osmnx geopandas requests`

## Collecting Data
1. Activate the virtual environment: `.\myenv\Scripts\activate`
2. Run program: `python get_images_global.py --city {city name} --country {country name} --output 256x256_global --icount {your quota left} --key {your API key}`
3. Deactivate before leaving: `deactivate`

## Check List (global ver.)
about 5000 images for each city (country)
`v`: 5000 images


- Asia
[] Bangkok (Thailand)
[] New Delhi (India)

- Europe
[] Paris (France)
[] Helsinki (Finland)

- America
[] New York (United States)
[] Toronto (Canada)

- Africa
[] Gauteng (South Africa)
[] Nairobi (Kenya)

- Australia
[] Sydney (Australia)
[] Auckland (New Zealand)