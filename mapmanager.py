import pickle
from direct.showbase.ShowBase import ShowBase

class Mapmanager():
    """Map management"""
    def __init__(self):
        self.model = 'block' 
        self.texture = 'block.png'          
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ] 
        self.startNew()


    def startNew(self):
        """creates the basis for the new map"""
        self.land = render.attachNewNode("Land") 

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) - 1]

    def addBlock(self, position):
        block_node = loader.loadModel(self.model)
        block_node.setTexture(loader.loadTexture(self.texture))
        block_node.setPos(position)
        
        color = self.getColor(int(position[2]))
        block_node.setColor(color)

        block_node.setTag("at", str(position))
        block_node.reparentTo(self.land)
        
        return block_node

    def clear(self):
        """resets the map"""
        if self.land:
            self.land.removeNode()
        self.startNew()

    def loadLand(self, filename):
        """creates a land map from a text file, returns its dimensions"""
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                        self.addBlock((x, y, z0))
                    x += 1
                y += 1
        return x,y
    
    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        return not blocks

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    def buildBlock(self, pos):
        """We place the block, taking gravity into account:"""
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlock(self, position):
        """removes blocks at the specified position""" 
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos_to_delete = x, y, z - 1
        
        if pos_to_delete[2] >= 1: 
            for block in self.findBlocks(pos_to_delete):
                block.removeNode()

    def saveMap(self):
        """saves all blocks, including structures, to a binary file"""
        blocks = self.land.getChildren()
        
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)

    def loadMap(self):
        self.clear()
        try:
            with open('my_map.dat', 'rb') as fin:
                length = pickle.load(fin)
                for i in range(length):
                    pos = pickle.load(fin)

                    self.addBlock(pos)
        except FileNotFoundError:
            print("my_map.dat not found. Cannot load map.")
        except Exception as e:
            print(f"Error loading map data: {e}")