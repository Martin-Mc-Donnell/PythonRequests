import requests

res = requests.get('https://martin-mc-donnell.github.io/chasing-down-game.html')
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))
print(len(res.text))
print(res.text[:250])
