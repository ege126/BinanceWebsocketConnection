# Binance WebSocket Connection with Auto-Reconnection

This repository provides a Python script that showcases how to establish a WebSocket connection to Binance's streaming API with automatic reconnection handling. The reconnection mechanism ensures seamless data streaming even if the WebSocket connection is closed, which is crucial given Binance's practice of closing connections approximately every 24 hours.

## Features

- Establish a persistent WebSocket connection to Binance's streaming API.
- Handle automatic reconnection when the WebSocket connection is closed due to Binance's disconnection policy.
- Utilize threading to manage the WebSocket connection concurrently with other tasks.

## Prerequisites

- Python 3.x
- Required libraries: `websocket-client`



 
