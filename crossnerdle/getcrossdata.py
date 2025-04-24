from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

Service=webdriver.FirefoxService
Manager=GeckoDriverManager
Options= webdriver.FirefoxOptions
WebDriver=webdriver.Firefox


numbs=list("0123456789")
operators=["plus","minus","divide","multiply","equals"]

def fetch_data():
    """
    Fetches the HTML content of the Crossnerdle game page using Selenium.

    Uses a headless Firefox browser to load the page, allowing JavaScript
    to render the grid content.

    Returns:
        str: The HTML source code of the page.
    """
    browser_options =Options()
    browser_options.add_argument("--headless")
    browser_options.add_argument("--no-sandbox")
    browser_options.add_argument("--disable-dev-shm-usage")
    service = Service(
    executable_path=GeckoDriverManager().install(),
    service_args=[
    "--allow-hosts", "localhost"    
    ])
    # Initialize the WebDriver
    with WebDriver(service=service, options=browser_options) as driver:
        url = "https://nerdlegame.com/crossnerdle"
        driver.get(url)
        #time.sleep(3)  
        html = driver.page_source
    return html



def get_table():
    """
    Parses the fetched HTML to extract the Crossnerdle grid.

    Returns:
        list: 2D list representing the grid, with characters 0123456789+-/*=■
    """
    htmldata=fetch_data()
    soup = BeautifulSoup(htmldata, 'html.parser')


    table =[] 
    for row in soup.find_all('div', attrs = {'class':'flex justify-center mb-1'})[1:]  :        
        table.append([])
        for square in row.find_all('button', attrs = {'role':'navigation'}):
            lasttenchars=str(square).strip("</button>")[-10:]
            lastchar=lasttenchars[-1]
            operator=square.find('svg', attrs = {'xmlns':'http://www.w3.org/2000/svg'})
            if lastchar in numbs:
                elem=lastchar
            elif lastchar==" ":
                elem="?"
            elif operator:
                match operator["aria-label"]:
                    case "plus":
                        elem="+"
                    case "minus":
                        elem="-"
                    case "divide":
                        elem="/"
                    case "multipy":
                        elem="*"
                    case "equals":
                        elem="="
                    case _:
                        print(f"unrecognised operator {lastchar}")
                        exit(0)
            else:
                elem="■"
            table[-1].append(elem)
    return table

def print_table(table,unknowns=None):
    Error=0
    L=len(table)
    print("┏━━"+("━┳━━")*(L-1)+"━┓")
    for i,rawrow in enumerate(table):
       row=[]
       for j,elem in enumerate(rawrow):
            if (unknowns) and (elem=="?"):
                Sol=unknowns.pos[(i,j)]["possibilities"]
                if len(Sol)==1:
                    Sol=f"\033[92m{str(*Sol)}\033[0m"
                else:
                    Error+=1
                row.append(Sol)
            elif elem=="■":
                #row.append(f"\033[90m{elem}\033[0m")
                row.append(" ")
            else:
                row.append(elem)
       print("┃ "+(" ┃ ").join(row)+" ┃")
       if i!=len(table)-1:
        print("┣━━"+("━╋━━")*(L-1)+"━┫")
    print("┗━━"+("━┻━━")*(L-1)+"━┛")
    Nvars=len(unknowns.pos.items())
    Neq=len(unknowns.getallequations())
    Error=sum(len(unknowns.pos[(i,j)]["possibilities"])!=1 for (i,j),val in unknowns.pos.items())
    print(f"Nvars:{Nvars}, Neq:{Neq},Error: {Error}")