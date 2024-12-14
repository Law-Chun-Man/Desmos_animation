import time
import os
from PIL import ImageGrab
from selenium import webdriver
import re
from paths import svg, desmos_frame


def desmos_capture_frame():
    driver = webdriver.Firefox()

    def write_html(filename):
        svg_file_path = f"{svg}/{filename}"
        with open(svg_file_path, 'r', encoding='utf-8') as file:
            pic = file.read()

        pattern = r'<path d="'
        match = re.search(pattern, pic)

        if match:
            pic = pic[match.end():-16]

        remove = re.sub('''"/>
<path d="''', "", pic)
        components = re.findall(r'-?\d+\.\d+|-?\d+|[a-zA-Z]', remove)
        list = components
        newlist = [10, 10, 10, 10, 10, 10, 10]

        for i in range(len(list)):

            if newlist[-3] == 'l':
                if list[i].isalpha() == False:
                    newlist.append('l')
            if newlist[-7] == 'c':
                if list[i].isalpha() == False:
                    newlist.append('c')
            newlist.append(list[i])


        desmos_string = ''''''

        list = newlist[7:]
        last_x = 0
        last_y = 0
        start_x = 0
        start_y = 0
        for i in range(len(list)):
            if list[i] == 'M':
                start_x = int(list[i + 1])
                start_y = int(list[i + 2])
                last_x = int(list[i + 1])
                last_y = int(list[i + 2])
            if list[i] == 'm':
                start_x = int(list[i + 1]) + last_x
                start_y = int(list[i + 2]) + last_y
                last_x = start_x
                last_y = start_y
            if list[i] == 'l':
                new_x = int(list[i + 1]) + last_x
                new_y = int(list[i + 2]) + last_y
                desmos_string += f'''calculator.setExpression({{latex: '({str(last_x)}, {str(last_y)})*(1-t)+({str(new_x)}, {str(new_y)})*t' }});
'''
                last_x = new_x
                last_y = new_y
            if list[i] == 'c':
                c_1 = (last_x, last_y)
                c_2 = (int(list[i + 1]) + last_x, int(list[i + 2]) + last_y)
                c_3 = (int(list[i + 3]) + last_x, int(list[i + 4]) + last_y)
                c_4 = (int(list[i + 5]) + last_x, int(list[i + 6]) + last_y)
                desmos_string += f'''calculator.setExpression({{latex: '({str(c_1[0])}, {str(c_1[1])})*(1-t)^3+3*({str(c_2[0])}, {str(c_2[1])})*(1-t)^2*t+3*({str(c_3[0])}, {str(c_3[1])})*(1-t)*t^2+({str(c_4[0])}, {str(c_4[1])})*t^3' }});
'''
                last_x = c_4[0]
                last_y = c_4[1]

            if list[i] == 'z':
                last_x = start_x
                last_y = start_y



        html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Desmos</title>
      <script src="https://www.desmos.com/api/v1.6/calculator.js?apiKey=dcb31709b452b1cf9dc26972add0fda6"></script>
    </head>
    <body>
      <div id="calculator" style="width: device-width; height: 97.5vh;"></div>
    <script>
      var elt = document.getElementById('calculator');
      var calculator = Desmos.GraphingCalculator(elt);
      {desmos_string};
      var t = calculator.HelperExpression({{latex: 't'}});
    calculator.setMathBounds({{
      left: -20,
      right: 6722,
      bottom: -20,
      top: 5539
    }});
    state=calculator.getState();
    for (i=0;i<state.expressions.list.length;i++) {{
       state.expressions.list[i].color="#000000"
    }}
    calculator.setState(state);
    </script>
    </body>
    </html>
"""

        with open("frame.html", "w") as html_file:
            html_file.write(html_content)


    num = 0
    for filename in os.listdir(svg):
        file_path = os.path.join(svg, filename)
        if os.path.isfile(file_path):
            write_html(f"frame_{num:04d}.svg")
            file_path = 'frame.html'
            file_url = f'file://{os.path.abspath(file_path)}'
            driver.get(file_url)
            driver.fullscreen_window()

            while True:
                time.sleep(0.2)
                x, y = 33, 133
                screenshot = ImageGrab.grab()
                color = screenshot.getpixel((x, y))
                if color == (0, 0, 0):
                    break

            time.sleep(0.1)
            screenshot = ImageGrab.grab()
            screenshot.save(f"{desmos_frame}/frame_{num:04d}.jpg", "JPEG")
            num += 1

    driver.quit()
