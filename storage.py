import json
import os


class Storage:
    VALID_MACHINE_TYPES = ["滚筒洗衣机", "波轮洗衣机", "烘干机", "洗烘一体"]
    STATUS_NORMAL = "正常"
    STATUS_REPAIR = "维修中"

    def __init__(self):
        self.data_path = os.path.expanduser("~/.laundry_mgr.json")
        self._data = None

    def load(self):
        if self._data is None:
            if os.path.exists(self.data_path):
                with open(self.data_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            else:
                self._data = {
                    "machines": {},
                    "usage_records": [],
                    "repair_records": []
                }
        return self._data

    def save(self):
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, ensure_ascii=False, indent=2)

    def get_machine(self, machine_id):
        data = self.load()
        return data["machines"].get(machine_id)

    def add_machine(self, machine_id, machine_type, price_per_use):
        data = self.load()
        if machine_id in data["machines"]:
            raise ValueError(f"设备 {machine_id} 已存在")
        if machine_type not in self.VALID_MACHINE_TYPES:
            raise ValueError(f"无效的设备类型: {machine_type}，必须是: {', '.join(self.VALID_MACHINE_TYPES)}")
        data["machines"][machine_id] = {
            "id": machine_id,
            "type": machine_type,
            "price_per_use": price_per_use,
            "status": self.STATUS_NORMAL,
            "total_uses": 0,
            "total_revenue": 0,
            "fault_count": 0
        }
        self.save()

    def add_usage_record(self, machine_id, date, user_phone, revenue):
        data = self.load()
        data["usage_records"].append({
            "machine_id": machine_id,
            "date": date,
            "user_phone": user_phone,
            "revenue": revenue
        })
        machine = data["machines"][machine_id]
        machine["total_uses"] += 1
        machine["total_revenue"] += revenue
        self.save()

    def add_repair_record(self, machine_id, date, issue, cost):
        data = self.load()
        data["repair_records"].append({
            "machine_id": machine_id,
            "start_date": date,
            "end_date": None,
            "issue": issue,
            "cost": cost
        })
        data["machines"][machine_id]["status"] = self.STATUS_REPAIR
        data["machines"][machine_id]["fault_count"] += 1
        self.save()

    def complete_repair(self, machine_id, date):
        data = self.load()
        for record in reversed(data["repair_records"]):
            if record["machine_id"] == machine_id and record["end_date"] is None:
                record["end_date"] = date
                break
        data["machines"][machine_id]["status"] = self.STATUS_NORMAL
        self.save()

    def get_all_machines(self):
        data = self.load()
        return list(data["machines"].values())

    def get_usage_records_by_month(self, month):
        data = self.load()
        return [r for r in data["usage_records"] if r["date"].startswith(month)]
