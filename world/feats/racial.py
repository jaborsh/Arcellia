from handlers import buffs


class HumanVersatility(buffs.BaseBuff):
    key = "human_versatility"
    name = "Human Versatility"
    flavor = "Humans are versatile creatures. You can carry 25% more weight."

    def at_apply(self):
        self.owner.stats.weight.max = self.owner.stats.weight.max * 1.25

    def at_remove(self):
        self.owner.stats.weight.max = self.owner.stats.weight.max / 1.25


class Darkvision(buffs.BaseBuff):
    key = "darkvision"
    name = "Darkvision"
    flavor = "You can see in the dark."
