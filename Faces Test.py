TG01_CodePATH = '/home/pedro/Documents/gits/github/TG01_Code'
import sys
from math import acos, pi
sys.path.append(TG01_CodePATH)
import TG01_Code
def makeRotatingPlacement(axis_origin, axis_dir, angle):
    #import FreeCAD as App
    OZ = App.Vector(0,0,1)
    local_cs = App.Placement(axis_origin, App.Rotation(OZ, axis_dir))
    return local_cs.multiply(   App.Placement( App.Vector(), App.Rotation(angle,0,0) ).multiply( local_cs.inverse() )   )

def Rotate2ShorterstHeight( objs ):
    for obj in objs:
        #print('\n////////////////////////////////////////\nlabel is {0}'.format(q))
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>":
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                r = p.Rotation
                faces = s.Faces
                #print(dir(faces[0]))
                size_list = len(faces)
                best_face = -1
                smallest_height = 9999999
                for i in range( size_list ):
                    height = -1
                    for j in range( size_list ):
                        if i == j:
                            continue
                        for vertex in faces[j].Vertexes:
                            distance = faces[i].distToShape( vertex )[0]
                            if height < distance:
                                height = distance
                    #print( "height = ", height )
                    if height < smallest_height:
                        smallest_height = height
                        best_face = i

                print( "best_face = {0}, smallest_height = {1}".format(best_face, smallest_height) )
                uv = faces[ best_face ].Surface.parameter(faces[ best_face ].CenterOfMass)
                faceNormalInCOM = faces[ best_face ].normalAt(uv[0], uv[1])
                #print("dir face = {0}".format( dir( faces[ best_face ] )))
                print( "Faces Normal = {0}".format(faceNormalInCOM) )
                center_mass = faces[best_face].CenterOfMass
                angle = acos( -faceNormalInCOM[2] )*180/(pi)
                spin = makeRotatingPlacement(App.Vector(b[0], b[1], b[2]), App.Vector(-faceNormalInCOM[1], faceNormalInCOM[0], 0), angle)
                obj.Placement = spin.multiply(obj.Placement)

def LowestHeightOnZero( objs ):
    for obj in objs:
        #print('\n////////////////////////////////////////\nlabel is {0}'.format(q))
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>":
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                r = p.Rotation
                faces = s.Faces
                #print(dir(faces[0]))
                size_list = len(faces)
                best_face = -1
                lowest_height = 9999999
                for vertex in s.Vertexes:
                    Point = vertex.Point
                    if lowest_height > Point[2]:
                        lowest_height = Point[2]
                #obj.Placement = App.Placement(App.Vector(b[0], b[1], b[2] - lowest_height), r)
                obj.Placement = App.Placement(App.Vector( 0, 0, b[2] - lowest_height), r)

def GetPositionsValues( objs ):
    vertexesAll = []
    positions = []
    CadData = []
    for obj in objs:
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>":
                # c = obj.Content
                l = obj.Label
                print("{0} Object type = {1}\n".format(l, str(type(obj))))
                p = obj.Placement
                b = p.Base
                positions.append( [ b[ 0 ], b[ 1 ], b[ 2 ] ] )
                vertexes = obj.Shape.Vertexes
                vertexes_list = []
                for vert in vertexes:
                    vertexes_list.append([vert.Point[0], vert.Point[1], vert.Point[2]])
                    try:
                        print('label is {0} content is {1}'.format(l, [vert.Point[0], vert.Point[1], vert.Point[2]]))
                    except:
                        print('label is %s \\n'.format(l))

                vertexesAll.append(vertexes_list)
    return [ positions, vertexesAll ]

def PlaceObjects( objs, values ):
    i = 0
    for obj in objs:
        #print('\n////////////////////////////////////////\nlabel is {0}'.format(q))
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>":
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                r = p.Rotation

                value = values[ i ]

                spin = makeRotatingPlacement(App.Vector(b[0], b[1], b[2]), App.Vector(0, 0, 1), value[ 1 ])
                obj.Placement = spin.multiply(obj.Placement)

                p = obj.Placement
                b = p.Base
                r = p.Rotation

                obj.Placement = App.Placement(App.Vector(value[ 0 ][ 0 ], value[ 0 ][ 1 ], b[2]), r)
                i += 1

if __name__ == '__main__':
    doc = FreeCAD.ActiveDocument
    objs = FreeCAD.ActiveDocument.Objects
    vertexes_obj = []
    positions_obj = []
    quaternions_obj = []
    Rotate2ShorterstHeight(objs)
    LowestHeightOnZero(objs)
    values = GetPositionsValues(objs)

    print("positions = ", values )
    new_values = TG01_Code.GeneticAlgoV01( 2, 10000, 1000, values[0], values[1] )
    PlaceObjects( objs, new_values)

    #print("positions = ", new_values )