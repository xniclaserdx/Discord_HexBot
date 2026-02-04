"""Module for converting LaTeX to PNG images."""
import PIL.Image
import PIL.ImageOps
import io
import aiohttp
import numpy as np


async def texToPng(latex: str) -> PIL.Image.Image:
    """
    Convert LaTeX code to PNG image.
    
    Args:
        latex: LaTeX document string
        
    Returns:
        PIL Image object with inverted colors
        
    Raises:
        RenderingError: If rendering fails
    """
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
                    error_detail = jdata.get('error', jdata.get('message', 'Unknown error'))
                    raise RenderingError(f"LaTeX rendering failed: {error_detail}")
                filename = jdata['filename']
            
            async with session.get('http://rtex.probablyaweb.site/api/v2' + '/' + filename, timeout=3) as img_req:
                img_req.raise_for_status()
                img_data = io.BytesIO(await img_req.read())
                image = PIL.Image.open(img_data).convert('RGBA')
        except aiohttp.client_exceptions.ClientResponseError as e:
            raise RenderingError(f"HTTP error: {e.status}")
        except aiohttp.client_exceptions.ClientError as e:
            raise RenderingError(f"Connection error: {str(e)}")
    
    # Crop image
    image = image.crop(bbox(image))
    
    # Invert colors
    r, g, b, a = image.split()
    rgb_image = PIL.Image.merge('RGB', (r, g, b))
    inverted_image = PIL.ImageOps.invert(rgb_image)
    r2, g2, b2 = inverted_image.split()
    final_transparent_image = PIL.Image.merge('RGBA', (r2, g2, b2, a))
    
    return final_transparent_image

    
def bbox(im: PIL.Image.Image) -> tuple:
    """
    Calculate bounding box for non-white pixels in image.
    
    Args:
        im: PIL Image object
        
    Returns:
        Tuple (x0, y0, x1, y1) of bounding box coordinates
    """
    a = np.array(im)[:, :, :3]  # keep RGB only
    m = np.any(a != [255, 255, 255], axis=2)
    coords = np.argwhere(m)
    y0, x0, y1, x1 = *np.min(coords, axis=0), *np.max(coords, axis=0)
    return (x0, y0, x1 + 1, y1 + 1)


class RenderingError(Exception):
    """Raised when LaTeX rendering fails."""
    pass