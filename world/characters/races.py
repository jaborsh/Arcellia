from class_registry import ClassRegistry
from evennia.utils import dedent

from world.features import racial as racial_feats
from world.spells import evocation

RaceRegistry = ClassRegistry("key")

RACE_INFO_DICT = {
    "human": dedent(
        """
        |YHumans|n:
        
        Human, you say? Oh, you poor, deluded grain of malt. Does it matter? You're a sack of meat and bones, electric impulses firing in a soggy brain. Human, cryptid, or cosmic horror -- what's the difference when you're hurtling through the void?
        
        But if you must know... yes, you reek of humanity. That stench of potential and futility, all wrapped up in a fragile shell. Tenacious like cockroaches, creative like a fever dream, always growing like a tumor.
        """
    ),
    "elf": dedent(
        """
        |cElves|n:
        
        Nature's spoiled brats, prancing around forests for millennia, acting all high and mighty. "Ooh, look at me. I'm immortal and in tune with the cosmos!" Bunch of salad-munching, poetry-spouting, arrow-shooting drama queens. Always going on about the stars and the trees and their precious balance.
        
        And you, my long-lived leafy friend, you've got that unmistakable whiff of pine needles and pretentiousness about you. Betting you've spent a few centuries communing with squirrels and writing sappy ballads about moonlight, haven't you?
        """
    ),
    "drow": dedent(
        """
        |xDrow|n:
        
        Those charming denizens of the subterranean, the elves' "misunderstood" cousins. A society built on matriarchal melodrama and spider fetishes. So edgy they probably cut themselves on their own earlobes, spider motifs, and bondage gear.
        
        But you, my darkling? Are you feeling a tingle of recognition? A little itch in your spider-loving soul? You have the essence of avoiding the sunlight. Is that you, you angsty, brooding thing?
        """
    ),
    "halfling": dedent(
        """
        |#A67B5BHalfling|n:
        
        Nature's little joke. Pint-sized gluttons with hairy feet and an unnatural obsession with food. They're like if someone took all the worst parts of humanity - the greed, the sloth, the endless appetite - and crammed it into a fun-sized package. Sure, they're \"lucky,\" if by lucky you mean stumbling ass-backwards through life, narrowly avoiding death by choking on a meat pie.
        
        Rather like you. That faint aroma of pipeweed and unearned self-satisfaction. You're probably itching to embark on some grand \"adventure\". The world's a big, scary place for a little morsel like you, but maybe your inherent \"luck\" will keep you from becoming a wolf's appetizer. Or maybe it won't!
        """
    ),
    "dwarf": dedent(
        """
        |#C19A6BDwarf|n:
        
        The vertically-challenged, beard-obsessed, ale-guzzling cave gremlins of Arcellia. Always digging holes and hitting rocks like deranged, armored prairie dogs insatiable for shiny things.
        
        You're rather stumpy-like. A little stumpy little meat-sack. You reek of stale ale and moldy cheese. Your beard has more personality than you do. Are you a dwarf? Well, if it waddles like a dwarf and belches like a dwarf... Let's just say the evidence is as short as you are, baby!
        """
    ),
    "gnome": dedent(
        """
        |#8DA399Gnome|n:
        
        Those pint-sized pests, scurrying about like caffeinated rodents with delusions of grandeur. Always poking their bulbous noses where they don't belong, thinking their \"cleverness\" will save them from the crushing weight of existence. Living for centuries, yet never growing an inch taller or wiser. They're proof that even eternity can't cure stupidity.
        
        You're starting to smell distinctly of garden ornament and pointy hat. Could it be? Has our eternal dance of nothingness been interrupted by a gnomish interloper? Oh, the indignity!
        """
    ),
}


class Race:
    key = "race"

    def initialize_race_features(self, caller):
        pass


@RaceRegistry.register
class Human(Race):
    key = "human"

    def initialize_race_features(self, caller):
        caller.feats.add(racial_feats.HumanVersatility)


@RaceRegistry.register
class Elf(Race):
    key = "elf"

    def initialize_race_features(self, caller):
        caller.feats.add(racial_feats.Darkvision)
        caller.spells.add(evocation.ElfFire)


@RaceRegistry.register
class Drow(Race):
    key = "drow"

    def initialize_race_features(self, caller):
        caller.feats.add(racial_feats.SuperiorDarkvision)
        caller.spells.add(evocation.OrbofLight)
        caller.spells.add(evocation.Darkness)


@RaceRegistry.register
class Halfling(Race):
    key = "halfling"

    def initialize_race_features(self, caller):
        pass


@RaceRegistry.register
class Dwarf(Race):
    key = "dwarf"

    def initialize_race_features(self, caller):
        caller.feats.add(racial_feats.Darkvision)


@RaceRegistry.register
class Gnome(Race):
    key = "gnome"

    def initialize_race_features(self, caller):
        pass


# Mob Races
@RaceRegistry.register
class Monster(Race):
    key = "monster"
