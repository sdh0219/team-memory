# 操作日志（只追加，最新在上）

## 2026-10-25 21:40 · Codex

- 做了：微信支付回调验签打通，notify_url 能正确落库
- 改动：pay/wechat/PayCallbackController.java、pay/PayCallbackTest.java
- 遗留：退款流程未动；验签密钥走环境变量 WECHAT_PAY_KEY，别写死

## 2026-10-24 15:12 · ZCode

- 做了：订单列表分页优化，P95 1.8s → 300ms
- 改动：api/OrdersController.java、db/migrations/V6__orders_index.sql（新增 idx_orders_user_created）
- 遗留：无

## 2026-10-23 10:05 · Claude Code

- 做了：Spring Boot 3.4 升级 + 依赖冲突清理
- 改动：pom.xml、17 个受影响的类
- 遗留：javax→jakarta 还有 2 处注释引用旧包名，不影响运行

## 2026-10-21 09:30 · Claude Code

- 做了：修复金额浮点计算事故，全部金额字段改为分（int）存储
- 改动：db/migrations/V7__amount_to_cents.sql、pay/Amount.java
- 遗留：无
