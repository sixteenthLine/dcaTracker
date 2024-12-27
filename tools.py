import time

class Tools:
    @staticmethod
    def getAmout(message):
        msg = message.split(" ")[0]
        if "M" in msg:
            return 1000
        return int(msg[1:-1].split(".")[0])
    
    @staticmethod
    def getDirection(message):
        return "selling" in message
        
    @staticmethod   
    def getPercentages(message):
        percentages = float(message.split("%")[0].split(" ")[-1])
        return percentages
    
    @staticmethod
    def isCanceledPossible(message):
        if "which is" in message :
            if int(message.split(" which is ")[1].split("%")[0]) >= 50:
                return False
        return True

    @staticmethod
    def idGoodTime(message):
        if "hour" in message.split("%")[0]:
            hours = int(message.split(" hour")[0].split(" ")[1])
            return hours < 2
        else:
            return True

    @staticmethod 
    def has_mexc(message):
        return "MEXC" in message

    @staticmethod
    def isValidMessage(message):
        try :   
            return Tools.has_mexc(message) and Tools.getPercentages(message) >= 5 and Tools.idGoodTime(message) and Tools.isCanceledPossible(message) and Tools.getAmout(message) > 300
        except:
            return False

    
    @staticmethod
    def getSymbol(message):
        return message.split(" ")[2]

    @staticmethod
    def createOrder(message):
        return {"symbol": Tools.getSymbol(message),
                "type": "market",
                "side": Tools.getDirection(message),
                "amount": 40
                }
    