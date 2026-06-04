from storage import Storage


class LaundryManager:
    def __init__(self):
        self.storage = Storage()

    def add_machine(self, machine_id, machine_type, price_per_use):
        if price_per_use <= 0:
            raise ValueError("每次费用必须是正整数")
        self.storage.add_machine(machine_id, machine_type, price_per_use)
        return f"设备 {machine_id} 添加成功"

    def use_machine(self, machine_id, date, user_phone):
        machine = self.storage.get_machine(machine_id)
        if machine is None:
            raise ValueError(f"设备 {machine_id} 不存在")
        if machine["status"] != Storage.STATUS_NORMAL:
            raise ValueError(f"设备 {machine_id} 当前状态为 {machine['status']}，无法使用")
        revenue = machine["price_per_use"]
        self.storage.add_usage_record(machine_id, date, user_phone, revenue)
        return f"设备 {machine_id} 使用记录已添加，收入 {revenue} 分"

    def repair_machine(self, machine_id, date, issue, cost):
        machine = self.storage.get_machine(machine_id)
        if machine is None:
            raise ValueError(f"设备 {machine_id} 不存在")
        if machine["status"] == Storage.STATUS_REPAIR:
            raise ValueError(f"设备 {machine_id} 已经在维修中")
        if cost <= 0:
            raise ValueError("维修费用必须是正整数")
        self.storage.add_repair_record(machine_id, date, issue, cost)
        return f"设备 {machine_id} 已报修，状态改为维修中"

    def fixed_machine(self, machine_id, date):
        machine = self.storage.get_machine(machine_id)
        if machine is None:
            raise ValueError(f"设备 {machine_id} 不存在")
        if machine["status"] != Storage.STATUS_REPAIR:
            raise ValueError(f"设备 {machine_id} 当前不在维修状态")
        self.storage.complete_repair(machine_id, date)
        return f"设备 {machine_id} 维修完成，状态恢复正常"

    def monthly_report(self, month):
        records = self.storage.get_usage_records_by_month(month)
        machines = self.storage.get_all_machines()
        
        report = {}
        for m in machines:
            report[m["id"]] = {
                "type": m["type"],
                "uses": 0,
                "revenue": 0
            }
        
        for r in records:
            mid = r["machine_id"]
            if mid in report:
                report[mid]["uses"] += 1
                report[mid]["revenue"] += r["revenue"]
        
        return report

    def fault_rate_report(self):
        machines = self.storage.get_all_machines()
        report = {}
        for m in machines:
            total_uses = m["total_uses"]
            fault_count = m["fault_count"]
            if total_uses > 0:
                rate = fault_count / total_uses
            else:
                rate = 0.0
            report[m["id"]] = {
                "type": m["type"],
                "fault_count": fault_count,
                "total_uses": total_uses,
                "fault_rate": rate
            }
        return report
