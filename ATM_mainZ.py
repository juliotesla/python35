#! /usr/bin/python3
import serial
import sys
import time,os
from PyQt4 import QtGui, QtCore,QtTest
import pygame
import psycopg2
import sqlite3
import pyautogui
import subprocess
import RPi.GPIO as GPIO
#============================================ ATM_main  mayo 4  2020   =======
# git config --global user.name 'juliotesla'
# git config --global user.email'flojulio@gmail.com'
# git config credential.helper  store
# git config --global credential.helper store
# git clone https://github.com/juliotesla/python35.git
# errores
# 001 NO HAY SERVIDOR


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.tablaN={1:0,2:31,3:59,4:90,5:120,6:151,7:181,8:212,9:243,10:273,11:304,12:334,13:365}# normal
        self.tablaB={1:0,2:31,3:60,4:91,5:121,6:152,7:182,8:213,9:244,10:274,11:305,12:335,13:366}# bisiesto
        self.tecBuffer =''
        self.meses=['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
        self.entraFecha=''
        self.fechaturno=''
        self.cajero='001'
        self.turno='01'
        self.dicelo='                '
        self.amos=''
        self.elRepetido=''
        self.nuBoletoCompleto=''
        self.minutosAcobrar=0
        self.cuotaDolares=0
        self.cuotaPesos=0
        self.cuotaPesosCortesia=0
        self.factor_periodo=60
        self.tipoCambio=18.00
        self.tipoPase='01'
        self.Tipo='00'
        self.kz='001'
        self.fechaCobro=''
        self.empNumero='101'
        self.boletoCortesia='0000000'
        self.minutosBoleto=0
        self.minutosBolSin=0
        self.numeroBolSin=''
        self.minutos=0
        self.anos=''
        self.segundos=''
        self.configuracion=0
        self.bolValidado=''
        self.boletoPerdido=''
        self.boletoPase=''
        self.valorPase=''
        self.boletoRecibo=''
        self.IP='192.168.100.10'
        self.chava='Y'
        self.envio='N'
        self.pase='--------'
        self.closed='CCCC'
        self.supervisor='201'
        self.operador='201'
        self.seleccion='000'
        self.ATMnum=1
        self.es_red='C'
        self.cualBoton='N' # Captura2
        self.boletoAnt=''
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(12,GPIO.OUT)# abre barrera salida
        GPIO.setup(24,GPIO.OUT)# gaveta
        GPIO.setup(25,GPIO.OUT)
        GPIO.setup(23,GPIO.OUT)# ABRE BARRERA DE ENTRADA
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)# loop detector
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)# paso boleto
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)# boleto presente( arriba)
        GPIO.output(12,True)
        GPIO.output(24,True)
        GPIO.output(25,True)
        GPIO.output(23,True)
        #GPIO.add_event_detect(22,GPIO.FALLING, self.event_callback, bouncetime=300)
        self.home()
        
    def borraTeclado(self):
        self.btUno.hide()
        self.btDos.hide()
        self.btTres.hide()
        self.btCuatro.hide()
        self.btCinco.hide()
        self.btSeis.hide()
        self.btSiete.hide()
        self.btOcho.hide()
        self.btNueve.hide()
        self.btCero.hide()
        self.btPunto.hide()
        self.btEnter.hide()
        self.btLimpiar.hide()
           
    def botones(self,mio):
        if self.cualBoton=='S':
            a= self.qleCaptura.text()
            self.qleCaptura.setText(a+mio)
            self.qleCaptura.setFocus()
        else:
            a= self.qleCaptura2.text()
            self.qleCaptura2.setText(a+mio)
            self.qleCaptura2.setFocus()
        
    def botonesBack(self):
        if self.cualBoton=='S':
            a= self.qleCaptura.text()
            if len(a)>0:
                s=len(a)-1
                b=a[0:s]
                self.qleCaptura.setText(b)
                self.qleCaptura.setFocus()
        else:
            a= self.qleCaptura2.text()
            if len(a)>0:
                s=len(a)-1
                b=a[0:s]
                self.qleCaptura2.setText(b)
                self.qleCaptura2.setFocus()

    def elEnter(self):
        if self.cualBoton=='S':
            self.qleCaptura.setFocus()
        else:
            self.qleCaptura2.setFocus()

        self.timer1.stop()    
       
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        #print(self.cualBoton,' es el boton')
        self.timer1.start(1000)
        self.qleCaptura.setFocus()
        f.write(imprimePag)

    def elLimpiar(self):
        self.qleCaptura.setFocus()
        self.qleCaptura.clear()
        self.qleCaptura2.clear()
        
    def teclado(self):
        fontButton = QtGui.QFont("Arial",40,QtGui.QFont.Bold,True)# ======Botones
        self.btUno=QtGui.QPushButton(self)
        self.btUno.setFont(fontButton)
        self.btUno.setGeometry(QtCore.QRect(30,150,100,100))
        self.btUno.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btUno.setText('7')
        self.btUno.move(840,100)
        self.btUno.clicked.connect(lambda: self.botones(self.btUno.text()))
        self.btUno.show()
        
        self.btDos=QtGui.QPushButton(self)
        self.btDos.setFont(fontButton)
        self.btDos.setGeometry(QtCore.QRect(30,150,100,100))
        self.btDos.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btDos.setText('8')
        self.btDos.move(955,100)
        self.btDos.clicked.connect(lambda: self.botones(self.btDos.text()))
        self.btDos.show()
        
        self.btTres=QtGui.QPushButton(self)
        self.btTres.setFont(fontButton)
        self.btTres.setGeometry(QtCore.QRect(30,150,100,100))
        self.btTres.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btTres.setText('9')
        self.btTres.move(1070,100)
        self.btTres.clicked.connect(lambda: self.botones(self.btTres.text()))
        self.btTres.show()
        
        self.btCuatro=QtGui.QPushButton(self)
        self.btCuatro.setFont(fontButton)
        self.btCuatro.setGeometry(QtCore.QRect(30,150,100,100))
        self.btCuatro.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btCuatro.setText('4')
        self.btCuatro.move(840,210)
        self.btCuatro.clicked.connect(lambda: self.botones(self.btCuatro.text()))
        self.btCuatro.show()
        
        self.btCinco=QtGui.QPushButton(self)
        self.btCinco.setFont(fontButton)
        self.btCinco.setGeometry(QtCore.QRect(30,150,100,100))
        self.btCinco.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btCinco.setText('5')
        self.btCinco.move(955,210)
        self.btCinco.clicked.connect(lambda: self.botones(self.btCinco.text()))
        self.btCinco.show()
        
        self.btSeis=QtGui.QPushButton(self)
        self.btSeis.setFont(fontButton)
        self.btSeis.setGeometry(QtCore.QRect(30,150,100,100))
        self.btSeis.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btSeis.setText('6')
        self.btSeis.move(1070,210)
        self.btSeis.clicked.connect(lambda: self.botones(self.btSeis.text()))
        self.btSeis.show()
        
        self.btSiete=QtGui.QPushButton(self)
        self.btSiete.setFont(fontButton)
        self.btSiete.setGeometry(QtCore.QRect(30,150,100,100))
        self.btSiete.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btSiete.setText('1')
        self.btSiete.move(840,320)
        self.btSiete.clicked.connect(lambda: self.botones(self.btSiete.text()))
        self.btSiete.show()
        
        self.btOcho=QtGui.QPushButton(self)
        self.btOcho.setFont(fontButton)
        self.btOcho.setGeometry(QtCore.QRect(30,150,100,100))
        self.btOcho.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btOcho.setText('2')
        self.btOcho.move(955,320)
        self.btOcho.clicked.connect(lambda: self.botones(self.btOcho.text()))
        self.btOcho.show()
        
        self.btNueve=QtGui.QPushButton(self)
        self.btNueve.setFont(fontButton)
        self.btNueve.setGeometry(QtCore.QRect(30,150,100,100))
        self.btNueve.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btNueve.setText('3')
        self.btNueve.move(1070,320)
        self.btNueve.clicked.connect(lambda: self.botones(self.btNueve.text()))
        self.btNueve.show()
        
        self.btCero=QtGui.QPushButton(self)
        self.btCero.setFont(fontButton)
        self.btCero.setGeometry(QtCore.QRect(30,150,220,100))
        self.btCero.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btCero.setText('0')
        self.btCero.move(840,430)
        self.btCero.clicked.connect(lambda: self.botones(self.btCero.text()))
        self.btCero.show()
        
        self.btPunto=QtGui.QPushButton(self)
        self.btPunto.setFont(fontButton)
        self.btPunto.setGeometry(QtCore.QRect(30,150,100,100))
        self.btPunto.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btPunto.setText('.')
        self.btPunto.move(1070,430)
        self.btPunto.clicked.connect(lambda: self.botones(self.btPunto.text()))
        self.btPunto.show()
        
        fontButtonE = QtGui.QFont("Arial",30,QtGui.QFont.Bold,True)
        fontButtonT = QtGui.QFont("Arial",20,QtGui.QFont.Bold,True)
        self.btEnter=QtGui.QPushButton(self)
        self.btEnter.setFont(fontButtonE)
        self.btEnter.setGeometry(QtCore.QRect(30,150,200,100))
        self.btEnter.setStyleSheet("background-color:'Green';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btEnter.setText('Enter')
        self.btEnter.move(840,560)
        self.btEnter.clicked.connect(self.elEnter)
        self.btEnter.show()
        
        self.btLimpiar=QtGui.QPushButton(self)
        self.btLimpiar.setFont(fontButton)
        self.btLimpiar.setGeometry(QtCore.QRect(30,150,100,100))
        self.btLimpiar.setStyleSheet("background-color:'Light Gray';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.btLimpiar.setText('Del')
        self.btLimpiar.move(1070,560)
        self.btLimpiar.clicked.connect(self.elLimpiar)
        self.btLimpiar.show()
        
       
    def botones(self,mio):
        if self.cualBoton=='S':
            a= self.qleCaptura.text()
            self.qleCaptura.setText(a+mio)
            self.qleCaptura.setFocus()
        else:
            a= self.qleCaptura2.text()
            self.qleCaptura2.setText(a+mio)
            self.qleCaptura2.setFocus()
        
    def botonesBack(self):
        if self.cualBoton=='S':
            a= self.qleCaptura.text()
            if len(a)>0:
                s=len(a)-1
                b=a[0:s]
                self.qleCaptura.setText(b)
                self.qleCaptura.setFocus()
        else:
            a= self.qleCaptura2.text()
            if len(a)>0:
                s=len(a)-1
                b=a[0:s]
                self.qleCaptura2.setText(b)
                self.qleCaptura2.setFocus()

    def elEnter(self):
        if self.cualBoton=='S':
            self.qleCaptura.setFocus()
        else:
            self.qleCaptura2.setFocus()

        self.timer1.stop()    
       
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        #print(self.cualBoton,' es el boton')
        self.timer1.start(1000)
        self.qleCaptura.setFocus()

    def elLimpiar(self):
        self.qleCaptura.setFocus()
        self.qleCaptura.clear()
        self.qleCaptura2.clear()
        
    def imprimeError(self,atm,err,des,fe,li,mo):
        try:
            f= open('/dev/usb/lp0','w+')
        except:
            print('NO HAY IMPRESOR')
            return
        pc00=chr(27)+'PC00;0100,0042,1,2,2,00,01'+chr(10)+chr(0)
        pc01=chr(27)+'PC01;0100,0112,1,2,2,00,01'+chr(10)+chr(0)
        pc02=chr(27)+'PC02;0100,0192,1,2,2,00,01'+chr(10)+chr(0)
        pc03=chr(27)+'PC03;0100,0272,1,2,2,00,01'+chr(10)+chr(0)
        pc04=chr(27)+'PC04;0100,0352,1,2,2,00,01'+chr(10)+chr(0)
        pc05=chr(27)+'PC05;0100,0432,1,2,2,00,01'+chr(10)+chr(0)
        pc06=chr(27)+'PC06;0100,0592,1,2,2,00,01'+chr(10)+chr(0)
        rc00=chr(27)+'RC00;CAJERO...: '+atm+chr(10)+chr(0)
        rc01=chr(27)+'RC01;EVENTO # : '+err+chr(10)+chr(0)
        rc02=chr(27)+'RC02;EVENTO ..: '+des+chr(10)+chr(0)
        rc03=chr(27)+'RC03;FECHA....: '+fe+chr(10)+chr(0)
        rc04=chr(27)+'RC04;LINEA....: '+li+chr(10)+chr(0)
        rc05=chr(27)+'RC05;MODULO...: '+mo+chr(10)+chr(0)
        rc06=chr(27)+'RC06;REPORTE PARA SMARTICKET..'+chr(10)+chr(0)
        printArea=chr(27)+'D0900'+chr(10)+chr(0)
        imprimePag=chr(27)+chr(73)+chr(10)+chr(0)
        cortaHoja=chr(27)+chr(66)+chr(10)+chr(0)
        limpiaMem=chr(27)+chr(67)+chr(10)+chr(0)
        f.write(limpiaMem)
        f.write(printArea)
        f.write(pc00)
        f.write(pc01)
        f.write(pc02)
        f.write(pc03)
        f.write(pc04)
        f.write(pc05)
        f.write(pc06)
        f.write(rc00)
        f.write(rc01)
        f.write(rc02)
        f.write(rc03)
        f.write(rc04)
        f.write(rc05)
        f.write(rc06)
        f.write(cortaHoja)
        f.write(imprimePag)
        f.close()
        return
        
           
    def home(self):
      
        #self.setFixedSize(800 self.IP='192.168.100.10',530)
        self.setFixedSize(1200,670)
        self.center()
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Foreground,QtCore.Qt.red)
        self.setWindowIcon(QtGui.QIcon('01072000.gif'))
        font = QtGui.QFont("Times",14,QtGui.QFont.Bold,True)
      
        #==obtengo IP local y numero de empresa integer========================================================
      
        db = sqlite3.connect('atm20.sqlite')
        cursor=db.cursor()
        cursor.execute("SELECT * FROM datosATM WHERE rowid =1")
        user1 = cursor.fetchone() #retrieve the first row
        self.IP=user1[1]
        self.ATMnum=user1[2]
        self.cajero=user1[3]# igual a cajero en tabla atmcaracter
        db.close()
        try:
            connLocal = psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
            cursor=connLocal.cursor()
            sql="SELECT * FROM atmcaracter WHERE indice={}".format(self.ATMnum)
            cursor.execute(sql)
            user1=cursor.fetchone()
            folio=user1[17]
            serie='No.serie '+user1[17]
            boletoTitle=user1[1]
            empresa=user1[2]
            f= os.popen('ifconfig wlan0 | grep "inet 192" | cut -c 13-26')
            mifeT=f.read()
            mife=mifeT[0:14]
            titulo=empresa+'  CAJERO # '+boletoTitle+'  2020    '+mife
            self.setWindowTitle(titulo)
            #print(user1[9])
            self.closed=user1[20]
            self.fechaturno=user1[9]
            self.supervisor=user1[21]
            self.operador=user1[15]
            self.rego=user1[9]
            self.rego=self.rego[0:4]
            self.fechaturno=self.fechaturno[6:10]
            self.tipoCambio=user1[7]
            #self.cajero=user1[1]
            folioBolcorte=user1[14]
            self.alfafolCorte='%05d' % folioBolcorte
            connLocal.close()
        except:
            print('no hay servidor local',self.IP)
            caj=self.ATMnum+'/'+self.cajero
            self.fechaReal()
            fecha=self.fechaCobro
            self.imprimeError(caj,'001',self.IP,fecha,'375','ATMmainZ')
            return
            
            
      
        #==========================================
        self.lblFoto = QtGui.QLabel(self) #================ foto de tesla
        self.lblFotoTesla = QtGui.QLabel(self) 
        self.lblFotoTesla.size()
        self.lblFotoTesla.move(50,20)
        #pixmapT = QtGui.QPixmap('00000001.gif')
        pixmapT = QtGui.QPixmap('00000001.gif')
        pixmapT = pixmapT.scaled(80,80, QtCore.Qt.KeepAspectRatio)
        self.lblFotoTesla.setPixmap(pixmapT)
        #===================================================================
        fontLblSerie= QtGui.QFont("Arial",14,QtGui.QFont.Bold,False)#========= numero de serie
        self.lblSerie=QtGui.QLabel(self)
        self.lblSerie.setFont(fontLblSerie)
        self.lblSerie.move(80,60)
        self.lblSerie.setText(serie)
        #=============================================================
        fontLblAviso= QtGui.QFont("Arial",10,QtGui.QFont.Bold,False)#========= Aviso
        self.lblAviso=QtGui.QLabel(self)
        self.lblAviso.setFont(fontLblAviso)
        self.lblAviso.setFixedWidth(450)
        self.lblAviso.move(80,35)
        
        #===== defino fecha ================================================
        fontLblFecha = QtGui.QFont("Arial Black",34,QtGui.QFont.Bold,True)#====== FECHA
        self.frame=QtGui.QFrame(self)
        self.lblFecha= QtGui.QLabel(self)
        self.lblFecha.setFont(fontLblFecha)
        self.lblFecha.setStyleSheet("background-color:'Yellow';border: 4px solid black;border-radius: 10px solid ;Bold,true") 
        self.lblFecha.setFrameStyle(self.frame.Panel | self.frame.Raised)
        self.lblFecha.setLineWidth(2)
        self.fechaReal()
        self.lblFecha.setGeometry(40,100,260,200)
        self.lblFecha.setText(self.fechaActual)
        #============termino definicion de fecha ===================
        fontLblTipoCambio= QtGui.QFont("Arial",18,QtGui.QFont.Bold,False)#=========TIPO DE CAMBIO
        self.lblTipoCambio=QtGui.QLabel(self)
        self.lblTipoCambio.setFont(fontLblTipoCambio)
        self.lblTipoCambio.move(56,320)
        strtipoCambio=' {0:,.2f}'.format(self.tipoCambio)
        self.lblTipoCambio.setText('                                           ')
        self.lblTipoCambio.setText('   Tipo:'+strtipoCambio)
        #=============================================
        fontLblCajero= QtGui.QFont("Arial",18,QtGui.QFont.Bold,False)#========== CAJERO
        self.lblCajero=QtGui.QLabel(self)
        self.lblCajero.setFont(fontLblCajero)
        self.lblCajero.move(66,360)
        self.lblCajero.setText(' Supervisor: '+self.supervisor) 
        #=============================================
        fontLblTurno= QtGui.QFont("Arial",18,QtGui.QFont.Bold,False)#========== TURNO
        self.lblTurno=QtGui.QLabel(self)
        self.lblTurno.setFont(fontLblTurno)
        self.lblTurno.move(60,400)
        turnoTemp='  Corte: '+self.alfafolCorte+'/'+self.fechaturno[0:2]+':'+self.fechaturno[2:5]
        self.lblTurno.setText(turnoTemp) 
        #=======================================================================
        self.lblFoto = QtGui.QLabel(self) # ================ LOGO DEL CLIENTE
        pixmap = QtGui.QPixmap('SmarTicket.jpg')
        pixmapT = pixmap.scaled(220,220,QtCore.Qt.KeepAspectRatio)
        self.lblFoto.setPixmap(pixmapT)
        self.lblFoto.move(50,450)
     
        #=============================================
        fontLblAviso2= QtGui.QFont("Arial",34,QtGui.QFont.Bold,False)#========== Renglon # 2 de avisos
        self.lblAviso2=QtGui.QLabel(self)
        self.lblAviso2.setFont(fontLblAviso2)
        self.lblAviso2.setPalette(palette)
        self.lblAviso2.move(250,480)
        self.lblAviso2.setText('                                                                       ')
        #=============================================
        fontLblAviso3= QtGui.QFont("Arial",34,QtGui.QFont.Bold,False)#========== Renglon # 3 de avisos
        self.lblAviso3=QtGui.QLabel(self)
        self.lblAviso3.setFont(fontLblAviso3)
        self.lblAviso3.setPalette(palette)
        self.lblAviso3.move(250,535)
        self.lblAviso3.setText('                                                                   ') 
        #=============================================
        fontLblAviso4= QtGui.QFont("Arial",14,QtGui.QFont.Bold,False)#========== Renglon # 4 de avisos
        self.lblAviso4=QtGui.QLabel(self)
        self.lblAviso4.setFont(fontLblAviso4)
        self.lblAviso4.setPalette(palette)
        self.lblAviso4.move(50,570)
        self.lblAviso4.setText('                                                                   ') 
        
        fontLblEntra= QtGui.QFont("Arial",17,QtGui.QFont.Bold,False)#========== ENTRO EN
        self.lblEntra=QtGui.QLabel(self)
        self.lblEntra.setFont(fontLblEntra)
        self.lblEntra.setFixedWidth(440)
        self.lblEntra.move(350,320)
        frameStyle = QtGui.QFrame.Sunken | QtGui.QFrame.Panel
        self.lblEntra.setFrameStyle(frameStyle)
       #===========================================================
        fontlblTiempo= QtGui.QFont("Arial",17,QtGui.QFont.Bold,False)#========== TIEMPOS
        self.lblTiempo=QtGui.QLabel(self)
        self.lblTiempo.setFont(fontlblTiempo)
        self.lblTiempo.setFixedWidth(440)
        self.lblTiempo.move(350,360)
        self.lblTiempo.setFrameStyle(frameStyle)
       
        #===========================================================
        fontLblBoleto= QtGui.QFont("Arial",18,QtGui.QFont.Bold,False)#========== NUMERO CAPTURADOonEnter
        self.lblBoleto=QtGui.QLabel(self)
        self.lblBoleto.setFont(fontLblBoleto)
        self.lblBoleto.setFixedWidth(440)
        self.lblBoleto.setAlignment(QtCore.Qt.AlignCenter)
        self.lblBoleto.setFrameStyle(frameStyle)
        self.lblBoleto.move(350,400)
       
        #================================================ self.cualBoton='S' # Captura============
        fontLblCuotaPesos= QtGui.QFont("Arial",58,QtGui.QFont.Bold,False)#========== CUOTA PESOS
        self.lblCuotaPesos=QtGui.QLabel(self)
        self.lblCuotaPesos.setFont(fontLblCuotaPesos)
        self.lblCuotaPesos.move(350,30)
        self.lblCuotaPesos.setFixedWidth(450)
        self.lblCuotaPesos.setText('     ')
         #============================================================
        fontLblCuotaDlls= QtGui.QFont("Arial",38,QtGui.QFont.Bold,False)#========== CUOTA DOLARES
        self.lblCuotaDlls=QtGui.QLabel(self)
        self.lblCuotaDlls.setFont(fontLblCuotaPesos)
        self.lblCuotaDlls.move(350,150)
        self.lblCuotaDlls.setFixedWidth(450)
        
        #============================================================
        font = QtGui.QFont("Arial",20,QtGui.QFont.Bold,True)# ======CAPTURA2 DATOS
        self.qleCaptura2 = QtGui.QLineEdit(self)
        self.qleCaptura2.setFont(font)
        self.qleCaptura2.setFixedWidth(250)
        self.qleCaptura2.move(50,600)
        self.qleCaptura2.setFocus()
        #self.qleCaptura2.textChanged[str].connect(self.onChanged)
        self.qleCaptura2.returnPressed.connect(self.onEnterDos)
        #============================================================
        font = QtGui.QFont("Arial",10,QtGui.QFont.Bold,True)# ======CAPTURA DATOS
        self.qleCaptura = QtGui.QLineEdit(self)
        self.qleCaptura.setFont(font)
        self.qleCaptura.setFixedWidth(190)
        self.qleCaptura.move(50,600)
        self.qleCaptura.hide()
        #self.qleCaptura.setFocus()
        #self.qleCaptura.returnPressed.connect(self.onEnter)
        #============================================================
        self.lblFotoError = QtGui.QLabel(self) 
        pixmapER = QtGui.QPixmap('error.jpg')
        pixmapER = pixmapER.scaled(320,290,QtCore.Qt.KeepAspectRatio)
        self.lblFotoError.setPixmap(pixmapER)
        self.lblFotoError.move(800,80)
        self.lblFotoError.hide()  
        self.timer1=QtCore.QTimer(self)
        self.timer1.timeout.connect(self.actualizaFecha)
        self.timer1.start(1000)
        self.timer2=QtCore.QTimer(self)
        self.timer2.timeout.connect(self.onEnter)
        self.timer2.start(10)
        self.timer3=QtCore.QTimer(self)
        self.timer3.timeout.connect(self.limpiaAvisosDos)
        self.timer4=QtCore.QTimer(self)
        self.timer4.timeout.connect(self.seacabo)
        self.show()
        self.qleCaptura2.hide()
        QtTest.QTest.qWait(1000)
        #self.avisoVoz('cobrado.mp3')
        print('ya..')
        #self.imprimePase()
        '''self.teclado()
        QtTest.QTest.qWait(5000)
        self.borraTeclado()'''
 
    def seacabo(self):
        print('paso un minuto')
        self.timer4.stop()
        self.avisoVoz('tiempopago.mp3')
        self.regresalo()
        
    
    def actualizaFecha(self):
        self.fechaReal()
        self.lblFecha.setText(self.fechaActual)
        
    def avisoVoz(self,voz):
        pygame.mixer.init()
        #pygame.mixer.music.load("Tesoro.mp3")
        #pygame.mixer.music.load("cobrado.mp3")
        pygame.mixer.music.load(voz)
        pygame.mixer.music.set_volume(2.0)
        pygame.mixer.music.play()

        
    def borraFotos(self):
        self.lblFotoError.hide()  
       
    def limpiaAvisosDos(self):
        self.lblAviso2.clear()
        self.lblAviso3.clear()
        self.lblAviso4.clear()
        self.lblFotoError.hide()  
        self.timer3.stop()
   
        
    def regresalo(self):
        GPIO.output(24,False)
        self.yafueleido()
        QtTest.QTest.qWait(1000)
        GPIO.output(24,True)
        
    def aceptado(self):
        GPIO.output(23,False)
        self.yafueleido()
        QtTest.QTest.qWait(1000)
        GPIO.output(23,True)

    def yafueleido(self):
        a='111111111'
        connLocal = psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
        cursor=connLocal.cursor()
        cursor.execute("UPDATE pendientes SET bolpendiente=%s WHERE refe=%s",(a,1))
        connLocal.commit()
        connLocal.close()
        return
          
        
    def onEnter(self):
        #print('es enter {}'.format(self.IP))
        GPIO.output(23,True)
        try:
            connLocal = psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
            cursor=connLocal.cursor()
            #print('si hay red')
            sql="SELECT * FROM pendientes WHERE refe={}".format(1)
            cursor.execute(sql)
            user1=cursor.fetchone()
            #print(user1[0])
        except:
            print('no hay red hh')
            return
            
        if user1[0]=='111111111':
            connLocal.close()
            return
       
        inputNumber= user1[0]
        self.lblAviso.clear()
        self.tecBuffer=inputNumber.lstrip()
        GPIO.output(25,False)
        if self.tecBuffer[0:3]=='088':
            connLocal2 = psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
            cursor1=connLocal2.cursor()
            az=self.tecBuffer
            cursor1.execute("SELECT * FROM tarjetas WHERE atmtarprox=%s",[az])
            user2=cursor1.fetchone()
            if user2==None:
                 self.yafueleido()
                 connLocal2.close()
                 self.lblAviso2.setText('                 TARJETA ....')
                 self.lblAviso3.setText('Esta tarjeta no valida..')
                 self.borraFotos()
                 self.lblFotoError.show()
                 self.qleCaptura.clear()
                 self.regresalo()
                 self.timer3.start(7000)
                 self.avisoVoz('valido.mp3')
                 return
                
            if len(user2[1])==9:
                self.operador=az
                self.tecBuffer=user2[1]
                connLocal2.close()
                self.yafueleido()
                               
        self.nuBoletoCompleto=self.tecBuffer
        
        if self.nuBoletoCompleto[0:3]=='000' and self.nuBoletoCompleto[5:6]=='0':
            self.tarjetaSin()
            return
        if self.nuBoletoCompleto[0:3]=='000' and self.nuBoletoCompleto[5:6]=='1':
            self.tarjetaCon()
            return
            
        if self.closed=='CCCC':
            self.lblAviso2.setText('                 CAJERO CERRADO....')
            self.lblAviso3.setText('Este cajero esta fuera de servicio..')
            self.borraFotos()
            self.lblFotoError.show()
            self.qleCaptura.clear()
            self.regresalo()
            self.timer3.start(7000)
            self.avisoVoz('cajero.mp3')
            return
          
        numeroBoleto=self.tecBuffer
        self.minutosBoleto=int(self.tecBuffer[3:9])
        minutosNow=self.fechaMinutos()
     
        if self.minutosBoleto>minutosNow:
            self.lblAviso2.setText('                 FECHA INCORRECTA..')
            self.lblAviso3.setText('La fecha del boleto esta adelantada')
            self.borraFotos()
            self.lblFotoError.show()
            self.qleCaptura.clear()
            self.regresalo()
            self.timer3.start(7000)
            self.avisoVoz('adelanta.mp3')
            return
      
        if self.repetido(self.tecBuffer[0:10]):
            self.lblAviso2.setText('                  YA COBRADO')
            self.lblAviso3.setText('Este boleto {}  ya fue cobrado'.format(self.elRepetido))
            self.borraFotos()
            self.lblFotoError.show()
            self.qleCaptura.clear()
            self.regresalo()
            self.timer3.start(7000)
            self.avisoVoz('cobrado.mp3')
            return
        
        if minutosNow-self.minutosBoleto>21600:
            self.lblAviso2.setText('                  TIEMPO LIMITE')
            self.lblAviso3.setText('Este boleto tiene mas de 15 dias')
            self.borraFotos()
            self.lblFotoError.show()
            self.qleCaptura.clear()
            self.regresalo()
            self.timer3.start(7000)
            self.avisoVoz('limite.mp3')
            return
        print('minutos..',self.minutosBoleto)
        if numeroBoleto==self.boletoAnt:
             self.yafueleido()
             return
        self.qleCaptura.clear()
        self.Tipo='01'
        self.calculaCuota()
        self.minutosBolSin=self.minutosBoleto
        self.numeroBolSin=self.tecBuffer[3:9]
        self.marcaPendientes()
        self.yafueleido()
        self.boletoAnt=numeroBoleto
        self.grabaVentas('P')
        connLocal.close()# &&&&&&&&&&&&&   temoral &&&&&&&&&&&&&&&&&&
        self.timer3.start(7000)
        self.avisoVoz('cuota.mp3')
        self.limpiaAvisosDos()
        self.timer4.start(60000)
        #self.validacion()
     
    def onEnterDos(self):
        
         
        if self.seleccion=='404':#====================ORDEN DE SALIDA ==================================     
            self.Tipo='16'
            inputNumber= self.qleCaptura2.text()
            if len(inputNumber)<1:
                self.qleCaptura2.clear()
                self.qleCaptura2.hide()
                self.borraTeclado()
                self.lblAviso4.clear()
                self.Tipo='00'
                self.lblAviso.clear()
                self.repaint()
                self.update()
                return
                
            if len(inputNumber)!=9:
                msg=QtGui.QMessageBox(self)
                msg.warning(self,"NUMERO INCORRECTO","Debe ser nueve digitos sin espacios",QtGui.QMessageBox.Ok,QtGui.QMessageBox.NoButton,QtGui.QMessageBox.NoButton)
                self.qleCaptura2.clear()
                self.avisoVoz('valido.mp3')
                self.qleCaptura2.clear()
                self.qleCaptura2.hide()
                self.borraTeclado()
                self.lblAviso4.clear()
                self.Tipo='00'
                self.lblAviso.clear()
                self.repaint()
                self.update()
                return
            #self.operador=self.seleccion
            self.nuBoletoCompleto=inputNumber
            tempo=int(self.nuBoletoCompleto[3:9])
            self.minutosBoleto=tempo
            self.minutosFecha(tempo)
            self.calculaCuota()
            self.boletoPase=self.nuBoletoCompleto
            self.grabaTarjetas('16')
            self.qleCaptura2.clear()
            self.qleCaptura2.hide()
            self.pesosCorte=0
            self.imprimePase()
            self.borraTeclado()
            self.lblAviso4.clear()
            self.Tipo='00'
            self.lblAviso.clear()
            self.lblAviso.setText('ORDEN DE SALIDA')
            self.repaint()
            self.update()
            self.lblAviso2.clear()
            self.lblAviso3.clear()
            self.lblAviso4.clear()
            
        if self.seleccion=='403':# ================================ CAMBIO DE FECHA
            inputNumber= self.qleCaptura2.text()
            #print(inputNumber)
            self.tecBuffer=inputNumber.lstrip()
            #print (self.tecBuffer,'inputnumber',inputNumber)
            if len(inputNumber)>11 and inputNumber[0:2]!='':
                month=['---','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                mezInt=int(self.tecBuffer[0:2])
                #print (self.tecBuffer[0:2])
                if mezInt>12 or mezInt<1:
                    mezInt=1
                mezAlfa=month[mezInt]
                dayAlfa=self.tecBuffer[2:4]
                yearAlfa=self.tecBuffer[4:8]
                horaAlfa=self.tecBuffer[8:10]
                minuAlfa=self.tecBuffer[10:12]
                if int(dayAlfa)>=1 and int(dayAlfa)<=31 and mezInt>=1 and mezInt<=12 and int(horaAlfa)<=23 and int(minuAlfa)<=59 and int(yearAlfa)>=2015:
                    fechaCaptada=mezAlfa+' '+dayAlfa+' '+yearAlfa+' '+horaAlfa+':'+minuAlfa+':00'
                    print(fechaCaptada)
                    self.Tipo='12'
                    # ====== no corre en windows
                    subprocess.Popen(["sudo","date","-s",fechaCaptada],shell=False)
                    print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
                    subprocess.Popen(["sudo","hwclock","-w"],shell=False)
                    print('dddddddddddddddddddddddddddddddddddddd')
                    self.fechaReal()
                    self.lblFecha.setText(self.fechaActual)
                    #self.operador=self.supervisor
                    self.minutosAcobrar=0
                    self.cuotaPesos=0
                    self.grabaTarjetas('12')
                    self.lblAviso.clear()
                    self.lblAviso.setText('CAMBIO DE FECHA')
                    
               
            self.lblAviso2.clear()
            self.lblAviso3.clear()
            self.lblAviso4.clear()
            self.qleCaptura2.clear()
            self.qleCaptura2.hide()
            self.borraTeclado()
            self.lblAviso4.clear() 
            self.avisoVoz('cajero.mp3')
            self.repaint()
            self.update()

        if self.seleccion=='402':# ================================ CAMBIAR TIPO DE CAMBIO
            inputNumber= self.qleCaptura2.text()
            tipoAnte=self.tipoCambio
            if len(inputNumber)>1:
                self.Tipo='11'
                self.tipoCambio=float(inputNumber)
                if self.tipoCambio==0 or self.tipoCambio>99:
                    self.tipoCambio=tipoAnte
                strtipoCambio=' {0:,.2f}'.format(self.tipoCambio)
                self.lblTipoCambio.setText('                                        ')
                self.lblTipoCambio.setText('   Tipo:'+strtipoCambio)
                a=self.tipoCambio
                b=self.operador
                c=self.ATMnum
                connLocal = psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
                cursor=connLocal.cursor()
                cursor.execute("UPDATE atmcaracter SET tipocambio=%s, operador=%s WHERE indice=%s",(a,b,c))
                connLocal.commit()
                connLocal.close()
                self.lblAviso.clear()
                self.lblAviso.setText('TIPO DE CAMBIO')
                self.minutosAcobrar=0
                self.cuotaPesos=0
                self.grabaTarjetas('11')
           
                strtipo=' {0:.2f}'.format(self.tipoCambio).lstrip()
                if len(strtipo)==4:
                    self.sendpesos='M10'+strtipo[0]+strtipo[2]+strtipo[3]
                if len(strtipo)==5:
                    self.sendpesos='M1'+strtipo[0]+strtipo[1]+strtipo[3]+strtipo[4]
                #print( self.sendpesos,' es el tipo')
               
            self.lblAviso2.clear()
            self.lblAviso3.clear()
            self.lblAviso4.clear()
            self.qleCaptura2.clear()
            self.qleCaptura2.hide()
            self.borraTeclado()
            self.lblAviso4.clear()
            self.repaint()
            self.update()
          
            
        
    #============== ES TARJETA CON CAPTURA ======================
    def tarjetaCon(self):
        #self.limpiaAvisos()
        self.lblAviso2.clear()
        self.lblAviso3.clear()
        self.lblAviso4.clear()
        self.qleCaptura.setFocus()
        self.seleccion=self.nuBoletoCompleto[6:9]
        #self.bolValidado=''
        if self.closed=='CCCC':
            self.lblAviso2.setText('                 CAJERO CERRADO....')
            self.lblAviso3.setText('Este cajero esta fuera de servicio..')
            self.borraFotos()
            self.lblFotoError.show()
            self.qleCaptura.clear()
            self.regresalo()
            self.timer3.start(7000)
            self.avisoVoz('cajero.mp3')
            return
          
        if self.seleccion=='404':
            self.lblCuotaPesos.clear()
            self.lblCuotaDlls.clear()
            self.teclado()
            self.qleCaptura2.show()
            self.qleCaptura2.setFocus()
            self.lblAviso4.setText('    NUMERO DE BOLETO ')
            
        if self.seleccion=='403':# ==================================== CAMBIAR DE HORA
            self.lblCuotaPesos.clear()
            self.lblCuotaDlls.clear()
            self.teclado()
            self.qleCaptura2.show()
            self.qleCaptura2.setFocus()
            self.lblAviso.setText('CAMBIO DE FECHA')
            self.lblAviso4.setText('Abr-21-2020-14:30 = 042120201430 ')

        if self.seleccion=='402':# ==================================== CAMBIAR TIPO DE CAMBIO
            self.lblCuotaPesos.clear()
            self.lblCuotaDlls.clear()
            self.teclado()
            self.qleCaptura2.show()
            self.qleCaptura2.setFocus()
            self.lblAviso.setText('TIPO DE CAMBIO')
            self.lblAviso4.setText ('     Pesos X Dolar')
        return
    #============== ES TARJETA SIN CAPTURA========================
    def tarjetaSin(self):
        self.qleCaptura.clear()
        self.limpiaAvisos()
        self.seleccion=self.nuBoletoCompleto[6:9]
        
        #print('tarjeta sin captura')
        if self.nuBoletoCompleto[6]=='1':
            if self.closed=='CCCC':
                self.lblAviso2.clear()
                self.lblAviso3.clear()
                self.lblAviso4.clear()
                #self.operador=self.seleccion
                self.closed='AAAA'
                self.lblAviso.clear()
                self.lblAviso.setText('REGISTRO ABIERTO')
            else:
                #self.operador=self.seleccion
                self.closed='CCCC'
                self.lblAviso.clear()
                self.lblAviso.setText('REGISTRO CERRADO')
           
            a=self.operador
            b=self.closed
            c=self.ATMnum
            connLocal = psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
            cursor=connLocal.cursor()
            cursor.execute("UPDATE atmcaracter SET operador=%s, closed=%s WHERE indice=%s",(a,b,c))
            connLocal.commit()
            connLocal.close()
            self.minutosAcobrar=0
            self.cuotaPesos=0
            self.Tipo = '13'
            self.grabaTarjetas('13')
            return
        
        if self.closed=='CCCC':
            self.lblAviso2.setText('                 CAJERO CERRADO....')
            self.lblAviso3.setText('Este cajero esta fuera de servicio..')
            self.borraFotos()
            self.lblFotoError.show()
            self.qleCaptura.clear()
            self.regresalo()
            self.timer3.start(7000)
            self.avisoVoz('cajero.mp3')
            return
        
        if self.nuBoletoCompleto[6]=='2':
            self.seleccion=self.nuBoletoCompleto[6:9]
            a=self.operador
            b=self.seleccion
            c=self.ATMnum
            connLocal = psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
            cursor=connLocal.cursor()
            cursor.execute("UPDATE atmcaracter SET operador=%s,supervisor=%s WHERE indice=%s",(a,b,c))
            connLocal.commit()
            connLocal.close()
            self.minutosAcobrar=0
            self.cuotaPesos=0
            self.Tipo = '15'
            self.grabaTarjetas('15')
            self.lblAviso.clear()
            self.lblAviso.setText('CAMBIO DE SUPERVISOR')
            self.lblCajero.setText(' Supervisor: '+self.supervisor) 
            self.repaint()
            self.update()
        print('val  ',self.bolValidado,self.seleccion)  
        #============================================VALIDA LA OPERACION  (herramienta)==========================
        if self.seleccion=='312' and self.bolValidado!='':
            conn= psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
            cursor=conn.cursor()
            az=self.nuBoletoCompleto
            cursor.execute("UPDATE atmventas SET atmesbol='B' WHERE atmesbol='P' and atmnumbol!=%s",[az])
            conn.commit()
            conn.close()
            self.aceptado()
            self.bolValidado=''
            self.lblAviso.setText('VALIDADO')
            self.imprimePase()
            GPIO.output(25,True)
        if self.seleccion == '321':#=========================================BORRA BASE DE DATOS=============================
            xxpp='2100000000'
            conn= psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
            cursor=conn.cursor()
            cursor.execute("DELETE  FROM atmventas WHERE atmfechcob<%s",[xxpp])
            conn.commit()
            conn.close()
            '''conn= psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
            cursor=conn.cursor()
            cursor.execute("VACUUM")
            conn.commit()
            conn.close()'''
            self.lblAviso.clear()
            self.lblAviso.setText('BASE DATOS BORRADO')

          

             
    
       
        
    def limpiaAvisos(self):
        self.qleCaptura.clear()
            
    
    #==============graba operacion en archivo 'ventas'==================       
    def grabaVentas(self,statu):
        global sinCobro
        conn= psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
        cursor=conn.cursor()
        az=self.nuBoletoCompleto
        cursor.execute("DELETE FROM atmventas WHERE atmesbol='P' and atmnumbol=%s",[az])
        conn.commit()
        conn.close()
        esboleto=statu
        if len(self.entraFecha)<4:
            self.anos=''
        valopera=self.cuotaPesos
        vacobra=self.cuotaPesos
        self.cuotaPesosCortesia=self.cuotaPesos
        conn= psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
        cursor=conn.cursor()
        az=self.nuBoletoCompleto
        cursor.execute("UPDATE atmventas SET atmesbol='N' WHERE atmesbol='P' and atmnumbol!=%s",[az])
        conn.commit()
        conn.close()
        if self.nuBoletoCompleto=='':
            self.nuBoletoCompleto='----------'
        conn= psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
        cursor=conn.cursor()
        query="""INSERT INTO atmventas (atmkz,atmcajero,atmesbol,atmtipo,atmnumbol,atmfechbol,atmfechcob,atmmincob,atmvalope,atmvalcob,atmtipocam,\
        atmturno,atmsuper,atmpase) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values=(self.kz,self.cajero,esboleto,self.Tipo,self.nuBoletoCompleto,self.anos+self.entraFecha,self.fechaCobro,self.minutosAcobrar,\
                valopera,vacobra,self.tipoCambio,self.turno,self.supervisor,self.pase)
        cursor.execute(query,values)
        conn.commit()
        conn.close()
        self.boletoPase=self.nuBoletoCompleto
        self.boletoCortesia=self.nuBoletoCompleto
        self.boletoRecibo=self.nuBoletoCompleto
        self.valorPase='${0:,.2f}'.format(vacobra)
        self.tipoPase=self.Tipo
        self.bolValidado=self.nuBoletoCompleto
        print('bolval....  '+self.bolValidado)
        #nuValidar=self.nuBoletoCompleto
        self.nuBoletoCompleto=''
        self.entraFecha=''
        self.minutos=0
        self.pesosCorte=self.cuotaPesos
        self.cuotaPesos=0
        self.Tipo='00'
       
    #=========== GRABA OPERACIONES CON TARJETAS (no ingresos)================
    def grabaTarjetas(self,statipo):
        self.qleCaptura.clear()
        self.Tipo=statipo
        esboleto='T'
        self.pase='--------'
        nuBoleto=self.nuBoletoCompleto
        self.fechaRealDos()
        self.fechaCobro=fechaCobro
        if self.Tipo!='16':
            nuBoleto='----------'
        self.minutos=0
        valopera=self.cuotaPesos
        vacobra=0
        if len(self.entraFecha)<4:
            self.entraFecha=self.fechaCobro[2:10]
        self.operador=self.operador[4:9]  
        print('graba tarjetas')
        conn= psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
        cursor=conn.cursor()
        query="""INSERT INTO atmventas (atmkz,atmcajero,atmesbol,atmtipo,atmnumbol,atmfechbol,atmfechcob,atmmincob,atmvalope,atmvalcob,atmtipocam,\
        atmturno,atmsuper,atmpase,atmoperador) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        values=(self.kz,self.cajero,esboleto,self.Tipo,nuBoleto,self.anos+self.entraFecha,self.fechaCobro,self.minutosAcobrar,\
                valopera,vacobra,self.tipoCambio,self.turno,self.supervisor,self.pase,self.operador)
        #print(values)
        cursor.execute(query,values)
        conn.commit()
        conn.close()
        
       
           
           
        if self.seleccion == '911':#========================= SALIR DEL PROGRAMA ===========================
            sys.exit(0)
            
       
   
         
    #==============CALCULA Y DESPLIEGA CUOTA =====================
    def calculaCuota(self):
        cuota = 0
        self.minutosAcobrar = self.fechaMinutos()-self.minutosBoleto
        entraFe= self.minutosFecha(self.minutosBoleto)
        tiempo = self.tiempoFecha()
        #print('minutos ',self.minutosAcobrar)
        periodo = self.periodoCobrar()
        
        cuotaPorDia=0
        if self.minutosAcobrar>1440:
            diax=int(self.minutosAcobrar/1440)
            cuotaPorDia=int(diax*80)
            #cuotaPorDia=int(diax*20.00)
            self.minutosAcobrar=self.minutosAcobrar-(diax*1440)
            periodo = self.periodoCobrar()
        cuota=10.00    
        if periodo>1 and periodo<=12:
            cuota=40
        if periodo>12:
            cuota=80
        cuota=cuota+cuotaPorDia
        self.cuotaPesos=cuota
        
        self.cuotaDolares=float(self.cuotaPesos)/float(self.tipoCambio)
        strcuotapesos='${0:,.2f}'.format(self.cuotaPesos)
        strcuotadolares='${0:,.2f}'.format(self.cuotaDolares)
        self.lblCuotaPesos.setText(strcuotapesos+'  m.n.')
        self.lblCuotaDlls.setText(strcuotadolares+' dlls')
        self.lblBoleto.setText(self.nuBoletoCompleto)
        self.lblTiempo.setText('Tiempo: '+tiempo)
        self.lblEntra.setText('   Entra: '+entraFe)  
        self.lblCuotaPesos.repaint()
        self.lblCuotaDlls.repaint()
        #self.cuotaCambio=self.cuotaPesos
      
           
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #========================= LA FECHA REAL  ==============================		
    def fechaReal(self):
        mes=int(time.strftime('%m'))
        dia=time.strftime('%d')
        hora=time.strftime('%H')
        minuto=time.strftime('%M')
        self.anos =time.strftime('%Y')
        self.anos = self.anos[2:4]
        self.tabla=self.tablaN
        
        if int(self.anos)%4==0:
            self.tabla=self.tablaB
            
        self.amos=self.anos
        strmes=self.meses[mes-1]
        self.fechaActual = strmes+' '+dia+'\n'+hora+':'+minuto
        if mes<10:
            self.fechaCobro=self.anos+'0'+str(mes)+dia+hora+minuto
        else:
            self.fechaCobro=self.anos+str(mes)+dia+hora+minuto 
        return self.fechaActual
    
    #========================= LA FECHA REAL DOS ==============================
    def fechaRealDos(self):  # en windows
        global fechaCobro
        global anos
        mes=int(time.strftime('%m'))
        dia=time.strftime('%d')
        hora=time.strftime('%H')
        minuto=time.strftime('%M')
        anos =time.strftime('%Y')
        anos = anos[2:4]
        strmes=self.meses[mes-1]
        fechaActual = strmes+' '+dia+' '+hora+':'+minuto
        if mes<10:
            fechaCobro=anos+'0'+str(mes)+dia+hora+minuto
        else:
            fechaCobro=anos+str(mes)+dia+hora+minuto 
        return fechaActual

    def minutosFecha(self,dime):
        dias = dime//1440
        tempo = (dime-(dias*1440))
        horas = tempo//60
        self.minutos = tempo-(horas*60)
        self.anos =time.strftime('%Y')
        self.anos = self.anos[2:4]
        self.tabla=self.tablaN
        if int(self.anos)%4==0:
            self.tabla=self.tablaB
            
        for mas in self.tabla:
            if self.tabla[mas]>=dias:
                mes=mas-1
                break
        strhoras=str(horas)
        if horas<10:
            strhoras='0'+str(horas)
        strmes=str(mes)
        if mes<10:
            strmes='0'+str(mes)
        
        dias = dias - self.tabla[mes]
       
        strdias=str(dias)
        if dias<10:
            strdias='0'+str(dias)
      
        elmes = self.meses[mes-1]
        strminutos = str(self.minutos)
        if self.minutos<10:
            strminutos='0'+str(self.minutos)
        fecha_entra = elmes+' '+strdias+' / '+strhoras+':'+strminutos
        self.entraFecha=strmes+strdias+strhoras+strminutos
        return fecha_entra
    
    def fechaMinutos(self):
        mes=int(time.strftime('%m'))
        dia=(int(time.strftime('%d')))*1440  
        hora=(int(time.strftime('%H')))*60
        minuto=int(time.strftime('%M'))
        self.segundos=time.strftime('%S')
        self.anos =time.strftime('%Y')
        self.anos = self.anos[2:4]
        self.tabla=self.tablaN
        if int(self.anos)%4==0:
            self.tabla=self.tablaB
        dtabla=self.tabla[mes]*1440
        #self.anos =int(time.strftime('%Y'))
        totaMinutos=dtabla+dia+hora+minuto
        return totaMinutos
    

    def repetido(self,numRepetido):
        conn = psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM atmventas WHERE atmesbol='B' and atmcorte='N'")
        for row in cursor:
            if numRepetido in row:
                self.elRepetido=row[6]
                conn.close()
                return True
       
        conn.close()
    #======  CONVIERTE LOS PERIODOS POR COBRAR A FECHA CALENDARIO ========
    def tiempoFecha(self):
        dias =0
        horas =0 
        if self.minutosAcobrar>=1440:
            dias = self.minutosAcobrar//1440
        tempo = (self.minutosAcobrar-(dias*1440))
        if tempo>=60:
            horas = tempo//60
        minutes = (tempo-(horas*60))
        self.fechacobro = str(dias)+' Dias '+str(horas)+' Horas '+str(minutes)+' Min'
        return self.fechacobro
    #========================== CALCULA LOS PERIODOS POR COBRAR ===============

    def periodoCobrar(self):
        dile=self.minutosAcobrar
        if self.minutosAcobrar<self.factor_periodo:
            dile = self.factor_periodo
        periodo = dile /self.factor_periodo
        if dile % self.factor_periodo != 0:
            periodo = periodo+1
        periodo=int(periodo)
        return periodo
    #=========== marca con una N  los boletos no operados ===============
    def marcaPendientes(self):
        conn= psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
        cursor=conn.cursor()
        az=self.nuBoletoCompleto
        cursor.execute("UPDATE atmventas SET atmesbol='N' WHERE atmesbol='P' and atmnumbol!=%s",[az])
        conn.commit()
        conn.close()
    
 
    #======================= VALIDACION ====================================================
    def validacion(self):
        GPIO.output(23,True)
        if self.bolValidado=='':
            return
        
    def imprimePase(self):
        ESC = 27
        GS = 29
        folioPase=0
        digitoStr=''
        try:
            f= open('/dev/usb/lp0','w+')
        except:
            print('NO HAY IMPRESOR')
            return
        connLocal = psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
        cursor=connLocal.cursor()
        sql="SELECT * FROM atmcaracter WHERE indice={}".format(self.ATMnum)
        cursor.execute(sql)
        user1=cursor.fetchone()
        tolerancia=user1[23]
        foliopase=user1[16]
        folioanterior=user1[16]
        digito=user1[22]
        razonPase=user1[24]
        domiPase=user1[25]
        coloPase=user1[26]
        ciuaPase=user1[27]
        connLocal.close()
        if digito<6:
            digito=6 # el primer digito del 6 al 9 indica que es un pase/recibo
        boletero=user1[8]
        if digito>9:
            digito=6
       
        fecMinutes=self.fechaMinutos()+tolerancia
        minutosPase=self.fechaMinutos()
        fechaPago=self.minutosFecha(minutosPase)
        if folioanterior==fecMinutes:
            digito=digito+1
        else:
            digito=6
        digitoStr=str(digito)
        digitoBol=boletero
        paseDigito=digitoStr+digitoBol
        #print('boletero ',boletero)
        alfaTemp=str(fecMinutes)
        boleto=paseDigito+alfaTemp.zfill(6)       
        fechaPase=self.minutosFecha(fecMinutes)
        print(' es el folio recibo ',foliopase)
        #foliopase=foliopase+1
        alfaTemp=str(foliopase)
        folioPaseAlfa=alfaTemp.zfill(6)
        alfaFolio='%09d'% foliopase 
        a=self.fechaReal()
        boletoPase=boleto
        #self.pesosCorte=100#========================================tempo
        strcuotapesos='${0:,.2f}'.format(self.pesosCorte)
        #print ('ano =20'+self.amos)
        ano='20'+self.amos
        #barcodeFormat=chr(27)+'PB00'+chr(59)+'0360'+chr(44)+'0430'+chr(44)+'4'+chr(44)+'1'+chr(44)+'1'+chr(44)+'0180'+chr(10)+chr(0) # 90 grados
        barcodeFormat=chr(27)+'PB00'+chr(59)+'0180'+chr(44)+'0680'+chr(44)+'1'+chr(44)+'1'+chr(44)+'0'+chr(44)+'0180'+chr(10)+chr(0) # 0 grados vertical 
        barcodeData=chr(27)+chr(82)+chr(66)+'00'+chr(59)+boletoPase+chr(10)+chr(0)
        #barcodeData=chr(27)+chr(82)+chr(66)+'00'+chr(59)+'0152490'+chr(10)+chr(0)
        printArea=chr(27)+'D0900'+chr(10)+chr(0)
        imprimePag=chr(27)+chr(73)+chr(10)+chr(0)
        cortaHoja=chr(27)+chr(66)+chr(10)+chr(0)
        limpiaMem=chr(27)+chr(67)+chr(10)+chr(0)

        pc00=chr(27)+'PC00;0180,0042,1,3,4,00,01'+chr(10)+chr(0)
        pc01=chr(27)+'PC01;0180,0275,1,1,2,00,01'+chr(10)+chr(0)
        #pc02=chr(27)+'PC02;0200,0300,1,1,1,00,01'+chr(10)+chr(0)
        pc03=chr(27)+'PC03;0200,0330,1,1,1,00,01'+chr(10)+chr(0)
        pc04=chr(27)+'PC04;0200,0360,1,1,1,00,01'+chr(10)+chr(0)
        pc05=chr(27)+'PC05;0020,0180,1,2,2,00,01'+chr(10)+chr(0)
        pc06=chr(27)+'PC06;0200,0390,1,1,1,00,01'+chr(10)+chr(0)
        pc07=chr(27)+'PC07;0200,0480,1,2,1,00,01'+chr(10)+chr(0)
        pc08=chr(27)+'PC08;0200,0530,1,1,1,00,01'+chr(10)+chr(0)
        pc09=chr(27)+'PC09;0200,0560,1,1,1,00,01'+chr(10)+chr(0)
        pc10=chr(27)+'PC10;0200,0590,1,1,1,00,01'+chr(10)+chr(0)
        pc11=chr(27)+'PC11;0200,0620,1,1,1,00,01'+chr(10)+chr(0)
        rc00=chr(27)+'RC00;PASE/SALIDA'+chr(10)+chr(0)
        rc01=chr(27)+'RC01;'+razonPase+chr(10)+chr(0)
        #rc02=chr(27)+'RC02;R.F.C. OPL130730RB1'+chr(10)+chr(0)
        rc03=chr(27)+'RC03;'+domiPase+chr(10)+chr(0)
        rc04=chr(27)+'RC04;'+coloPase+chr(10)+chr(0)
        rc05=chr(27)+'RC05;Este pase vence en '+fechaPase+chr(10)+chr(0)
        rc06=chr(27)+'RC06;'+ciuaPase+chr(10)+chr(0)
        rc07=chr(27)+'RC07;COMPROBANTE DE PAGO POR: '+strcuotapesos+chr(10)+chr(0)
        rc08=chr(27)+'RC08;CAJERO No. '+boletero+chr(10)+chr(0)
        rc09=chr(27)+'RC09;BOLETO No. '+self.boletoPase+chr(10)+chr(0)
        rc10=chr(27)+'RC10;PASE No... '+boletoPase+chr(10)+chr(0)
        rc11=chr(27)+'RC11;FECHA PAGO.'+fechaPago+chr(10)+chr(0)
       
        f.write(limpiaMem)
        f.write(printArea)
        f.write(barcodeFormat)
        f.write(pc00)
        f.write(pc01)
        #f.write(pc02)
        f.write(pc03)
        f.write(pc04)
        f.write(pc05)
        f.write(pc06)
        f.write(pc07)
        f.write(pc08)
        f.write(pc09)
        f.write(pc10)
        f.write(pc11)
        f.write(rc00)
        f.write(rc01)
        #f.write(rc02)
        f.write(rc03)
        f.write(rc04)
        f.write(rc05)
        f.write(rc06)
        f.write(rc07)
        f.write(rc08)
        f.write(rc09)
        f.write(rc10)
        f.write(rc11)
        f.write(barcodeData)
        f.write(cortaHoja)
        f.write(imprimePag)
        f.close()
         
        print ('el fol es',foliopase)
        a=fecMinutes
        b=digito
        c=self.ATMnum
        connLocal = psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
        cursor=connLocal.cursor()
        cursor.execute("UPDATE atmcaracter SET foliopases=%s, digitopase=%s WHERE indice=%s",(a,b,c))
        connLocal.commit()
        connLocal.close()

        a=boletoPase
        b=self.boletoPase
        connLocal = psycopg2.connect(dbname="smart" , host=self.IP , port="5432",  user="pi", password="raspberry")
        cursor=connLocal.cursor()
        cursor.execute("UPDATE atmventas SET atmpase=%s WHERE atmnumbol=%s",(a,b))
        connLocal.commit()
        connLocal.close()
        QtTest.QTest.qWait(2000)
        self.timer3.start(7000)
        self.avisoVoz('pase.mp3')
        
     
   
       
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
