## Building Env(if you haven't had one)
1. Enter the data directory
2. Create a virtual environment: `python -m venv myenv`
3. Install required modules: `pip install osmnx geopandas requests`

## Collecting Data
1. Activate the virtual environment: `.\myenv\Scripts\activate`
2. Run program: `python get_images_osmnx.py --city {city name} --output 256x256 --icount {your quota left} --key {your API key}`
3. Deactivate before leaving: `deactivate`

## Check List (3000 images for each city)
- [v] Keelung
- [ ] New Taipei
- [v] Taipei
- [v] Taoyuan
- [v] Hsinchu
- [v] Miaoli
- [v] Taichung
- [ ] Changhua
- [ ] Nantou
- [ ] Yunlin
- [ ] Chiayi
- [ ] Tainan
- [ ] Kaohsiung
- [ ] Pingtung
- [ ] Yilan
- [ ] Hualien
- [ ] Taitung
- [ ] Penghu
- [ ] Green Island
- [ ] Orchid Island
- [ ] Kinmen County
- [ ] Matsu
- [ ] Lienchiang