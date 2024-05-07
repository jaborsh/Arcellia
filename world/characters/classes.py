"""
Legal Information
The System Reference Document 5.1 is provided to you free of charge under the terms of the Creative Commons
Attribution 4.0 International License (“CC-BY-4.0”). You are free to use this content in any manner permitted by
that license as long as you include the following attribution statement in your own work:
This work includes material taken from the System Reference Document 5.1 (“SRD 5.1”) by Wizards of
the Coast LLC and available at https://dnd.wizards.com/resources/systems-reference-document. The
SRD 5.1 is licensed under the Creative Commons Attribution 4.0 International License available at
https://creativecommons.org/licenses/by/4.0/legalcode.
Please do not include any other attribution regarding Wizards other than that provided above. You may, however,
include a statement on your work that it is “compatible with fifth edition” or “5E compatible.”
Section 5 of CC-BY-4.0 includes a Disclaimer of Warranties and Limitation of Liability that limits our liability to you.
"""

from copy import copy

from class_registry import ClassRegistry
from handlers.equipment import EQUIPMENT_DEFAULTS
from prototypes import armor, weapons
from typeclasses.equipment.equipment import EquipmentType

from .score import AbilityScore

ClsRegistry = ClassRegistry("cls")

CLASS_INFO_DICT = {
    "barbarian": "|YBarbarian|n:\n\nThese are the ones who are attuned to the raw, untamed rhythms of existence, their every sinew thrumming with the pulse of ancient instincts. They carry within them the legacy of the hunt - a primal physicality that speaks of strength honed through countless trials and, above all, a ferocious, insatiable rage that smolders like embers.",
    "bard": "|mBard|n:\n\nTo the untrained eye, their artistry might appear as mere dalliance, a frivolous indulgence. Yet, beneath this veneer lies a profound mastery over a dominion where art transcends the realm of simple entertainment to touch the fabric of reality itself.",
    "cleric": "|yCleric|n:\n\nThese hallowed emissaries stand as tangible conduits between the realms of the gods they venerate and the tumultuous world of mortals. With every incantation uttered, every reverent gesture performed, they channel the potent magic bequeathed to them by their patrons, wielding it within the precision of a master sculptor chiseling reality to mirror the divine blueprint.",
    "druid": "|gDruid|n:\n\nThese sages of the wild serve as the custodians of an age-old pact between the flora, fauna, and the elemental forces that orchestrate life. With hands that can as easily mend a withering bloom as summon the fury of a storm, they channel the raw, untamed energy of nature.",
    "fighter": "|rFighter|n:\n\nForged in the crucible of relentless training and tempered in the flames of countless skirmishes, these paragons of warfare stride with purpose. Weapons become extensions of their very beings, wielded with an artistry that belies the lethal intent with which they dance their deadly dance.",
    "monk": "|CMonk|n:\n\nThese ascetics walk the razor's edge between serenity and strife. With bodies honed through the rigors of discipline and minds sharpened by the stillness of meditative introspection, they navigate the world as both warrior and sage. An intrinsic force flows through them like an unbroken river. By manipulating this energy, they transform their bodies into instruments of formidable power.",
    "paladin": "|wPaladin|n:\n\nThis paragon carries within their heart a promise. This is no ordinary oath, mind you, but a sacred covenant that resonates with the very essence of the divine, a vow so profound and imbued with conviction that it transcends mortality, elevating the paladin to the vanguard of divine will. This promise courses through their being like a resplendent river, an incandescent testament to their unbreakable bond.",
    "ranger": "|GRanger|n:\n\nWhere every whispering leaf and shadowed glen harbors secrets known only to the earth itself, the ranger emerges as the master of the untamed world. These wardens of nature inhibit the liminal spaces between civilization and the vast, verdant wilderness. Their prowess as scouts and trackers is the stuff of legend, born of an intimate communion with the natural world blossomed into a profound symbiosis.",
    "rogue": "|xRogue|n:\n\nTheirs is a realm not of brute force but of cunning; not of frontal assaults but of precise strikes from the veil of obscurity. Rogues embody the essence of versatility, their arsenal a collection of skills honed through narrow escapes and daring exploits.",
    "sorcerer": "|RSorcerer|n:\n\nBorn of a lineage steeped in mystique, or perhaps the recipients of a cosmic boon that has irrevocably altered their essence, these individuals walk a path illuminated by the innate luminescence of their own magic. Like a wellspring of power that knows no bounds, the sorcerer's gift flows from within, an ever-present reservoir of arcane energy that courses through their veins, as natural as breathing.",
    "warlock": "|MWarlock|n:\n\nThe warlock stands as a figure both envied and feared. These arcanists trade a piece of their essence for a shard of the infinite. This exchange transforms the warlock into a vessel of supernatural might, a conduit for forces that rend the fabric of reality and reshape it to their will.",
    "wizard": "|cWizard|n:\n\nWizards pursue the path of the arcane with a devotion that borders on zealotry. These scholars of the mystic arts understand that power - true power - lies not in brute force, but in the nuanced comprehension of the foundations upon which reality itself is built. Through a synthesis of rigorous study and the untangling of arcane scripts left by their predecessors, wizard engage in a continual dialogue between the ancient and the contemporary, their magic a bridge across either.",
}


class Cls:
    cls = "cls"

    recommended_stats = {
        AbilityScore.STRENGTH: 10,
        AbilityScore.DEXTERITY: 10,
        AbilityScore.CONSTITUTION: 10,
        AbilityScore.INTELLIGENCE: 10,
        AbilityScore.WISDOM: 10,
        AbilityScore.CHARISMA: 10,
    }

    def __init__(
        self,
        level=1,
        health=100,
        mana=100,
        stamina=100,
    ):
        self.level = level
        self.health = health
        self.mana = mana
        self.stamina = stamina


@ClsRegistry.register
class Barbarian(Cls):
    cls = "barbarian"

    default_equipment = copy(EQUIPMENT_DEFAULTS)
    default_equipment[EquipmentType.WEAPON] = [weapons.GREATAXE]
    default_equipment[EquipmentType.ARMOR] = armor.BARBARIAN_ARMOR
    default_equipment[EquipmentType.FOOTWEAR] = armor.LEATHER_BOOTS

    recommended_stats = {
        AbilityScore.STRENGTH: 20,
        AbilityScore.DEXTERITY: 12,
        AbilityScore.CONSTITUTION: 16,
        AbilityScore.INTELLIGENCE: 8,
        AbilityScore.WISDOM: 8,
        AbilityScore.CHARISMA: 8,
    }


@ClsRegistry.register
class Bard(Cls):
    cls = "bard"

    default_equipment = copy(EQUIPMENT_DEFAULTS)
    default_equipment[EquipmentType.WEAPON] = [weapons.HAND_CROSSBOW]
    default_equipment[EquipmentType.ARMOR] = armor.SIMPLE_JERKIN
    default_equipment[EquipmentType.FOOTWEAR] = armor.LEATHER_BOOTS

    recommended_stats = {
        AbilityScore.STRENGTH: 8,
        AbilityScore.DEXTERITY: 16,
        AbilityScore.CONSTITUTION: 12,
        AbilityScore.INTELLIGENCE: 8,
        AbilityScore.WISDOM: 8,
        AbilityScore.CHARISMA: 20,
    }


@ClsRegistry.register
class Cleric(Cls):
    cls = "cleric"

    default_equipment = copy(EQUIPMENT_DEFAULTS)
    default_equipment[EquipmentType.WEAPON] = [weapons.MACE]
    default_equipment[EquipmentType.SHIELD] = armor.STUDDED_SHIELD
    default_equipment[EquipmentType.ARMOR] = armor.SIMPLE_JERKIN
    default_equipment[EquipmentType.FOOTWEAR] = armor.LEATHER_BOOTS

    recommended_stats = {
        AbilityScore.STRENGTH: 8,
        AbilityScore.DEXTERITY: 14,
        AbilityScore.CONSTITUTION: 16,
        AbilityScore.INTELLIGENCE: 8,
        AbilityScore.WISDOM: 18,
        AbilityScore.CHARISMA: 8,
    }


@ClsRegistry.register
class Druid(Cls):
    cls = "druid"

    default_equipment = copy(EQUIPMENT_DEFAULTS)
    default_equipment[EquipmentType.WEAPON] = [weapons.QUARTERSTAFF]
    default_equipment[EquipmentType.ARMOR] = armor.SIMPLE_JERKIN
    default_equipment[EquipmentType.FOOTWEAR] = armor.LEATHER_BOOTS

    recommended_stats = {
        AbilityScore.STRENGTH: 8,
        AbilityScore.DEXTERITY: 12,
        AbilityScore.CONSTITUTION: 16,
        AbilityScore.INTELLIGENCE: 8,
        AbilityScore.WISDOM: 20,
        AbilityScore.CHARISMA: 8,
    }


@ClsRegistry.register
class Fighter(Cls):
    cls = "fighter"

    default_equipment = copy(EQUIPMENT_DEFAULTS)
    default_equipment[EquipmentType.WEAPON] = [weapons.LONGSWORD]
    default_equipment[EquipmentType.ARMOR] = armor.SCALE_MAIL
    default_equipment[EquipmentType.FOOTWEAR] = armor.LEATHER_BOOTS

    recommended_stats = {
        AbilityScore.STRENGTH: 16,
        AbilityScore.DEXTERITY: 16,
        AbilityScore.CONSTITUTION: 16,
        AbilityScore.INTELLIGENCE: 8,
        AbilityScore.WISDOM: 8,
        AbilityScore.CHARISMA: 8,
    }


@ClsRegistry.register
class Monk(Cls):
    cls = "monk"

    recommended_stats = {
        AbilityScore.STRENGTH: 8,
        AbilityScore.DEXTERITY: 18,
        AbilityScore.CONSTITUTION: 14,
        AbilityScore.INTELLIGENCE: 8,
        AbilityScore.WISDOM: 16,
        AbilityScore.CHARISMA: 8,
    }


@ClsRegistry.register
class Paladin(Cls):
    cls = "paladin"

    recommended_stats = {
        AbilityScore.STRENGTH: 16,
        AbilityScore.DEXTERITY: 12,
        AbilityScore.CONSTITUTION: 12,
        AbilityScore.INTELLIGENCE: 8,
        AbilityScore.WISDOM: 8,
        AbilityScore.CHARISMA: 16,
    }


@ClsRegistry.register
class Ranger(Cls):
    cls = "ranger"

    recommended_stats = {
        AbilityScore.STRENGTH: 10,
        AbilityScore.DEXTERITY: 16,
        AbilityScore.CONSTITUTION: 14,
        AbilityScore.INTELLIGENCE: 8,
        AbilityScore.WISDOM: 16,
        AbilityScore.CHARISMA: 8,
    }


@ClsRegistry.register
class Rogue(Cls):
    cls = "rogue"

    recommended_stats = {
        AbilityScore.STRENGTH: 8,
        AbilityScore.DEXTERITY: 20,
        AbilityScore.CONSTITUTION: 12,
        AbilityScore.INTELLIGENCE: 8,
        AbilityScore.WISDOM: 10,
        AbilityScore.CHARISMA: 14,
    }


@ClsRegistry.register
class Sorcerer(Cls):
    cls = "sorcerer"

    recommended_stats = {
        AbilityScore.STRENGTH: 8,
        AbilityScore.DEXTERITY: 14,
        AbilityScore.CONSTITUTION: 12,
        AbilityScore.INTELLIGENCE: 8,
        AbilityScore.WISDOM: 10,
        AbilityScore.CHARISMA: 20,
    }


@ClsRegistry.register
class Warlock(Cls):
    cls = "warlock"

    recommended_stats = {
        AbilityScore.STRENGTH: 8,
        AbilityScore.DEXTERITY: 16,
        AbilityScore.CONSTITUTION: 12,
        AbilityScore.INTELLIGENCE: 8,
        AbilityScore.WISDOM: 8,
        AbilityScore.CHARISMA: 20,
    }


@ClsRegistry.register
class Wizard(Cls):
    cls = "wizard"

    recommended_stats = {
        AbilityScore.STRENGTH: 8,
        AbilityScore.DEXTERITY: 14,
        AbilityScore.CONSTITUTION: 14,
        AbilityScore.INTELLIGENCE: 20,
        AbilityScore.WISDOM: 8,
        AbilityScore.CHARISMA: 8,
    }
