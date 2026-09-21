---
name: lithium-window-scanner
version: 0.1.0
language: zh-CN
status: research-only
---

# 碳酸锂资产时间窗口扫描器 V0.1

## 目标

把《财经占书》已经冻结的 Source Layer 转成一个可审计的“时间事件账本 + 去重 + 候选窗口”执行层，并与碳酸锂现实市场信息分开保存。

本版本**不输出涨跌结论、不生成买卖信号、不使用隐式评分**。

## 核心原则

1. Source / Engineering / Validation 分离。
2. 同一底层几何只能计为一个独立证据：
   - 90° aspect
   - D45 alignment
   - H8 projection
   若来自同一对天体、同一时间、同一底层角距，则 `Independent_Evidence_Count = 1`。
3. 同一事件可有多个标签，但不能重复计数：
   - ECLIPSE
   - MARKET_EVENT
   - HISTORICAL_HIGH_LOW
4. `OPEN` 与 `SOURCE_UNSPECIFIED` 分开：
   - OPEN = 仍需 Source Audit；
   - SOURCE_UNSPECIFIED = 已审计，但原书没有给出数值/语义。
5. 所有数值窗口、orb、权重、评分、聚类阈值都属于 ENGINEERED；没有显式批准不得进入正式 Runtime。
6. Exact hit 是 timing anchor，不是唯一有效性 gate。
7. 2H / 8H 等宫位必须带 chart namespace，禁止跨个人盘/国家盘/市场盘重复解释。

## V0.1 输入

每个时间事件至少包含：

- event_id
- timestamp
- family
- rule_id
- source_status
- chart_context
- geometry_key
- underlying_event_id
- labels
- note

支持的 `source_status`：

- BOOK-EXACT
- BOOK-EXACT-EXAMPLE
- BOOK-INTERPRETED
- SOURCE_UNSPECIFIED
- ENGINEERED
- VALIDATION
- OPEN
- REJECTED-AS-SOURCE

## V0.1 输出

- 可执行事件（排除 OPEN / REJECTED-AS-SOURCE）
- SAME_GEOMETRY_DEDUP 后的独立证据
- Anchor 去重后的事件
- exact timestamp 共现事件
- 若提供并显式批准 `cluster_window_hours`，才允许做时间聚类
- Reality Layer 单独保存，不参与占星证据数量

## 碳酸锂 Reality Layer

建议字段：

- GFEX warehouse receipts / 注销与注册
- spot-futures basis
- upstream maintenance / restart
- domestic production
- cathode / battery production schedule
- ESS demand
- spodumene / lepidolite feedstock
- Chile shipments / imports / arrivals
- social inventory
- policy / environmental / mining disruptions

这些字段属于现实市场层，不得伪装成占星 Source evidence。

## 禁止

- 单一星象直接映射 BUY / SELL
- HitCount -> SignalStrength
- fixed 1° orb
- fixed ±N-day window
- 90° + D45 + H8 算三份独立证据
- 同一日食既作 Eclipse Anchor 又作 Historical Event Anchor 后计两次
- Personal 2H/8H 与 Market 2H/8H 混用
- 未批准的 `cluster_window_hours`

## V0.1 的定位

这是“可审计时间扫描器”，不是交易策略。下一阶段应接真实天文事件数据和碳酸锂历史行情，做 Validation Layer。
