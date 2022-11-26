import PIL
import PIL.Image
import io
import aiohttp
import numpy as np

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
        image = image.crop(bbox(image))

        # Farben invertieren
        r,g,b,a = image.split()
        rgb_image = PIL.Image.merge('RGB', (r,g,b))
        inverted_image = PIL.ImageOps.invert(rgb_image)
        r2,g2,b2 = inverted_image.split()
        final_transparent_image = PIL.Image.merge('RGBA', (r2,g2,b2,a))

        return final_transparent_image
    
    # Bild zuschneiden
def bbox(im):
    a = np.array(im)[:,:,:3]  # keep RGB only
    m = np.any(a != [255, 255, 255], axis=2)
    coords = np.argwhere(m)
    y0, x0, y1, x1 = *np.min(coords, axis=0), *np.max(coords, axis=0)
    # return (x0, y0, x1+1, y1+1)
    return (x0, y0, x1+1, y1+1)


class RenderingError(Exception):
    pass