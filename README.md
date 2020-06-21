# スケジュール管理
## schedule
```shell script
pip install schedule
```
### 使い方

```python
import schedule
import time

def job():
    print("some job...")

# 10分ごとの実行
schedule.every(10).minutes.do(job)
# 一時間ごとの実行
schedule.every().hour.do(job)
# 毎日10:30分の実行
schedule.every().day.at("10:30").do(job)
# 毎週一回実行
schedule.every().monday.do(job)
# 水曜日13:15実行
schedule.every().wednesday.at("13:15").do(job)

while True:
   schedule.run_pending()  
   time.sleep(1)
```

## celery

### インストール

使用する場合Brokerを作る必要がある、基本選択肢は二つ
- redis
- RabbitMQ

```shell script
pip install celery
pip install celery[redis]
```

### 使い方

```python
from celery import Celery
from celery.schedules import crontab

app = Celery("tasks", broker_url="redis://127.0.0.1:6379/5")
app.conf.beat_schedule = {
       "greet": {
                 "task": "tasks.greet",
                 "schedule": crontab(minute="*/1"),
                 "args": ["何か"]
                }

}

@app.task
def greet(word):
    print("hello", word)
```

### 実行

```python
celery -A tasks beat # 監視 tasks[ファイル名] 
celery -A tasks worker -loglevel=info #タスク起動
```
