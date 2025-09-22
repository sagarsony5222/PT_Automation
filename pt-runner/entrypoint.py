import os, json, time
pt_json = os.environ.get("PT_RUN_JSON", "{}")
print("PT Runner started with JSON:", pt_json)
# simulate work
for i in range(5):
    print(f"Working... {i+1}/5")
    time.sleep(1)
print("PT Runner finished.")
