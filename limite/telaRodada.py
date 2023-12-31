from controle.controladorPartida import ControladorPartida
from controle.controlador_barco_super import ControladorBarcoSuper
import PySimpleGUI as sg
import time

class TelaRodada():
    def __init__(self):
        self.__controlador_partida = ControladorPartida(self)
        self.__window = None
        sg.theme('darkpurple1')

    @property
    def controlador_partida(self):
        return self.__controlador_partida
    
    def mostra_rodada(self, dados_rodada):
        layout = [
                [sg.Table(values=dados_rodada,
                        headings=["Pontos jogador", "Pontos computador"],
                        auto_size_columns=False,
                        col_widths=[22, 22], 
                        font=('Bookman Old Style', 15),
                        justification='center',
                        key='-TABLE-')],
                [sg.Button("Retornar", key="-RETORNAR-", font=('Bookman Old Style', 11))]
            ]
        self.__window = sg.Window("Lista de rodadas", resizable=True).Layout(layout)
        
        while True:
            event, values = self.__window.read()
            if event == '-RETORNAR-' or event == sg.WIN_CLOSED:
                break
        self.__window.close()
    
    
            
            #############################################################################
                
    def rodada1(self, oceano, barcos, jatiro):
        

        def faztela( matrix):

            def create_layout(matrix, font_size):
                layout = [
                    [sg.Text(f'Selecione onde deseja atirar', font=('Bookman Old Style', 14))],  # Texto acima do layout principal
                ]
                for i, row in enumerate(matrix):
                    row_layout = []
                    for j, value in enumerate(row):
                        if value != '~~':  
                            button = sg.Button(str(value), size=(2, 1), key=(i, j), font=('Bookman Old Style', 12), pad=(1, 1), disabled=sg.BUTTON_DISABLED_MEANS_IGNORE)
                        else:
                            button = sg.Button(str(value), size=(2, 1), key=(i, j), font=('Bookman Old Style', 12), pad=(1, 1))
                        row_layout.append(button)
                    layout.append(row_layout)
                return layout

            def show_confirmation_dialog(row, col, barco):
                layout = [
                    [sg.Text(f'Deseja atirar na linha:{row} e coluna:{ col }', font=('Bookman Old Style', 11))],
                    [sg.Button('Sim', font=('Bookman Old Style', 11)), sg.Button('Cancelar', font=('Bookman Old Style', 11))]
                ]
                window = sg.Window('Confirmação', layout, finalize=True)
                while True:
                    event, _ = window.read()
                    if event in (sg.WIN_CLOSED, 'Cancelar'):
                        window.close()
                        return None
                    elif event == 'Sim':
                        window.close()
                        return [row, col]

            font_size = 12

            layout = create_layout(matrix, font_size)

            window = sg.Window('Matriz como Botões', layout)

            while True:
                event, values = window.read()

                if event == sg.WIN_CLOSED:
                    break
                elif isinstance(event, tuple):
                    row, col = event
                    if matrix[row][col] != '~~':
                        continue  
                    selection = show_confirmation_dialog(row+1, col+1, barco)
                    if selection is not None:
                        break  

            window.close()
            return selection
        
        


        for ycolunas in range(len(oceano)):
            for xlinha in range(len(oceano[ycolunas])):
                tembarco=False
                for barco in barcos:
                    for posicao in barco['_BS__posicoes']:
                        if posicao[0]==ycolunas and posicao[1]==xlinha:
                            if barco['_BS__estado']==True:
                                if posicao[2]==True:
                                    
                                    oceano[ycolunas][xlinha] = '~~'
                                    tembarco=True
                                else:
                                    oceano[ycolunas][xlinha] = '%'
                                    tembarco=True
                            else:
                                oceano[ycolunas][xlinha] = barco['_BS__nome'][0].lower()
                                tembarco=True

                if tembarco == False:
                    marzin=True
                    for jatiroin in jatiro:
                        if jatiroin[0] == ycolunas+1 and jatiroin[1] == xlinha+1:
                            oceano[ycolunas][xlinha] = '@'
                            marzin=False
                    if marzin==True:
                        oceano[ycolunas][xlinha] = '~~'
        
        selection = faztela(oceano)
        
        valory = selection[0]
        valorx = selection[1]

    


        #y é o primeiro  e x o segundo
        return (valory, valorx, True)
        
            
        
        #retorna true se acerta e false se erra
    ###################################################### 
    def tela_acerto(self, oceano, barcos, jatiro, tiro):

        def faztela(mostra):
            if mostra == 'mar':
                sg.popup('Você acertou o mar :(', font=('Bookman Old Style', 11))
            elif mostra == 'barco':
                sg.popup('Você acertou um barco :) mas ainda nao destruiu ele :(', font=('Bookman Old Style', 11))
            else:
                sg.popup(f'Você acertou e destruiu um barco do tipo {mostra} :)', font=('Bookman Old Style', 11))

        for ycolunas in range(len(oceano)):
            for xlinha in range(len(oceano[ycolunas])):
                tembarco=False
                for barco in barcos:
                    for posicao in barco['_BS__posicoes']:
                        if posicao[0]==ycolunas and posicao[1]==xlinha:
                            if barco['_BS__estado']==True:
                                if posicao[2]==True:
                                    if len(barco['_BS__posicoes'])==1:
                                        oceano[ycolunas][xlinha] = barco['_BS__nome']
                                        tembarco = True
                                    else:
                                        oceano[ycolunas][xlinha] = 'barco'
                                        tembarco=True
                                else:
                                    oceano[ycolunas][xlinha] = 'barco'
                                    tembarco=True
                            else:
                                oceano[ycolunas][xlinha] = barco['_BS__nome']
                                tembarco=True

                if tembarco == False:
                    marzin=True
                    for jatiroin in jatiro:
                        if jatiroin[0] == ycolunas+1 and jatiroin[1] == xlinha+1:
                            oceano[ycolunas][xlinha] = 'mar'
                            marzin=False
                    if marzin==True:
                        oceano[ycolunas][xlinha] = 'mar'
        
        prateleira = oceano[tiro[0]-1][tiro[1]-1]

        faztela(prateleira)

        ####################################################################################
    def conc_rodada(self, jogadnv, acertou):
        if jogadnv==True:
            acertou+=1
        return acertou
            
    def rodada1_comp(self, oceano, barcos, jatiro, tiroyx):
        
        def faztela(oceano, tiroyx):


            def show_matrix(matrix):
                layout = [
                    [sg.Text(f'O computador está selecionando onde vai atirar', font=('Bookman Old Style', 14))], 
                ]
                for row in matrix:
                    row_layout = []
                    for col in row:
                        button = sg.Button(col, disabled=sg.BUTTON_DISABLED_MEANS_IGNORE, size=(2, 1), pad=(1,1))
                        row_layout.append(button)
                    layout.append(row_layout)

                window = sg.Window('Matriz de Botões', layout, finalize=True)
                window.read(timeout=3000)  # Mantém a janela aberta por 2 segundos
                window.close()

            def show_popup(message):
                sg.popup(message, font=('Bookman Old Style', 11))

            def show_matrix2(matrix, highlight_coords):
                layout = [
                    [sg.Text(f'O computador irá atirar', font=('Bookman Old Style', 14))], 
                ]
                for i, row in enumerate(matrix):
                    row_layout = []
                    for j, col in enumerate(row):
                        button = sg.Button(col, disabled=sg.BUTTON_DISABLED_MEANS_IGNORE, size=(2, 1), pad = (1,1))
                        if [i, j] == highlight_coords:  
                            button = sg.Button(col, disabled=sg.BUTTON_DISABLED_MEANS_IGNORE, size=(2, 1), pad = (1,1), button_color=('white', 'red')) 
                        else:
                            button = sg.Button(col, disabled=sg.BUTTON_DISABLED_MEANS_IGNORE, size=(2, 1), pad = (1,1))
                        row_layout.append(button)
                    layout.append(row_layout)

                window = sg.Window('Matriz de Botões', layout, finalize=True)
                window.read(timeout=2000)  
                window.close()


            show_matrix(oceano)


          
            show_popup(f"O computador vai atirar em na linha {tiroyx[0]} e coluna { tiroyx[1]}")

            show_matrix2(oceano, [tiroyx[0]-1, tiroyx[1]-1])
        
        


        for ycolunas in range(len(oceano)):
            for xlinha in range(len(oceano[ycolunas])):
                tembarco=False
                for barco in barcos:
                    for posicao in barco['_BS__posicoes']:
                        if posicao[0]==ycolunas and posicao[1]==xlinha:
                            if barco['_BS__estado']==True:
                                if posicao[2]==True:
                                    
                                    oceano[ycolunas][xlinha] = barco['_BS__nome'][0]
                                    tembarco=True
                                else:
                                    oceano[ycolunas][xlinha] = '%'
                                    tembarco=True
                            else:
                                oceano[ycolunas][xlinha] = barco['_BS__nome'][0].lower()
                                tembarco=True

                if tembarco == False:
                    marzin=True
                    for jatiroin in jatiro:
                        if jatiroin[0] == ycolunas+1 and jatiroin[1] == xlinha+1:
                            oceano[ycolunas][xlinha] = '@'
                            marzin=False
                    if marzin==True:
                        oceano[ycolunas][xlinha] = '~~'
        
        faztela(oceano, tiroyx)
        


        ######################33
        valory = tiroyx[0]
        valorx = tiroyx[1]
        return (valory, valorx, True)
    
    def tela_acerto_comp(self, oceano, barcos, jatiro, tiro):

        def faztela(mostra):
            if mostra == 'mar':
                sg.popup('O Computador acertou o mar :)', font=('Bookman Old Style', 12))
            elif mostra == 'barco':
                sg.popup('O Computador acertou seu barco :( mas ainda não destruiu ele :)', font=('Bookman Old Style', 12))
            else:
                sg.popup(f'O Computador destruiu seu barco do tipo {mostra} :(', font=('Bookman Old Style', 12))

        for ycolunas in range(len(oceano)):
            for xlinha in range(len(oceano[ycolunas])):
                tembarco=False
                for barco in barcos:
                    for posicao in barco['_BS__posicoes']:
                        if posicao[0]==ycolunas and posicao[1]==xlinha:
                            if barco['_BS__estado']==True:
                                if posicao[2]==True:
                                    if len(barco['_BS__posicoes'])==1:
                                        oceano[ycolunas][xlinha] = barco['_BS__nome']
                                        tembarco = True
                                    else:
                                        oceano[ycolunas][xlinha] = 'barco'
                                        tembarco=True
                                else:
                                    oceano[ycolunas][xlinha] = 'barco'
                                    tembarco=True
                            else:
                                oceano[ycolunas][xlinha] = barco['_BS__nome']
                                tembarco=True

                if tembarco == False:
                    marzin=True
                    for jatiroin in jatiro:
                        if jatiroin[0] == ycolunas+1 and jatiroin[1] == xlinha+1:
                            oceano[ycolunas][xlinha] = 'mar'
                            marzin=False
                    if marzin==True:
                        oceano[ycolunas][xlinha] = 'mar'
        
    
        prateleira = oceano[tiro[0]-1][tiro[1]-1]

        faztela(prateleira)