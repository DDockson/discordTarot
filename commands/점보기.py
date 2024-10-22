import discord
from discord.ext import commands
from discord import app_commands
import random
import google.generativeai as genai
import json

tarot = {
    0: {"name": "바보", "ordinary": ":black_joker:", "reverse": "<:joker_r:1297916023160307813>"},
    1: {"name": "마술사", "ordinary": ":magic_wand:", "reverse": "<:magician_r:1297915986372198440>"},
    2: {"name": "여사제", "ordinary": ":person_with_veil:", "reverse": "<:priestness_r:1297915965501214771>"},
    3: {"name": "여황제", "ordinary": ":princess:", "reverse": "<:empress_r:1297916047684407336>"},
    4: {"name": "황제", "ordinary": ":prince:", "reverse": "<:emperor_r:1297916056999821344>"},
    5: {"name": "교황", "ordinary": ":crown:", "reverse": "<:hierophant_r:1297916030781362197>"},
    6: {"name": "연인", "ordinary": ":couple_with_heart_woman_man:", "reverse": "<:lovers_r:1297915995465191465>"},
    7: {"name": "전차", "ordinary": ":suspension_railway:", "reverse": "<:chariot_r:1297916084912914505>"},
    8: {"name": "힘", "ordinary": ":lion:", "reverse": "<:strength_r:1297915946685693972>"},
    9: {"name": "은둔자", "ordinary": ":man_mage:", "reverse": "<:hermit_r:1297916039371296848>"},
    10: {"name": "운명의 수레바퀴", "ordinary": ":compass:", "reverse": "<:wheel_r:1297915907053588501>"},
    11: {"name": "정의", "ordinary": ":scales:", "reverse": "<:justice_r:1297916003946205244>"},
    12: {"name": "매달린 남자", "ordinary": ":upside_down:", "reverse": ":slight_smile:"},
    13: {"name": "죽음", "ordinary": ":skull:", "reverse": "<:death_r:1297916076553932820>"},
    14: {"name": "절제", "ordinary": ":woman_fairy:", "reverse": "<:temperance_r:1297915926913749025>"},
    15: {"name": "악마", "ordinary": ":japanese_ogre:", "reverse": "<:devil_r:1297916068702195752>"},
    16: {"name": "탑", "ordinary": ":tokyo_tower:", "reverse": "<:tower_r:1297915917568577556>"},
    17: {"name": "별", "ordinary": ":sparkles:", "reverse": "<:star_r:1297915956693041172>"},
    18: {"name": "달", "ordinary": ":first_quarter_moon_with_face:", "reverse": "<:moon_r:1297915977815560255>"},
    19: {"name": "태양", "ordinary": ":sun_with_face:", "reverse": "<:sun_r:1297915937311166474>"},
    20: {"name": "심판", "ordinary": ":judge:", "reverse": "<:judgement_r:1297916014150811659>"},
    21: {"name": "세계", "ordinary": ":earth_asia:", "reverse": "<:world_r:1297915889752084582>"}
}

luck = {
    "올해 회고": "",
    "미래 전망": "",
    "연애운": "",
    "직업운": "",
    "인간관계": "",
    "가져야 할 마음가짐": ""
}

luck_list = ["올해 회고", "미래 전망", "연애운", "직업운", "인간관계", "가져야 할 마음가짐"]

with open("token.json", 'r', encoding='utf-8') as f:
    config = json.load(f)
genai.configure(api_key=config['api'])

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  },
]

generation_config = {
  "temperature": 0.9,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  safety_settings=safety_settings,
  system_instruction="너는 타로 점을 보는 사람이야. 메이저 아르카나를 기준으로 타로 점을 보고, 내가 너한테 '보고자 하는 운세'와 '내가 뽑은 카드'를 보내주면 해당 카드의 설명을 간단히 해주고, 그에 대한 운세를 마크다운 없이, 조언 느낌으로, 짧고 존댓말로 보내줘",
)

convo = model.start_chat(history=[])

class 점보기(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="점보기", description="점을 봅니다")
    async def 점보기(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        options = [discord.SelectOption(label=str(i), value=str(i)) for i in range(0, 22)]
        
        select = discord.ui.Select(
            placeholder="카드를 선택하세요",
            min_values=6,
            max_values=6,
            options=options
        )

        async def select_callback(interaction: discord.Interaction):
            await interaction.response.defer()  # 응답 지연

            await interaction.edit_original_response(content="🔮 점을 보는 중입니다. 잠시만 기다려주세요...", view=None)

            if interaction.user.id != user_id:
                await interaction.followup.send("이 선택은 명령어를 실행한 사람만 사용할 수 있습니다.", ephemeral=True)
                return

            select_list = list(map(int, select.values))
            reverse_list = [1 if random.random() > 0.5 else 0 for _ in range(6)]
            random_list = [i for i in range(22)]
            random.shuffle(random_list)
            tarot_list = []
            for i in range(6):
                card = tarot[random_list[select_list[i]]]
                if reverse_list[i] == 1:
                    tarot_list.append((card["name"] + "(역)", card["reverse"]))
                else:
                    tarot_list.append((card["name"], card["ordinary"]))

                response = convo.send_message(f"{luck_list[i]}, {tarot_list[i][0]}")
                luck[luck_list[i]] = response.text.strip()

            current_page = 0

            def create_embed(page):
                embed = discord.Embed(title=f"{interaction.user.name}님의 타로", color=0x00b0f4)
                name, emoji = tarot_list[page]
                embed.add_field(name="뽑은 카드", value=f"{emoji} {name}", inline=False)
                embed.add_field(name=f"{luck_list[page]}", value=f"{luck[luck_list[page]]}", inline=False)
                embed.set_footer(text=f"{page + 1}/6 페이지")
                return embed

            async def update_embed(interaction, page):
                embed = create_embed(page)
                left_button.disabled = page == 0
                right_button.disabled = page == 5
                await interaction.response.edit_message(embed=embed, view=view)

            class PageButton(discord.ui.Button):
                def __init__(self, label, direction):
                    super().__init__(label=label, style=discord.ButtonStyle.primary)
                    self.direction = direction

                async def callback(self, interaction: discord.Interaction):
                    nonlocal current_page
                    if self.direction == "left":
                        current_page = max(current_page - 1, 0)
                    else:
                        current_page = min(current_page + 1, 5)
                    await update_embed(interaction, current_page)

            left_button = PageButton("◀️", "left")
            right_button = PageButton("▶️", "right")

            view = discord.ui.View()
            view.add_item(left_button)
            view.add_item(right_button)

            left_button.disabled = True

            await interaction.followup.send(embed=create_embed(current_page), view=view)

        select.callback = select_callback

        view = discord.ui.View()
        view.add_item(select)

        await interaction.response.send_message("0에서 21까지 원하시는 숫자 6개를 골라주세요.", view=view)

async def setup(bot):
    await bot.add_cog(점보기(bot))