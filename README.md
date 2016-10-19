# kk-dailies-slate
Fast cross platform ffmpeg based utility for generating movie files for video production review sessions.

Dailies utility can generate movie with cutomizable slate image on zero frame and frame burnins. Movie format can be specified via video pressets listed in `config.yml`. Optional LUT file can be applied to generated mov.

Instalation:
```
# Clone this repo
git clone https://github.com/Kif11/kk-dailies dailies
cd dailies

# Make run script executable
sudo chmod +x run

# Install dependencies
./run setup

To run test
./run test
```
Check `./tests/tmp` folder for generated movie

Usage:
```
values = {
    'company_name': 'CompanyName',
    'project_name': 'ZeroDayProject',
    'lut': 'someLutHere',
    'shot_name': 'sh0000',
    'file_name': 'blaFileName.png',
    'fps': '24',
    'frame_range': '1001-1100',
    'frame_total': '100',
    'handles': '5/5',
    'comp_res': '1920x1080',
    'date': '21/10/1900',
    'user': 'Kif11',
    'description': 'Some comment here',
}

slate = Dailies()
slate.fields_from_dict(values)

slate.make_mov('/path/sh0000_test_v003_%04d.jpg', 'out_video_pjpeg.mov', preset='pjpeg', lut='some_lut.cube')
```
