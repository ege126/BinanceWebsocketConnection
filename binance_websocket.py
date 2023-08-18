import websocket
import json
import time
import threading

class BinanceWebSocket:

    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval

        self.ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@kline_{self.interval}"
        self.ws = websocket.WebSocketApp(self.ws_url, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
        self.ws.on_open = self.on_open

        self.latest_price_info = None
        self.is_force_stopped = False

    def on_message(self, ws, message):
        data = json.loads(message)
        kline = data['k'] 
        close = kline['c']
        self.latest_price_info = close  # Directly update the latest price
        print("From WEBSOCKET - Latest current price updated: ", self.latest_price_info)


    def on_error(self, ws, error):
        print(f"Error: {error}") 

    def on_close(self, ws, close_status_code, close_msg):
        print("WebSocket connection closed")
        if not self.is_force_stopped:
            self.reconnect()
        else:
            print("WebSocket was force-stopped by user.")
        self.is_force_stopped = False

    def force_stop(self):
        self.is_force_stopped = True
        self.ws.close()  # Close the WebSocket connection will call on_close

    def on_open(self, ws):
        print("WebSocket connection opened")
        subscription_payload = {
            "method": "SUBSCRIBE",
            "params": [
                f"{self.symbol}@kline_{self.interval}"
            ],
            "id": 1
        }
        self.ws.send(json.dumps(subscription_payload))

    #Binance disconnects websocket connections every 24h, therefore reconnecting when disconnected
    def reconnect(self):
        while True:
            try:
                print("Reconnecting...")
                time.sleep(5)  # Delay before reconnecting
                self.ws = websocket.WebSocketApp(self.ws_url, on_message=self.on_message, on_error=self.on_error, on_close=self.on_close)
                self.ws.on_open = self.on_open
                self.ws.run_forever()
            except Exception as e:
                print(f"Reconnection failed: {e}")

# EXAMPLE USAGE:
def run_websocket_instance(ws):
    binance_ws.ws.run_forever()

if __name__ == "__main__":

    symbol = "btcusdt"
    interval = "1m"

    binance_ws = BinanceWebSocket(symbol, interval)
    websocket_thread = threading.Thread(target=run_websocket_instance, args=(binance_ws, ))
    websocket_thread.start()   

    
    last_price_from_ws = binance_ws.latest_price_info

    # DO SOMETHING WITH THE PRICE INFO

    
    time.sleep(5)
      
    # STOP THE WEBSOCKET AND JOIN THE THREAD
    binance_ws.force_stop()
    websocket_thread.join()
    
    print("Main thread finished")
