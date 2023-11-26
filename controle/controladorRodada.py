from entidade.rodada import Rodada
from limite.telaRodada import TelaRodada
from entidade.partida import Partida

class ControladorRodada():
    def __init__(self, controlador_sistema):
        self.__controlador_sistema = controlador_sistema
        self.__tela_rodada = TelaRodada()
        self.__rodadas = []
        self.__aux_acertos = 0
    

    @property
    def rodadas(self):
        return self.__rodadas
    
    @property
    def controlador_sistema(self):
        return self.__controlador_sistema
    
    @property
    def tela_rodada(self):
        return self.__tela_rodada
    
    @property
    def aux_acertos(self):
        return self.__aux_acertos
    
    @aux_acertos.setter
    def aux_acertos(self, aux_acertos):
        self.__aux_acertos = aux_acertos
    
    
    def lista_rodadas(self, rodadas):
        aux = []
        for rodada in rodadas:
            aux.append([rodada.jogada_jog, rodada.jogada_comp, rodada.pontos_jog, rodada.pontos_comp])
        self.__tela_rodada.mostra_rodada(aux)       


    def rodada(self, partida):
        acertos = 0
        self.controlador_sistema.controlador_partida.aux_jog = []
        jogadnv = True
        while jogadnv==True:
            self.controlador_sistema.controlador_barco_super.destruido(partida.lista_barcos_comp)   

            poretorna=False
            acertou = 0
            while poretorna == False:
                self.controlador_sistema.controlador_barco_super.destruido(partida.lista_barcos_comp)
                
                list_oceano = partida.oceano.oceano
                dic_barcos = []
                for dic_obj in partida.lista_barcos_comp:
                    dic_barcos.append(vars(dic_obj))
                lista_jatiro = partida.jatiro

                list_escolhexy = self.controlador_sistema.tela_rodada.rodada1(list_oceano, dic_barcos, lista_jatiro)
                poretorna = list_escolhexy[2]
                seracertou = self.controlador_sistema.controlador_barco_super.tomoutiro(partida.lista_barcos_comp,list_escolhexy[0], list_escolhexy[1])

                jogadnv = seracertou
                
                partida.jatiro.append([list_escolhexy[0],list_escolhexy[1]])

                tiros = []
                tiros.append(list_escolhexy[0])
                tiros.append(list_escolhexy[1])
                self.controlador_sistema.controlador_barco_super.destruido(partida.lista_barcos_comp)
                if seracertou==True:
                    acertos+=1
                    acertos+= self.__aux_acertos
                
                if all(not barco.estado for barco in partida.lista_barcos_comp):
                    jogadnv = False
                
                
                list_oceano = partida.oceano.oceano
                dic_barcos = []
                for dic_obj in partida.lista_barcos_comp:
                    dic_barcos.append(vars(dic_obj))
                lista_jatiro = partida.jatiro

                self.controlador_sistema.tela_rodada.tela_acerto(list_oceano, dic_barcos, lista_jatiro, list_escolhexy)

                aux_ace = self.controlador_sistema.tela_rodada.conc_rodada(jogadnv, acertou)
                self.controlador_sistema.controlador_partida.aux_jog.append([tiros, aux_ace])
        return acertos

        
    def rodada_comp(self, partida):
        acertos = 0
        self.controlador_sistema.controlador_partida.aux_comp = []
        jogadnv = True
        while jogadnv==True:
            self.controlador_sistema.controlador_barco_super.destruido(partida.lista_barcos)   

            poretorna=False
            acertou = 0
            while poretorna == False:
                self.controlador_sistema.controlador_barco_super.destruido(partida.lista_barcos)
                
                list_oceano = partida.oceano.oceano
                dic_barcos = []
                for dic_obj in partida.lista_barcos:
                    dic_barcos.append(vars(dic_obj))
                lista_jatiro = partida.jatiro_comp
                
                list_escolhexy = self.controlador_sistema.tela_rodada.rodada1_comp(list_oceano, dic_barcos, lista_jatiro, partida.computador.joga(partida.oceano.oceano, partida.jatiro_comp))
                poretorna = list_escolhexy[2]
                seracertou = self.controlador_sistema.controlador_barco_super.tomoutiro(partida.lista_barcos,list_escolhexy[0], list_escolhexy[1] )
                
                jogadnv = seracertou

                partida.jatiro_comp.append([list_escolhexy[0],list_escolhexy[1]])

                tiros = []
                tiros.append(list_escolhexy[0])
                tiros.append(list_escolhexy[1])
                self.controlador_sistema.controlador_barco_super.destruido(partida.lista_barcos)
                if seracertou==True:
                    acertos+=1
                    acertos+= self.__aux_acertos
                
                if all(not barco.estado for barco in partida.lista_barcos):
                    jogadnv = False
                
                
                list_oceano = partida.oceano.oceano
                dic_barcos = []
                for dic_obj in partida.lista_barcos_comp:
                    dic_barcos.append(vars(dic_obj))
                lista_jatiro = partida.jatiro

                self.controlador_sistema.tela_rodada.tela_acerto_comp(list_oceano, dic_barcos, lista_jatiro, list_escolhexy)

                aux_ace = self.controlador_sistema.tela_rodada.conc_rodada(jogadnv, acertou)
                self.controlador_sistema.controlador_partida.aux_comp.append([tiros, aux_ace])
        return acertos
        
    def rodada_total(self, acertos_jog, acertos_comp):
        if self.__controlador_sistema.controlador_partida.aux_comp != []:
            aux_comp = self.__controlador_sistema.controlador_partida.aux_comp[0]
        else:
            aux_comp = self.__controlador_sistema.controlador_partida.aux_comp

        aux_jog = self.__controlador_sistema.controlador_partida.aux_jog[0]
        if len(aux_comp)==2 and len(aux_jog)==2:
            rodada = Rodada(self.__controlador_sistema.controlador_partida.aux_jog[0][0], self.__controlador_sistema.controlador_partida.aux_comp[0][0], self.__controlador_sistema.controlador_partida.aux_jog[0][1], self.__controlador_sistema.controlador_partida.aux_comp[0][1])
        elif len(aux_comp)==2:
            rodada = Rodada([self.__controlador_sistema.controlador_partida.aux_jog[0][0], self.__controlador_sistema.controlador_partida.aux_jog[0][1]], self.__controlador_sistema.controlador_partida.aux_comp[0][0], self.__controlador_sistema.controlador_partida.aux_jog[0][2], self.__controlador_sistema.controlador_partida.aux_comp[0][1])
        elif len(aux_jog)==2 and aux_comp==[]:
            rodada = Rodada(self.__controlador_sistema.controlador_partida.aux_jog[0][0], [self.__controlador_sistema.controlador_partida.aux_comp[0][0], self.__controlador_sistema.controlador_partida.aux_comp[0][1]], self.__controlador_sistema.controlador_partida.aux_jog[0][1], self.__controlador_sistema.controlador_partida.aux_comp[0][2])
        elif len(aux_jog)==2:
            rodada = Rodada(self.__controlador_sistema.controlador_partida.aux_jog[0][0], [self.__controlador_sistema.controlador_partida.aux_comp[0][0], self.__controlador_sistema.controlador_partida.aux_comp[0][1]], self.__controlador_sistema.controlador_partida.aux_jog[0][1], self.__controlador_sistema.controlador_partida.aux_comp[0][2])
        else:
            rodada = Rodada([self.__controlador_sistema.controlador_partida.aux_jog[0][0], self.__controlador_sistema.controlador_partida.aux_jog[0][1]], [self.__controlador_sistema.controlador_partida.aux_comp[0][0], self.__controlador_sistema.controlador_partida.aux_comp[0][1]], self.__controlador_sistema.controlador_partida.aux_jog[0][2], self.__controlador_sistema.controlador_partida.aux_comp[0][2])
        rodada.pontos_jog = acertos_jog
        rodada.pontos_comp = acertos_comp
        self.__rodadas.append(rodada)
        
        return rodada
        
        
        
    
        