'''
参考了 Kyomotoi佬的AnimeThesaurus（GitHub： https://github.com/Kyomotoi/AnimeThesaurus）
所有有关的词库，想了想还是放内存里比较好
考虑到有设置别名的问题，用[NICK]代表别名（xxx），[NICKS]代表某人的（xxx的），发送时会自动替换。
'''


words = {
    "fail":[
        "雾子...还要再亲近一点才行哦×",
        "果咩...雾子还不是很信任你呢...",
        "不...不行的哦（推开）",
        "打咩唷...！！（后退）"
        ],
    "over":[
        "太多次啦！！就算是雾子也是会烦的哦（口亨"
        ],
    "pet_over":[
        "[NICK]摸摸太多次了啦...！",
        "等..等会再来吧（逃）",
        "头发...头发乱掉了啦×",
        "再摸摸 雾子可就不理你了！！（口亨）",
        "不可以一直摸哦...雾子...会变奇怪的//v//"
        ],
    "pet":[
        "[NICKS]手掌...好温暖♡",
        "以后也可以这样摸摸雾子吗~？",
        "[NICK]...心里总有种暖暖的感觉呢...♡",
        "嗯嗯..有种...莫名安心的感觉呢...♡",
        "雾子...蹭蹭~",
        "嗯...唔...头发要乱了啦！！",
        "好舒服...雾子快长不高啦~",
        "好哦~就一下下...好了！！（逃",
        "欸，现在么..也不是不可以啦(小小声)"
        ],
    "tete_over":[
        "贴贴太久了啦...！",
        "等..等会再来吧（逃）",
        "贴贴太紧了...有点难为情呢×"
        ],
    "tete":[
        "只...只能贴一下哦！",
        "贴贴贴贴[NICK]...♡",
        "[NICK]...爱你哦~♡",
        "心里总有种暖暖的感觉呢...[NICK]♡"
        ],
    "hug":[
        "好哦~抱抱[NICK]",
        "只...只能抱一会哦~♡",
        "抱抱...[NICK]就像个孩子一样呢...",
        "真是拿你没办法呢...就一小会儿哦~",
        "抱抱[NICK]...有感觉舒服一些吗？",
        "嗯嗯，抱抱哦~",
        "抱抱[NICK]...不...不要蹭了啦/////",
        "抱抱[NICK]...好孩子，好孩子...",
        "抱抱...有[NICK]独特的味道呢~"
    ],
    "lift":[
        "笨...笨蛋！！快放雾子下来！！",
        "诶...诶！！！！！",
        "不...要掉下来了啦！！",
        "不...不要在空中挠痒痒！！"
    ],
    "rua":[
        "请...请温柔的揉揉哦~",
        "好哦~不要揉奇怪的地方啦！！",
        "再揉揉 雾子就戳你肚子哦！！",
        "揉揉...好舒服...♡",
        "揉吧揉吧...但是只能这一次哦?"
    ],
    "nip":[
        "别捏啦别捏啦！！",
        "唔...雾子的脸被捏了...",
        "疼...疼疼疼...快放手了啦！！"
    ],
    "rub":[
        "嗯~嗯~♡",
        "[NICKS]蹭蹭~舒服呢~",
        "噗哈哈哈~[NICK]！！好痒的...!!",
        "好孩子~好孩子~让雾子治愈你吧~",
        "[NICK]真是粘人呢~（摸头）",
        "雾子的身上...温暖吗~？"
    ],
    "kiss":[
        "啾啾[NICK]...爱你哦♡",
        "亲亲[NICK]...总感觉有点害羞呢~♡",
        "亲亲[NICK]...雾子好像有点奇怪了...♡",
        "muamua~!!",
        "唔...诶诶诶！！！",
        "只......只许这一次哦///v///",
        "[NICK]...下次...也可以这样亲亲雾子吗...♡",
        "！啾~~！",
        "诶，现在么..也不是不可以啦...(小小声)",
        "唔...嗯...？舌头...伸进来了..."
        ],
    "dirty":[
        "雾子...被骂了",
        "[NICK]...讨厌鬼",
        "雾子不会再理你了...！！",
        "呜呜...被骂了..."
        ],
    "sex_fail":[
        "笨...笨蛋！！！！！才不行呢！",
        "这种事情...怎么想都很奇怪吧...×",
        "不...不行的哦（推开）",
        "雾子...才不要呢！！",
        "抱歉...今天不行哦...",
        "笨~蛋~...（小声",
        "诶...让雾子考虑一下可以吗...",
        "嗯...嗯？雾...雾子要报警了哦？"
    ],
    "sex_over":[
        "...（没有回应）",
        "雾子酱...想休息呢...",
        "不...不行呢..."
    ],
    "sex":[
        "[NICK]...爱你♡",
        "...总感觉有点害羞呢...[NICK]，爱你♡",
        "...雾子...变得奇怪了...[NICK]♡",
        "那...那个...请♡",
        "请...轻一点哦...[NICK]♡"
    ],
    "wife_fail": [
        "雾...雾子才不是你老婆呢！！",
        "那个...美少女都是你老婆吗？",
        "再调戏雾子，雾子可就不理你了哦？",
        "打咩唷...雾子才不是你老婆呢"
    ],
    "wife":[
        "好呢~[NICK]suki唷~",
        "被这样叫还有点...害羞呢//V//",
        "[NICK]达令~，以后也可以这样叫雾子吗？"
    ],
    "like":[
        "雾子也·喜·欢·你·哦·~",
        "[NICK]...雾子也喜欢你哦~",
        "好啦好啦~雾子知道啦~爱你哦♡",
        "能被[NICK]这样说，雾子很高兴呢~",
        "其实雾子也...没、没什么///A///"
    ],
    "kabedon": [
        "诶...欸欸欸？？///w///",
        "请...请不要这样啦..",
        "诶——雾子...会害羞的啦...",
        "太...太近了啦",
        "讨...讨厌！！",
        "脸...脸好近——（心跳声）",
        "[NICK]...这是要干什么呢...（小声）"
    ],
    "prpr": [
        "雾子...要...要融化了啦!!",
        "唔...舌头...",
        "好啦好啦！！快停下来！",
        "好痒...噗哈哈哈...快停下！！"
    ],
    "cute": [
        "诶嘿嘿~[NICK]你也很可爱哦~",
        "能被这样夸雾子很高兴哦~",
        "嗯...嗯嗯！！雾子是最可爱的！！",
        "诶...诶！！（脸红）",
        "那个...你不会在骗雾子吧//v//"
    ],
    "cute_over": [
        "诶嘿嘿~[NICK]你也很可爱哦~",
        "能被这样夸雾子很高兴哦~",
        "嗯...嗯嗯！！雾子是最可爱的！！",
        "诶...诶！！（脸红）",
        "那个...你不会在骗雾子吧//v//"
    ],
    "eat": [
        "诶？请...请温柔一点对雾子哦...",
        "不...不可以这样！",
        "雾子才不能吃呢！！（敲头）",
        "雾子的味道...好吃吗？",
        "快...快停下...好疼...",
        "请...请品尝雾子吧♡"
    ],
}