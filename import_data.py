from dataclasses import dataclass


@dataclass
class Hour:
    '''Records an hour's weather report, with a field for each value in the EPA dataset. 
       See definitions for most units.'''
    # !   2    002 - 011  Date                   yyyy-mm-dd             Integer     i4,1x,i2,1x,i2
    date: str
    # !   3    012 - 014  *Hour of the day       Hour                   Integer     i3
    hour: int
    # !   4    016 - 021  Extraterrestrial       *Wh/m2                 Integer     i5,a1    
    # !                    Horizontal
    # !                    Radiation (Ra)
    ehr: int
    # !   5    023 - 028  Extraterrestrial       Wh/m2                  Integer     i5,a1
    # !                    Direct Normal Radiation
    ednr: int
    # !   6    030 - 037  Global Horizontal      Wh/m2                  Integer     i5,a3
    # !                    Radiation (Rs)
    ghr: int
    # !   7    039 - 046  Direct Normal          Wh/m2                  Integer     i5,a3
    # !                    Radiation
    dnr: int
    # !   8    048 - 055  Diffuse Horizontal     Wh/m2                  Integer     i5,a3
    # !                    Radiation
    dhr: int
    # !   9    057 - 059  Total Sky Cover        tenths of sky covered  Integer     i2,a1
    total_sky_cover: int
    # !  10    061 - 063  Opaque_Sky_Cover       tenths of sky covered  Integer     i2,a1
    opaque_sky_cover: int
    # !  11    065 - 070  Dry Bulb Temperature   degrees Centigrade     Real        f5.1,a1
    dry_bulb_temp_c: float
    # !  12    072 - 077  Dew Point Temperature  degrees Centigrade     Real        f5.1,a1
    dew_point_temp_c: float
    # !  13    079 - 082  Relative_Humidity      percent                Integer     i3,a1
    relative_humidity: int
    # !  14    084 - 089  Station_Pressure       *kPa                   Real        f5.1,a1
    station_pressure: float
    # !  15    091 - 094  Wind_Direction         degrees(N=0,E=90,...)  Integer     i3,a1
    wind_direction: int
    # !  16    096 - 101  Wind_Speed @10meter    m/s                    Real        f5.1,a1
    wind_speed: float
    # !  17    103 - 109  Horizontal Visibility  km                     Real        f6.1,a1
    h_visibility: float
    # !  18    111 - 117  Ceiling Height         m                      Integer     i6,a1
    ceiling_height: int
    # !  19    119 - 120  Observation Indicator  N/A                    Integer     i1,a1
    observation_indicator: int
    # !  20    122 - 131  Present_weather        N/A                    Character   a9,a1
    present_weather: str
    # !  21    133 - 136  Precipitable Water     mm                     Integer     i3,a1
    precipitable_Water: int
    # !  22    138 - 144  Broadband Aerosol      Optical_Depth          Real        f6.3,a1
    broadband_aerosol: float
    # !  23    146 - 150  Snow Depth             cm                     Integer     i4,a1
    snow_depth: int
    # !  24    152 - 155  Days since last        day                    Integer     i3,a1
    # !                    Snowfall
    days_since_last_snowfall: int
    # !  25    157 - 164  Hourly Precipitation   cm                     Real        f6.2,a2
    hourly_precipitation: float
    # !  26    166 - 172  Eto, FAO Short Grass   mm/day                 Real        f6.2,a1
    eto_fao_short_grass: float
    # !  27    174 - 180  Ep, Class A pan        mm/day                 Real        f6.2,a1
    # !                     Evaporation
    ep_class_a_pan_evaporation: float

def slice_spec(line: str, spec_start, spec_end): 
    '''split() will discard the leading empty-space character, so the starting indexes 
    here are off by _2_ when compared to the metadata file's specification, which starts 
    indexes at 1, not 0. Ending indexes are off by _1_, because Python's slicing is not 
    inclusive of the ending index.'''
    result = line[(spec_start-2):(spec_end-1)] 
    print(f'slice_spec: {spec_start}:{spec_end} -> {result}')
    return result   

def read_hourly_file(year_2digits: str, location: str, loc_id: str): 
    '''Read in an EPA hourly datafile, returning a dictionary of hourly records
       with '''
    filename = f'w{loc_id}.h{year_2digits}'
    filepath = f'data/{location}/hourly/{filename}'
    data_file = open(filepath, "r", encoding="UTF-8")

    # Discard the header information (time zone, latitude, etc.) unless it's needed.
    header_row: str = data_file.readline()
    
    for row in data_file.readlines():
        # Use slice_spec so that the numbers here at a glance match what's given in the metadata. 
        hour_data = Hour(      slice_spec(row,   2,  11),
                         int(  slice_spec(row,  12,  14)),
                         int(  slice_spec(row,  16,  21)),
                         int(  slice_spec(row,  23,  28)),
                         int(  slice_spec(row,  30,  37)), # TODO: handle character-codes
                         int(  slice_spec(row,  39,  46)),
                         int(  slice_spec(row,  48,  55)),
                         int(  slice_spec(row,  57,  59)),
                         int(  slice_spec(row,  61,  63)),
                         int(  slice_spec(row,  65,  70)),
                         int(  slice_spec(row,  72,  77)),
                         int(  slice_spec(row,  79,  82)),
                         float(slice_spec(row,  84,  89)),
                         int(  slice_spec(row,  91,  94)),
                         int(  slice_spec(row,  96, 101)),
                         int(  slice_spec(row, 103, 109)),
                         int(  slice_spec(row, 111, 117)),
                         int(  slice_spec(row, 119, 120)),
                               slice_spec(row, 122, 131),
                         int(  slice_spec(row, 133, 136)),
                         int(  slice_spec(row, 138, 144)),
                         int(  slice_spec(row, 146, 150)),
                         int(  slice_spec(row, 152, 155)),
                         int(  slice_spec(row, 157, 164)),
                         float(slice_spec(row, 166, 172)), # TODO: last 2 fields are daily; not present except if hour is 25
                         float(slice_spec(row, 174, 180)))
        print(hour_data)
        exit()

if __name__ == '__main__':
    read_hourly_file('75', 'worcester', '94746')