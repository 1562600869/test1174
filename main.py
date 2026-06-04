import argparse
import sys
from manager import LaundryManager
from storage import Storage


def main():
    parser = argparse.ArgumentParser(description="自助洗衣店管理系统")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    add_parser = subparsers.add_parser("add-machine", help="添加设备")
    add_parser.add_argument("machine_id", help="设备ID")
    add_parser.add_argument("--type", required=True, dest="machine_type",
                           choices=Storage.VALID_MACHINE_TYPES,
                           help=f"设备类型: {', '.join(Storage.VALID_MACHINE_TYPES)}")
    add_parser.add_argument("--price-per-use", type=int, required=True, help="每次费用（整数分）")

    use_parser = subparsers.add_parser("use", help="记录使用")
    use_parser.add_argument("machine_id", help="设备ID")
    use_parser.add_argument("--date", required=True, help="使用日期 YYYY-MM-DD")
    use_parser.add_argument("--user-phone", required=True, help="用户手机号")

    repair_parser = subparsers.add_parser("repair", help="报修设备")
    repair_parser.add_argument("machine_id", help="设备ID")
    repair_parser.add_argument("--date", required=True, help="报修日期 YYYY-MM-DD")
    repair_parser.add_argument("--issue", required=True, help="故障描述")
    repair_parser.add_argument("--cost", type=int, required=True, help="维修费用（整数分）")

    fixed_parser = subparsers.add_parser("fixed", help="维修完成")
    fixed_parser.add_argument("machine_id", help="设备ID")
    fixed_parser.add_argument("--date", required=True, help="完成日期 YYYY-MM-DD")

    monthly_parser = subparsers.add_parser("monthly", help="月度统计")
    monthly_parser.add_argument("--month", required=True, help="月份 YYYY-MM")

    subparsers.add_parser("fault-rate", help="故障率统计")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = LaundryManager()

    try:
        if args.command == "add-machine":
            result = manager.add_machine(args.machine_id, args.machine_type, args.price_per_use)
            print(result)

        elif args.command == "use":
            result = manager.use_machine(args.machine_id, args.date, args.user_phone)
            print(result)

        elif args.command == "repair":
            result = manager.repair_machine(args.machine_id, args.date, args.issue, args.cost)
            print(result)

        elif args.command == "fixed":
            result = manager.fixed_machine(args.machine_id, args.date)
            print(result)

        elif args.command == "monthly":
            report = manager.monthly_report(args.month)
            print(f"\n{args.month} 月度统计报表")
            print("-" * 60)
            total_uses = 0
            total_revenue = 0
            for mid, data in report.items():
                print(f"设备 {mid} ({data['type']}):")
                print(f"  使用次数: {data['uses']} 次")
                print(f"  总收入: {data['revenue']} 分 ({data['revenue']/100:.2f} 元)")
                total_uses += data["uses"]
                total_revenue += data["revenue"]
            print("-" * 60)
            print(f"总计: 使用 {total_uses} 次, 收入 {total_revenue} 分 ({total_revenue/100:.2f} 元)")

        elif args.command == "fault-rate":
            report = manager.fault_rate_report()
            print("\n设备故障率统计报表")
            print("-" * 70)
            for mid, data in report.items():
                print(f"设备 {mid} ({data['type']}):")
                print(f"  故障次数: {data['fault_count']} 次")
                print(f"  总使用次数: {data['total_uses']} 次")
                if data["fault_rate"] is None:
                    print(f"  故障率: 暂无使用记录")
                else:
                    print(f"  故障率: {data['fault_rate']:.2%}")
            print("-" * 70)

    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
