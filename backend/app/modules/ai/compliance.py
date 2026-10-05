"""HR合规引擎：内置劳动法/社保/个税规则，校验AI输出"""

# 内置合规规则库
COMPLIANCE_RULES = {
    "overtime": {
        "name": "加班时长合规",
        "rule": "每月加班不得超过36小时，每日不超过3小时",
        "check": lambda hours_per_month: hours_per_month <= 36,
        "risk": "high" if True else "low",
    },
    "annual_leave": {
        "name": "年假天数",
        "rule": "工作满1年享5天年假，满10年10天，满20年15天",
        "min_days": 5,
    },
    "probation": {
        "name": "试用期期限",
        "rule": "合同3个月以上不满1年：试用期不超1个月；1-3年：不超2个月；3年以上：不超6个月",
        "max_months": 6,
    },
    "social_insurance": {
        "name": "社保公积金缴纳",
        "rule": "入职30日内必须缴纳社保，公积金比例5%-12%",
    },
    "termination": {
        "name": "解除劳动合同",
        "rule": "经济性裁员需提前30天通知工会或全体职工，N+1补偿",
    },
    "maternity": {
        "name": "产假天数",
        "rule": "基础产假98天，难产+15天，多胞胎每多一胎+15天",
        "min_days": 98,
    },
}


def check_compliance(category: str, data: dict) -> dict:
    """合规检查入口"""
    rule = COMPLIANCE_RULES.get(category)
    if not rule:
        return {"pass": True, "message": "无对应规则"}

    result = {"category": category, "rule_name": rule["name"], "rule": rule["rule"], "warnings": []}

    if category == "overtime" and "hours" in data:
        if data["hours"] > 36:
            result["warnings"].append(f"月加班{data['hours']}小时，超过法定36小时上限")
            result["pass"] = False
        else:
            result["pass"] = True

    elif category == "probation" and "months" in data:
        if data["months"] > 6:
            result["warnings"].append("试用期超过法定6个月上限")
            result["pass"] = False
        else:
            result["pass"] = True

    elif category == "annual_leave" and "days" in data:
        if data["days"] < 5:
            result["warnings"].append("年假少于法定5天")
            result["pass"] = False
        else:
            result["pass"] = True

    else:
        result["pass"] = True

    return result


def get_rules() -> list:
    """返回所有规则列表"""
    return [{"key": k, "name": v["name"], "rule": v["rule"]} for k, v in COMPLIANCE_RULES.items()]
