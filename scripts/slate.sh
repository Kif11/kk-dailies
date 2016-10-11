#! /bin/bash

CURDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

PROJECT_NAME=Bolden
COMPANY_NAME='Company Name'
TARGET="$CURDIR/10framesDPX/test_image_seq_v003_%04d.dpx"
FILE_NAME=$(basename "$TARGET")
START_FRAME=1
OUTPUT_IMG="./tmp_slate.png"
LOGO="resources/logo.png"
LOGO_FONT_FILE="resources/lunatix.otf"
FONT_FILE="resources/liberationsans_regular.ttf"
BARS="resources/bars.png"
COLOR_BARS="resources/cbar.png"
FONT_SIZE=40
FONT_COLOR="White"
LINE_SPACING=40
TOP_TEXT_MARGIN=380
LEFT_TEXT_MARGIN=(w)/2+150
LUT="/Users/kif/Desktop/eep_slate/bdn_all_log2vid_3D_16_v004.dat"

P="x=${LEFT_TEXT_MARGIN}-text_w:y=${TOP_TEXT_MARGIN}+$LINE_SPACING"
TEXT="drawtext=fontsize=${FONT_SIZE}:fontcolor=${FONT_COLOR}:fontfile='${FONT_FILE}':text"

# Find image demensions
eval $(ffprobe -v error -of flat=s=_ -select_streams v:0 -start_number $START_FRAME -show_entries stream=height,width,duration_ts $TARGET)
NFRAMES=${streams_stream_0_duration_ts}
DURATION=`echo "(1000+$NFRAMES) / 1" | bc`
SIZE_X=${streams_stream_0_width}
SIZE_Y=${streams_stream_0_height}
TARGET_ASPECT=`bc -l <<< "$SIZE_Y/$SIZE_X"`
NEW_X=1920
NEW_Y=`echo "(1920*$TARGET_ASPECT) / 1" | bc`

# Check if the hight was defined
if [ -z "$NEW_Y" ]; then
  echo "Can not determine new hight of the image!"
  exit
fi

# Generate a slate
ffmpeg -y -start_number $START_FRAME -i $TARGET -f lavfi -i color=c=black -i $BARS -i $COLOR_BARS -i $LOGO -vframes 1  \
-filter_complex " \
[1:v] scale=$NEW_X:$NEW_Y, setsar=1:1 [base]; \
[0:v] scale=$NEW_X:$NEW_Y [thumbnail]; \
[thumbnail][3:v] overlay [thumbnail]; \
[thumbnail][3:v] overlay=x=(main_w-overlay_w):y=(main_h-overlay_h) [thumbnail]; \
[thumbnail] scale=(iw/4):(ih/4) [thumbnail]; \
[base][thumbnail] overlay=((main_w-overlay_w)/2)-500:(main_h-overlay_h)/2 [base]; \
[2:v] scale=-1:-1 [bars]; \
[base][bars] overlay=x=(main_w-overlay_w):y=(main_h-overlay_h-50) [base]; \
[4:v] scale=(iw*0.2):(ih*0.2) [logo]; \
[base][logo] overlay=x=500:y=100 [base]; \
[base] \
  drawtext=fontsize=80:fontcolor=${FONT_COLOR}:fontfile=${LOGO_FONT_FILE}:text=${COMPANY_NAME}:x=690:y=130, \
  drawtext=fontsize=50:fontcolor=${FONT_COLOR}:fontfile=${FONT_FILE}:text=${PROJECT_NAME}:x=(w)/2:y=250, \
       $TEXT='LUT\: ':x=${LEFT_TEXT_MARGIN}-text_w:y=${TOP_TEXT_MARGIN}, \
       $TEXT='Shot name\: ':${P}*1 \
       $TEXT='File name\: ':${P}*2, \
       $TEXT='FPS\: ':${P}*3, \
       $TEXT='Frame range\: ':${P}*4, \
       $TEXT='Frame total\: ':${P}*5, \
       $TEXT='Handles\: ':${P}*6, \
       $TEXT='Comp resolution\: ':${P}*7, \
       $TEXT='Date\: ':${P}*8, \
       $TEXT='User\: ':${P}*9, \
       $TEXT='Description\: ':${P}*10 \
" $OUTPUT_IMG

# Generate an mov with the attached slate
ffmpeg -y -i ./tmp_slate.png -start_number $START_FRAME -i $TARGET -crf 18 -vcodec mjpeg -pix_fmt yuvj444p -qmin 1 -qmax 1 -r 24 \
-filter_complex " \
[1:v] scale=$NEW_X:$NEW_Y, setsar=1:1 [base]; \
[0:v] trim=start_frame=0:end_frame=1 [slate]; \
[slate][base] concat [base]; \
[base] \
  drawtext=fontsize=30:fontcolor=${FONT_COLOR}:fontfile=${FONT_FILE}:expansion=none:text=$FILE_NAME:x=10:y=(h-(text_h+10)):enable='between(n,1,99999)', \
  drawtext=fontsize=30:fontcolor=${FONT_COLOR}:fontfile=${FONT_FILE}:start_number=1000:text=%{n} \[1001-$DURATION\]:x=(w-(text_w+10)):y=(h-(text_h+10)):enable='between(n,1,99999)' \
" concat.mov
