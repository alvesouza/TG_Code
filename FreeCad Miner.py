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
        '''print('\n////////////////////////////////////////\nlabel is {0}'.format(objs))'''
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>" and obj.Label != "Board Body":
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                faces = s.Faces
                size_list = len(faces)
                print("len = ", len(faces), "obj.Label = ", obj.Label)
                best_face = -1
                smallest_height = 9999999

                #Look through object faces, looking for the one which on the bottom would gives us the shortest height
                for i in range( size_list ):
                    height = -1
                    for j in range( size_list ):
                        if i == j:
                            continue
                        for vertex in faces[j].Vertexes:
                            distance = faces[i].distToShape( vertex )[0]
                            if height < distance:
                                height = distance
                    print( "height = ", height )
                    if height < smallest_height:
                        smallest_height = height
                        best_face = i

                '''print( "best_face = {0}, smallest_height = {1}".format(best_face, smallest_height) )'''

                #Find Axis and angle to rotate
                uv = faces[ best_face ].Surface.parameter(faces[ best_face ].CenterOfMass)
                faceNormalInCOM = faces[ best_face ].normalAt(uv[0], uv[1])
                angle = acos( -faceNormalInCOM[2] )*180/(pi)

                # Make rotaion, so that face is on the bottom, and orthogonal to XY
                spin = makeRotatingPlacement(App.Vector(b[0], b[1], b[2]), App.Vector(-faceNormalInCOM[1], faceNormalInCOM[0], 0), angle)
                obj.Placement = spin.multiply(obj.Placement)

                #After rotation, sets find lowest high and sets it on zero
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                r = p.Rotation
                lowest_height = 9999999
                for vertex in s.Vertexes:
                    Point = vertex.Point
                    if lowest_height > Point[2]:
                        lowest_height = Point[2]

                obj.Placement = App.Placement(App.Vector(b[0], b[1], b[2] - lowest_height), r)

def VetexOnZero(objs):
    for obj in objs:
        #print('\n////////////////////////////////////////\nlabel is {0}'.format(q))
        #Go through objets
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>" and obj.Label != "Board Body":
                #Have to make sure that the type, is Body, and can't be Board
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                r = p.Rotation

                best_face = -1
                highest_x = -9999999
                highest_y = -9999999
                #Go through every vertex to find vertex highest value
                for vertex in s.Vertexes:
                    Point = vertex.Point
                    if highest_x < Point[0]:
                        highest_x = Point[0]
                    if highest_y < Point[1]:
                        highest_y = Point[1]

                obj.Placement = App.Placement(App.Vector( b[0]-highest_x, b[1]-highest_y, b[2] ), r)

def Initial_Position( objs ):
    for obj in objs:
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>" and obj.Label != "Board Body":
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                r = p.Rotation
                highest_x = -9999999
                highest_y = -9999999
                for vertex in s.Vertexes:
                    Point = vertex.Point
                    if highest_x < Point[0]:
                        highest_x = Point[0]
                    if highest_y < Point[1]:
                        highest_y = Point[1]

                obj.Placement = App.Placement(App.Vector( b[0]-highest_x, b[1]-highest_y, b[2], r) )

def getPositionsValues(objs):
    vertexesAll = []
    positions = []
    CadData = []
    for obj in objs:
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>" and obj.Label != "Board Body":
                # c = obj.Content
                l = obj.Label
                '''print("{0} Object type = {1}\n".format(l, str(type(obj))))'''
                p = obj.Placement
                b = p.Base
                positions.append( [ b[ 0 ], b[ 1 ], b[ 2 ] ] )
                vertexes = obj.Shape.Vertexes
                vertexes_list = []
                for vert in vertexes:
                    vertexes_list.append([vert.Point[0], vert.Point[1], vert.Point[2]])
                    '''try:
                        print('label is {0} content is {1}'.format(l, [vert.Point[0], vert.Point[1], vert.Point[2]]))
                    except:
                        print('label is %s \\n'.format(l))'''

                vertexesAll.append(vertexes_list)
    return [ positions, vertexesAll ]

def PlaceObjects( objs, values ):
    i = 0
    for obj in objs:
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>"  and obj.Label != "Board Body":
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                r = p.Rotation

                value = values[ i ]

                spin = makeRotatingPlacement(App.Vector(0, 0, 0), App.Vector(0, 0, 1), value[ 1 ])
                obj.Placement = spin.multiply(obj.Placement)

                p = obj.Placement
                b = p.Base
                r = p.Rotation

                obj.Placement = App.Placement(App.Vector(value[ 0 ][ 0 ] + b[0], value[ 0 ][ 1 ] + b[1], b[2]), r)
                i += 1

def Initial_Position_Board( objs ):
    for obj in objs:
        if 'Shape' in dir(obj):
            if str(type(obj)) == "<class 'PartDesign.Body'>" and obj.Label == "Board Body":
                s = obj.Shape
                p = obj.Placement
                b = p.Base
                r = p.Rotation
                lowest_x = 9999999
                lowest_y = 9999999
                highest_z = -9999999
                for vertex in s.Vertexes:
                    Point = vertex.Point
                    if lowest_x > Point[0]:
                        lowest_x = Point[0]
                    if lowest_y > Point[1]:
                        lowest_y = Point[1]
                    if highest_z < Point[2]:
                        highest_z = Point[2]
                print(b)
                print([ b[0]-lowest_x, b[1]-lowest_y, b[2] - highest_z ])
                obj.Placement = App.Placement(App.Vector( b[0]-lowest_x, b[1]-lowest_y, b[2] - highest_z ), r )

def GetBoard( objs ):
    for obj in objs:
        if obj.Label == "Board Body":
            vertexes = obj.Shape.Vertexes
            vertexes_list = []
            for vert in vertexes:
                if vert.Point[2] == 0:
                    vertexes_list.append([vert.Point[0], vert.Point[1], 0])
            return vertexes_list
def WriteValues( values ):
    print( "values = [" )
    print("             [")
    for i in range(len(values[0])):
        print("                 ", values[0][i], end="")
        if i + 1 < len(values[0]):
            print(",")
        else:
            print("\n], [");

    for i in range( len( values[1] ) ):
        print( " [ " )
        for j in range(len(values[1][i])):
            if j == 0:
                print("         ", end ="")
            print( values[1][i][j], end="" )
            if j + 1 < len( values[1][i] ):
                if j%2 == 0:
                    print(", ", end="")
                else:
                    print(", ", end="\n         ")
            else:
                print("\n]", end="")
                if i + 1 != len( values[1] ):
                    print("", end=",")
    print( "]] " )

if __name__ == '__main__':
    doc = FreeCAD.ActiveDocument
    objs = FreeCAD.ActiveDocument.Objects
    vertexes_obj = []
    positions_obj = []
    quaternions_obj = []


    #Rotate2ShorterstHeight(objs)
    #VetexOnZero(objs)
    #Initial_Position_Board( objs )
    #vertex_board = GetBoard( objs )

    #print( vertex_board )
    #LowestHeightOnZero(objs)
    #values = GetPositionsValues(objs)

    #WriteValues( values )
    #new_values = TG01_Code.GeneticAlgoV01_parser01( 1, 1000,1000, values[0], values[1] )
    #new_values = TG01_Code.GeneticAlgo_knolling_V01_parser01( 1, 1000, 1000, values[0], values[1], [[0,0,0]], vertex_board, 3, 3)

    new_values = [[[4.400000095367432, 57.599998474121094], 102.0], [[0.20000000298023224, 106.0], 102.0], [[204.8000030517578, 109.0], 102.0], [[115.19999694824219, 109.19999694824219], 102.0], [[212.0, 109.19999694824219], 6.0], [[218.0, 109.19999694824219], 0.0], [[218.39999389648438, 6.800000190734863], 0.0], [[218.39999389648438, 0.4000000059604645], 0.0], [[218.39999389648438, 0.0], 96.0], [[13.600000381469727, 0.0], 6.0], [[0.800000011920929, 102.4000015258789], 96.0], [[0.0, 6.400000095367432], 198.0], [[0.0, 102.80000305175781], 12.0], [[204.8000030517578, 211.1999969482422], 192.0], [[12.800000190734863, 13.199999809265137], 252.0]]
    #scores = new_values[4]
    #scores_Final = new_values[5]
    #print("new positions = ", new_values[0] )
    #print("scores = ", scores  )
    #print("scores_Final = ", scores_Final )
    PlaceObjects( objs, new_values )
