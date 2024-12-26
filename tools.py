import time

class Tools:
    @staticmethod
    def getAmout(message):
        return int(message.split(" ")[0][1:-1].split(".")[0])
    
    @staticmethod
    def getDirection(message):
        return "selling" in message
        
    @staticmethod   
    def getPercentages(message):
        percentages = float(message.split("Potential price change: ")[1].split("%")[0])
        return percentages
    
    @staticmethod
    def isCanceledPossible(message):
        if "which is" in message :
            if int(message.split(" which is ")[1].split("%")[0]) >= 50:
                return False
        return True

    @staticmethod
    def idGoodTime(message):
        try:
            if "hour" in message:
                hours = int(message.split(" hours")[0].split(" ")[1])
                return hours < 2
            else:
                return True
        except (IndexError, ValueError):
            return False
    
    @staticmethod
    def isValidMessage(message):
        try:
            return Tools.getPercentages(message) >= 5 and Tools.idGoodTime(message) and Tools.isCanceledPossible(message) and Tools.getAmout(message) > 300
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
    
    @staticmethod
    def getCurrentPrice(client):
        start_time = time.time()
        while client.last is None or 'id' in client.last:
            if time.time() - start_time > 15:   
                return None
        return float(client.last['d']['deals'][0]['p'])
    
    @staticmethod
    def getExpectedPrice(client, message):
        if Tools.getDirection(message):
            return float((Tools.getCurrentPrice(client) - Tools.getCurrentPrice(client) * Tools.getPercentages(message)/100)*1600)
        else: 
            return float((Tools.getCurrentPrice(client) + Tools.getCurrentPrice(client) * Tools.getPercentages(message)/100)*1600)

    @staticmethod
    def getOpeningPrice(client):
        return float(client.first['d']['deals'][0]['p'])

    @staticmethod
    def getCurrentProfit(client, message):
        if(Tools.getDirection(message)):
            return float((Tools.getOpeningPrice(client)-Tools.getCurrentPrice(client))*1600)
        else:
            return float((Tools.getCurrentPrice(client)-Tools.getOpeningPrice(client))*1600)