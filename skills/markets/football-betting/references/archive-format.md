# 足彩 V0.3 逐票档案

本目录用于保存**不可覆盖的逐票决策档案**。生产实现应采用 append-only 或内容寻址方式；赛后结果只能追加，不能回写覆盖原始预测。

建议每张票至少保存：

```json
{
  "ticket_id": "unique-id",
  "rule_version": "V0.3",
  "code_commit": "git-sha",
  "experiment_id": "exp-id",
  "mode": "COVER",
  "T_ticket": "ISO-8601 with timezone",
  "candidate_pool_snapshot": "snapshot-id-or-content-hash",
  "selected_matches": ["m1", "m2", "m3", "m4", "m5", "m6", "m7"],
  "p_forecast": {
    "m1": {"H": 0.50, "D": 0.30, "A": 0.20}
  },
  "execution_odds": {
    "m1": {"H": 2.00, "D": 3.20, "A": 4.50}
  },
  "paths": [
    {
      "outcomes": ["H", "H", "D", "A", "H", "D", "H"],
      "probability": 0.0123,
      "execution_odds": 63.4
    }
  ],
  "coverage": 0.087,
  "return_constraint": null,
  "search_status": "EXACT",
  "final_results": null,
  "settlement": null
}
```

## 冻结规则

1. `T_ticket`、候选池、概率、赔率、8条路径、覆盖率和约束配置在出票时冻结。
2. `final_results` 与 `settlement` 只能通过新增版本/追加记录写入。
3. 不允许为了赛后复盘改写原概率、原赔率、原候选池或原8注。
4. 若缺少能证明当时可用的历史快照，该样本标记为不可用于无泄漏回测。
