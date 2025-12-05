#!/bin/bash

# URL سرور API
API_URL="http://localhost:8000/api/v1/tasks/auto-close-overdue"

# فایل Log
LOG_FILE="/Users/reyhanehhashemi/Documents/university/Term 7/todolist-python-oop-api/logs/autoclose_api.log"

# زمان شروع
START_TIME=$(date '+%Y-%m-%d %H:%M:%S')

# صدا زدن API
echo "[$START_TIME] Starting auto-close via API..." >> "$LOG_FILE"

RESPONSE=$(curl -s -X POST "$API_URL" -w "\nHTTP_CODE:%{http_code}")

HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE" | cut -d: -f2)

# زمان پایان
END_TIME=$(date '+%Y-%m-%d %H:%M:%S')

if [ "$HTTP_CODE" = "200" ]; then
    echo "[$END_TIME] ✅ Success: Auto-close completed" >> "$LOG_FILE"
    echo "$RESPONSE" | grep -v "HTTP_CODE" >> "$LOG_FILE"
else
    echo "[$END_TIME] ❌ Error: HTTP $HTTP_CODE" >> "$LOG_FILE"
    echo "$RESPONSE" >> "$LOG_FILE"
fi

echo "----------------------------------------" >> "$LOG_FILE"
