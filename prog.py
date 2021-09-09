import os
from user import Cadastro


carrinho = []
produtos = []
usuario_atual = []


class Store:


    def __init__(self):
        self.i_produtos()
        self.logo()
        self.menu_inicial()


    def i_produtos(self):
        with open('a_produtos.txt', 'r') as arquivo:
            for l in arquivo:
                x = l.split(',')
                x[2] = x[2].replace('\n', '')
                x[1] = float(x[1].replace('R$ ', ''))
                produtos.append(x)
        

    def menu_inicial(self):
        self.linha()
        print('''
        [1] - CADASTRAR
        [2] - LOGIN
        [0] - SAIR
        ''')
        self.linha()

        while True:
            self.opc = input('Digite uma opção: ')
            
            if self.opc == '1':
                Cadastro()
            elif self.opc == '2':
                a = self.logar()
                if a:
                    self.menu_loja(carrinho)
            elif self.opc == '0':
                self.exit()
            else:
                print('Opção não encontrada.')


    def menu_loja(self, carrinho):
        self.linha()
        print('''
        [1] - VER PRODUTOS
        [2] - VER CARRINHO
        [3] - EFETUAR PAGAMENTO
        [4] - MEUS DADOS
        [0] - LOGOUT
        ''')
        self.linha()

        while True:
            opx = input('Digite uma opção: ')
            
            if opx == '1':
                self.ver_produtos(produtos)
            elif opx == '2':
                self.ver_carrinho(carrinho, produtos)
            elif opx == '3':
                self.opcoes_pagamento()
            elif opx == '4':
                self.meus_dados(usuario_atual)
            elif opx == '0':
                carrinho.clear()
                usuario_atual.clear()
                self.menu_inicial()
            else:
                print('Opção não encontrada.')


    def logo(self):
        self.linha()
        print(f'''
                __   __                          
                \ \ / /  __ _   _ __   ___   _ _ 
                 \ V /  / _` | | '_ \ / _ \ | '_|
                  \_/   \__,_| | .__/ \___/ |_|  
                               |_|''')


    def linha(self):
        print('=='*33)
        

    def exit(self):
        exit()


    def logar(self):
        while True:
            self.cpf = input('Digite seu cpf: ').replace('.', '').replace('-', '')
            self.senha = input('Digite sua senha: ')
            if self.verificar_usuario(self.cpf, self.senha):
                print('Usuario logado com sucesso.')
                break
            else:
                print('Cpf ou senha invalida.')
        return True
        

    def verificar_usuario(self, cpf, senha):
        r_user = []
        
        with open('a_user_register.txt','r') as arquivo:
            for l in arquivo:
                r_user.append(l.split(','))

        for user in r_user:
            try:
                if str(user[3].replace('\n', '')) == str(cpf) and str(user[1].replace('\n', '')) == str(senha):
                    user[4] = user[4].replace('\n', '')
                    usuario_atual.append(user)
                    usuario_atual[0].append(user[4])
                    return True
            except IndexError:
                pass
        return False

    
    def ver_produtos(self, produtos):
        
        self.linha()      
        print('|Cód|  |Descrição|                                         |Preço|')
        self.linha()

        for produto in produtos:
            print(f'  {produto[0]:<5}{produto[2]:<50}R$ {int(produto[1]):.2f}')
        
        self.linha()

        print('''
        [CÓD 1-20] - COLOCAR NO CARRINHO
        [99] - VER CARRINHO
        [0] - VOLTAR
        ''')
        self.linha()

        while True:
            self.op = input('Digite uma opção: ')
            if self.op.isnumeric():
                if 1 <= int(self.op) <= 20 :
                    un = int(input(f'[{self.op}] - QUANTIDADE DE UNIDADES: '))
                    self.colocar_carrinho(self.op, un, produtos, usuario_atual, carrinho)
                elif self.op == '99':
                    self.ver_carrinho(carrinho, produtos)
                elif self.op == '0':
                    self.menu_loja(carrinho)
                else:
                    print('Opção não encontrada.')
            else:
                print('Opção não encontrada.')


    def colocar_carrinho(self, cod, un, produtos, usuario_atual, carrinho):
        saldo = float(usuario_atual[0][4])
        sum = 0
        registro = []
        for produto in produtos:
            if produto[0] == cod:
                sum += (produto[1] * un)
                if sum > saldo:
                    print(f'Limite do seu saldo foi ultrapassado.')
                    return False
                else:
                    print(f'{un} unidades do cód {cod} foram adicionados ao carrinho.')
                    usuario_atual[0][4] = float(usuario_atual[0][4]) - sum
                    existe = 0
                    for i in carrinho:
                        if i[0] == cod:
                            i[1] += un
                            existe = 1
                    if existe == 0:
                        registro.append(cod)
                        registro.append(un)
                        carrinho.append(registro)
    

    def ver_carrinho(self, carrinho, produtos):
        
        sum = 0
        self.linha()     
        print('|Cód|  |Descrição|                                    |un| |Preço|')
        self.linha()
        try:
            for item in carrinho:
                for produto in produtos:
                    if item[0] == produto[0]:
                        sum += item[1] * produto[1]
                        print(f'  {produto[0]:<5}{produto[2]:<47} {item[1]}  R$ {produto[1]}')
        except:
            pass
        
        self.linha()     
        print(f'|Total:  {sum:>56.2f}|')
        self.linha()


        self.linha()

        print('''
        [1] - REMOVER PRODUTO DO CARRINHO
        [2] - EFETUAR PAGAMENTO 
        [0] - VOLTAR
        ''')
        self.linha()

        while True:
            self.opa = input('Digite uma opção: ')
            
            if self.opa == '1':
                self.remover_produto(carrinho, usuario_atual[0][4], produtos, usuario_atual)
            elif self.opa == '2':
                self.opcoes_pagamento()
            elif self.opa == '0':
                self.menu_loja(carrinho)
            else:
                print('Opção não encontrada.')


    def opcoes_pagamento(self):
        self.linha()
        print('''
        [1] - DESCONTAR DO SALDO
        [2] - PAGAR CONTA 
        [0] - VOLTAR
        ''')
        self.linha()

        while True:
            self.opr = input('Digite uma opção: ')
            
            if self.opr == '1':
                self.descontar_saldo(usuario_atual[0][3], usuario_atual[0][4], carrinho)
            elif self.opr == '2':
                self.pagar_conta(usuario_atual[0][3], carrinho, usuario_atual)
            elif self.opr == '0':
                self.menu_loja(carrinho)
            else:
                print('Opção não encontrada.')


    def descontar_saldo(self, cpf, novo_saldo, carrinho):
        senha = input('Digite sua senha para confirmar o pagamento: ')
        conf = self.conferir_senha(senha, cpf)
        if conf:
            if len(carrinho) != 0:
                conta = []
                with open('a_user_register.txt','r') as arquivo:
                    for linha in arquivo:
                        a = linha.split(',')
                        if len(a) < 5:
                            continue
                        if a[3] == str(cpf):
                            a[4] = str(novo_saldo) + '\n'
                        conta.append(a)

                with open('a_user_register.txt','w') as arquivo:
                    for c in conta:
                        arquivo.write(str(f'{c[0]},{c[1]},{c[2]},{c[3]},{c[4]}')+'\n')
                print(f'Sua conta foi descontada, seu novo saldo é R$ {float(novo_saldo):.2f}')
                carrinho.clear()
                self.menu_loja(carrinho)
            else:
                print('Seu carrinho esta vazio.')
        else:
            print('Senha incorreta.')
            self.descontar_saldo(usuario_atual[0][3], usuario_atual[0][4], carrinho)


    def pagar_conta(self, cpf, carrinho, usuario_atual):
        senha = input('Digite sua senha para confirmar o pagamento: ')
        conf = self.conferir_senha(senha, cpf)
        if conf:
            if len(carrinho) != 0 or usuario_atual[0][4] != '1000':
                conta = []
                with open('a_user_register.txt','r') as arquivo:
                    for linha in arquivo:
                        a = linha.split(',')
                        if len(a) < 5:
                            continue
                        if a[3] == str(cpf):
                            a[4] = str(1000) + '\n'
                        conta.append(a)

                with open('a_user_register.txt','w') as arquivo:
                    for c in conta:
                        arquivo.write(str(f'{c[0]},{c[1]},{c[2]},{c[3]},{c[4]}')+'\n')

                print(f'Sua conta foi paga, seu novo saldo é de R$ 1.000,00')
                usuario_atual[0][4] = '1000'
                carrinho.clear()
                self.menu_loja(carrinho)
            else:
                print('Seu carrinho esta vazio.')
        else:
            print('Senha incorreta.')
            self.pagar_conta(usuario_atual[0][3], carrinho, usuario_atual)


    def meus_dados(self, usuario):
        self.linha()
        print()
        print(f'        Nome cadastrado: {usuario[0][0]}')
        print(f'        Email cadastrado: {usuario[0][2]}')
        print(f'        Cpf cadastrado: {self.cpf_formatado(usuario[0][3])}')
        print(f'        Saldo atual: R$ {self.saldo_atual(usuario[0][3]):.2f}')
        print(f'        Saldo com produtos no carrinho: R$ {float(usuario[0][4]):.2f}')
        print()
        self.menu_loja(carrinho)


    def cpf_formatado(self, cpf):
        cpf_f = ''
        c = 0
        for i in cpf:
            cpf_f += i
            c+=1
            if c == 3:
                cpf_f += '.'
            if c == 6:
                cpf_f += '.'
            if c == 9:
                cpf_f += '-'
        return cpf_f


    def remover_produto(self, carrinho, saldo, produtos, usuario_atual):
        novo_carrinho = []
        cod = input('Digite o código do produto: ')
        un = input('Digite a quantidade que deseja remover: ')
        if len(carrinho) != 0:
            for prod in carrinho:
                if int(prod[0]) == int(cod):
                    if int(prod[1]) <= int(un):
                        un = int(prod[1])
                        pass
                    else:
                        prod[1] = int(prod[1]) - int(un)
                        novo_carrinho.append(prod)
                else:
                    novo_carrinho.append(prod)
            
            for produto in produtos:
                if produto[0] == cod:
                    saldo += float(produto[1]) * int(un)
            usuario_atual[0][4] = saldo
            carrinho = novo_carrinho
            self.ver_carrinho(carrinho, produtos)
        else:
            print('Seu carrinho esta vazio.')


    def conferir_senha(self, senha, cpf):
        r_user = []
        
        with open('a_user_register.txt','r') as arquivo:
            for l in arquivo:
                r_user.append(l.split(','))

        for user in r_user:
            try:
                if str(user[3].replace('\n', '')) == str(cpf) and str(user[1].replace('\n', '')) == str(senha):
                    return True
            except IndexError:
                pass
        return False
    

    def saldo_atual(self, cpf):
        r_user = []
        with open('a_user_register.txt','r') as arquivo:
            for l in arquivo:
                r_user.append(l.split(','))
        
        for user in r_user:
            try:
                if str(user[3].replace('\n', '')) == str(cpf):
                    return float(user[4])
            except IndexError:
                pass
        