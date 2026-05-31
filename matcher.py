"""合作匹配器 - 发现潜在合作机会"""


class Collaborator:
    """合作者档案，记录个人技能、资源和目标以便匹配。"""

    def __init__(self, name: str, skills: list, resources: list,
                 goals: list, industry: str = ""):
        """初始化合作者档案。

        Args:
            name: 合作者姓名
            skills: 技能列表，如["写作", "运营"]
            resources: 资源列表，如["公众号", "知乎"]
            goals: 目标列表，如["知识付费", "个人品牌"]
            industry: 所在行业，如"内容"、"技术"
        """
        self.name = name
        self.skills = set(skills)
        self.resources = set(resources)
        self.goals = set(goals)
        self.industry = industry


class MatchMaker:
    """合作匹配器，分析多个合作者之间的技能互补和目标一致性。"""

    def __init__(self):
        """初始化匹配器，创建空的合作者列表。"""
        self.people = []

    def register(self, person: Collaborator):
        """注册一个合作者到匹配池。

        Args:
            person: Collaborator 实例

        Returns:
            返回自身以支持链式调用
        """
        self.people.append(person)
        return self

    def find_matches(self, person: Collaborator,
                     min_skills: int = 1, min_goals: int = 0) -> list:
        """查找与指定合作者匹配的潜在伙伴。

        Args:
            person: 目标合作者
            min_skills: 最小共同技能数量阈值
            min_goals: 最小共同目标数量阈值

        Returns:
            匹配结果列表，按匹配度降序排列，每项包含伙伴信息、匹配度、共同技能等
        """
        results = []
        for other in self.people:
            if other.name == person.name:
                continue

            skill_overlap = person.skills & other.skills
            goal_overlap = person.goals & other.goals
            resource_sync = person.resources & other.resources

            # 互补匹配: 对方有我没有的技能
            complement = other.skills - person.skills

            score = len(skill_overlap) * 2 + len(goal_overlap) * 3 + len(resource_sync) * 1

            if len(skill_overlap) >= min_skills and len(goal_overlap) >= min_goals:
                results.append({
                    "partner": other.name,
                    "industry": other.industry,
                    "匹配度": f"{min(100, score * 10)}%",
                    "共同技能": list(skill_overlap),
                    "共同目标": list(goal_overlap),
                    "互补技能": list(complement)[:5],
                    "可共享资源": list(resource_sync),
                })

        return sorted(results, key=lambda r: int(r["匹配度"].rstrip("%")), reverse=True)


if __name__ == "__main__":
    mm = MatchMaker()
    mm \
        .register(Collaborator("Alice", {"写作", "运营", "数据分析"}, {"公众号", "知乎"},
                               ["知识付费", "个人品牌"], "内容")) \
        .register(Collaborator("Bob", {"编程", "AI", "产品设计"}, {"GitHub项目", "API"},
                               ["SaaS产品", "知识付费"], "技术")) \
        .register(Collaborator("Carol", {"设计", "视频剪辑", "写作"}, {"小红书", "B站"},
                               ["个人品牌", "在线课程"], "内容"))

    me = Collaborator("我", {"写作", "编程"}, {"公众号", "GitHub"},
                      ["知识付费", "SaaS产品"])
    matches = mm.find_matches(me)
    for m in matches:
        print(f"{m['partner']} ({m['industry']}) — 匹配度 {m['匹配度']}")
        print(f"  共同目标: {', '.join(m['共同目标'])}")
        print(f"  互补技能: {', '.join(m['互补技能'])}")
        print()
