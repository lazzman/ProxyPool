## 介绍
自动爬取多个代理网站代理IP，自动校验并存入Redis数据库中，使用flask框架提供Web接口获取可用代理IP。

---

## 环境

- python3.6
- Miniconda或者Anaconda
- Redis

---

## 安装

使用conda命令创建运行环境，将自动创建一个名为python36的环境

```
conda env create -f conda-env.yml
```

---

## 配置

进入proxypool目录，修改setting.py文件

---

## 运行

使用conda命令切换运行环境

```
activate python36
```

开启API监听与代理池

```
python run.py
```

启动后默认监听127.0.0.1:5000，提供了两个获取代理的地址

```
# 获取1个代理
http://127.0.0.1:5000/getProxy

# 获取n个代理
http://127.0.0.1:5000/getMoreProxy/n
```

---

## 模块介绍

- crawl.py 爬虫模块
  - class proxy.crawl.ProxyCrawl 爬虫类，用于爬取代理网站上的代理，可按照已有方法名添加新的爬取规则
- schedule.py 调度器模块
  - class proxypool.schedule.ValidityChecker 代理校验类，可以对给定的代理的可用性进行异步检测。 
  - class proxypool.schedule.PoolAdder 代理添加器，用来触发爬虫模块，对代理池内的代理进行补充，代理池代理数达到阈值时停止工作。 
  - class proxypool.schedule.Schedule 代理池启动类，运行RUN函数时，会创建两个进程，负责对代理池内容的增加和更新。 
- db.py Redis数据库连接模块 
  - class proxypool.db.RedisClient 数据库操作类，与Redis建立连接和对Redis数据库的增删改查
- error.py 异常模块
  - class proxypool.error.ResourceDepletionError 资源枯竭异常，如果从所有抓取网站都抓不到可用的代理资源，则抛出此异常。
  - class proxypool.error.PoolEmptyError 代理池空异常，如果代理池长时间为空，则抛出此异常。
- api.py API模块，启动一个Web服务器，使用Flask实现，对外提供代理的获取功能。
- utils.py 工具模块
- setting.py 元数据配置模块
- test.py 测试爬虫函数模块
---

## 项目参考 

https://github.com/WiseDoge/ProxyPool 