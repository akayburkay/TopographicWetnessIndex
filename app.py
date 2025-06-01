from whitebox.whitebox_tools import WhiteboxTools
import rasterio
import numpy as np

# WhiteboxTools nesnesi oluştur
wbt = WhiteboxTools()

input_dem = r"C:\Users\Msi\Desktop\dem_raster\merge_dem.tif"
output_filled = r"C:\Users\Msi\Desktop\dem_raster\filled_dem.tif"

# Sink fill işlemi (çukurları doldurmak amacıyla)
wbt.fill_depressions(
    input_dem,
    output_filled,
    fix_flats=True
)
print("✅ Sink fill işlemi tamamlandı:", output_filled)

flow_dir = r"C:\Users\Msi\Desktop\dem_raster\flow_direction.tif"
# Akış yönü hesaplaması
wbt.d8_pointer(
    output_filled,
    flow_dir
)
print("✅ Akış yönü (D8) hesaplandı:", flow_dir)

flow_accum = r"C:\Users\Msi\Desktop\dem_raster\flow_accumulation.tif"
# Akış birimi hesaplaması
wbt.d8_flow_accumulation(
    flow_dir,
    flow_accum,
    out_type='specific contributing area'
)
print("✅ Akış birimi hesaplandı:", flow_accum)

output_slope = r"C:\Users\Msi\Desktop\dem_raster\slope_radians.tif"
# Eğim hesaplaması (radyan cinsinden)
wbt.slope(
    output_filled,
    output_slope,
    zfactor=1.0,
    units='radians'
)
print("Eğim hesaplandı:", output_slope)


twi_output = r"C:\Users\Msi\Desktop\dem_raster\twi.tif"
with rasterio.open(flow_accum) as fa_srs:
    flow_accum_data = fa_srs.read(1).astype("float32")
    profile = fa_srs.profile

with rasterio.open(output_slope) as slope_srs:
    slope_data = slope_srs.read(1).astype("float32")

slope_data[slope_data < 0.0001] = 0.0001

with np.errstate(divide='ignore', invalid='ignore'):
    twi = np.log(flow_accum_data / np.tan(slope_data))

twi = np.where(np.isfinite(twi), twi, np.nan)

# Metadata güncelleme
profile.update(dtype=rasterio.float32, count=1, compress='lzw')

with rasterio.open(twi_output, 'w', **profile) as dst:
    dst.write(twi.astype(rasterio.float32), 1)

print("✅ TWI hesaplandı ve kaydedildi:", twi_output)
