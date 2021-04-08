import requests
from bs4 import BeautifulSoup

logo = """
,--.   ,--.                              ,--.                           ,--.        ,--.
|   `.'   |,---.,--.--.,---. ,---.     ,-'  '-,--.--.,--,--,--,--, ,---.|  |,--,--,-'  '-.,---.,--.--.
|  |'.'|  | .-. |  .--(  .-'| .-. :    '-.  .-|  .--' ,-.  |      (  .-'|  ' ,-.  '-.  .-| .-. |  .--'
|  |   |  ' '-' |  |  .-'  `\   --.      |  | |  |  \ '-'  |  ||  .-'  `|  \ '-'  | |  | ' '-' |  |
`--'   `--'`---'`--'  `----' `----'      `--' `--'   `--`--`--''--`----'`--'`--`--' `--'  `---'`--'
"""

response = requests.get('https://en.wikipedia.org/wiki/Morse_code').content

soup = BeautifulSoup(response, 'html.parser')

data = soup.find('table', class_='wikitable sortable').find_all('b')
text_data = [_.get_text() for _ in data]

symbols = text_data[0::2][:54]
codes = text_data[1::2][:54]

symbols = [_.strip().replace(']', '')[-1] if (_ != ' Parenthesis (Open)') else '(' for _ in symbols]
codes = [_.replace(' ', '').replace('\u200a', '').replace('·', '.').replace('−', '-') for _ in codes]

encode = dict(zip(symbols, codes))
decode = dict(zip(codes, symbols))
supported_symbols = list(encode.keys())
punctuation_marks = supported_symbols[36:]

print(logo)
print('Supported symbols: A-z 0-9', ''.join(punctuation_marks))
print('To see morse code: enter "morse".')
print('For exit: enter "exit".')

user_want_exit = False
while not user_want_exit:
    message = input('\nEnter text or morse code: ')
    if message == 'exit':
        user_want_exit = True
    elif message == 'morse':
        morse_code = ''
        for row in range(9):
            chars = supported_symbols[row::9]
            for char in chars:
                morse_code += f'{char:3}{encode[char]:12}'
            morse_code += '\n'
        print(morse_code, end='')
    else:
        try:
            if message.strip('.- ') == '':
                result = ''.join(
                    [decode[_] if (_ != '') else ' ' for _ in message.split(' ')]
                ).replace('  ', ' ')
            else:
                result = ' '.join(
                    [encode[_] if (_ != ' ') else ' ' for _ in list(message.lower())]
                )
            print(result)
        except KeyError:
            print('Unknown symbol or code. For help enter: "morse".')
