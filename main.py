import os
from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urljoin, urlparse
from colorama import init, Fore
from tqdm import tqdm


# Define vars
osname = "Undefined"
if os.name == 'nt':
    osname = 'Windows'
elif os.name == 'posix':
    osname = 'Linux'

# Functions
def get_user_agent():
    try:
        with open("user_agent.json", "r") as file:
            data = json.load(file)
            return data["user_agent"]
    except FileNotFoundError:
        return ""

def set_user_agent(user_agent):
    data = {"user_agent": user_agent}
    with open("user_agent.json", "w") as file:
        json.dump(data, file)
        

def write_content_site(target_url, content):
    parsed_url = urlparse(target_url)
    target_name = parsed_url.netloc.replace("https://", "") + ".txt"

    if not os.path.exists("out"):
        os.makedirs("out")

    file_path = os.path.join("out", target_name)

    with open(file_path, "w") as file:
        file.write("<!-- Data extracted with the tool: https://github.com/GuimaSpace/WebScrappingTool --> \n\n\n" + str(content))

def download_image(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]',
                        ncols=80, dynamic_ncols=True)

    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()

def clearConsole():
    if osname == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def getPageContent():
    if osname == 'Windows':
        clearConsole()
    else:
        os.system('clear')
    print(Fore.WHITE + '🚩 Enter the URL you want to extract the files from.')
    targetUrl = input('🌐 ➤ ')
    try:
        response = requests.get(targetUrl, headers={'user-agent': get_user_agent()})
        print('✅ Data extraction was successful and saved in the Out folder.')
        write_content_site(targetUrl, response.text)
        input("Press enter to return to the menu")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"An error occurred: {e}")
        input("Press enter to return to the menu")
        
def extractAllImgFromWebsite():
    if osname == 'Windows':
        clearConsole()
    else:
        os.system('clear')
    print(Fore.WHITE + '🚩 Enter the URL you want to extract the files from.')
    targetUrl = input('🌐 ➤ ')
    try:
        response = requests.get(targetUrl, headers={'user-agent': get_user_agent()})
        print('✅ Data extraction was successful and saved in the Out folder.')
        while True:
            clearConsole()
            print('📦 Web Scrapping Tool')
            print(Fore.CYAN + "0️⃣ - Save <img> with html")
            print(Fore.CYAN + "1️⃣ - Save all Url in Json")
            print(Fore.CYAN + "2️⃣ - Download all Images")
            print(Fore.CYAN + "3️⃣ - Exit")
            choose = input('➤ ')
            if choose.lower() == '0':
                soup = BeautifulSoup(response.content, 'html.parser')
                img_tags = soup.find_all('img')
                write_content_site(targetUrl, img_tags)              
                break
            elif choose.lower() == '1':
                parsed_url = urlparse(targetUrl)
                target_name = parsed_url.netloc.replace("https://", "") + ".json"
                soup = BeautifulSoup(response.content, 'html.parser')
                img_tags = soup.find_all('img')
                image_urls = []
                for img in img_tags:
                    if 'src' in img.attrs:
                        image_url = img['src']
                        if not image_url.startswith('https'):
                            image_url = urljoin(targetUrl, image_url)
                        image_urls.append({"url": image_url})
                  
                if not os.path.exists('out/json/'):
                 os.makedirs('out/json/')
                 
                file_path = os.path.join("out/json/", target_name)
                with open(file_path, "w") as file:
                    json.dump(image_urls, file, indent=4, ensure_ascii=False)
                 
                 
                    print('✅ JSON successfully saved')
                    input()
                break
            elif choose.lower() == '2': 
                #Clean Name
                parsed_url = urlparse(targetUrl)
                target_name = parsed_url.netloc.replace("https://", "")
                #Get images URL
                soup = BeautifulSoup(response.content, 'html.parser')
                img_tags = soup.find_all('img')
                image_urls = []
                for img in img_tags:
                    if 'src' in img.attrs:
                        image_url = img['src']
                        # Verifica se a URL é relativa e a combina com o URL base da página
                        if not image_url.startswith('https'):
                            image_url = urljoin(targetUrl, image_url)
                        image_urls.append(image_url)
                #Make images folder
                if not os.path.exists('out/images/' + target_name):
                  os.makedirs('out/images/' + target_name)
        
                for i, image_url in enumerate(image_urls):
                    filename = f'out/images/{target_name}/image{i+1}.{image_url.split(".")[-1]}'
                    print(Fore.GREEN + 'Starting the download')
                    print(Fore.GREEN + f'Downloading image {i+1}/{len(image_urls)}: {image_url}')
                    download_image(image_url, filename)
                break
            elif choose.lower() == '3':
                break
            else:
                print('Invalid option. Please choose again.')
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"An error occurred: {e}")
        input("Press enter to return to the menu")
# Show menu function
def show_menu():
    clearConsole()
    print(Fore.RED + "📦 Web Scrapping Tool")
    print(Fore.BLUE + "💻 OS: " + osname)
    print(Fore.CYAN + "0️⃣ - See Header")
    print(Fore.CYAN + "1️⃣ - Change Header")
    print(Fore.CYAN + "2️⃣ - Get all content from Website")
    print(Fore.CYAN + "3️⃣ - Get all <img> tag from Website")
    print(Fore.CYAN + "4️⃣ - Get all <video> tag from Website")
    print(Fore.CYAN + "9️⃣ - Exit")

# Code
init(autoreset=True)

while True:
    show_menu()
    option = input(Fore.GREEN + 'Choose option ➤ ' + Fore.WHITE)
    
    if option == '0':
        clearConsole()
        print(Fore.CYAN + 'Header: ')
        print({'user-agent': get_user_agent()})
        input("Press enter to return to the menu")
        
    elif option == '1':
        clearConsole()
        print(Fore.CYAN + 'Change header: User Agent')
        print({'user-agent': get_user_agent()})
        print('🔄 Enter the new User-Agent value. obs: Use a valid User-Agent')
        user_agent = input('Default: Mozilla/5.0 ➤ ')
        set_user_agent(user_agent)
        print("✅ The User-Agent of the header was changed successfully")
        input("Press enter to return to the menu")
        
    elif option == '2':
        clearConsole()
        getPageContent()
        input("Press enter to return to the menu")
        
    elif option == '3':
        clearConsole()
        extractAllImgFromWebsite()
        input("Press enter to return to the menu")
    
    elif option == '9':
        clearConsole()
        print('**✧ *✧･💜 thanks for using･ﾟ:･ﾟﾟ: *✧゜・')
        break
    
    else:
        print(Fore.RED + "❌ This menu option was not found, press enter and try again")
        input("Press enter to return to the menu")
