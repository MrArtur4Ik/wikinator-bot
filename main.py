
###########################################
#Простой wiki бот для вк от MrArthur4Ik :)#
###########################################

import requests
import wikipedia
import vk_api
import traceback
import random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from wikipedia.exceptions import PageError
wikipedia.set_lang("RU")

def get_corona_info():
    response = requests.get("https://api.thevirustracker.com/free-api?global=stats")
    return response.json()
def get_corona_info_in_russia(str):
	response = requests.get("https://api.thevirustracker.com/free-api?countryTotal=" + str)
	return response.json()

class RichVkBotLongPoll(VkBotLongPoll):
    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as e:
                print('error', e)

vk_session = vk_api.VkApi(token="dc5eeba2f760e2e677e6dd2fe15a72f961af622dd27c558b783c589aa0911d5434be5e5d92b2af1202161");
search_requests = {}
groupid = '171098026'
longpoll = RichVkBotLongPoll(vk_session, groupid);
vk = vk_session.get_api();
def msg(label):
	if event.from_user:
		vk.messages.send(
			random_id=random.randint(1, 2147483647),
			peer_id=event.obj.from_id,
			message=label,
			v='5.45'
		)
	if event.from_chat:
		vk.messages.send(
			random_id=random.randint(1, 2147483647),
			chat_id=event.chat_id,
			message=label,
			v='5.45'
		)
def msg_with_photo(label, att):
	if event.from_user:
		vk.messages.send(
			random_id=random.randint(1, 2147483647),
			peer_id=event.obj.from_id,
			message=label,
			attachment=att,
			v='5.45'
		)
	if event.from_chat:
		vk.messages.send(
			random_id=random.randint(1, 2147483647),
			chat_id=event.chat_id,
			message=label,
			attachment=att,
			v='5.45'
		)
for event in longpoll.listen():
	try:
		if event.type == VkBotEventType.MESSAGE_NEW:
			with_verify = False
			screen_name = vk.groups.getById(
				group_id=groupid,
				v='5.45'
			)[0]['screen_name'];
			msg_text = event.object.text
			user_id = event.obj.from_id
			args = msg_text.split(" ")
			if args[0].startswith("[club" + str(event.group_id)):
				args = args[1:]
				with_verify = True
			if len(args) == 0:
				if event.from_chat:
					msg("Меня кто-то звал?")
				else:
					msg("&#128543; Такой команды нет!")
				continue
			if args[0].lower() == "помощь" or args[0].lower() == "начать":
				msg("Мои команды:\n"
					""
					"&#128240; Статья <название> - открыть статью по его названию.\n"
					"&#127760; Вики/Найти <текст> - найти статьи и получить их список.\n"
					"&#128194; Открыть <число> - открыть статью из полученого списка.\n"
					"🦠 Коронавирус - данные о коронавирусе.")
			elif args[0].lower() == "статья":
				if len(args) < 2:
					msg("&#10071; Недостаточно аргументов в команде!")
				else:
					msg("&#128270; Уже ищу...")
					result_str = ""
					request = args[1:]
					for s in request:
						result_str = result_str + s + " "
					try:
						result = wikipedia.summary(result_str)
						msg("&#128240; Результат: \n" + result)
					except PageError:
						msg("&#10071; В Википедии нет статьи с таким названием")
					except Exception:
						msg("&#10071; Произошла ошибка!")
			elif args[0].lower() == "найти" or args[0].lower() == "вики":
				if len(args) < 2:
					msg("&#10071; Недостаточно аргументов в команде!")
				else:
					msg("&#128270; Уже ищу...")
					result_str = ""
					request = args[1:]
					for s in request:
						result_str = result_str + s + " "
					try:
						result = wikipedia.search(result_str)
						if len(result) == 0:
							msg("&#128542; Ничего не найдено.")
						else:
							result_search = ""
							for i in range(len(result)):
								s = result[i]
								result_search = result_search + "&#128206; " + str(i + 1) + ": " + s + "\n"
							search_requests[user_id] = result
							msg("&#128240; Результат: \n" + result_search + "&#128240; Напишите \"Открыть <число>\" чтобы открыть соответствующую статью из списка.")
					except Exception:
						msg("&#10071; Произошла ошибка!")
						print(traceback.format_exc())
			elif args[0].lower() == "открыть":
				if user_id in search_requests:
					if len(args) < 2:
						msg("&#10071; Недостаточно аргументов в команде!")
					else:
						try:
							page = int(args[1])
							msg("&#128270; Уже ищу...")
							if (page - 1) >= 0 and (page - 1) < len(search_requests[user_id]):
								result = wikipedia.summary(search_requests[user_id][page - 1])
								msg("&#128240; Результат: \n" + result)
							else:
								msg("&#10071; По этому номеру нет статьи.")
						except ValueError:
							msg("&#10071; Введите целое число!")
						except Exception:
							msg("&#10071; Произошла ошибка!")
				else:
					msg("&#10071; Для начала найдите статьи чтобы получить список.")
			elif args[0].lower() == "коронавирус":
				try:
					viruses = get_corona_info()["results"][0]["total_cases"]
					viruses_in_ru = get_corona_info_in_russia("RU")["countrydata"][0]["total_cases"]
					msg("&#129298; Всего больных: " + str(viruses) + "\n"
						"&#129319; Всего больных в России: " + str(viruses_in_ru)
					)
				except Exception:
					msg("&#10071; Произошла ошибка!")
			else:
				if with_verify or event.from_user:
					msg("&#128543; Такой команды нет!")
	except Exception:
		print(traceback.format_exc())