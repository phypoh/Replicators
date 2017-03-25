import cognitive_face as CF
from PIL import Image
import requests
from io import BytesIO
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

KEY = ''  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)

def photoshop(url):
    face_url = url #Backwords compatibility

    response = requests.get(face_url) #Used to download an image from the url
    face = Image.open(BytesIO(response.content)).convert("RGBA")

    response = requests.get('http://brokenmyth.net/wp-content/uploads/blackfeather_splash.jpg')
    im = Image.open(BytesIO(response.content)).convert("RGBA")
    result = CF.face.detect(face_url, attributes='headPose')

    if len(result) == 0: #If no head found
        w,h = im.size
        response = requests.get('http://vignette2.wikia.nocookie.net/parody/images/5/55/Po_kung_fu_panda_3.png/revision/latest?cb=20150824041523')
        face = Image.open(BytesIO(response.content)).convert("RGBA")
        im.paste(face, (w//2, 1), face)
        im.save('tmp.jpg')
        return(['tmp.jpg'])


    result = result[0]
    dim = result['faceRectangle']
    #w, h = im.size
    face = face.crop((dim['left'], dim['top'], dim['width']+dim['left'], dim['top']+dim['height'])).convert("RGBA") #CRops it so all you see is the face
    angle = result['faceAttributes']['headPose']['yaw']
    w,h = face.size
    ratio = h/w
    face = face.resize((75, int(75*ratio)), Image.ANTIALIAS)
    face = face.rotate(angle+17, resample=Image.BICUBIC, expand=True) #max quality & no crop

    bands = list(face.split()) #no idea wth this works but it changes the opacity
    opacity = 0.9
    if len(bands) == 4:
        # Assuming alpha is the last band
        bands[3] = bands[3].point(lambda x: x*opacity)

    face = Image.merge(face.mode, bands) #Applys the opacity change

    im.paste(face, (615, 100), face) #Pastes the image onto blackfeather's face
    im.save('tmp.jpg')
    return('tmp.jpg')

class FaceReplace():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.cooldown(1, 20, BucketType.user)
    async def bface(self,ctx, url=''):
        """
        Blackfeather is near.
        $bface <link to img>
        Become blackfeather.
        """
        if url == '':
            pic = ctx.message.attachments[0]['url']
        elif 'http' in url:
            pic = url
        else:
            await self.bot.say("Sorry, please provide an image or link.")
            return
        pic = photoshop(pic)
        if isinstance(pic,str):
            await self.bot.send_file(ctx.message.channel, fp = pic)
        else:
            await self.bot.send_file(ctx.message.channel, fp = pic[0], content='**Error 404:** Face Not Found :no_mouth:')

def setup(bot):
    bot.add_cog(FaceReplace(bot))
