from dailies import Dailies
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
test_seq = os.path.join(script_dir, 'jpg_seq', 'sh0000_test_v003_%04d.jpg')
tmp_dir = os.path.join(script_dir, 'tmp')
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)
out_mov_pjpeg = os.path.join(tmp_dir, 'out_video_pjpeg.mov')
out_mov_dnxhd = os.path.join(tmp_dir, 'out_video_dnxhd.mov')


values = {
    'company_name': 'Company Name',
    'project_name': 'Zero Day Project',
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

slate.make_mov(test_seq, out_mov_pjpeg, preset='pjpeg')
# slate.make_mov(test_seq, out_mov_dnxhd, preset='dnxhd')
