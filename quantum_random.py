import qrng
import psutil
import random
from PIL import Image, ImageColor, ImageFilter

my_token = "insert_your_ibmq_token"

qrng.set_provider_as_IBMQ(my_token)
qrng.set_backend('ibmq_santiago')
quantum_random = qrng.get_random_int32() # prawdziwie losowa liczba

quantum_random = 84215045
love_int = psutil.sensors_temperatures()["coretemp"][0].current # temperatura procesora
thoughts = (psutil.getloadavg()[0]/ psutil.cpu_count() * 100) # % obłożenia procesora

print(quantum_random)

im = mg = Image.new('RGB', [512,512], 0x000000) # create the Image of size 1 pixel

def get_pixel_color():
    r = (max(0,(random.randint(0,50)*quantum_random)%(100) + (love_int-40)*4))%160
    g = (max(0,(random.randint(0,50)*quantum_random)%(100) + 10))%160
    b = (max(0,(random.randint(0,50)*quantum_random)%(100) + (60-love_int)*4))%160
    if ((quantum_random*random.randint(0,10000)) % 100 <= thoughts):
        r = (r+100)%255
        g = (g+100)%255
        b = (b+100)%255
    return (int(r),int(g),int(b),255)

def get_median(i,j,k,l):
    r1, g1, b1 = im.getpixel((i, j))
    r2, g2, b2 = im.getpixel((k, l))
    return ((r1+r2)//2,(g1+g2)//2,(b1+b2)//2,255)

def draw_image():
    for i in range(128):
        for j in range(128):
            im.putpixel((4*i,4*j), get_pixel_color() ) # or whatever color you wish
    for i in range(127):
        for j in range(256):
            im.putpixel((4*i+2,2*j), get_median(4*i,2*j,4*i+4,2*j) ) # or whatever color you wish
    for i in range(256):
        for j in range(127):
            im.putpixel((2*i,4*j+2), get_median(2*i,4*j,2*i,4*j+4) ) # or whatever color you wish
    for i in range(255):
        for j in range(512):
            im.putpixel((2*i+1,j), get_median(2*i,j,2*i+2,j) ) # or whatever color you wish
    for i in range(512):
        for j in range(255):
            im.putpixel((i,2*j+1), get_median(i,2*j,i,2*j+2) ) # or whatever color you wish


im = im.filter(ImageFilter.BLUR)

draw_image()
im.save('simplePixel.png') # or any image format
