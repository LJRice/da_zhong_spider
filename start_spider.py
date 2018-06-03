import time
import os
n=0
while n==0:
    # n=os.system('scrapy crawl CommentSpider')
    input_dir=""
    output_dir=""
    model=""
    n = os.system('python pix2pix.py --mode test --input_dir %s --output_dir %s --checkpoint %s' %(input_dir,out_dir,model))
    print("结束状态码为：",n)

    # time.sleep(180)    #每隔3分钟运行一次  60*3=180
