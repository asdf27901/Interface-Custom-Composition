## 自动参数组合请求小工具
#### （仅适用于百茶台）

1. yaml文件需要存放在./yaml/目录下
     
   接口yaml文件取名为interface.yaml


2. interface.yaml文件中配置如下
```yaml
# 文件开头需要配置下列
- env:
    wx_app_host: &wx_host xxx   # 小程序环境域名 
    backend_host: &backend_host xxxxx   # 后台环境域名
    wx_code: xxxxxxx    # 小程序code
    username: xxxx  # 后台有权限的管理员的用户名
    password: xxxx  # 后台有权限的管理员的密码
    username_no_permissions: xxx    # 后台无权限的管理员的用户名
    password_no_permissions: xxxx   # 后台无权限的管理员的密码
    
# 以下用于方便修改配置文件
# https://xxxxx  测试环境小程序域名
# https://xxxx  测试环境后台域名
# https://api-pre.xxxx.com  预发布环境小程序域名
# https://api-back-pre.xxxxx.com  预发布环境后台域名
```
3. interface文件配置如下
### &nbsp;&nbsp;&nbsp;&nbsp;interface.yaml注意事项
+ 1. <font color="#dd0000">x-token和token只能存在一个，如果都存在只会处理x-token</font>
```python
        try:
            if self.headers['x-token'] is None:
                ···
        except KeyError:
            ···
```
+ 2. <font color="#dd0000">错误数据前必须要加英文格式的分号":"，否则会当作正确参数</font>
```python
       for lis in value:
           after_split_data = str(lis).split('、')
           # 错误项中一定包含符号':',使用列表推导式找到所有包含':'的字符串
           error_data = [x for x in after_split_data if x.__contains__(':')]
           # 正确项中一定不包含符号':',使用列表推导式找到所有不包含':'的字符串
           correct_data = [x for x in after_split_data if not x.__contains__(':')]
```
+ 3. <font color="#dd0000">Content-Type为multipart/form-data时，不要写到Content-Type中，否则会报错</font>

+ 请求为只有query参数，无请求体（后台接口）
```yaml
- host: *backend_host
  interface_address: /auctionsample/bargainList
  interface_name: 采购议价样品列表
  method: post
  headers:
    Content-Type: application/json;charset=UTF-8
    Connection: keep-alive
    x-token: # x-token无需传值
  params:
    pageSize: 5、10、空值:null、错误:0
    pageCurrent: 1、空值:null、错误:0
```
+ 请求有query参数，json请求体（小程序接口）
```yaml
- host: *wx_host
  interface_address: /auctionsample/bargainList
  interface_name: 采购议价样品列表
  method: post
  headers:
    Content-Type: application/json;charset=UTF-8  # 如果使用json传值，application/json必须填入
    Connection: keep-alive
  params:
    pageSize: 5、10、空值:null、错误:0
    pageCurrent: 1、空值:null、错误:0
  json:
    data:
      token: # token无需传值
      test: xxxx
      test-list:
         - 10,20,30、40,50,60、错误:0,0,0、负数:-1,-2,-3  # 数组类型的参数需要将所有正确错误写在一行
```
+ 请求有query参数，json请求体（后台接口）
```yaml
- host: *backend_host
  interface_address: /auctionsample/bargainList
  interface_name: 采购议价样品列表
  method: post
  headers:
    Content-Type: application/json;charset=UTF-8 # 如果使用json传值，application/json必须填入
    Connection: keep-alive
    x-token: # x-token无需传值
  params:
    pageSize: 5、10、空值:null、错误:0
    pageCurrent: 1、空值:null、错误:0
  json:
   test: xxxx
   test-list:
      - 10,20,30、40,50,60、错误:0,0,0、负数:-1,-2,-3  # 数组类型的参数需要将所有正确错误写在一行
```
+ 请求有query参数，key-value（application/x-www-form-urlencoded）请求体（小程序接口）
```yaml
- host: *wx_host
  interface_address: /auctionsample/bargainList
  interface_name: 采购议价样品列表
  method: post
  headers:
    Content-Type: application/x-www-form-urlencoded;charset=UTF-8  # 如果使用application/x-www-form-urlencoded传值，必须填入
    Connection: keep-alive
  params:
    pageSize: 5、10、空值:null、错误:0
    pageCurrent: 1、空值:null、错误:0
  data:
    token: # token无需传值
    test: 123
```
+ 请求有query参数，key-value（application/x-www-form-urlencoded）请求体（后台接口）
```yaml
- host: *backend_host
  interface_address: /auctionsample/bargainList
  interface_name: 采购议价样品列表
  method: post
  headers:
    Content-Type: application/x-www-form-urlencoded;charset=UTF-8  # 如果使用application/x-www-form-urlencoded传值，必须填入
    Connection: keep-alive
    x-token: # x-token无需传值
  params:
    pageSize: 5、10、空值:null、错误:0
    pageCurrent: 1、空值:null、错误:0
  data:
    test: 123
```
+ 请求有query参数，key-value（multipart/form-data）请求体，不带文件（小程序接口）
```yaml
- host: *wx_host
  interface_address: /auctionsample/bargainList
  interface_name: 采购议价样品列表
  method: post
  headers:
    Content-Type: charset=UTF-8  # 如果使用multipart/form-data传值，绝对不能填入！！
    Connection: keep-alive
  params:
    pageSize: 5、10、空值:null、错误:0
    pageCurrent: 1、空值:null、错误:0
  data:
    token: # token无需传值
    test: 123
```
+ 请求有query参数，key-value（multipart/form-data）请求体，带文件（小程序接口）
```yaml
- host: *wx_host
  interface_address: /auctionsample/bargainList
  interface_name: 采购议价样品列表
  method: post
  headers:
    Content-Type: charset=UTF-8  # 如果使用multipart/form-data传值，绝对不能填入！！
    Connection: keep-alive
  params:
    pageSize: 5、10、空值:null、错误:0
    pageCurrent: 1、空值:null、错误:0
  data:
    token: # token无需传值
    test: 123
  files:
    file1: /Users/xxx/Desktop/xxx-报销单.xls # 传入文件路径 file1指参数名
    file2: /Users/xxx/Desktop/xxx-报销单.xls # 传入文件路径 file2指参数名
```
+ 请求有query参数，key-value（multipart/form-data）请求体，不带文件（后台接口）
```yaml
- host: *backend_host
  interface_address: /auctionsample/bargainList
  interface_name: 采购议价样品列表
  method: post
  headers:
    Content-Type: charset=UTF-8  # 如果使用multipart/form-data传值，绝对不能填入！！
    Connection: keep-alive
    x-token: # x-token无需传值
  params:
    pageSize: 5、10、空值:null、错误:0
    pageCurrent: 1、空值:null、错误:0
  data:
    test: 123
```
+ 请求有query参数，key-value（multipart/form-data）请求体，带文件（后台接口）
```yaml
- host: *backend_host
  interface_address: /auctionsample/bargainList
  interface_name: 采购议价样品列表
  method: post
  headers:
    Content-Type: charset=UTF-8  # 如果使用multipart/form-data传值，绝对不能填入！！
    Connection: keep-alive
    x-token: # x-token无需传值
  params:
    pageSize: 5、10、空值:null、错误:0
    pageCurrent: 1、空值:null、错误:0
  data:
    test: 123
  files:
    file1: /Users/xxx/Desktop/xxx-报销单.xls # 传入文件路径 file1指参数名
    file2: /Users/xxx/Desktop/xxx-报销单.xls # 传入文件路径 file2指参数名
```
+ 请求有query参数，请求体，需要下载文件（后台接口）
```yaml
- host: *backend_host
  interface_address: /sample/export
  interface_name: 样品导出
  method: post
  headers:
    Content-Type: application/json;charset=UTF-8
    Connection: keep-alive
    x-token: # x-token无需传值
  json:
    businessNo: BU0000000308
  download: # 需要增加download字段
    file_name: 样品导出文件.xlsx  # 下载完成后的文件名
```

+ 对于一些必填参数和可选参数，可以通过optional参数去去除
  + optional存在一些弊端 
     - 错误参数不会和可选参数绑定，仍然是和所有正确参数发送，例如下方只是将id替换为错误值
```yaml
- host: *backend_host
  interface_address: /exitStockOrder/artificialDeliver
  interface_name: 人工发货
  method: post
  headers:
    Content-Type: charset=UTF-8  # 如果使用multipart/form-data传值，绝对不能填入！！
    Connection: keep-alive
    x-token: # x-token无需传值
  data:
    id: 1、错误:0
    logisticsCompany: 顺丰速递
    expressNumber: SF12323213123
    remark: test
    batchFlag: 0
  files:
    file: /Users/xxx/Desktop/xxx-报销单.xls # 传入文件路径 file指参数名
  optional:
     - remark,files # 其中一个请求去除掉remark和files参数
     - batchFlag=1|id,logisticsCompany,expressNumber,remark # 当batchFlag=1时，id、logisticsCompany、expressNumber、remark去掉不传
     - batchFlag=0|files # 当batchFlag=0时，去掉files不传
```