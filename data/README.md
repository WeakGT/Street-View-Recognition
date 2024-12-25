

## Building Env(if you haven't had one)
1. Enter the data directory
2. Create a virtual environment: `python -m venv myenv`
3. Install required modules: `pip install osmnx geopandas requests`

## Collecting Data
1. Activate the virtual environment: `.\myenv\Scripts\activate`
2. Run program: `python get_images_global.py --city {city name} --country {country name} --output 256x256_global --icount {your quota left} --key {your API key}`
3. Deactivate before leaving: `deactivate`

## Check List (global ver.)
about 1000 images for each city (country)
`v`: 1000 images

- Asia
[v] Bangkok (Thailand)
[v] New Delhi (India)

- Europe
[v] Paris (France)
[v] Helsinki (Finland)

- America
[v] New York (United States)
[v] Toronto (Canada)

- Africa
[v] Gauteng (South Africa)
[v] Nairobi (Kenya)

- Australia
[v] Sydney (Australia)
[v] Auckland (New Zealand)