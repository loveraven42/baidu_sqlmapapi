# baidu_sqlmapapi
- 作用：
  - 提供一个关键字，然后用百度搜索进行查找sqlmap注入
- 用途: 刷教育行业src的应该比较不错
***
```
usage: crawl.py [-h] [-w WORD] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -w WORD, --word WORD  the single word that you want to crawl
  -f FILE, --file FILE  get the word from the file
```

***
- **install**
  - pip install BeautifulSoup gevent
***

- 先开启sqlmapapi  命令: sqlmapapi -s
- 注意事项 word关键字如果有空格的话需要加上引号 example: -w "site:edu.cn inurl:?id="

***
**ps: 对文件处理的多线程还没有测试过(测试过有问题的话请提issue，谢谢)**
