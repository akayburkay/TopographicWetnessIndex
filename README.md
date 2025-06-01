# Topographic Wetness Index (TWI) Hesaplama

Bu Python uygulama, bir Dijital Yükseklik Modeli (DEM) raster verisi üzerinden Topographic Wetness Index (TWI) hesaplamak için WhiteboxTools, Rasterio ve NumPy kütüphanelerini kullanır.

## Girdi Verisi
- `merge_dem.tif`: Projeksiyonu tanımlı dijital yükseklik modeli raster dosyası.

## İşlem Adımları

1. **Çukurların Doldurulması (Sink Fill):**  
   DEM üzerindeki hidrolik çukurlar `WhiteboxTools.fill_depressions()` fonksiyonu ile doldurulur (`fix_flats=True`).

2. **Akış Yönü Hesaplama (Flow Direction):**  
   Doldurulmuş DEM kullanılarak D8 algoritması ile her pikselin akış yönü `d8_pointer()` fonksiyonu ile hesaplanır.

3. **Akış Birimi Hesaplama (Flow Accumulation):**  
   Akış yönü verisi kullanılarak `d8_flow_accumulation()` ile her hücreye gelen katkı alanı (`specific contributing area`) hesaplanır.

4. **Eğim Hesaplama (Slope):**  
   `slope()` fonksiyonu ile DEM'den radyan cinsinden eğim hesaplanır (`units='radians'`, `zfactor=1.0`).

5. **TWI Hesaplama:**  
   `Rasterio` ve `NumPy` ile flow accumulation ve eğim rasterları okunur.  
   Eğim değeri çok küçükse (0.0001'den küçük) bölme hatalarını önlemek için minimum eşik değeri atanır.  
   TWI, şu formülle hesaplanır:

  TWI=ln( flow_accumulation /
          tan(slope) ​)

## Üretilen Dosyalar

- `filled_dem.tif`: Doldurulmuş DEM  
- `flow_direction.tif`: Akış yönü (D8) rasterı  
- `flow_accumulation.tif`: Akış birimi (specific contributing area) rasterı  
- `slope_radians.tif`: Eğim rasterı (radyan)  
- `twi.tif`: Topographic Wetness Index rasterı

## Gereksinimler

- Python 3.7+
- [WhiteboxTools](https://www.whiteboxgeo.com/)
- rasterio
- numpy

### Kurulum

```bash
pip install rasterio numpy
