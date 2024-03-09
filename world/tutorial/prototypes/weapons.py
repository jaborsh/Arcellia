from typeclasses.equipment import EquipmentType

from world.items.rarity import ItemRarity

EMBERWISP_BLADE = {
    "key": "blade",
    "aliases": ["emberwisp", "emberwisp blade"],
    "display_name": "|rEmberwisp Blade|n",
    "typeclass": "world.tutorial.weapons.EmberwispBlade",
    "desc": "This sword is a union of lethality and enchantment, its metal forged in the breath of a dragon's smoldering heart. While dormant within its scabbard, the appearance of the weapon is unassuming, its potential for inferno veiled. However, at the moment of unsheathing, a marvel unfolds: silent flames awaken and run along the blade's edge, a visual serenade of fire. The steel surface alights with an ethereal blaze that mimics the auroras in the night sky - crimson, gold, and scarlet coalescing into a visual choir.",
    "senses": {
        "feel": "One feels a curious warmth suffuse the hand, the sensation of power harnessed and awaiting command.",
        "smell": "The air around the drawn sword fills with the scent of embers rekindled, the fragrance of a hearth without the sting of smoke.",
        "sound": "Silence enshrouds the flaming spectacle; the blaze dances without the crackle and spit of true fire, a sorcery wrought in quietude.",
        "taste": "A taste akin to the warmth of spiced wine teases the senses when the sword is bared, a savor of comfort and might intertwined.",
    },
    "weight": 5.4,
    "price": 130,
    "equipment_type": EquipmentType.WEAPON,
    "rarity": ItemRarity.UNCOMMON,
}
