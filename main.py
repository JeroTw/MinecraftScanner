import os
from mcstatus import JavaServer
import socket
import random
from threading import Thread
from discord_webhook import DiscordWebhook

url = "discord webhook url"


def get_random_ip() -> str:
  return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))


def scan(ip):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.settimeout(0.5)
  try:
    s.connect((ip, 25565))
    s.shutdown(socket.SHUT_RDWR)
  except:
    return False
  finally:
    s.close()
  server = JavaServer.lookup(f"{ip}:25565")
  query = server.status()
  players = []
  for player in query.players.sample:
    players.append('#' + player.name)
  text = f'<@&1087386487559032932> | IP: {ip}:25565 | {query.players.online}/{query.players.max} players | Nicknames: {players} | MOTD: {query.description} | Version: {query.version.name} | Ping: {query.latency}'
  print(text)
  webhook = DiscordWebhook(url=url, content=text)
  response = webhook.execute()
  print(query.players.online,
        players,
        query.players.max,
        query.description,
        query.version.name,
        query.latency,
        sep=" | ")
  return True


def thread():
  while 1:
    ip = get_random_ip()
    try:
      if scan(ip):
        print(f"{ip} is online")
    except Exception as error:
      print(error)
      continue


if __name__ == "__main__":
  for i in range(800):
    Thread(target=thread).start()

while 1:
  pass
