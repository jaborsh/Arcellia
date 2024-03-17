from evennia.contrib.grid.xyzgrid import xymap_legend
from typeclasses.builders.mob_builder import MobBuilder

NodeTypeclass = None
MobileTypeclass = None

MobBuilder = MobBuilder()


class MapNode(xymap_legend.MapNode):
    def spawn_mobiles(self, mobiles):
        """
        Build actual in-game mobiles based on the nodes of the map.

        This should be called after all `sync_node_to_grid` operations have finished across
        the entire XYZgrid. This creates/syncs all mobiles to their locations.
        """

        global MobileTypeclass
        if not MobileTypeclass:
            from typeclasses.mobs import Mob as MobileTypeclass
        global NodeTypeclass
        if not NodeTypeclass:
            from typeclasses.rooms import XYRoom as NodeTypeclass

        if not self.prototype:
            return

        xyz = self.get_spawn_xyz()
        nodeobj = NodeTypeclass.objects.get_xyz(xyz=xyz)

        for k, v in mobiles.items():
            # MobBuilder.set_key("Test", "Test!")
            MobBuilder.set_name(v["name"])
            MobBuilder.set_desc(v["desc"])
            MobBuilder.set_location(nodeobj)
            MobBuilder.build()
