import PIL
import PIL.Image
import io
import aiohttp

async def texToPng(latex):
    payload = {
        'format': 'png',
        'code': latex,
        'density': 220,
        'quality': 100
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post('http://rtex.probablyaweb.site/api/v2', json=payload, timeout=8) as req:
                req.raise_for_status()
                jdata = await req.json()
                if jdata['status'] == 'error':
                    raise RenderingError
                filename = jdata['filename']
            async with session.get('http://rtex.probablyaweb.site/api/v2' + '/' + filename, timeout=3) as imgReq:
                imgReq.raise_for_status()
                imgData = io.BytesIO(await imgReq.read())
                image = PIL.Image.open(imgData).convert('RGBA')
        except aiohttp.client_exceptions.ClientResponseError:
            raise RenderingError
        imageByteArr = io.BytesIO()
        image.save(imageByteArr, format='PNG')
        imageByteArr = imageByteArr.getvalue()
        return imageByteArr

class RenderingError:
    pass