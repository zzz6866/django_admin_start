import telegram

chii_token = '763953984:AAHZYhC_K5g8c11skZglFdohl6j9JX2t6Hs'
chii = telegram.Bot(token=chii_token)
updates = chii.getUpdates()
for u in updates:
    print(u.message)
