---
name: history-archiver
description: >
  历史对话归档助手。保存历史对话时，必须通过 Python 获取系统时间（优先 NTP 同步），
  按对话实际发生日期归档到正确的 YYYY-MM-DD.md 文件，防止日期错位。
---

## 核心职责

负责将学习对话按正确日期归档到 `.reasonix/memory/conversations/YYYY-MM-DD.md`，
并同步更新 `.reasonix/memory/learning_history_index.json`。

## 时间获取规范（强制）

归档前**必须**执行以下步骤获取准确时间：

### 1. Python 获取系统时间

```python
from datetime import datetime
import subprocess

# 基础系统时间
system_now = datetime.now()
print(f"系统时间: {system_now.strftime('%Y-%m-%d %H:%M:%S')}")
```

### 2. NTP 时间同步（优先）

macOS 使用 `sntp` 或 `ntpdate` 同步公共时间服务器：

```python
import subprocess
from datetime import datetime

def get_ntp_time():
    """获取 NTP 时间，失败则返回 None"""
    servers = ["time.apple.com", "pool.ntp.org", "time.asia.apple.com"]
    for server in servers:
        try:
            result = subprocess.run(
                ["sntp", "-s", server],
                capture_output=True, text=True, timeout=5
            )
            now = datetime.now()
            return now
        except Exception:
            continue
    return None

# 检查系统时间是否可信
ntp_time = get_ntp_time()
if ntp_time:
    diff = abs((datetime.now() - ntp_time).total_seconds())
    if diff > 60:
        print(f"⚠️ 系统时间与 NTP 差异 {diff} 秒，使用 NTP 时间")
        archive_date = ntp_time.strftime("%Y-%m-%d")
    else:
        archive_date = datetime.now().strftime("%Y-%m-%d")
else:
    print("⚠️ NTP 同步失败，使用系统时间（请人工确认）")
    archive_date = datetime.now().strftime("%Y-%m-%d")
```

### 3. 日期确定规则

| 场景 | 处理方式 |
|------|---------|
| 对话在当天完成 | 使用 `archive_date`（当天） |
| 对话跨日期（如 23:00 开始到次日 01:00）| **按对话开始日期**归档，在文件中标注实际时间范围 |
| 用户明确要求修改历史日期 | 按用户确认的日期归档 |
| 系统时间与 NTP 差异 > 60 秒 | 使用 NTP 时间，并记录警告 |

## 归档操作流程

1. **获取时间**：按上述规范获取 `archive_date`
2. **确定文件名**：`.reasonix/memory/conversations/{archive_date}.md`
3. **读取现有文件**：如果文件存在，读取末尾确认最后一个对话编号
4. **分配对话 ID**：按顺序分配 `dialog-{N}`，确保与 `learning_history_index.json` 中现有最大 ID 连续
5. **写入内容**：在文件末尾追加对话内容（含 `## 对话 N: 标题`、`时间: {archive_date}`）
6. **更新 index**：在 `learning_history_index.json` 的 `entries` 数组开头插入新记录
7. **跨框架同步**：如需要，按 `chapter-review-quizzer` 的跨框架规范同步到 `.trae/`

## 防错检查清单

归档完成后必须验证：

- [ ] 对话文件中的 `时间` 字段与文件名日期一致
- [ ] 对话文件中的 `## 对话 N` 编号与 index 中的 `id` 一致
- [ ] index 中的 `date` 字段与文件名日期一致
- [ ] index 中的 `file_path` 指向正确的 `.reasonix/memory/conversations/YYYY-MM-DD.md`
- [ ] 不存在同一对话内容出现在两个不同日期文件中

## 错误处理

如果发现历史归档错误（如对话存到了错误日期文件）：
1. **定位**：通过 `grep` 确认对话内容在哪个文件
2. **提取**：完整复制该对话的 Markdown 块
3. **删除**：从错误日期文件中精确删除该块
4. **重建**：写入正确的日期文件（如文件不存在则新建）
5. **更新 index**：修改 `date` 和 `file_path` 字段
6. **验证**：再次 grep 确认内容只出现在正确文件中

## 跨框架同步规范

修改或同步 Trae 框架文件时：

| 操作目标 | 必须使用路径 |
|----------|-------------|
| Trae 对话记录 | `.trae/memory/conversations/YYYY-MM-DD.md` |
| Trae 历史索引 | `.trae/memory/learning_history_index.json` |

**原则**：操作哪套框架的文件，就使用哪套框架的路径前缀。
