import vk_api

print("Hello!")
def send_nsg(vk, user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 1000)})
token = "f15a2281047461d9894772dc28b1789f364f83dd812889b042ddda46313dda839874fcebf109d20fe661a"
from vk_api.longpoll import VkLongPoll, VkEventType
vk = vk_api.VkApi (token=token)
longpoll = VkLongPoll(vk)
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
      if event.to_me:
            # Сообщение от пользователя
            request = event.text
            user = vk.method("users.get", {"user_ids": event.user_id, "fields": "photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online, domain, has_mobile, contacts, site, education, universities, schools, status, last_seen, followers_count, occupation, nickname, relatives, relation, personal, connections, exports, activities, interests, music, movies, tv, books, games, about, quotes, can_post, can_see_all_posts, can_see_audio, can_write_private_message, can_send_friend_request, is_favorite, is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo, is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group"})[0]
            print("Пришло сообщение от пользователя"+user["first_name"]+user["last_name"])
            send_nsg(vk, event.user_id, "Здравствуйте,"+user["first_name"]+user["last_name"])