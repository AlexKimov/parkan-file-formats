from inc_noesis import *
import os

NAME_LENGTH_CONST = 64


def registerNoesisTypes():
    handle = noesis.register( "PARKAN 2 (2007) LMDL format", ".lmdl")

    noesis.setHandlerTypeCheck(handle, parkModelCheckType)
    noesis.setHandlerLoadModel(handle, parkModelLoadModel)
        
    return 1 
 
  
class Vector3UI16:
    def read(self, reader):
        self.x = reader.readShort()
        self.y = reader.readShort()
        self.z = reader.readShort()
        
    def getStorage(self):
        return (self.x, self.y, self.z)    
   

class Vector3F:
    def read(self, reader):
        self.x = reader.readFloat()
        self.y = reader.readFloat()
        self.z = reader.readFloat() 
        
    def getStorage(self):
        return (self.x, self.y, self.z)     
        

class Vector2F:
    def read(self, reader):
        self.x = reader.readFloat()
        self.y = reader.readFloat()
 
    def getStorage(self):
        return (self.x, self.y) 
   

class PKChunkRec:
    def __init__(self, reader):
        self.reader = reader
        self.name = ""
        self.offset = 0
        
    def read(self):
        self.name =  noeAsciiFromBytes(self.reader.readBytes(NAME_LENGTH_CONST)).lower()        
        self.offset =  self.reader.readUInt() 
 
 
class PKPosition:
    def __init__(self, reader):
        self.reader = reader
        self.X = 0
        self.Y = 0
        self.Z = 0
         
    def read(self):
        pos = Vector3F()
        pos.read(self.reader)
        
        self.X, self.Y, self.Z = pos.getStorage()

    def getStorage(self):
        return (self.X, self.Y, self.Z)  


class PKVertex:
    def __init__(self, reader):
        self.reader = reader
        self.index0 = 0
        self.index1 = 0
        self.index2 = 0
        self.index3 = 0
        self.index4 = 0
        self.index5 = 0
        
    def read(self):
        self.index0, self.index1, self.index2, self.index3, self.index4, self.index5 = \
            noeUnpack('6H', self.reader.readBytes(12))           
        
        
class PKIndexTris:
    def __init__(self, reader):
        self.reader = reader
        self.i1 = 0
        self.i2 = 0
        self.i3 = 0
         
    def read(self):
        tris = Vector3UI16()
        tris.read(self.reader)
        
        self.i1, self.i2, self.i3 = tris.getStorage()
 
    def getStorage(self):
        return (self.i1, self.i2, self.i3)  
 

class PKTexCoords:
    def __init__(self, reader):
        self.reader = reader
        self.U = 0
        self.V = 0
        
    def read(self):
        uvs = Vector2F()
        uvs.read(self.reader)
        self.U, self.V = uvs.getStorage()

    def getStorage(self):
        return (self.U, self.V)          
    
    
class PKModel:
    def __init__(self, reader):
        self.reader = reader
        self.chunkCount = 0
        self.chunks = []
        self.positions = []
        self.vertexes = []
        self.positionTris = []
        self.texcoords = []
        self.vertexTris = []
        self.materials = []
        self.materialTris = []
        
    def readHeader(self, reader):
        self.reader.seek(24, NOESEEK_REL)     
        
    def readChunkTable(self, reader):   
        self.chunkCount = reader.readUInt() 
        
        for i in range(self.chunkCount):
            chunkRec = PKChunkRec(self.reader)
            chunkRec.read()
            
            self.chunks.append(chunkRec)
    
    def readData(self, reader):
        for chunk in self.chunks:
            self.reader.seek(chunk.offset, NOESEEK_ABS)
            
            if chunk.name == "positions":
                for i in range(reader.readUInt()): 
                    position = PKPosition(self.reader)
                    position.read()   
       
                    self.positions.append(position)
                
            if chunk.name == "position_tris":
                for i in range(reader.readUInt()):             
                    positionTris = PKIndexTris(self.reader)  
                    positionTris.read()  
                 
                    self.positionTris.append(positionTris)
                
            if chunk.name == "texcoords":
                for i in range(reader.readUInt()):              
                    texcoords = PKTexCoords(self.reader)  
                    texcoords.read()  
                
                    self.texcoords.append(texcoords) 

            if chunk.name == "vertexes":
                for i in range(reader.readUInt()):            
                    vertex = PKVertex(self.reader)  
                    vertex.read()  
                                 
                    self.vertexes.append(vertex)

            if chunk.name == "vertex_tris":
                for i in range(reader.readUInt()):            
                    vertexTris = PKIndexTris(self.reader)  
                    vertexTris.read()  
                                 
                    self.vertexTris.append(vertexTris)  

            # material names 
            if chunk.name == "materials":
                for i in range(reader.readUInt()):            
                    material = noeAsciiFromBytes(self.reader.readBytes(NAME_LENGTH_CONST)) 
                    self.materials.append(material)   

            # material indexes
            if chunk.name == "material_tris":
                for i in range(reader.readUInt()):            
                    self.materialTris.append(reader.readUShort())                        
                
    def read(self):
        self.readHeader(self.reader)
        self.readChunkTable(self.reader) 
       
        self.readData(self.reader)  
        
           
def parkModelCheckType(data):     
            
    return 1     
   

def parkModelLoadModel(data, mdlList): 
    noesis.logPopup()

    parkModel = PKModel(NoeBitStream(data)) 
    parkModel.read()

    ctx = rapi.rpgCreateContext()
 
    transMatrix = NoeMat43( ((1, 0, 0), (0, 0, 1), (0, 1, 0), (0, 0, 0)) ) 
    rapi.rpgSetTransform(transMatrix)
    
    textures = []
    materials = []
    
    dir = "F:\\Games\\Parkan 2\\texture\\"
    
    for texture in parkModel.materials:
        filename = ""

        for root, dirs, files in os.walk(dir):  
            for file in files:
                if texture in file.lower():
                    filename = "{}\{}.dds".format(root, texture)
                    
        tex = rapi.loadExternalTex(filename)
        
        if tex == None:
            tex = NoeTexture(texture, 0, 0, bytearray())
        tex.name = texture    
        textures.append(tex)  
        
        material = NoeMaterial(texture, texture)
        
        material.setFlags(noesis.NMATFLAG_TWOSIDED, 1)
        materials.append(material)       
    
    for index, vTris in enumerate(parkModel.vertexTris):    
        indxs = vTris.getStorage()
        
        matIndx = parkModel.materialTris[index]
        rapi.rpgSetMaterial(parkModel.materials[matIndx])         
        rapi.immBegin(noesis.RPGEO_TRIANGLE)   
        
        for indx in indxs:         
            vertex = parkModel.vertexes[indx]
            
            texCoords = parkModel.texcoords[vertex.index2].getStorage()
            positions = parkModel.positions[vertex.index0].getStorage()
            
            rapi.immUV2(texCoords)        
            rapi.immVertex3(positions) 
            
        rapi.immEnd()     
        
    mdl = rapi.rpgConstructModelSlim()
    mdl.setModelMaterials(NoeModelMaterials(textures, materials)) 
    mdlList.append(mdl)
    
    return 1