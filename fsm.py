from transitions.extensions import GraphMachine

from utils import send_text_message, send_image_message

picture = 0

image_data = [
    "https://imgur.com/dEc6lTp.png",#週邊地圖
    "https://imgur.com/4EF7Qih.png" #園區地圖
]

service_answer = [
    "輸入'Z'可以重新使用本服務\n輸入'E'可以本離開服務",
    "請您遵守下列事項:\n全園禁菸(2009年7月11日起，違者最高可罰一萬)\n禁止寵物及充氣氣球進入園區\n禁止腳踏車、幼兒三輪車、滑板及直排輪進入園區\n禁止跨越欄杆進入動物展示場\n禁止進入作業區及遊客列車車道\n禁止餵食動物\n各室內展示館禁止飲食\n不得任意餵食、危害動物權益及妨礙動物保育\n不得任意進行影響其他遊客參觀權益及遊園品質之行為\n\n提醒您留意事項:\n臺北市立動物園是一處結合自然景觀的環境，同時為許多野生動物和昆蟲的活動棲息地。建議穿著長袖、長褲等透氣衣物喔！\n建議來園時穿著輕便行走的休閒鞋，如要預防日曬與蚊蟲叮咬，請自行攜帶防曬及防蚊用品\n新光特展館（大貓熊館）、無尾熊館、兩棲爬蟲動物館及保育廊道禁止使用閃光燈\n園區內緊急電話設置地點共13處:\n1.臺灣動物區(近臺灣黑熊)\n2.昆蟲館服務台外牆面\n3.蟲蟲探索谷(谷內廁所旁)\n4.熱帶雨林區(孟加拉虎與亞洲象間)\n5.沙澳動物區(近駱駝販賣站)\n6.非洲動物區(近長頸鹿)\n7.非洲動物區(河馬與非洲象間)\n8.非洲動物區(近黑臀羚羊)\n9.兩棲爬蟲動物館服務臺\n10.兩棲爬蟲動物館內參觀動線中段\n11.鳥園區(近鶴園)\n12.企鵝館內\n13.溫帶動物區廁所(近小貓熊)\n\n輸入'P'可以看到園區地圖\n",
    "本園沒有展示兔子，也請勿攜帶兔子以及其他寵物進園\n\n",
    "大象是一種體型巨大、有著扇子一般的耳朵、鼻子很長、腿粗得像柱子的生物，本園有非洲象與亞洲象，歡迎大家前往參觀\n 非洲象位於非洲動物區，亞洲象位於熱帶雨林區；沒有辦法一起看到，輸入'P'可以看到園區地圖\n\n",
    "不要投餵獅子，其餘動物也通通不行\n 本園也沒有白獅子，不用特別去數獅子的數目\n\n",
    "不要觸碰、不要過度靠近動物、不要擅自摘剪植栽，若看到有其他遊客做了以上行為，可柔聲提醒或請工作人員協助\n\n",
    "可以給12歲及以下的孩子購買任何動物周邊商品；13-17歲的孩子可以買多一點；18歲及以上的人群可以買更多\n 裡面有標示價格的商品都可以買，只要你有錢，買多少都不是問題\n\n",
    "為響應節能減碳愛地球，歡迎大家多多使用大眾運輸工具；輸入'P'可以顯示週邊地圖\n\n",
    "如果您遭遇任何您無法解決的事件，請立刻、盡一切可能前往遊客服務中心，親切的服務人員能協助您。或請撥打(02)2938-2300 #630\n 你可以看周遭來判斷你在哪裡，輸入'P'可以看到園區地圖\n\n"
]

greeting = [
    "親愛的遊客，歡迎使用臺北市立動物園應用服務。我們是一處結合自然保育、研究、教育與遊憩功能的社教機構。豐富、多樣化且融合自然景觀的動物探索場域。如需要本服務協助，請打'START'\n'HELP'或'e'則能幫助你在任何時候看到這則訊息",
    "感謝你使用本服務，請依據你所在位置選擇，你可以抬頭看看身邊有沒有什麼告示排或標誌，在動物園請輸入'Z'，在海洋館請輸入'M'",
    "很高興你正在臺北市立動物園，請問有什麼可以協助你的嗎？輸入\n\n1:遊園須知\n2:兔子\n3:大象\n4:獅子\n5:植栽\n6:禮品區\n7:交通資訊\n8:其他"
]

wrong_msg = [
    "我們沒有海洋館，沒有水母小夜燈也不能過夜；如果你已經看見海洋館，請檢查你的定位，應該不是臺北市立動物園\n雖然沒有海洋館，但熱帶雨林館內的水族展示區有魟魚、象魚及其他魚類，輸入'P'可以看到園區地圖\n\n輸入'HELP'可以重新取得本服務\n輸入'z'代表你在動物園"
]


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    #entering function
    def check_place(self, event):
        text = event.message.text
        return text.rstrip().lower() == 'start'

    def check_zoo(self, event):
        text = event.message.text
        return text.rstrip().lower() == "z"

    def check_marine(self, event):
        text = event.message.text
        return text.rstrip().lower() == "m"

    def go_rule1(self, event):
        text = event.message.text
        return text.rstrip() == "1"

    def go_rule2(self, event):
        text = event.message.text
        return text.rstrip() == "2"

    def go_rule3(self, event):
        text = event.message.text
        return text.rstrip() == "3"

    def go_rule4(self, event):
        text = event.message.text
        return text.rstrip() == "4"

    def go_rule5(self, event):
        text = event.message.text
        return text.rstrip() == "5"

    def go_rule6(self, event):
        text = event.message.text
        return text.rstrip() == "6"

    def go_rule7(self, event):
        text = event.message.text
        return text.rstrip() == "7"

    def go_rule8(self, event):
        text = event.message.text
        return text.rstrip() == "8"

    def back_start(self, event):
        text = event.message.text
        return (text.rstrip().lower() == "e") or (text.rstrip().lower() == 'help')

    def go_picture(self, event):
        text = event.message.text
        return text.rstrip().lower() == "p"

    #on enter function
    def on_enter_welcome(self, event):
        print("Entering greeting\n")
        reply_token = event.reply_token
        send_text_message(reply_token, greeting[0])

    def on_enter_place(self, event):
        print("Entering place\n")
        reply_token = event.reply_token
        send_text_message(reply_token, greeting[1])

    def on_enter_zoo(self, event):
        print("Entering zoo\n")
        reply_token = event.reply_token
        send_text_message(reply_token, greeting[2])

    def on_enter_marine(self, event):
        print("Entering marine\n")
        global picture
        picture = 1
        reply_token = event.reply_token
        send_text_message(reply_token, wrong_msg[0])
        self.on_enter_place()

    def on_enter_rule1(self, event):
        print("Entering rule1\n")
        global picture
        picture = 1
        reply_token = event.reply_token
        send_text_message(reply_token, service_answer[1]+service_answer[0])

    def on_enter_rule2(self, event):
        print("Entering rule2\n")
        reply_token = event.reply_token
        send_text_message(reply_token, service_answer[2]+service_answer[0])

    def on_enter_rule3(self, event):
        print("Entering marine\n")
        global picture
        picture = 1
        reply_token = event.reply_token
        send_text_message(reply_token, service_answer[3]+service_answer[0])

    def on_enter_rule4(self, event):
        print("Entering marine\n")
        reply_token = event.reply_token
        send_text_message(reply_token, service_answer[4]+service_answer[0])

    def on_enter_rule5(self, event):
        print("Entering marine\n")
        reply_token = event.reply_token
        send_text_message(reply_token, service_answer[5]+service_answer[0])

    def on_enter_rule6(self, event):
        print("Entering marine\n")
        reply_token = event.reply_token
        send_text_message(reply_token, service_answer[6]+service_answer[0])

    def on_enter_rule7(self, event):
        print("Entering marine\n")
        global picture
        picture = 0
        reply_token = event.reply_token
        send_text_message(reply_token, service_answer[7]+service_answer[0])

    def on_enter_rule8(self, event):
        print("Entering marine\n")
        global picture
        picture = 1
        reply_token = event.reply_token
        send_text_message(reply_token, service_answer[8]+service_answer[0])

    def on_enter_picture(self, event):
        print("Entering picture\n")
        reply_token = event.reply_token
        send_image_message( reply_token, image_data[picture])