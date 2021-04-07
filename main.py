import requests
from bs4 import BeautifulSoup

response = requests.get('https://en.wikipedia.org/wiki/Morse_code').content

soup = BeautifulSoup(response, 'html.parser')

table = soup.find('table', class_='wikitable sortable')
raw_data = table.find_all('b')
text_data = [_.get_text() for _ in raw_data]

symbols = text_data[0::2][:54]
codes = text_data[1::2][:54]

symbols = [_.strip().replace(']', '')[-1] if (_ != ' Parenthesis (Open)') else '(' for _ in symbols]
codes = [_.replace(' ', '').replace('\u200a', '').replace('·', '.').replace('−', '-') for _ in codes]

encode = dict(zip(symbols, codes))
decode = dict(zip(codes, symbols))
supported_symbols = list(encode.keys())

user_want_exit = False

print('\nText <---> Morse')
print('Supported symbols: A-z 0-9', ''.join(supported_symbols)[36:])
print('To see dictionary type "morse" and press Enter.')
print('For exit type "exit" and press Enter.', end='\n\n')

while not user_want_exit:
    message = input('Type you message & press Enter: ')
    if message == 'exit':
        user_want_exit = True
    elif message == 'morse':
        i, j = 0, 6
        for five in range(9):
            row = supported_symbols[i:j]
            print(f'{row[0]:3}{encode[row[0]]:12}'
                  f'{row[1]:3}{encode[row[1]]:12}'
                  f'{row[2]:3}{encode[row[2]]:12}'
                  f'{row[3]:3}{encode[row[3]]:12}'
                  f'{row[4]:3}{encode[row[4]]:12}'
                  f'{row[5]:3}{encode[row[5]]:12}')
            i += 6
            j += 6
        print()
    else:
        try:
            if message.strip('.- ') == '':
                result = ''.join(
                    [decode[_] if (_ != '') else ' ' for _ in message.split(' ')]).replace('  ', ' ')
            else:
                result = ' '.join(
                    [encode[_] if (_ != ' ') else ' ' for _ in list(message.lower())])
            print(result, end='\n\n')
        except KeyError:
            print('Unsupported symbol detected. Only A-z 0-9',
                  ''.join(supported_symbols)[36:], end='\n\n')
