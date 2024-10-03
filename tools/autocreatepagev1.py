
import logging
import subprocess
import requests
import re
import json
import random
import uuid
import time
import os
from colorama import Fore, Style, init
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
logo = r"""
             ██████╗ ███████╗ ██████╗██████╗ 
             ██╔══██╗██╔════╝██╔════╝██╔══██╗
             ██████╔╝█████╗  ██║     ██████╔╝
             ██╔══██╗██╔══╝  ██║     ██╔═══╝ 
             ██║  ██║██║     ╚██████╗██║     
             ╚═╝  ╚═╝╚═╝      ╚═════╝╚═╝  [V1]
             ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ ʟᴇɪɴᴀᴛʜᴀɴ ᴏʀᴇᴍᴏʀ
"""
def get_approval_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
def approval():
    clear_console()
    print(Fore.CYAN + logo + Style.RESET_ALL)  # Display logo in cyan
    user_id = str(os.geteuid())
    uuid = f"{user_id}DS{user_id}"
    key = f"RFCP-{uuid}"

    print("\033[1;37m [\u001b[36m•\033[1;37m] You Need Approval To Use This Tool   \033[1;37m")
    print(f"\033[1;37m [\u001b[36m•\033[1;37m] Your Key :\u001b[36m {key}")
    
    urls = [
        "https://github.com/rfcptoolsofficial/approval/blob/main/approval.txt"
    ]
    
    key_found = False
    for url in urls:
        approval_data = get_approval_data(url)
        if key in approval_data:
            key_found = True
            break

    if key_found:
        print(f"\033[1;97m >> Your Key Has Been Approved!!!")
        return key
    else:
        
        exit()

# Initialize colorama
init()

def read_tokens(file_path):
    """Read tokens from a file and return them as a list."""
    if not os.path.isfile(file_path):
        print(f"{Fore.RED}Error: Token file not found.{Style.RESET_ALL}")
        return []
    
    with open(file_path, 'r') as file:
        tokens = file.read().splitlines()
    return tokens

def write_page_link(file_path, link):
    """Write the created page link to a file."""
    with open(file_path, 'a') as file:
        file.write(link + '\n')

def delete_token(file_path, token):
    """Delete a token from the file."""
    with open(file_path, 'r') as file:
        tokens = file.readlines()
    
    with open(file_path, 'w') as file:
        for t in tokens:
            if t.strip() != token:
                file.write(t)

def CreatePage(name: str, category: list, token: str, picture: str):
    if not name or not category or not token or not picture:
        return f"{Fore.RED}Error: Missing required fields. Ensure you provide a name, category, and access token.{Style.RESET_ALL}"

    r = requests.Session()
    vir = {
        "params": {
            "client_input_params": {
                "cp_upsell_declined": 0,
                "category_ids": category,
                "profile_plus_id": "0",
                "page_id": "0"
            },
            "server_params": {
                "name": name,
                "INTERNAL__latency_qpl_instance_id": random.randrange(36700000, 36800000),
                "creation_source": "android",
                "screen": "category",
                "referrer": "pages_tab_launch_point",
                "INTERNAL__latency_qpl_marker_id": float(f'{random.random() + 3:.13f}E13'),
                "variant": 5
            }
        }
    }
    var = {
        "params": {
            "params": json.dumps(vir),
            "bloks_versioning_id": 'c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec',
            "app_id": "com.bloks.www.additional.profile.plus.creation.action.category.submit"
        },
        "scale": "1",
        "nt_context": {
            "styles_id": 'e6c6f61b7a86cdf3fa2eaaffa982fbd1',
            "using_white_navbar": True,
            "pixel_ratio": 1,
            "is_push_on": True,
            "bloks_version": 'c3cc18230235472b54176a5922f9b91d291342c3a276e2644dbdb9760b96deec'
        }
    }
    data = {
        'access_token': token,
        'method': 'post',
        'pretty': False,
        'format': 'json',
        'server_timestamps': True,
        'locale': 'id_ID',
        'purpose': 'fetch',
        'fb_api_req_friendly_name': 'FbBloksActionRootQuery-com.bloks.www.additional.profile.plus.creation.action.category.submit',
        'fb_api_caller_class': 'graphservice',
        'client_doc_id': '11994080423068421059028841356',
        'variables': json.dumps(var),
        'fb_api_analytics_tags': ["GraphServices"],
        'client_trace_id': str(uuid.uuid4())
    }

    try:
        response = r.post('https://graph.facebook.com/graphql', data=data)
        pos = response.text.replace('\\', '')

        if ('profile_plus_id' in pos) and ('page_id' in pos):
            try:
                name, page_id, profile_id = re.findall(r'"android", "pages_tab_launch_point", "(.*?)", "(.*?)", "(.*?)", "intent_selection"', pos)[0]
                page_link = f"https://www.facebook.com/{page_id}"
                response = requests.get(f"https://graph.facebook.com/v2.2/{page_id}?fields=access_token&access_token={token}").json()
                if 'access_token' in response:
                    page_token = response['access_token']
                    upload_url = f'https://graph.facebook.com/v12.0/{page_id}/photos'
                    upload_response = requests.post(upload_url, data={'url': picture, 'access_token': page_token, 'published': 'false'})
                    if upload_response.status_code == 200:
                        photo_id = upload_response.json().get('id')
                        set_profile_pic_url = f'https://graph.facebook.com/v12.0/{page_id}/picture'
                        set_profile_pic_response = requests.post(set_profile_pic_url, data={'access_token': page_token, 'photo': photo_id})
                        if set_profile_pic_response.status_code == 200:
                            return (f"{Fore.GREEN}Success Create Page!{Style.RESET_ALL}\n"
                                    f"Page Name  : {Fore.CYAN}{name}{Style.RESET_ALL}\n"
                                    f"Page Link  : {Fore.CYAN}{page_link}{Style.RESET_ALL}\n"
                                    f"Profile Picture  : {Fore.CYAN}Successfully added!{Style.RESET_ALL}")
                        else:
                            return (f"{Fore.GREEN}Success Create Page!{Style.RESET_ALL}\n"
                                    f"Page Name  : {Fore.CYAN}{name}{Style.RESET_ALL}\n"
                              
                                    f"Page Link  : {Fore.CYAN}{page_link}{Style.RESET_ALL}\n"
                                    f"Profile Picture  : {Fore.CYAN}Failed to set profile picture!{Style.RESET_ALL}")
                    else:
                        return (f"{Fore.GREEN}Success Create Page!{Style.RESET_ALL}\n"
                                f"Page Name  : {Fore.CYAN}{name}{Style.RESET_ALL}\n"
                             
                                f"Page Link  : {Fore.CYAN}{page_link}{Style.RESET_ALL}\n"
                                f"Profile Picture  : {Fore.CYAN}Failed to upload picture!{Style.RESET_ALL}")
                else:
                    return (f"{Fore.GREEN}Success Create Page!{Style.RESET_ALL}\n"
                            f"Page Name  : {Fore.CYAN}{name}{Style.RESET_ALL}\n"
                            f"Page Link  : {Fore.CYAN}{page_link}{Style.RESET_ALL}\n"
                            f"Profile Picture  : {Fore.CYAN}Failed to upload picture!{Style.RESET_ALL}")
            except IndexError:
                return f"{Fore.RED}Error: Unable to extract IDs from the response.{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}Failed Create Page!{Style.RESET_ALL}\n{Fore.RED}Response Details:{Style.RESET_ALL}\n{pos}"

    except requests.RequestException as e:
        return f"{Fore.RED}Request failed: {e}{Style.RESET_ALL}"

def main():
    clear_console()
    approval()
    print(f"{Fore.YELLOW}Facebook Page Creator{Style.RESET_ALL}")

    # Define file paths
    tokens_file = '/sdcard/RFCPTOOLS/pagecreate/tokens/tokens.txt'
    page_file = '/sdcard/RFCPTOOLS/pagecreate/page.txt'

    # Function to create a file if it does not exist
    def create_file_if_not_exists(file_path):
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                # Optionally write some initial content
                f.write("")

    # Create directories if they do not exist
    def create_directories_for_file(file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Create directories for both files
    create_directories_for_file(tokens_file)
    create_directories_for_file(page_file)

    # Create the files if they do not exist
    create_file_if_not_exists(tokens_file)
    create_file_if_not_exists(page_file)

    # Define name components and picture lists
    nameMc = ["Aaron","Adrian","Aiden","Aidric","Albert","Alfie","Alistair","Alonso","Alvin","Andy","Angelo","Aquinnah","Arellano","Aries","Arvin","Ash","Axel","Benjamin","Benny","Bernhard","Bryan","Caelan","Calgary","Calix","Cedric","Charlie","Christian","Crisanto","Cyler","Cyril","Daniel","Danilo","Dexter","Dranreb","Dream","Dwyn","Dylan","Eason","Elton","Ernest","Ernie","Ethan","Ethaniel","Euan","Eugene","Evan","Ezekiel","Faro","Felix","Fergus","Finn","Fraley","Gabriel","Galeno","Gavin","Genkei","Harlem","Harvey","Itzan","Jacob","Jaime","Jalen","James","Jayson","Jejomar","Jermaine","Jerome","Jess","Jiro","John Carlo","John Lloyd","John Mark","John Michael","John Paul","John Rey","Johnny","Jonas","Jonathan","Joshua","Juan","Justin","Justine","Kemp","Kenneth","Kyel","Kyle","Kylen","Lancel","Landis","Leroy","Luca","Lucas","Marco","Mark","Mark Anthony","Melchor","Miles","Morris","Mueller","Murphy","Nathan","Nathaniel","Nigel","Noah","Otto","Rafael","Ricardo","Riley","Rizalino","Rodrigo","Ryan","Ryuu","Shawn","Shayne","Shea","Skye","Sunday","Theo","Uhtred","Vern","Vin","Vince","Wayne","Wilfred","Xavier","Yuji","Zedhryx","Zion"]
    
    nameFc = ["Aaliyah","Acadia","Aintza","Alina","Alizeé","Althea","Amelie","Andrea","Angel","Angela","Angelica","Angeline","Angelou","Aquene","Aquinnah","Ariel","Aries","Ashley","Aurora","Avery","Avis","Bancroft","Bea","Beverly","Bituin","Blessica","Bora","Caia","Cara","Caroline","Cassie","Charlene","Charlie","Charlotte","Charmaine","Chesa","Chloe","Christine","Cynthia","Dream","Elaine","Ellie","Ellis","Eloise","Erica","Esther","Florence","Francesca","Francine","Fyra","Georgina","Gillian","Giselle","Gracelyn","Hailey","Hazel","Holly","Hyacinth","Iris","Jaime","Janeeva","Janelle","Janice","Jasmine","Jeneth","Jenny","Jessa Mae","Jezel","Jillian","Joie","Jorgie","Jovia","Jovie","Joyce","Jyn","Katrice","Kimberly","Kyla","Leah","Leslie","Liddy","Lillian","Liz","Louvel","Lyka Mae","Maricar","Mariel","Mary Grace","Mary Joy","Michelle","Murphy","Myra","Nara","Natalie","Nathalie","Nemo","Nicole","Nora","Norjannah","Ophelia","Phaedra","Princess","Quinn","Rhodette","Riley","Rosa","Samantha","Sasha","Seren","Serenity","Sirena","Skylar","Sofia","Sophia","Sophiel","Stephanie","Sunday","Sylvia","Thea","Titania","Vaiana","Valerie","Viola","Vivi","Wynne","Ysanne","Zenaida","Zoe","Zyanya"]
    
    nameLast = ["dela Cruz","Garcia","Reyes","Ramos","Mendoza","Santos","Flores","Gonzales","Bautista","Villanueva","Fernandez","Cruz","de Guzman","Lopez","Perez","Castillo","Francisco","Rivera","Aquino","Castro","Sanchez","Torres","de Leon","Domingo","Martinez","Rodriguez","Santiago","Soriano","Delos Santos","Diaz","Hernandez","Tolentino","Valdez","Ramirez","Morales","Mercado","Tan","Aguilar","Navarro","Manalo","Gomez","Dizon","del Rosario","Javier","Corpuz","Gutierrez","Salvador","Velasco","Miranda","David","Salazar","Ferrer","Alvarez","Sarmiento","Pascual","Lim","Delos Reyes","Marquez","Jimenez","Cortez","Antonio","Agustin","Rosales","Manuel","Mariano","Evangelista","Pineda","Enriquez","Ocampo","Alcantara","Pascua","de Vera","Romero","de Jesus","dela Peña","Valencia","Ignacio","Vergara","Padilla","Angeles","Espiritu","Fuentes","Legaspi","Cañete","Peralta","Vargas","Cabrera","Fajardo","Gonzaga","Espinosa","Guevarra","Samson","Ortega","Molina","Serrano","Chavez","Briones","Medina","Palma","Tamayo","Arellano","Atienza","Villegas","Estrada","Martin","Acosta","Ortiz","Sison","Trinidad","Zamora","Asuncion","Abad","Moreno","Valenzuela","Mallari","Caballero","Villamor","Bernardo","Robles","Concepcion","Fernando","Gregorio","Borja","Magbanua","de Castro","Panganiban","Galang","Nuñez","Roxas","Ruiz","Pangilinan","Vicente","Chua","Suarez","Avila","Ali","Austria","Magno","dela Torre","Luna","de La Cruz","Pepito","Solis","Uy","dela Rosa","Duran","Abella","Mahinay","Esguerra","Roque","Andres","Jose","Sevilla","Beltran","Gabriel","Mateo","Ybañez","Nicolas","Mendez","Cunanan","Vasquez","Ancheta","Ventura","Lorenzo","Cordero","Toledo","Galvez","Abdul","Natividad","Marasigan","Herrera","Silva","Miguel","Gamboa","Estrella","Villa","Bartolome","Usman","Sales","Custodio","Ong","Lucero","Abdullah","Manzano","Ibañez","Marcelo","Ponce","Gallardo","Rosario","Delgado","Canlas","Cariño","Yap","Go","Esteban","Ilagan","Tuazon","Carpio","Carreon","Baltazar","Pablo","Lozada","Guzman","Guerrero","Padua","Salcedo","Camacho","San Juan","Bueno","Blanco","Cuevas","Carlos","Andaya","Lozano","Aguirre","Baguio","Cervantes","Bernal","Bustamante","Arevalo","Villar","Sabado","Labrador","Ronquillo","Panes","Cristobal","Prado","Guillermo","Dulay","Apostol","Oliveros","Santillan","Abalos","Quinto","Montero","Alfonso","Umali","Campos","Constantino","Baylon","Malinao","Franco","Calderon","Quijano","Velasquez","Marcos","Alonzo","Lazaro","Mata","Cinco","Geronimo","Cordova","Eugenio","Rubio","Viray","Delfin","Canoy","Crisostomo","Mejia","Rico","Punzalan","Benitez","Bernabe","Buenaventura","Ballesteros","Clemente","Sy","Peña","Jacinto","Vidal","Salas","Tomas","Matias","Yu","de Asis","Andrade","Magallanes","Roldan","Asis","Ledesma","Cortes","Feliciano","Sayson","de Luna","Borromeo","del Mundo","Bello","Manansala","Bondoc","Lacson","Salinas","Barrientos","Conde","Collado","Juan","Villareal","Teves","Laurente","Quiambao","Mohammad","Oliva","Bonifacio","Rojas","Alejandro","Sebastian","Frias","Catalan","Espina","Lee","Lucas","Sali","Dominguez","Mangubat","Calma","Chan","Villarin","Cayabyab","Rosal","Basa","Basilio","Tejada","Samonte","Viernes","Plaza","Gallego","Castor","Dionisio","Musa","Sultan","Tenorio","Solomon","Española","Narciso","San Jose","Pangan","Pelayo","Romano","Lachica","Arcilla","Alba","Espino","Raymundo","Pilapil","Cuizon","Aragon","Medrano","Ang","Guinto","Castañeda","Paras","Alvarado","Omar","Hipolito","Porras","de Mesa","Tecson","Basco","Pimentel","Adriano","Santa Ana","Sagun","Pacheco","Muñoz","Landicho","Arroyo","Rodrigo","Neri","Malabanan","Bravo","Lara","dela Cerna","Villaflor","Galicia","Junio","de Los Santos","Villaruel","Hilario","Añonuevo","Felipe","Montes","Gaspar","Belen","Sotto","Patricio","Bernardino","Madrid","Alarcon","Verano","Casas","Barrios","Ariola","Cano","Advincula","Marcelino","Macaraeg","Alejo","Andal","Dalisay","Aguila"]
    
    PictureMC = [
        "https://i.pinimg.com/originals/05/dc/aa/05dcaa5d13b21ac457709ba1d6b5abee.jpg",
        "https://i.pinimg.com/originals/9e/2b/52/9e2b52afdbc8b629ad013183aa8631e2.jpg",
        "https://i.pinimg.com/originals/ef/f8/15/eff815c73077a1be798cf694d9baca03.jpg",
        "https://i.pinimg.com/originals/4a/1c/75/4a1c75806c1dfdeb67c8006336b15782.jpg",
        "https://i.pinimg.com/originals/9f/fc/66/9ffc66229e9221dcfd9352c46f43d13b.jpg",
        "https://i.pinimg.com/originals/8f/e7/73/8fe77331e4427846c4a3fd186fe590ed.jpg",
        "https://i.pinimg.com/originals/6b/e0/32/6be032bcdb1373692166c1976436bac0.jpg",
        "https://i.pinimg.com/originals/e6/13/9b/e6139beebd58267d328b107990724855.jpg",
        "https://i.pinimg.com/originals/c1/f5/70/c1f570063019c75830f28da5808e5d61.jpg",
        "https://i.pinimg.com/originals/c5/32/dd/c532ddd002f2384b6b6347a4dc1ecd50.jpg",
        "https://i.pinimg.com/originals/05/dc/aa/05dcaa5d13b21ac457709ba1d6b5abee.jpg",
        "https://i.pinimg.com/originals/9e/2b/52/9e2b52afdbc8b629ad013183aa8631e2.jpg",
        "https://i.pinimg.com/originals/ef/f8/15/eff815c73077a1be798cf694d9baca03.jpg",
        "https://i.pinimg.com/originals/4a/1c/75/4a1c75806c1dfdeb67c8006336b15782.jpg",
        "https://i.pinimg.com/originals/9f/fc/66/9ffc66229e9221dcfd9352c46f43d13b.jpg",
        "https://i.pinimg.com/originals/8f/e7/73/8fe77331e4427846c4a3fd186fe590ed.jpg",
        "https://i.pinimg.com/originals/6b/e0/32/6be032bcdb1373692166c1976436bac0.jpg",
        "https://i.pinimg.com/originals/e6/13/9b/e6139beebd58267d328b107990724855.jpg",
        "https://i.pinimg.com/originals/c1/f5/70/c1f570063019c75830f28da5808e5d61.jpg",
        "https://i.pinimg.com/originals/c5/32/dd/c532ddd002f2384b6b6347a4dc1ecd50.jpg",
        "https://i.pinimg.com/originals/7b/95/41/7b95414ab615338138bc5a460d55ce5f.jpg",
        "https://i.pinimg.com/originals/68/aa/8c/68aa8c84e5371c6ad0b3d01140fb9938.jpg",
        "https://i.pinimg.com/originals/d3/fb/94/d3fb942425ac2792dad336992de3df89.jpg",
        "https://i.pinimg.com/originals/05/dc/aa/05dcaa5d13b21ac457709ba1d6b5abee.jpg",
        "https://i.pinimg.com/originals/69/83/6b/69836b1bd8859006f2356ffd7e4adcd8.jpg",
        "https://i.pinimg.com/originals/aa/d6/95/aad6956b75968ab16796f15c10871cb0.jpg",
        "https://i.pinimg.com/originals/9e/2b/52/9e2b52afdbc8b629ad013183aa8631e2.jpg",
        "https://i.pinimg.com/originals/ef/f8/15/eff815c73077a1be798cf694d9baca03.jpg",
        "https://i.pinimg.com/originals/4a/1c/75/4a1c75806c1dfdeb67c8006336b15782.jpg",
        "https://i.pinimg.com/originals/9f/fc/66/9ffc66229e9221dcfd9352c46f43d13b.jpg",
        "https://i.pinimg.com/originals/8f/e7/73/8fe77331e4427846c4a3fd186fe590ed.jpg",
        "https://i.pinimg.com/originals/6b/e0/32/6be032bcdb1373692166c1976436bac0.jpg",
        "https://i.pinimg.com/originals/e6/13/9b/e6139beebd58267d328b107990724855.jpg",
        "https://i.pinimg.com/originals/c1/f5/70/c1f570063019c75830f28da5808e5d61.jpg",
        "https://i.pinimg.com/originals/c5/32/dd/c532ddd002f2384b6b6347a4dc1ecd50.jpg",
        "https://i.pinimg.com/originals/7b/95/41/7b95414ab615338138bc5a460d55ce5f.jpg",
        "https://i.pinimg.com/originals/a5/e5/ba/a5e5ba12e07617d075e5605322c14828.jpg",
        "https://i.pinimg.com/originals/68/aa/8c/68aa8c84e5371c6ad0b3d01140fb9938.jpg",
        "https://i.pinimg.com/originals/d3/fb/94/d3fb942425ac2792dad336992de3df89.jpg",
        "https://i.pinimg.com/originals/af/09/b8/af09b86048adebdac96c7588f841cb01.jpg",
        "https://i.pinimg.com/originals/1e/fe/2c/1efe2c43a0e480798660708e4e73ff6f.jpg",
        "https://i.pinimg.com/originals/05/dc/aa/05dcaa5d13b21ac457709ba1d6b5abee.jpg",
        "https://i.pinimg.com/originals/69/83/6b/69836b1bd8859006f2356ffd7e4adcd8.jpg",
        "https://i.pinimg.com/originals/aa/d6/95/aad6956b75968ab16796f15c10871cb0.jpg",
        "https://i.pinimg.com/originals/9e/2b/52/9e2b52afdbc8b629ad013183aa8631e2.jpg",
        "https://i.pinimg.com/originals/ef/f8/15/eff815c73077a1be798cf694d9baca03.jpg",
        "https://i.pinimg.com/originals/4a/1c/75/4a1c75806c1dfdeb67c8006336b15782.jpg",
        "https://i.pinimg.com/originals/9f/fc/66/9ffc66229e9221dcfd9352c46f43d13b.jpg",
        "https://i.pinimg.com/originals/8f/e7/73/8fe77331e4427846c4a3fd186fe590ed.jpg",
        "https://i.pinimg.com/originals/6b/e0/32/6be032bcdb1373692166c1976436bac0.jpg",
        "https://i.pinimg.com/originals/e6/13/9b/e6139beebd58267d328b107990724855.jpg",
        "https://i.pinimg.com/originals/c1/f5/70/c1f570063019c75830f28da5808e5d61.jpg",
        "https://i.pinimg.com/originals/c5/32/dd/c532ddd002f2384b6b6347a4dc1ecd50.jpg",
        "https://i.pinimg.com/originals/7b/95/41/7b95414ab615338138bc5a460d55ce5f.jpg",
        "https://i.pinimg.com/originals/a5/e5/ba/a5e5ba12e07617d075e5605322c14828.jpg",
        "https://i.pinimg.com/originals/68/aa/8c/68aa8c84e5371c6ad0b3d01140fb9938.jpg",
        "https://i.pinimg.com/originals/d3/fb/94/d3fb942425ac2792dad336992de3df89.jpg",
        "https://i.pinimg.com/originals/af/09/b8/af09b86048adebdac96c7588f841cb01.jpg",
        "https://i.pinimg.com/originals/1e/fe/2c/1efe2c43a0e480798660708e4e73ff6f.jpg",
        "https://i.pinimg.com/originals/c1/f5/70/c1f570063019c75830f28da5808e5d61.jpg",
        "https://i.pinimg.com/originals/9f/fc/66/9ffc66229e9221dcfd9352c46f43d13b.jpg",
        "https://i.pinimg.com/originals/ef/f8/15/eff815c73077a1be798cf694d9baca03.jpg",
        "https://i.pinimg.com/originals/9f/4d/b1/9f4db1b4d0877ac399425be7256365b8.jpg",
        "https://i.pinimg.com/originals/43/ad/fa/43adfa87a3692400afbd2edfdad34abb.jpg",
        "https://i.pinimg.com/originals/9b/db/96/9bdb96ef210bbd047c18eb46f065654f.jpg",
        "https://i.pinimg.com/originals/a2/a5/53/a2a553d9af8b28736af8c18c88a079ef.jpg",
        "https://i.pinimg.com/originals/da/47/42/da47427cdd256edb5e0da11786c4a0b3.jpg",
        "https://i.pinimg.com/originals/b4/49/c8/b449c8b34a5af3f64179d1f30471d68c.jpg",
        "https://i.pinimg.com/originals/76/74/81/7674813378dbe95cbf21234b936a31fd.jpg",
        "https://i.pinimg.com/originals/c1/f5/70/c1f570063019c75830f28da5808e5d61.jpg",
        "https://i.pinimg.com/originals/9f/fc/66/9ffc66229e9221dcfd9352c46f43d13b.jpg",
        "https://i.pinimg.com/originals/ef/f8/15/eff815c73077a1be798cf694d9baca03.jpg",
        "https://i.pinimg.com/originals/9f/4d/b1/9f4db1b4d0877ac399425be7256365b8.jpg",
        "https://i.pinimg.com/originals/43/ad/fa/43adfa87a3692400afbd2edfdad34abb.jpg",
        "https://i.pinimg.com/originals/9b/db/96/9bdb96ef210bbd047c18eb46f065654f.jpg",
        "https://i.pinimg.com/originals/a2/a5/53/a2a553d9af8b28736af8c18c88a079ef.jpg",
        "https://i.pinimg.com/originals/da/47/42/da47427cdd256edb5e0da11786c4a0b3.jpg",
        "https://i.pinimg.com/originals/b4/49/c8/b449c8b34a5af3f64179d1f30471d68c.jpg",
        "https://i.pinimg.com/originals/76/74/81/7674813378dbe95cbf21234b936a31fd.jpg",
        "https://i.pinimg.com/originals/18/4d/c1/184dc1c19baccbb6557b30868c0fc446.jpg",
        "https://i.pinimg.com/originals/af/31/11/af31110033bdce8b42375c8cedd7ae8c.jpg",
        "https://i.pinimg.com/originals/d2/c1/d8/d2c1d87872c3a148122224040bf2bd5e.jpg",
        "https://i.pinimg.com/originals/c1/f5/70/c1f570063019c75830f28da5808e5d61.jpg",
        "https://i.pinimg.com/originals/9f/fc/66/9ffc66229e9221dcfd9352c46f43d13b.jpg",
        "https://i.pinimg.com/originals/ef/f8/15/eff815c73077a1be798cf694d9baca03.jpg",
        "https://i.pinimg.com/originals/9f/4d/b1/9f4db1b4d0877ac399425be7256365b8.jpg",
        "https://i.pinimg.com/originals/43/ad/fa/43adfa87a3692400afbd2edfdad34abb.jpg",
        "https://i.pinimg.com/originals/9b/db/96/9bdb96ef210bbd047c18eb46f065654f.jpg",
        "https://i.pinimg.com/originals/86/9a/06/869a066b117c8763f597701c385964d2.jpg",
        "https://i.pinimg.com/originals/a2/a5/53/a2a553d9af8b28736af8c18c88a079ef.jpg",
        "https://i.pinimg.com/originals/da/47/42/da47427cdd256edb5e0da11786c4a0b3.jpg",
        "https://i.pinimg.com/originals/b4/49/c8/b449c8b34a5af3f64179d1f30471d68c.jpg",
        "https://i.pinimg.com/originals/fb/ea/23/fbea2391187a0ccd6430c4f72362d5df.jpg",
        "https://i.pinimg.com/originals/76/74/81/7674813378dbe95cbf21234b936a31fd.jpg",
        "https://i.pinimg.com/originals/f2/77/2d/f2772d828813ba480f5c6b12adb4575c.jpg",
        "https://i.pinimg.com/originals/18/4d/c1/184dc1c19baccbb6557b30868c0fc446.jpg",
        "https://i.pinimg.com/originals/0e/01/53/0e01536bcc8b118b1c9540d25475aa2d.jpg",
        "https://i.pinimg.com/originals/af/31/11/af31110033bdce8b42375c8cedd7ae8c.jpg",
        "https://i.pinimg.com/originals/d2/c1/d8/d2c1d87872c3a148122224040bf2bd5e.jpg",
        "https://i.pinimg.com/originals/a5/e5/ba/a5e5ba12e07617d075e5605322c14828.jpg",
        "https://i.pinimg.com/originals/c1/f5/70/c1f570063019c75830f28da5808e5d61.jpg",
        "https://i.pinimg.com/originals/9f/fc/66/9ffc66229e9221dcfd9352c46f43d13b.jpg",
        "https://i.pinimg.com/originals/ef/f8/15/eff815c73077a1be798cf694d9baca03.jpg",
        "https://i.pinimg.com/originals/9f/4d/b1/9f4db1b4d0877ac399425be7256365b8.jpg",
        "https://i.pinimg.com/originals/43/ad/fa/43adfa87a3692400afbd2edfdad34abb.jpg",
        "https://i.pinimg.com/originals/9b/db/96/9bdb96ef210bbd047c18eb46f065654f.jpg",
        "https://i.pinimg.com/originals/86/9a/06/869a066b117c8763f597701c385964d2.jpg",
        "https://i.pinimg.com/originals/a2/a5/53/a2a553d9af8b28736af8c18c88a079ef.jpg",
        "https://i.pinimg.com/originals/da/47/42/da47427cdd256edb5e0da11786c4a0b3.jpg",
        "https://i.pinimg.com/originals/b4/49/c8/b449c8b34a5af3f64179d1f30471d68c.jpg",
        "https://i.pinimg.com/originals/fb/ea/23/fbea2391187a0ccd6430c4f72362d5df.jpg",
        "https://i.pinimg.com/originals/76/74/81/7674813378dbe95cbf21234b936a31fd.jpg",
        "https://i.pinimg.com/originals/f2/77/2d/f2772d828813ba480f5c6b12adb4575c.jpg",
        "https://i.pinimg.com/originals/18/4d/c1/184dc1c19baccbb6557b30868c0fc446.jpg",
        "https://i.pinimg.com/originals/0e/01/53/0e01536bcc8b118b1c9540d25475aa2d.jpg",
        "https://i.pinimg.com/originals/af/31/11/af31110033bdce8b42375c8cedd7ae8c.jpg",
        "https://i.pinimg.com/originals/d2/c1/d8/d2c1d87872c3a148122224040bf2bd5e.jpg",
        "https://i.pinimg.com/originals/a5/e5/ba/a5e5ba12e07617d075e5605322c14828.jpg"
    ]
    
    PictureFC = [
        "https://i.pinimg.com/originals/09/97/60/0997609e8e0b37039e75d7d80c846296.jpg",
        "https://i.pinimg.com/originals/d4/eb/d5/d4ebd58047535fc0b64b67c370c3e546.jpg",
        "https://i.pinimg.com/originals/92/43/1c/92431c99d84c15fc9bd4918f054cff5a.jpg",
        "https://i.pinimg.com/originals/9d/5a/50/9d5a5029938a2de1488940e6d6b858b0.jpg",
        "https://i.pinimg.com/originals/5f/0c/58/5f0c585b36fa10ec466565abc5118ba1.jpg",
        "https://i.pinimg.com/originals/9d/41/33/9d41334c92bd4cddf471e9ffb7647e14.jpg",
        "https://i.pinimg.com/originals/c9/1a/65/c91a65fcc1debc2f46094fe6fa1b9269.jpg",
        "https://i.pinimg.com/originals/5a/a5/38/5aa5386bf1666c01be19bef2671960e2.jpg",
        "https://i.pinimg.com/originals/8f/84/fd/8f84fd30df2be65728520958c88309b3.jpg",
        "https://i.pinimg.com/originals/c8/6f/d4/c86fd438e7a08abfdb777ad6a607a4a0.jpg",
        "https://i.pinimg.com/originals/09/97/60/0997609e8e0b37039e75d7d80c846296.jpg",
        "https://i.pinimg.com/originals/d4/eb/d5/d4ebd58047535fc0b64b67c370c3e546.jpg",
        "https://i.pinimg.com/originals/92/43/1c/92431c99d84c15fc9bd4918f054cff5a.jpg",
        "https://i.pinimg.com/originals/9d/5a/50/9d5a5029938a2de1488940e6d6b858b0.jpg",
        "https://i.pinimg.com/originals/5f/0c/58/5f0c585b36fa10ec466565abc5118ba1.jpg",
        "https://i.pinimg.com/originals/9d/41/33/9d41334c92bd4cddf471e9ffb7647e14.jpg",
        "https://i.pinimg.com/originals/c9/1a/65/c91a65fcc1debc2f46094fe6fa1b9269.jpg",
        "https://i.pinimg.com/originals/5a/a5/38/5aa5386bf1666c01be19bef2671960e2.jpg",
        "https://i.pinimg.com/originals/8f/84/fd/8f84fd30df2be65728520958c88309b3.jpg",
        "https://i.pinimg.com/originals/c8/6f/d4/c86fd438e7a08abfdb777ad6a607a4a0.jpg",
        "https://i.pinimg.com/originals/48/68/b5/4868b544e10d48b70760b7a4701c245d.jpg",
        "https://i.pinimg.com/originals/37/04/3d/37043d77c1c30ba177f08e6cbb71a348.jpg",
        "https://i.pinimg.com/originals/55/5e/1f/555e1f7976054c55b966ccc240499a85.jpg",
        "https://i.pinimg.com/originals/78/82/a6/7882a6d2773dbc492dab5c198b5ecb82.jpg",
        "https://i.pinimg.com/originals/c9/ce/e0/c9cee06877d29391a4e5a32530c1d02d.jpg",
        "https://i.pinimg.com/originals/09/97/60/0997609e8e0b37039e75d7d80c846296.jpg",
        "https://i.pinimg.com/originals/d4/eb/d5/d4ebd58047535fc0b64b67c370c3e546.jpg",
        "https://i.pinimg.com/originals/92/43/1c/92431c99d84c15fc9bd4918f054cff5a.jpg",
        "https://i.pinimg.com/originals/9d/5a/50/9d5a5029938a2de1488940e6d6b858b0.jpg",
        "https://i.pinimg.com/originals/5f/0c/58/5f0c585b36fa10ec466565abc5118ba1.jpg",
        "https://i.pinimg.com/originals/9d/41/33/9d41334c92bd4cddf471e9ffb7647e14.jpg",
        "https://i.pinimg.com/originals/c9/1a/65/c91a65fcc1debc2f46094fe6fa1b9269.jpg",
        "https://i.pinimg.com/originals/5a/a5/38/5aa5386bf1666c01be19bef2671960e2.jpg",
        "https://i.pinimg.com/originals/8f/84/fd/8f84fd30df2be65728520958c88309b3.jpg",
        "https://i.pinimg.com/originals/c8/6f/d4/c86fd438e7a08abfdb777ad6a607a4a0.jpg",
        "https://i.pinimg.com/originals/48/68/b5/4868b544e10d48b70760b7a4701c245d.jpg",
        "https://i.pinimg.com/originals/37/04/3d/37043d77c1c30ba177f08e6cbb71a348.jpg",
        "https://i.pinimg.com/originals/55/5e/1f/555e1f7976054c55b966ccc240499a85.jpg",
        "https://i.pinimg.com/originals/11/e1/ae/11e1ae985ef831bc8e3566601bb0568b.jpg",
        "https://i.pinimg.com/originals/78/82/a6/7882a6d2773dbc492dab5c198b5ecb82.jpg",
        "https://i.pinimg.com/originals/c9/ce/e0/c9cee06877d29391a4e5a32530c1d02d.jpg",
        "https://i.pinimg.com/originals/09/97/60/0997609e8e0b37039e75d7d80c846296.jpg",
        "https://i.pinimg.com/originals/d4/eb/d5/d4ebd58047535fc0b64b67c370c3e546.jpg",
        "https://i.pinimg.com/originals/92/43/1c/92431c99d84c15fc9bd4918f054cff5a.jpg",
        "https://i.pinimg.com/originals/9d/5a/50/9d5a5029938a2de1488940e6d6b858b0.jpg",
        "https://i.pinimg.com/originals/5f/0c/58/5f0c585b36fa10ec466565abc5118ba1.jpg",
        "https://i.pinimg.com/originals/9d/41/33/9d41334c92bd4cddf471e9ffb7647e14.jpg",
        "https://i.pinimg.com/originals/c9/1a/65/c91a65fcc1debc2f46094fe6fa1b9269.jpg",
        "https://i.pinimg.com/originals/5a/a5/38/5aa5386bf1666c01be19bef2671960e2.jpg",
        "https://i.pinimg.com/originals/8f/84/fd/8f84fd30df2be65728520958c88309b3.jpg",
        "https://i.pinimg.com/originals/c8/6f/d4/c86fd438e7a08abfdb777ad6a607a4a0.jpg",
        "https://i.pinimg.com/originals/48/68/b5/4868b544e10d48b70760b7a4701c245d.jpg",
        "https://i.pinimg.com/originals/37/04/3d/37043d77c1c30ba177f08e6cbb71a348.jpg",
        "https://i.pinimg.com/originals/55/5e/1f/555e1f7976054c55b966ccc240499a85.jpg",
        "https://i.pinimg.com/originals/11/e1/ae/11e1ae985ef831bc8e3566601bb0568b.jpg",
        "https://i.pinimg.com/originals/78/82/a6/7882a6d2773dbc492dab5c198b5ecb82.jpg",
        "https://i.pinimg.com/originals/c9/ce/e0/c9cee06877d29391a4e5a32530c1d02d.jpg",
        "https://i.pinimg.com/originals/48/68/b5/4868b544e10d48b70760b7a4701c245d.jpg",
        "https://i.pinimg.com/originals/34/4c/c0/344cc0e70263ae9943ee0c8dfdddcbd1.jpg",
        "https://i.pinimg.com/originals/1a/d8/ce/1ad8ce27832e1cf4c662b3855211cc49.jpg",
        "https://i.pinimg.com/originals/8a/22/be/8a22be171dbf3ee674cad8a01d24831a.jpg",
        "https://i.pinimg.com/originals/84/d8/cc/84d8cca598193ff7646b1a064a9daca5.jpg",
        "https://i.pinimg.com/originals/db/42/ef/db42efef2dec36911976320de1d96201.jpg",
        "https://i.pinimg.com/originals/98/e5/60/98e56076d90df9b44bf3dea60cb2f0a4.jpg",
        "https://i.pinimg.com/originals/74/65/2d/74652dcc92c8daf7dffa75125859d760.jpg",
        "https://i.pinimg.com/originals/ed/bc/8d/edbc8dc33edcea05ddff565d2425dcd7.jpg",
        "https://i.pinimg.com/originals/08/c0/91/08c091ef270811c68dce271d1daea062.jpg",
        "https://i.pinimg.com/originals/48/68/b5/4868b544e10d48b70760b7a4701c245d.jpg",
        "https://i.pinimg.com/originals/34/4c/c0/344cc0e70263ae9943ee0c8dfdddcbd1.jpg",
        "https://i.pinimg.com/originals/1a/d8/ce/1ad8ce27832e1cf4c662b3855211cc49.jpg",
        "https://i.pinimg.com/originals/8a/22/be/8a22be171dbf3ee674cad8a01d24831a.jpg",
        "https://i.pinimg.com/originals/84/d8/cc/84d8cca598193ff7646b1a064a9daca5.jpg",
        "https://i.pinimg.com/originals/db/42/ef/db42efef2dec36911976320de1d96201.jpg",
        "https://i.pinimg.com/originals/98/e5/60/98e56076d90df9b44bf3dea60cb2f0a4.jpg",
        "https://i.pinimg.com/originals/74/65/2d/74652dcc92c8daf7dffa75125859d760.jpg",
        "https://i.pinimg.com/originals/ed/bc/8d/edbc8dc33edcea05ddff565d2425dcd7.jpg",
        "https://i.pinimg.com/originals/08/c0/91/08c091ef270811c68dce271d1daea062.jpg",
        "https://i.pinimg.com/originals/32/90/2f/32902febd1f837e1edd18da862fd6a86.jpg",
        "https://i.pinimg.com/originals/bb/9e/1b/bb9e1b98a2e30b3109328f44ae6d4aec.jpg",
        "https://i.pinimg.com/originals/78/8d/cd/788dcd537e4d71203fe22e52765ee38d.jpg",
        "https://i.pinimg.com/originals/9c/dc/ee/9cdcee6b496115664c224e80ac737409.jpg",
        "https://i.pinimg.com/originals/48/68/b5/4868b544e10d48b70760b7a4701c245d.jpg",
        "https://i.pinimg.com/originals/34/4c/c0/344cc0e70263ae9943ee0c8dfdddcbd1.jpg",
        "https://i.pinimg.com/originals/1a/d8/ce/1ad8ce27832e1cf4c662b3855211cc49.jpg",
        "https://i.pinimg.com/originals/8a/22/be/8a22be171dbf3ee674cad8a01d24831a.jpg",
        "https://i.pinimg.com/originals/84/d8/cc/84d8cca598193ff7646b1a064a9daca5.jpg",
        "https://i.pinimg.com/originals/db/42/ef/db42efef2dec36911976320de1d96201.jpg",
        "https://i.pinimg.com/originals/ed/81/f7/ed81f74e462df56d0e9bd79c9eb7d820.jpg",
        "https://i.pinimg.com/originals/98/e5/60/98e56076d90df9b44bf3dea60cb2f0a4.jpg",
        "https://i.pinimg.com/originals/74/65/2d/74652dcc92c8daf7dffa75125859d760.jpg",
        "https://i.pinimg.com/originals/ed/bc/8d/edbc8dc33edcea05ddff565d2425dcd7.jpg",
        "https://i.pinimg.com/originals/08/c0/91/08c091ef270811c68dce271d1daea062.jpg",
        "https://i.pinimg.com/originals/f2/5e/fd/f25efdfac4fa861ff17bc9aba5b42369.jpg",
        "https://i.pinimg.com/originals/32/90/2f/32902febd1f837e1edd18da862fd6a86.jpg",
        "https://i.pinimg.com/originals/bb/9e/1b/bb9e1b98a2e30b3109328f44ae6d4aec.jpg",
        "https://i.pinimg.com/originals/b7/23/43/b723435aa60f05734481a63a28de56bf.jpg",
        "https://i.pinimg.com/originals/78/8d/cd/788dcd537e4d71203fe22e52765ee38d.jpg",
        "https://i.pinimg.com/originals/9c/dc/ee/9cdcee6b496115664c224e80ac737409.jpg",
        "https://i.pinimg.com/originals/48/68/b5/4868b544e10d48b70760b7a4701c245d.jpg",
        "https://i.pinimg.com/originals/34/4c/c0/344cc0e70263ae9943ee0c8dfdddcbd1.jpg",
        "https://i.pinimg.com/originals/1a/d8/ce/1ad8ce27832e1cf4c662b3855211cc49.jpg",
        "https://i.pinimg.com/originals/8a/22/be/8a22be171dbf3ee674cad8a01d24831a.jpg",
        "https://i.pinimg.com/originals/84/d8/cc/84d8cca598193ff7646b1a064a9daca5.jpg",
        "https://i.pinimg.com/originals/db/42/ef/db42efef2dec36911976320de1d96201.jpg",
        "https://i.pinimg.com/originals/ed/81/f7/ed81f74e462df56d0e9bd79c9eb7d820.jpg",
        "https://i.pinimg.com/originals/98/e5/60/98e56076d90df9b44bf3dea60cb2f0a4.jpg",
        "https://i.pinimg.com/originals/74/65/2d/74652dcc92c8daf7dffa75125859d760.jpg",
        "https://i.pinimg.com/originals/ed/bc/8d/edbc8dc33edcea05ddff565d2425dcd7.jpg",
        "https://i.pinimg.com/originals/08/c0/91/08c091ef270811c68dce271d1daea062.jpg",
        "https://i.pinimg.com/originals/f2/5e/fd/f25efdfac4fa861ff17bc9aba5b42369.jpg",
        "https://i.pinimg.com/originals/32/90/2f/32902febd1f837e1edd18da862fd6a86.jpg",
        "https://i.pinimg.com/originals/bb/9e/1b/bb9e1b98a2e30b3109328f44ae6d4aec.jpg",
        "https://i.pinimg.com/originals/b7/23/43/b723435aa60f05734481a63a28de56bf.jpg",
        "https://i.pinimg.com/originals/78/8d/cd/788dcd537e4d71203fe22e52765ee38d.jpg",
        "https://i.pinimg.com/originals/9c/dc/ee/9cdcee6b496115664c224e80ac737409.jpg"
    ]

    delay = int(input(f"{Fore.YELLOW}Delay (seconds) between creations: {Style.RESET_ALL}"))
    count = int(input(f"{Fore.YELLOW}Number of pages to create: {Style.RESET_ALL}"))

    tokens = read_tokens(tokens_file)

    if not tokens:
        print(f"{Fore.RED}Error: No tokens found in tokens.txt.{Style.RESET_ALL}")
        return

    for _ in range(count):
        # Randomize name and photo for each page creation
        randomizer = random.choice(["M", "F"])
        name = random.choice(nameMc) + " " + random.choice(nameLast) if randomizer == "M" else random.choice(nameFc) + " " + random.choice(nameLast)
        photos = random.choice(PictureMC) if randomizer == "M" else random.choice(PictureFC)
        category_input = "2211"
        category = category_input.split(',')
        
        results = []
        for token in tokens[:]:  # Iterate over a copy of the tokens list
            name = random.choice(nameMc) + " " + random.choice(nameLast) if randomizer == "M" else random.choice(nameFc) + " " + random.choice(nameLast)
            photos = random.choice(PictureMC) if randomizer == "M" else random.choice(PictureFC)
            
            result = CreatePage(name=name, category=category, token=token, picture=photos)
            results.append(result)
            time.sleep(delay)
            
            # Remove the token used from the list
            delete_token(tokens_file, token)
            break  # Move to the next iteration of page creation

        with open(page_file, "a") as f:
            f.write("\n".join(results) + '\n')
        
        print("\n".join(results))

if __name__ == "__main__":
    main()
