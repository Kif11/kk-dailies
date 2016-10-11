import os
import yaml
import subprocess as sp

class Slate(object):

    def __init__(self, source, output):

        self.source = source
        self.output = output

        script_dir = os.path.dirname(os.path.realpath(__file__))
        config_file = os.path.join(script_dir, 'config.yml')
        with open(config_file, 'r') as f:
            self.config = yaml.load(f)
        self.ffmpeg = os.path.join(script_dir, 'bin', 'ffmpeg')

        # Resource files
        self.res = os.path.join(script_dir, 'resources')
        self.bars = os.path.join(self.res, self.config['bars'])
        self.color_bars = os.path.join(self.res, self.config['color_bar'])
        self.logo = os.path.join(self.res, self.config['company_logo'])
        self.logo_font_file = os.path.join(self.res, self.config['company_font'])
        self.font_file = os.path.join(self.res, self.config['body_font'])

        # Global alignment properties
        self.left_text_margin = '(w)/2+150'
        self.top_text_margin = '380'
        self.font_size = 40
        self.line_spacing = 40
        self.font_color = 'White'

        self.start_frame = '1'
        self.new_x = '1920'
        self.new_y = '1080'

        # Contains data for all of the dynamic field used on slate
        self.fields_data = {
            'company_name': None,
            'project_name': None,
            'lut': None,
            'shot_name': None,
            'file_name': None,
            'fps': None,
            'frame_range': None,
            'frame_total': None,
            'handles': None,
            'comp_res': None,
            'date': None,
            'user': None,
            'description': None,
        }

    def fields_from_dict(self, fields_dict):
        for k, v in self.fields_data.items():
            self.fields_data[k] = fields_dict[k]

    def make(self):

        # Alignment properties for slate field
        p = " \
            x={left_text_margin}-text_w:y={top_text_margin}+{line_spacing} \
        ".format(
            left_text_margin=self.left_text_margin,
            top_text_margin=self.top_text_margin,
            line_spacing=self.line_spacing
        )

        # Alignment properties for slate field value
        pv = " \
            x={left_text_margin}+10:y={top_text_margin}+{line_spacing} \
        ".format(
            left_text_margin=self.left_text_margin,
            top_text_margin=self.top_text_margin,
            line_spacing=self.line_spacing
        )

        # Slate main body text style
        text = " \
            drawtext=fontsize={font_size}:fontcolor={font_color}:fontfile='{font_file}':text \
        ".format(
            font_size=self.font_size,
            font_color=self.font_color,
            font_file=self.font_file
        )

        # Generate a slate
        filters = " \
            [1:v] scale={new_x}:{new_y}, setsar=1:1 [base]; \
            [0:v] scale={new_x}:{new_y} [thumbnail]; \
            [thumbnail][3:v] overlay [thumbnail]; \
            [thumbnail][3:v] overlay=x=(main_w-overlay_w):y=(main_h-overlay_h) [thumbnail]; \
            [thumbnail] scale=(iw/4):(ih/4) [thumbnail]; \
            [base][thumbnail] overlay=((main_w-overlay_w)/2)-500:(main_h-overlay_h)/2 [base]; \
            [2:v] scale=-1:-1 [self.bars]; \
            [base][self.bars] overlay=x=(main_w-overlay_w):y=(main_h-overlay_h-50) [base]; \
            [4:v] scale=(iw*0.2):(ih*0.2) [self.logo]; \
            [base][self.logo] overlay=x=500:y=100 [base]; \
            [base] \
              drawtext=fontsize=80:fontcolor={font_color}:fontfile={logo_font_file}:text={company_name}:x=690:y=130, \
              drawtext=fontsize=50:fontcolor={font_color}:fontfile={font_file}:text={project_name}:x=(w)/2:y=250, \
                   {text}='LUT\: ':{p}*0, \
                   {text}={lut}:{pv}*0, \
                   {text}='Shot name\: ':{p}*1, \
                   {text}={shot_name}:{pv}*1, \
                   {text}='File name\: ':{p}*2, \
                   {text}={file_name}:{pv}*2, \
                   {text}='FPS\: ':{p}*3, \
                   {text}={fps}:{pv}*3, \
                   {text}='Frame range\: ':{p}*4, \
                   {text}={frame_range}:{pv}*4, \
                   {text}='Frame total\: ':{p}*5, \
                   {text}={frame_total}:{pv}*5, \
                   {text}='Handles\: ':{p}*6, \
                   {text}={handles}:{pv}*6, \
                   {text}='Comp resolution\: ':{p}*7, \
                   {text}={comp_res}:{pv}*7, \
                   {text}='Date\: ':{p}*8, \
                   {text}={date}:{pv}*8, \
                   {text}='User\: ':{p}*9, \
                   {text}={user}:{pv}*9, \
                   {text}='Description\: ':{p}*10, \
                   {text}={description}:{pv}*10 \
        ".format(
            font_color=self.font_color, logo_font_file=self.logo_font_file,
            font_file=self.font_file, line_spacing=self.line_spacing,
            left_text_margin=self.left_text_margin,
            top_text_margin=self.top_text_margin, new_x=self.new_x,
            new_y=self.new_y, text=text, p=p, pv=pv,
            # Fields values
            project_name=self.fields_data['project_name'],
            company_name=self.fields_data['company_name'],
            lut=self.fields_data['lut'],
            shot_name=self.fields_data['shot_name'],
            file_name=self.fields_data['file_name'],
            fps=self.fields_data['fps'],
            frame_range=self.fields_data['frame_range'],
            frame_total=self.fields_data['frame_total'],
            handles=self.fields_data['handles'],
            comp_res=self.fields_data['comp_res'],
            date=self.fields_data['date'],
            user=self.fields_data['user'],
            description=self.fields_data['description']
        )
        cmd = [
            self.ffmpeg, '-y', '-start_number', self.start_frame, '-i', self.source,
            '-f', 'lavfi', '-i', 'color=c=black', '-i', self.bars, '-i', self.color_bars,
            '-i', self.logo, '-vframes', '1', '-filter_complex', filters, self.output
        ]

        sp.call(cmd)
