import csv
import datetime
import glob
import os
import re
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pygubu
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

print("Bem vindo ao AutoSus. Digite o nome do usuario e senha do site E-Sus:")
loginsenha = None
if loginsenha == None:
    loginuser = input("Digite o usuário: ")
    loginsenha = input("Digite a senha: ")
# PASTA QUE MANDA SELECIONAR O DESTINO DO DOWNLOAD DO CHROME
root = tk.Tk()
pastadestino = filedialog.askdirectory(initialdir='C:/Downloads', title='Selecione a pasta de Downloads do Chrome:')
print('Pasta destino será = {0}'.format(pastadestino))
root.destroy()

#SELECIONE A UI
root = tk.Tk()
uidoprograma = filedialog.askopenfilename(initialdir='C:/Downloads', title='Selecione o arquivo "UiAutoSus4.ui" na pasta do programa AutoSus:')
print('O arquivo UiAutoSus4.ui está localizado em = {0}'.format(uidoprograma))
root.destroy()

#workingdirectory = os.getcwd()
#os.chdir("AutoSus")

#os.chdir(workingdirectory)
print(uidoprograma)


# CAIXA DE TEXTO COM LUGAR PARA DIGITAR O NUMERO DOS PROFISSIONAIS E BOTAO PARA CONFIRMAR
class MyApplication(pygubu.TkApplication):
    def _create_ui(self):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file(uidoprograma)

        # 3: Create the widget using self.master as parent
        self.mainwindow = builder.get_object('Frame_1', self.master)
        self.entry_1 = self.builder.get_object('Text_1')
        self.entry_2 = self.builder.get_object('Text_2')
        self.entry_endereco = self.builder.get_object('Combobox_1')
        #self.entry_3 = self.builder.get_object('Text_3')
        #self.entry_4 = self.builder.get_object('Text_4')

        # Configure callbacks
        callbacks = {
            'botao_click': self.botao_click,
            'botao_click1': self.botao_click1,
        }
        builder.connect_callbacks(callbacks)

    def botao_click(self):
        global pn1  # Médicos e enfermeiros
        global pn2  # Agentes comunitários
        global pn3  # Técnicos de Enfermagem
        global pn4  # Dentistas
        global enderecopg
        global bypass
        pn1 = self.entry_1.get('1.0', tk.END)
        pn2 = self.entry_2.get('1.0', tk.END)
        enderecopg = self.entry_endereco.get()
        #pn3 = self.entry_3.get('1.0', tk.END)
        #pn4 = self.entry_4.get('1.0', tk.END)
        bypass = False
        root.destroy()

    def botao_click1(self):
        global bypass
        bypass = True
        root.destroy()



if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    # root.iconbitmap('icon.ico')
    app = MyApplication(root)
    app.run()


# NAVEGAÇÃO PELO SITE E-SUS E NAVEGAÇÃO ATÉ MENU PARA DIGITAR O PROFISSIONAL E COPIAR PRODUÇÃO
if bypass == False:
    lista_medenf = pn1.split()
    print("Os números dos profissionais procurados serão:", lista_medenf, )
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(enderecopg)
    driver.implicitly_wait(10)


    username = driver.find_element_by_class_name("login-input").send_keys(loginuser)

    driver.implicitly_wait(10)
    password = driver.find_element_by_xpath(
        "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div/div/div/div/div[3]/div/div[4]/input").send_keys(loginsenha)

    botao = driver.find_element_by_css_selector(".login-acessar").click()
    driver.implicitly_wait(10)
    gestormunicipal = driver.find_element_by_xpath('//*[@peid="GERIRMUNICIPIOS.GESTORMUNICIPAL-ALVORADARS"]').click()
    driver.implicitly_wait(10)

    if len(pn1) > 3:
        relatorio = driver.find_element_by_xpath(
            "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div[1]/div").click()
        driver.implicitly_wait(10)
        producao = driver.find_element_by_xpath('//*[@peid="RelatoriosViewImpl.RelatorioProducao"]').click()
        driver.implicitly_wait(10)
        atendimento = driver.find_element_by_xpath(
            "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[2]/div/div/div").click()
        driver.implicitly_wait(10)

        # BAIXANDO TODOS .CSV X. X = QUANTIDADE DE NUMEROS

        for x in range(len(lista_medenf)):  #
            print('profissional ' + str(x + 1))
            profissional = driver.find_element_by_xpath(
                "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[2]/div/div/div/div[14]/input")
            profissional.clear()
            profissional.click()
            profissional.send_keys(Keys.PAGE_DOWN)
            profissional.send_keys(lista_medenf[x])  # aqui será colocada o numero na hora de inicializar o programa
            time.sleep(1)
            pg = int(driver.find_elements_by_xpath('//*[@class="ytb-text"]')[1].text[-1])

            for j in range(pg):
                print('pagina ' + str(j + 1))
                profissional.click()
                profissional.clear()
                profissional.send_keys(lista_medenf[x])
                time.sleep(1)
                for k in range(j):
                    driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                    time.sleep(1)
                itens = driver.find_elements_by_xpath('//*[@class="search-item"]')
                for i in range(len(itens)):
                    print('pagina ' + str(j + 1) + ' - item ' + str(i + 1))
                    profissional.click()
                    profissional.clear()
                    profissional.send_keys(lista_medenf[x])
                    time.sleep(1)
                    for k in range(j):
                        driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                        time.sleep(1)
                    itens = driver.find_elements_by_xpath('//*[@class="search-item"]')
                    itens[i].click()
                    time.sleep(1)
                    driver.find_element_by_xpath(
                        "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button").click()
                    time.sleep(2)

                    wait = WebDriverWait(driver, timeout=60)
                    element = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                     "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button")))
                    print('CSV Impresso')
                    try:
                        driver.find_element_by_xpath('//*[@peid="EsusMessages.OK"]').click()
                    except:
                        print('baixou')
        print('Médicos e enfermeiros baixados.')

    # AGENTE COMUNITARIO CIDADAOS ATIVOS
    if len(pn2) > 3:
        lista_acs = pn2.split()
        # TENTANDO VOLTAR SE ESTIVER EM UM MENU DIFERENTE
        driver.get("http://esus.alvorada.rs.gov.br:8080/esus/#/pec/user?EhmB9Al5PDSU")
        driver.find_element_by_xpath(
            "//*[@peid='class br.gov.saude.esus.EsusUserMenuViewImpl.relatorios']").click()
        driver.find_element_by_xpath(
            "//*[@peid='RelatoriosViewImpl.RelatorioConsolidados']").click()  # link para consolidados
        driver.find_element_by_xpath("//*[@peid='CADASTRO_INDIVIDUAL']").click()  # cadastro individual

        for x in range(len(lista_acs)):  # conferir todos os caminhos
            print('ACS ' + str(x + 1))
            profissional = driver.find_element_by_xpath(
                "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[2]/div/div/div/div[12]/input")
            profissional.clear()
            profissional.click()
            profissional.send_keys(Keys.PAGE_DOWN)
            profissional.send_keys(lista_acs[x])  # aqui será colocada o numero na hora de inicializar o programa
            time.sleep(1)
            pg = None
            pg = int(driver.find_elements_by_xpath('//*[@class="ytb-text"]')[1].text[-1])

            for j in range(pg):  # contagem da pagina
                print('pagina ' + str(j + 1))
                profissional.click()
                profissional.clear()
                profissional.send_keys(lista_acs[x])
                time.sleep(1)
                for k in range(j):
                    driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                    time.sleep(1)

                itens = driver.find_elements_by_xpath('//*[@class="search-item"]')
                for i in range(len(itens)):
                    print('pagina ' + str(j + 1) + ' - item ' + str(i + 1))
                    profissional.click()
                    profissional.clear()
                    profissional.send_keys(lista_acs[x])
                    time.sleep(1)
                    for k in range(j):
                        driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                        time.sleep(1)
                    itens = driver.find_elements_by_xpath('//*[@class="search-item"]')
                    itens[i].click()
                    time.sleep(1)
                    driver.find_element_by_xpath(
                        "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button").click()
                    time.sleep(1)
                    wait = WebDriverWait(driver, timeout=60)
                    element = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                     "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button")))

                    print('CSV Impresso')
                    try:
                        driver.find_element_by_xpath('//*[@peid="EsusMessages.OK"]').click()
                    except:
                        print('baixou')
        print('ACS cidadaos ativos baixados.')

        '''# AGENTE COMUNITARIOS REGISTROS IDENTIFICADOS
        driver.get("http://esus.alvorada.rs.gov.br:8080/esus/#/pec/user?EhmB9Al5PDSU")
        driver.find_element_by_xpath(
            "//*[@peid='class br.gov.saude.esus.EsusUserMenuViewImpl.relatorios']").click()  # link para relatorios
        driver.find_element_by_xpath("//*[@peid='RelatoriosViewImpl.RelatorioProducao']").click()  # link para produção
        driver.find_element_by_xpath(
            "//*[@peid='VISITA_DOMICILIAR']").click()  # link para visita domiciliar e territorial
        for x in range(len(lista_acs)):  # conferir todos os caminhos
            print('ACS ' + str(x + 1))
            profissional = driver.find_element_by_xpath(
                "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[2]/div/div/div/div[14]/input")
            profissional.clear()
            profissional.click()
            profissional.send_keys(Keys.PAGE_DOWN)
            profissional.send_keys(lista_acs[x])  # aqui será colocada o numero na hora de inicializar o programa
            time.sleep(1)
            pg = 0
            driver.implicitly_wait(10)
            pg = int(driver.find_elements_by_xpath('//*[@class="ytb-text "]')[3].text[-1])
            driver.implicitly_wait(10)
            for j in range(pg):  # contagem da pagina
                print('pagina ' + str(j + 1))
                profissional.click()
                profissional.clear()
                profissional.send_keys(lista_acs[x])
                time.sleep(1)
                for k in range(j):
                    driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                    time.sleep(1)
                driver.implicitly_wait(10)
                itens2 = driver.find_elements_by_xpath('//*[@class="search-item "]')
                driver.implicitly_wait(10)
                for i in range(len(itens2)):
                    print('pagina ' + str(j + 1) + ' - item ' + str(i + 1))
                    profissional.click()
                    profissional.clear()
                    profissional.send_keys(lista_acs[x])
                    time.sleep(1)
                    for k in range(j):
                        driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                        time.sleep(1)
                    driver.implicitly_wait(10)
    
                    itens2 = driver.find_elements_by_xpath('//*[@class="search-item"]')
                    driver.implicitly_wait(10)
    
                    itens2[i].click()
    
                    driver.find_element_by_xpath(
                        "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button").click()
    
                    wait = WebDriverWait(driver, timeout=60)
                    element = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                     "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button")))
                    print('CSV Impresso')
                    try:
                        driver.find_element_by_xpath('//*[@peid="EsusMessages.OK"]').click()
                    except:
                        print('baixou')
    
    # TÉCNICO DE ENFERMAGEM ARRUMAR CAMINHO
    if len(pn3) > 3:
        lista_dent = pn3.split()
        try:  # TENTANDO VOLTAR SE ESTIVER EM UM MENU DIFERENTE
            driver.find_element_by_xpath(
                '/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[1]').click()
            time.sleep(1)
            driver.find_element_by_xpath(
                '/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[1]').click()
            time.sleep(1)
            driver.find_element_by_xpath(
                '/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[1]').click()
            time.sleep(1)
            driver.find_element_by_xpath(
                '/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[1]').click()
        finally:
            driver.find_element_by_xpath(
                "//*[@peid='class br.gov.saude.esus.EsusUserMenuViewImpl.relatorios']").click()  # link para relatorios
            driver.find_element_by_xpath("//*[@peid='RelatoriosViewImpl.RelatorioProducao']").click()  # link para produção
            driver.find_element_by_xpath("//*[@peid='ATENDIMENTO_ODONTOLOGICO']").click()  # link para
            # link para pegar total
            for x in range(len(lista_dent)):  # CONFERIR TODOS OS CAMINHOS
                print('Tec/Aux Enf ' + str(x + 1))
                profissional = driver.find_element_by_xpath(
                    "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[2]/div/div/div/div[14]/input")
                profissional.clear()
                profissional.click()
                profissional.send_keys(Keys.PAGE_DOWN)
                profissional.send_keys(lista_dent[x])  # aqui será colocada o numero na hora de inicializar o programa
                time.sleep(1)
                pg3 = int(driver.find_elements_by_xpath('//*[@class="ytb-text"]')[1].text[-1])
    
                for j in range(pg3):  # contagem da pagina
                    print('pagina ' + str(j + 1))
                    profissional.click()
                    profissional.clear()
                    profissional.send_keys(lista_dent[x])
                    time.sleep(1)
                    for k in range(j):
                        driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                        time.sleep(1)
                    itens = driver.find_elements_by_xpath('//*[@class="search-item"]')
                    for i in range(len(itens)):
                        print('pagina ' + str(j + 1) + ' - item ' + str(i + 1))
                        profissional.click()
                        profissional.clear()
                        profissional.send_keys(lista_dent[x])
                        time.sleep(1)
                        for k in range(j):
                            driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                            time.sleep(1)
                        itens = driver.find_elements_by_xpath('//*[@class="search-item"]')
                        itens[i].click()
                        time.sleep(1)
                        driver.find_element_by_xpath(
                            "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button").click()
                        time.sleep(1)
                        for k in range(j):
                            driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                            time.sleep(1)
                        itens = driver.find_elements_by_xpath('//*[@class="search-item"]')
                        itens[i].click()
                        time.sleep(1)
                        driver.find_element_by_xpath(
                            "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button").click()
                        time.sleep(2)
                        wait = WebDriverWait(driver, timeout=60)
                        element = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                         "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button")))
    
                        print('CSV Impresso')
                        try:
                            driver.find_element_by_xpath('//*[@peid="EsusMessages.OK"]').click()
                        except:
                            print('baixou')
    
                        try:
                            driver.find_element_by_xpath('//*[@peid="EsusMessages.OK"]').click()
                        except:
                            print('baixou')
            print(' baixados.')
    
    # DENTISTAS
    if len(pn4) > 3:
        lista_dent = pn4.split()
        driver.get("http://esus.alvorada.rs.gov.br:8080/esus/#/pec/user?EhmB9Al5PDSU")
        driver.find_element_by_xpath(
            "//*[@peid='class br.gov.saude.esus.EsusUserMenuViewImpl.relatorios']").click()  # link para relatorios
        driver.find_element_by_xpath("//*[@peid='RelatoriosViewImpl.RelatorioProducao']").click()  # link para produção
        driver.find_element_by_xpath("//*[@peid='ATENDIMENTO_ODONTOLOGICO']").click()  # link para
        # link para pegar total
        for x in range(len(lista_dent)):  # CONFERIR TODOS OS CAMINHOS
            print('Tec/Aux Enf ' + str(x + 1))
            profissional = driver.find_element_by_xpath(
                "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[2]/div/div/div/div[14]/input")
            profissional.clear()
            profissional.click()
            profissional.send_keys(Keys.PAGE_DOWN)
            profissional.send_keys(lista_dent[x])  # aqui será colocada o numero na hora de inicializar o programa
            time.sleep(1)
            pg = None
            pg = int(driver.find_elements_by_xpath('//*[@class="ytb-text"]')[1].text[-1])
    
            for j in range(pg):  # contagem da pagina
                print('pagina ' + str(j + 1))
                profissional.click()
                profissional.clear()
                profissional.send_keys(lista_dent[x])
                time.sleep(1)
                for k in range(j):
                    driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                    time.sleep(1)
                itens = driver.find_elements_by_xpath('//*[@class="search-item"]')
                for i in range(len(itens)):
                    print('pagina ' + str(j + 1) + ' - item ' + str(i + 1))
                    profissional.click()
                    profissional.clear()
                    profissional.send_keys(lista_dent[x])
                    time.sleep(1)
                    for k in range(j):
                        driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                        time.sleep(1)
                    itens = driver.find_elements_by_xpath('//*[@class="search-item"]')
                    itens[i].click()
                    time.sleep(1)
                    driver.find_element_by_xpath(
                        "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button").click()
                    time.sleep(1)
                    for k in range(j):
                        driver.find_element_by_xpath('//*[@class="x-btn-text x-tbar-page-next"]').click()
                        time.sleep(1)
                    itens = driver.find_elements_by_xpath('//*[@class="search-item"]')
                    itens[i].click()
                    time.sleep(1)
                    driver.find_element_by_xpath(
                        "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button").click()
                    time.sleep(2)
                    wait = WebDriverWait(driver, timeout=60)
                    element = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                     "/html/body/div[3]/div/div[2]/div/div/div/div/div/div[3]/div/div[3]/div/div/div/div[3]/button")))
                    print('CSV Impresso')
                    try:
                        driver.find_element_by_xpath('//*[@peid="EsusMessages.OK"]').click()
                    except:
                        print('baixou')
    
        print('Dentistas baixados.')
    '''
    bypass == True
else:
    print("foi")
    y = 0
    os.chdir(pastadestino)
    from openpyxl import Workbook
    workbook = Workbook()
    sheet = workbook.active
    sheet.column_dimensions['A'].width = 60
    sheet.column_dimensions['B'].width = 30
    data = [
        ["Nome do Funcionário", "Número da produção ou cidadãos ativos"],
    ]
    for file in glob.glob("*.csv"):
        with open(file) as File:
            reader = csv.reader(File, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            rows = list(reader)
            resultado = str(rows[10])   # Equipe
            resultado1 = str(rows[11])  # Profissional, nome + numero
            resultado2 = str(rows[12])  # CBO , Médico ou enfermeiro
            resultado3 = str(rows[23])  # Registros idetificados
            resultado4 = str(rows[22])  # Registros não identificados

            '''resultado5 = resultado3 + resultado4
            resultado6 = re.findall("\d\d\d?\d?", resultado5)
            resultado7 = str(sum([int(i) for i in resultado6]))  # SOMA TOTAL

            # RETIRANDO ALGUNS CARACTERES E SOMANDO TODOS NA MESMA LINHA
            total = resultado + "  " + resultado1 + "  " + resultado2 + "  " + resultado3 + "  " + resultado4 + "   " + "Total: " + resultado7
            total1 = total.replace(";", ":")
            total2 = total1.replace("[", "")
            total3 = total2.replace("]", "")
            total4 = total3.replace("'", "")
            total5 = total4.replace("DA ESTRATÉGIA DE SAÚDE DA FAMÍLIA", "")
            total6 = total5.replace("   ", ",")
            total7 = total6.split(",")
            '''
            # CRIAÇÃO DO ARQUIVO COM A DATA CERTA
            filename = datetime.datetime.now()
            titulo = filename.strftime("%d" + "-" + "%b" + "-" + "%Y" + " horário " + "%H" + "%M")

            resultado1 = resultado1.replace("Profissional;", "")
            resultado1 = resultado1.replace("'", "")
            resultado1 = resultado1.replace("]", "")
            resultado1 = resultado1.replace("[", "")
            resultado4 = resultado4.replace("'", "")
            resultado4 = resultado4.replace("[", "")
            resultado4 = resultado4.replace("]", "")
            resultado4 = resultado4.replace(";", " ")

            resultado2 = resultado2.replace("'", "")
            resultado2 = resultado2.replace("[", "")
            resultado2 = resultado2.replace("]", "")
            resultado2 = resultado2.replace(";", " ")
            resultado2 = resultado2.replace("CBO","")


            data.append([resultado1, resultado4])
            #with open(pastadestino + '/' + titulo + ".txt", "a") as file:
            #    file.write(str(total7) + "\n\n")
    for row in data:
        sheet.append(row)
    workbook.save(filename=pastadestino + '/' + titulo + '.xlsx')
    workbook.close()

    tk.messagebox.showinfo(title="AutoSus", message="Pesquisa concluída! Dados copiados para o .txt")

        #os.startfile(pastadestino + '/' + titulo + ".txt")


'''  
        workbook = xlsxwriter.Workbook(pastadestino + '/' + titulo + '.xlsx')
        worksheet = workbook.add_worksheet()

        k = 0
        while k <= 5:
            worksheet.write_row(0 + k, 0, total7)
            workbook.close()
            k = k + 1
        y = y + 1
else:
    print(
        "Números copiados para arquivo .xlsx com sucesso!")  # pegar linhas especificas como Nome, total. etc. Perguntar para mãe quais informações pegar
    os.startfile(pastadestino + '/' + titulo + '.xlsx')

SALVAR EM ARQUIVO .XLSX (EM TESTES, NÃO ESTÁ FUNCIONANDO O APPEND)
'''
