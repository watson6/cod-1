项目: Cod

维护: peizhenfei

邮箱: peizhenfei@cvte.com

> ### 项目简介
基于告警消息收敛为事件，以其为核心进行多维度的策略管制的告警平台。

## 环境变量设置

```
# cat .envrc
export RUN_ENV=DEVELOP
export SECRET_KEY=j2704w39k^p*7*1$*9v-g@c7%!0sd-gege-jideyaoxiugaioooo
export REDIS_HOST=localhost
export REDIS_PWD=pwd
export REDIS_PORT=6379
export redirect=http://cod.localhost/
export WX_WORK_CORP_ID=wx1deaa200000000xxxxx
export WX_WORK_CORP_SECRET=rdHbushizhendetokenE7_1agR5S8rEiDemsg-Nc0000000000000s7xRCVyYfY

```

## 初始化开发环境
根目录下面有一个Makefile文件，具体详情可以看里面写了什么。初始化环境需要执行如下命令：
> make clean  &&  make make