# CAU-Annual-Eat

## 前置条件

- HTTPS 抓包工具
- 登录农大 e 卡小程序

## 使用说明

- 开始抓包并打开 e 卡小程序，找到 `GET https://vcard.cau.edu.cn/wechatApp...` 请求，复制请求信息中的 `openid`
- 修改 `eCard.py` 中的 `OPENID`
- 运行 `eCard.py` 获取消费记录
- 运行 `draw.py` 生成消费记录图表

## 注意事项

- <font color=red>**请勿将`OPENID`发送给任何人**</font>
- 本项目仅供学习交流，请勿用于其他用途
- 本项目不保证长期有效，如需使用请自行测试

#### 小提示

其实有办法可以不抓包获取 `OPENID`，但有较高风险。如有兴趣，欢迎自行尝试。
